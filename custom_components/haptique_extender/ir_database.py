"""IR Database for Haptique Extender - Strict Validation Version."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


class InvalidNameError(Exception):
    """Exception raised when a name contains invalid characters."""
    pass


def validate_name(name: str) -> str:

    # Convert to string and strip whitespace
    name = str(name).strip()
    
    if not name:
        raise InvalidNameError("Name cannot be empty")
    
    # Check for forbidden characters
    # Only allow: a-z, A-Z, 0-9, space, hyphen, underscore
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
        forbidden_chars = re.findall(r'[^a-zA-Z0-9\s\-_]', name)
        raise InvalidNameError(
            f"Name '{name}' contains forbidden characters: {', '.join(set(forbidden_chars))}. "
            f"Only letters, numbers, spaces, hyphens (-) and underscores (_) are allowed."
        )
    
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    
    # Final validation: reasonable length
    if len(name) > 100:
        raise InvalidNameError("Name too long (max 100 characters)")
    
    if len(name) < 1:
        raise InvalidNameError("Name too short (min 1 character)")
    
    return name


class IRDatabase:
    """IR Database manager."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the database."""
        self.hass = hass
        self._data: dict[str, Any] = {"devices": {}}
        self._file_path = Path(hass.config.path("haptique_ir_database.json"))

    async def async_load(self) -> None:
        """Load database from file."""
        try:
            if self._file_path.exists():
                await self.hass.async_add_executor_job(self._load_sync)
                _LOGGER.info("IR database loaded: %d devices", len(self._data["devices"]))
            else:
                _LOGGER.info("No existing IR database found, starting fresh")
        except Exception as err:
            _LOGGER.error("Error loading IR database: %s", err)
            self._data = {"devices": {}}

    def _load_sync(self) -> None:
        """Synchronous load operation."""
        with open(self._file_path, encoding="utf-8") as file:
            self._data = json.load(file)

    def _save_sync(self) -> None:
        """Synchronous save operation."""
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=2, ensure_ascii=False)
        _LOGGER.debug("IR database saved")
    
    async def async_save(self) -> None:
        """Save database to file asynchronously."""
        try:
            await self.hass.async_add_executor_job(self._save_sync)
        except Exception as err:
            _LOGGER.error("Error saving IR database: %s", err)
    
    def _save(self) -> None:
        """Save database to file (deprecated - use async_save)."""
        try:
            with open(self._file_path, "w", encoding="utf-8") as file:
                json.dump(self._data, file, indent=2, ensure_ascii=False)
            _LOGGER.debug("IR database saved")
        except Exception as err:
            _LOGGER.error("Error saving IR database: %s", err)

    async def add_device(self, device_name: str) -> bool:
        """Add or update a device."""
        try:
            # Validate device name
            device_name = validate_name(device_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot add device: %s", err)
            return False
        
        if device_name not in self._data["devices"]:
            self._data["devices"][device_name] = {
                "created_at": dt_util.utcnow().isoformat(),
                "commands": {},
            }
            await self.async_save()
            _LOGGER.info("Device '%s' added to database", device_name)
            return True
        else:
            _LOGGER.info("Device '%s' already exists", device_name)
            return True

    async def add_command(
        self,
        device_name: str,
        command_name: str,
        freq_khz: int,
        duty: int,
        repeat: int,
        raw_data: list[int],
    ) -> bool:
        """Add or update a command for a device."""
        try:
            # Validate names
            device_name = validate_name(device_name)
            command_name = validate_name(command_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot add command: %s", err)
            return False
        
        # Add device if it doesn't exist
        if device_name not in self._data["devices"]:
            await self.add_device(device_name)

        _LOGGER.info("Adding command '%s' to device '%s'", command_name, device_name)

        self._data["devices"][device_name]["commands"][command_name] = {
            "freq_khz": freq_khz,
            "duty": duty,
            "repeat": repeat,
            "raw": raw_data,
            "learned_at": dt_util.utcnow().isoformat(),
        }
        await self.async_save()
        _LOGGER.info("Command '%s' added to device '%s'", command_name, device_name)
        return True

    def get_command(
        self, device_name: str, command_name: str
    ) -> dict[str, Any] | None:
        """Get a specific command."""
        try:
            # Validate names for lookup
            device_name = validate_name(device_name)
            command_name = validate_name(command_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot get command: %s", err)
            return None
        
        if device_name in self._data["devices"]:
            commands = self._data["devices"][device_name]["commands"]
            if command_name in commands:
                return commands[command_name]
        return None

    def list_devices(self) -> list[dict[str, Any]]:
        """List all devices."""
        devices = []
        for device_name in self._data["devices"]:
            device_data = self._data["devices"][device_name]
            devices.append({
                "name": device_name,
                "created_at": device_data.get("created_at"),
                "command_count": len(device_data.get("commands", {})),
            })
        return devices

    def list_commands(self, device_name: str) -> list[dict[str, Any]]:
        """List all commands for a device."""
        try:
            # Validate device name for lookup
            device_name = validate_name(device_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot list commands: %s", err)
            return []
        
        if device_name not in self._data["devices"]:
            return []

        commands = []
        device_commands = self._data["devices"][device_name]["commands"]
        
        for command_name, command_data in device_commands.items():
            commands.append({
                "name": command_name,
                "freq_khz": command_data.get("freq_khz"),
                "duty": command_data.get("duty"),
                "repeat": command_data.get("repeat"),
                "learned_at": command_data.get("learned_at"),
            })
        
        return commands

    async def delete_command(self, device_name: str, command_name: str) -> bool:
        """Delete a command from a device."""
        try:
            # Validate names for lookup
            device_name = validate_name(device_name)
            command_name = validate_name(command_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot delete command: %s", err)
            return False
        
        if device_name in self._data["devices"]:
            commands = self._data["devices"][device_name]["commands"]
            if command_name in commands:
                del commands[command_name]
                await self.async_save()
                _LOGGER.info(
                    "Command '%s' deleted from device '%s'",
                    command_name,
                    device_name,
                )
                
                # If no more commands, optionally delete device
                if not commands:
                    _LOGGER.info(
                        "Device '%s' has no more commands",
                        device_name,
                    )
                
                return True
        
        _LOGGER.warning(
            "Command '%s' not found in device '%s'",
            command_name,
            device_name,
        )
        return False

    async def delete_device(self, device_name: str) -> bool:
        """Delete a device and all its commands."""
        try:
            # Validate device name for lookup
            device_name = validate_name(device_name)
        except InvalidNameError as err:
            _LOGGER.error("Cannot delete device: %s", err)
            return False
        
        if device_name in self._data["devices"]:
            del self._data["devices"][device_name]
            await self.async_save()
            _LOGGER.info("Device '%s' deleted", device_name)
            return True
        
        _LOGGER.warning("Device '%s' not found", device_name)
        return False

    def get_all_data(self) -> dict[str, Any]:
        """Get all database data."""
        return self._data
