"""Coordinator for Haptique Extender - Simplified Event System."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    API_IR_LAST,
    API_IR_RXINFO,
    API_IR_SAVED,
    API_IR_SEND,
    API_STATUS,
    API_WIFI_STATUS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class HaptiqueCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage fetching Haptique data."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        token: str = "",
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.token = token
        self.session = async_get_clientsession(hass)
        self.base_url = f"http://{host}"
        
        # Device info
        self.device_info: dict[str, Any] = {}
        
        # IR RX info
        self.ir_rx_info: dict[str, Any] = {}
        
        # Storage info
        self.storage_info: dict[str, Any] = {}
        
        # Learning state
        self._learning_mode = False
        self._learning_context: dict[str, Any] | None = None
        self._learning_task: asyncio.Task | None = None
        self._last_ir_data_captured: dict[str, Any] | None = None  # Track last captured data
        
        # Last learned IR code
        self.last_learn_ir_code: dict[str, Any] | None = None
        self.last_learn_ir_timestamp: Any = None

    @property
    def learning_mode(self) -> bool:
        """Return current learning mode state."""
        return self._learning_mode

    def set_learning_mode(self, enabled: bool) -> None:
        """Set learning mode and start/stop polling."""
        was_learning = self._learning_mode
        self._learning_mode = enabled
        
        if enabled and not was_learning:
            # Clear previous capture when starting new learning
            self._last_ir_data_captured = None
            
            # Start learning polling
            if self._learning_task:
                self._learning_task.cancel()
            self._learning_task = asyncio.create_task(self._learning_poll_loop())
            _LOGGER.info("Learning mode enabled, started polling")
        elif not enabled and was_learning:
            # Stop learning polling
            if self._learning_task:
                self._learning_task.cancel()
                self._learning_task = None
            _LOGGER.info("Learning mode disabled, stopped polling")
    
    async def _learning_poll_loop(self) -> None:
        """Poll for new IR codes while in learning mode."""
        timeout_counter = 0
        max_timeout = 30  # 30 seconds timeout
        poll_interval = 5  # Poll every 5 seconds
        
        try:
            while self._learning_mode and timeout_counter < max_timeout:
                await asyncio.sleep(poll_interval)
                timeout_counter += poll_interval
                
                try:
                    # Poll /api/ir/last
                    ir_data = await self._request("GET", API_IR_LAST)
                    
                    # Check if we have new data and it's different from last capture
                    if ir_data and ir_data.get("combined"):
                        # Check if this is new data (different from last captured)
                        if self._is_new_ir_data(ir_data):
                            _LOGGER.info("New IR code detected!")
                            self._last_ir_data_captured = ir_data.copy()
                            await self.handle_ir_learned(ir_data)
                            # Stop learning after capturing
                            self.set_learning_mode(False)
                            return
                        else:
                            _LOGGER.debug("IR data unchanged, waiting for new capture...")
                        
                except Exception as err:
                    _LOGGER.debug("Polling error: %s", err)
                    continue
            
            # Timeout reached
            if timeout_counter >= max_timeout:
                _LOGGER.warning("Learning timeout reached")
                self.set_learning_mode(False)
                
                # Fire unified event - TIMEOUT
                self.hass.bus.async_fire(
                    "haptique_operation",
                    {
                        "operation": "learn",
                        "status": "timeout",
                        "entity_type": "command",
                        "device_name": self._learning_context.get("device_name") if self._learning_context else None,
                        "command_name": self._learning_context.get("command_name") if self._learning_context else None,
                    }
                )
                
        except asyncio.CancelledError:
            _LOGGER.debug("Learning poll loop cancelled")
            raise

    def _is_new_ir_data(self, ir_data: dict[str, Any]) -> bool:
        """Check if IR data is new (different from last captured)."""
        if not self._last_ir_data_captured:
            return True
        
        # Compare the combined array
        new_combined = ir_data.get("combined", [])
        old_combined = self._last_ir_data_captured.get("combined", [])
        
        # If lengths differ, it's new data
        if len(new_combined) != len(old_combined):
            return True
        
        # If any value differs, it's new data
        for i, val in enumerate(new_combined):
            if i >= len(old_combined) or val != old_combined[i]:
                return True
        
        # Data is identical
        return False

    def set_learning_context(
        self, device_name: str, command_name: str
    ) -> None:
        """Set learning context for service-based learning."""
        self._learning_context = {
            "device_name": device_name,
            "command_name": command_name,
        }

    async def handle_ir_learned(self, ir_data: dict[str, Any]) -> None:
        """Handle IR data learned from the device."""
        # Update learn sensor
        await self.update_learn_ir_code(ir_data)
        
        # Check if there's a learning context (from learn_ir_command service)
        learning_context = self._learning_context
        
        if learning_context:
            # Save to database
            from .ir_database import IRDatabase
            
            ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
            
            success = await ir_db.add_command(
                device_name=learning_context["device_name"],
                command_name=learning_context["command_name"],
                freq_khz=ir_data.get("freq_khz", 38),
                duty=33,
                repeat=1,
                raw_data=ir_data.get("combined", []),
            )
            
            if success:
                _LOGGER.info(
                    "Command '%s' saved to database for device '%s'",
                    learning_context["command_name"],
                    learning_context["device_name"],
                )
                
                # Fire unified event - SUCCESS
                self.hass.bus.async_fire(
                    "haptique_operation",
                    {
                        "operation": "learn",
                        "status": "success",
                        "entity_type": "command",
                        "device_name": learning_context["device_name"],
                        "command_name": learning_context["command_name"],
                        "data": {
                            "freq_khz": ir_data.get("freq_khz", 38),
                            "count": len(ir_data.get("combined", [])),
                            "frames": ir_data.get("frames", 1),
                        }
                    }
                )
                
                # Clear learning context
                self._learning_context = None
                
                # Force refresh to update storage sensors
                await self.async_refresh()
            else:
                _LOGGER.error("Failed to save command to database")
                
                # Fire unified event - ERROR
                self.hass.bus.async_fire(
                    "haptique_operation",
                    {
                        "operation": "learn",
                        "status": "error",
                        "entity_type": "command",
                        "device_name": learning_context["device_name"],
                        "command_name": learning_context["command_name"],
                        "error": "Failed to save to database"
                    }
                )
        else:
            # Standard manual learning (no context)
            raw_data = ir_data.get("combined", [])
            freq_khz = ir_data.get("freq_khz", 38)
            frames = ir_data.get("frames", 1)
            count = len(raw_data)
            
            _LOGGER.info("Manual learning captured: %d values", count)
            
            # Fire capture event (for manual raw capture)
            self.hass.bus.async_fire(
                "haptique_ir_captured",
                {
                    "raw_data": raw_data,
                    "freq_khz": freq_khz,
                    "frames": frames,
                    "count": count,
                }
            )

    async def update_learn_ir_code(self, ir_data: dict[str, Any]) -> None:
        """Update the learned IR code."""
        self.last_learn_ir_code = ir_data
        self.last_learn_ir_timestamp = dt_util.utcnow()
        _LOGGER.info(
            "Learn IR code updated: %d values", len(ir_data.get("combined", []))
        )
        # Force immediate refresh
        await self.async_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            # Get main status
            _LOGGER.debug("Fetching main status from %s", API_STATUS)
            status_data = await self._request("GET", API_STATUS)
            _LOGGER.debug("Status data type: %s, content: %s", type(status_data), status_data)
            
            # Get WiFi status
            _LOGGER.debug("Fetching WiFi status from %s", API_WIFI_STATUS)
            wifi_data = await self._request("GET", API_WIFI_STATUS)
            _LOGGER.debug("WiFi data type: %s, content: %s", type(wifi_data), wifi_data)
            
            # Get IR RX info
            try:
                _LOGGER.debug("Fetching IR RX info from %s", API_IR_RXINFO)
                ir_rx_info = await self._request("GET", API_IR_RXINFO)
                _LOGGER.debug("IR RX info type: %s, content: %s", type(ir_rx_info), ir_rx_info)
                self.ir_rx_info = ir_rx_info
            except Exception as err:
                _LOGGER.warning("Failed to get IR RX info: %s", err)
                self.ir_rx_info = {}
            
            # Get storage info from /api/ir/saved
            try:
                _LOGGER.debug("Fetching storage info from %s", API_IR_SAVED)
                saved_data = await self._request("GET", API_IR_SAVED)
                _LOGGER.debug("Saved data type: %s, content: %s", type(saved_data), saved_data)
                
                # Map the API response to expected format
                self.storage_info = {
                    "ir_count": saved_data.get("count", 0),
                    "ir_max": saved_data.get("max", 50),
                    "ir_available": saved_data.get("available", 50),
                }
                _LOGGER.debug("Mapped storage info: %s", self.storage_info)
            except Exception as err:
                _LOGGER.warning("Failed to get storage info: %s", err)
                self.storage_info = {
                    "ir_count": 0,
                    "ir_max": 50,
                    "ir_available": 50,
                }
            
            # Update device info
            self.device_info = {
                "hostname": status_data.get("hostname", "haptique-extender"),
                "instance": status_data.get("instance", "Haptique Extender"),
                "mac": status_data.get("mac", ""),
                "fw_ver": status_data.get("fw_ver", "unknown"),
                "ap_on": status_data.get("ap_on", False),
                "sta_ok": status_data.get("sta_ok", False),
                "sta_ssid": status_data.get("sta_ssid", ""),
            }
            _LOGGER.debug("Device info updated: %s", self.device_info)
            
            return {
                "status": status_data,
                "wifi": wifi_data,
                "ir_rx_info": self.ir_rx_info,
                "storage_info": self.storage_info,
                "last_learn_ir_code": self.last_learn_ir_code,
                "last_learn_ir_timestamp": self.last_learn_ir_timestamp,
                "learning_mode": self._learning_mode,
            }
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _request(
        self, method: str, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a request to the API."""
        url = f"{self.base_url}{endpoint}"
        
        # Prepare headers with authentication
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method == "GET":
                async with self.session.get(url, headers=headers, timeout=10) as response:
                    response.raise_for_status()
                    result = await response.json()
                    # Ensure we always return a dict
                    if isinstance(result, dict):
                        return result
                    else:
                        _LOGGER.warning("API %s returned non-dict: %s", endpoint, type(result))
                        return {}
            elif method == "POST":
                async with self.session.post(
                    url, json=data, headers=headers, timeout=10
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    # Ensure we always return a dict
                    if isinstance(result, dict):
                        return result
                    else:
                        _LOGGER.warning("API %s returned non-dict: %s", endpoint, type(result))
                        return {}
            else:
                raise ValueError(f"Unsupported method: {method}")
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Error requesting %s: %s", url, err)
            raise
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout requesting %s", url)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error requesting %s: %s", url, err)
            raise
    
    async def send_ir_code(
        self,
        raw_data: list[int],
        freq_khz: int = 38,
        duty: int = 33,
        repeat: int = 1,
    ) -> bool:
        """Send an IR code to the device."""
        try:
            payload = {
                "freq": freq_khz * 1000,  # Convert kHz to Hz
                "duty": duty,
                "repeat": repeat,
                "raw": raw_data,
            }
            
            # Debug: Log complete request details
            _LOGGER.debug(
                "=== IR SEND REQUEST ===\n"
                "URL: %s%s\n"
                "Method: POST\n"
                "Payload:\n"
                "  freq: %d Hz (%d kHz)\n"
                "  duty: %d%%\n"
                "  repeat: %d\n"
                "  raw: %s (length: %d)\n"
                "=======================\n"
                "\n"
                "CURL Command to reproduce:\n"
                "curl -X POST \\\n"
                "  -H 'Authorization: Bearer YOUR_TOKEN' \\\n"
                "  -H 'Content-Type: application/json' \\\n"
                "  -d '{\"freq\":%d,\"duty\":%d,\"repeat\":%d,\"raw\":%s}' \\\n"
                "  %s%s",
                self.base_url,
                API_IR_SEND,
                payload["freq"],
                freq_khz,
                duty,
                repeat,
                raw_data,
                len(raw_data),
                payload["freq"],
                duty,
                repeat,
                raw_data,
                self.base_url,
                API_IR_SEND
            )
            
            await self._request("POST", API_IR_SEND, payload)
            _LOGGER.info("IR code sent successfully")
            return True
            
        except Exception as err:
            _LOGGER.error("Failed to send IR code: %s", err)
            return False
