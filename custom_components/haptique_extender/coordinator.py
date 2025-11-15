"""DataUpdateCoordinator for Haptique Extender - Version 2.0 (No WebSocket, API Polling)."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    API_IR_LAST,
    API_IR_RXINFO,
    API_STATUS,
    API_WIFI_STATUS,
    API_STORAGE_INFO,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class HaptiqueCoordinator(DataUpdateCoordinator):
    """Haptique Extender coordinator - API polling version."""

    def __init__(self, hass: HomeAssistant, host: str, token: str) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.host = host
        self.token = token
        self.session = async_get_clientsession(hass)
        self.device_info: dict[str, Any] = {}
        
        # Separate storage for learn mode
        self.last_learn_ir_code: dict[str, Any] | None = None
        self.last_learn_ir_timestamp = None
        
        # IR RX info for monitoring
        self.ir_rx_info: dict[str, Any] = {}
        
        # Storage info
        self.storage_info: dict[str, Any] = {}
        
        self._learning_mode = False
        self._learning_context: dict[str, Any] | None = None
        self._learning_task: asyncio.Task | None = None
        self._last_ir_raw_hash: int | None = None  # To detect new IR codes

    @property
    def learning_mode(self) -> bool:
        """Return if learning mode is active."""
        return self._learning_mode

    def set_learning_mode(self, enabled: bool) -> None:
        """Set learning mode."""
        was_learning = self._learning_mode
        self._learning_mode = enabled
        
        if enabled and not was_learning:
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
        max_timeout = 30  # 30 seconds total timeout
        check_interval = 2  # Check every 2 seconds (pas 1s)
        initial_delay = 3  # Attendre 3s avant le premier check
        
        try:
            # Récupérer le hash initial AVANT d'attendre
            try:
                initial_ir_data = await self.get_last_ir_code()
                if initial_ir_data and "combined" in initial_ir_data:
                    self._last_ir_raw_hash = hash(tuple(initial_ir_data.get("combined", [])))
                    _LOGGER.info("Initial IR hash captured: %s", self._last_ir_raw_hash)
                else:
                    self._last_ir_raw_hash = None
            except Exception as err:
                _LOGGER.debug("No initial IR code: %s", err)
                self._last_ir_raw_hash = None
            
            # Attendre 3 secondes AVANT de commencer à checker
            _LOGGER.info("Waiting %ds before starting to check for new IR codes...", initial_delay)
            await asyncio.sleep(initial_delay)
            
            elapsed = initial_delay
            
            while self._learning_mode and elapsed < max_timeout:
                # Poll every 2 seconds
                await asyncio.sleep(check_interval)
                elapsed += check_interval
                
                _LOGGER.debug("Learning poll check at %ds/%ds", elapsed, max_timeout)
                
                try:
                    ir_data = await self.get_last_ir_code()
                    
                    if ir_data and "combined" in ir_data:
                        # Calculate hash to detect new codes
                        raw_data = ir_data.get("combined", [])
                        current_hash = hash(tuple(raw_data))
                        
                        if current_hash != self._last_ir_raw_hash:
                            # New IR code detected!
                            _LOGGER.info(
                                "🎯 NEW IR code detected after %ds: %d values, %d frames",
                                elapsed,
                                len(raw_data),
                                ir_data.get("frames", 1),
                            )
                            
                            # Process the captured code
                            await self._process_captured_ir_code(ir_data)
                            
                            # Stop learning mode
                            self.set_learning_mode(False)
                            break
                        else:
                            _LOGGER.debug("Same IR code (hash: %s), waiting for new one...", current_hash)
                            
                except Exception as err:
                    _LOGGER.debug("Error during learning poll: %s", err)
            
            # Timeout reached
            if elapsed >= max_timeout and self._learning_mode:
                _LOGGER.info("Learning mode timeout after %ds", max_timeout)
                self.set_learning_mode(False)
                
                # Fire timeout event (notification handled by automation)
                self.hass.bus.async_fire(
                    "haptique_learning_timeout",
                    {"timeout": max_timeout}
                )
                    
        except asyncio.CancelledError:
            _LOGGER.debug("Learning poll loop cancelled")
        except Exception as err:
            _LOGGER.error("Unexpected error in learning poll loop: %s", err)
            self.set_learning_mode(False)

    async def _process_captured_ir_code(self, ir_data: dict[str, Any]) -> None:
        """Process a captured IR code."""
        # Update learn sensor
        await self.update_learn_ir_code(ir_data)
        
        # Check if there's a learning context (from learn_ir_command service)
        learning_context = self._learning_context
        
        if learning_context:
            # Save to database
            from .ir_database import IRDatabase
            
            ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
            
            success = ir_db.add_command(
                device_id=learning_context["device_id"],
                command_name=learning_context["command_name"],
                freq_khz=ir_data.get("freq_khz", 38),
                duty=33,
                repeat=1,
                raw_data=ir_data.get("combined", []),
                command_label=learning_context.get(
                    "command_label", learning_context["command_name"]
                ),
            )
            
            if success:
                _LOGGER.info(
                    "Command '%s' saved to database for device '%s'",
                    learning_context["command_name"],
                    learning_context["device_id"],
                )
                
                # Fire success event (notification handled by automation)
                self.hass.bus.async_fire(
                    "haptique_command_learned",
                    {
                        "device_id": learning_context["device_id"],
                        "device_name": learning_context["device_name"],
                        "command_name": learning_context["command_name"],
                        "command_label": learning_context.get("command_label", learning_context["command_name"]),
                    }
                )
                
                # Clear learning context
                self._learning_context = None
            else:
                _LOGGER.error("Failed to save command to database")
                
                # Fire error event (notification handled by automation)
                self.hass.bus.async_fire("haptique_learning_error", {})
        else:
            # Standard manual learning (no context) - fire event
            raw_data = ir_data.get("combined", [])
            freq_khz = ir_data.get("freq_khz", 38)
            frames = ir_data.get("frames", 1)
            count = len(raw_data)
            
            _LOGGER.info("Manual learning captured: %d values", count)
            
            # Fire manual capture event (notification handled by automation)
            self.hass.bus.async_fire(
                "haptique_ir_captured_manual",
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
            status_data = await self._request("GET", API_STATUS)
            
            # Get WiFi status
            wifi_data = await self._request("GET", API_WIFI_STATUS)
            
            # Get IR RX info
            try:
                ir_rx_info = await self._request("GET", API_IR_RXINFO)
                self.ir_rx_info = ir_rx_info
            except Exception:
                self.ir_rx_info = {}
            
            # Get storage info
            try:
                storage_info = await self._request("GET", API_STORAGE_INFO)
                self.storage_info = storage_info
            except Exception:
                self.storage_info = {}
            
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
        url = f"http://{self.host}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        
        try:
            async with self.session.request(
                method, url, json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 401:
                    raise UpdateFailed("Authentication failed")
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status}")
                return await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Request failed: {err}") from err

    async def send_ir_code(
        self, raw_data: list[int], freq_khz: int = 38, duty: int = 33, repeat: int = 1
    ) -> bool:
        """Send IR code."""
        payload = {"freq_khz": freq_khz, "duty": duty, "repeat": repeat, "raw": raw_data}
        
        try:
            result = await self._request("POST", "/api/ir/send", payload)
            return result.get("status") == "sent"
        except Exception as err:
            _LOGGER.error("Failed to send IR code: %s", err)
            return False

    async def get_last_ir_code(self) -> dict[str, Any] | None:
        """Get last captured IR code."""
        try:
            return await self._request("GET", API_IR_LAST)
        except Exception:
            return None

    async def async_shutdown(self) -> None:
        """Shutdown coordinator."""
        if self._learning_task:
            self._learning_task.cancel()
            try:
                await self._learning_task
            except asyncio.CancelledError:
                pass