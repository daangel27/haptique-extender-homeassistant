"""Firmware IR Storage API Helper for Haptique Extender."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)


class FirmwareIRStorage:
    """Helper class to interact with firmware's IR command storage API."""

    def __init__(self, host: str, token: str, session: aiohttp.ClientSession) -> None:
        """Initialize the firmware storage helper."""
        self.host = host
        self.token = token
        self.session = session
        self.base_url = f"http://{host}"

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a request to the firmware API."""
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        
        try:
            async with self.session.request(
                method,
                url,
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 401:
                    raise Exception("Authentication failed")
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")
                return await resp.json()
        except aiohttp.ClientError as err:
            raise Exception(f"Request failed: {err}") from err

    async def save_last_ir(self, name: str) -> bool:
        """Save the last received IR code with a name."""
        try:
            result = await self._request("POST", "/api/ir/save", {"name": name})
            return result.get("status") == "saved"
        except Exception as err:
            _LOGGER.error("Failed to save IR command '%s': %s", name, err)
            return False

    async def list_saved_ir(self) -> list[str]:
        """List all saved IR command names."""
        try:
            result = await self._request("GET", "/api/ir/saved")
            return result.get("names", [])
        except Exception as err:
            _LOGGER.error("Failed to list saved IR commands: %s", err)
            return []

    async def send_ir_by_name(self, name: str) -> bool:
        """Send a saved IR command by name."""
        try:
            result = await self._request("POST", "/api/ir/send/name", {"name": name})
            return result.get("status") == "sent"
        except Exception as err:
            _LOGGER.error("Failed to send IR command '%s': %s", name, err)
            return False

    async def delete_ir_command(self, name: str) -> bool:
        """Delete a saved IR command."""
        try:
            result = await self._request("DELETE", "/api/ir/delete", {"name": name})
            return result.get("status") == "deleted"
        except Exception as err:
            _LOGGER.error("Failed to delete IR command '%s': %s", name, err)
            return False

    async def clear_all_ir(self) -> bool:
        """Clear all saved IR commands."""
        try:
            result = await self._request("POST", "/api/ir/clear")
            return result.get("status") == "cleared"
        except Exception as err:
            _LOGGER.error("Failed to clear IR commands: %s", err)
            return False
