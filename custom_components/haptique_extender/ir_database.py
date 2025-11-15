"""IR Device Database Manager for Haptique Extender - VERSION ULTRA CORRIGÉE."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from homeassistant.util.file import write_utf8_file

_LOGGER = logging.getLogger(__name__)

DEFAULT_DATABASE_FILE = "haptique_ir_devices.json"


class IRDatabase:
    """Manage IR devices and commands in JSON format."""

    def __init__(self, hass: HomeAssistant, config_dir: str | None = None) -> None:
        """Initialize the IR database."""
        self.hass = hass
        self.config_dir = config_dir or hass.config.path()
        self.db_file = os.path.join(self.config_dir, DEFAULT_DATABASE_FILE)
        self._data: dict[str, Any] = {"version": "1.0", "devices": {}}

    async def async_load(self) -> None:
        """Load database from JSON file asynchronously."""
        if os.path.exists(self.db_file):
            try:
                content = await self.hass.async_add_executor_job(
                    lambda: open(self.db_file, "r", encoding="utf-8").read()
                )
                self._data = json.loads(content)
                
                # CORRECTION ULTRA: Normaliser TOUTES les clés de commandes en strings
                for device_id in self._data.get("devices", {}):
                    commands = self._data["devices"][device_id].get("commands", {})
                    normalized_commands = {}
                    for key, value in commands.items():
                        # Force la clé en string
                        normalized_commands[str(key)] = value
                    self._data["devices"][device_id]["commands"] = normalized_commands
                
                _LOGGER.info("IR database loaded and normalized from %s", self.db_file)
            except Exception as err:
                _LOGGER.error("Failed to load IR database: %s", err)
                self._data = {"version": "1.0", "devices": {}}
        else:
            _LOGGER.info("IR database file not found, creating new one")
            await self._save()

    def _save(self) -> None:
        """Save database to JSON file (non-blocking)."""
        try:
            # CORRECTION ULTRA: Avant de sauvegarder, s'assurer que toutes les clés sont des strings
            for device_id in self._data.get("devices", {}):
                commands = self._data["devices"][device_id].get("commands", {})
                normalized_commands = {}
                for key, value in commands.items():
                    normalized_commands[str(key)] = value
                self._data["devices"][device_id]["commands"] = normalized_commands
            
            data_str = json.dumps(self._data, indent=2, ensure_ascii=False)
            write_utf8_file(self.db_file, data_str)
            _LOGGER.debug("IR database saved to %s", self.db_file)
        except Exception as err:
            _LOGGER.error("Failed to save IR database: %s", err)

    def add_device(
        self,
        device_id: str,
        device_name: str | None = None,
        device_type: str | None = None,
    ) -> bool:
        """Add or update a device."""
        if device_id not in self._data["devices"]:
            self._data["devices"][device_id] = {
                "name": device_name or device_id,
                "type": device_type or "Generic",
                "created_at": dt_util.utcnow().isoformat(),
                "commands": {},
            }
            self._save()
            _LOGGER.info("Device '%s' added to database", device_id)
            return True
        else:
            # Update existing device info
            if device_name:
                self._data["devices"][device_id]["name"] = device_name
            if device_type:
                self._data["devices"][device_id]["type"] = device_type
            self._save()
            _LOGGER.info("Device '%s' updated in database", device_id)
            return True

    def add_command(
        self,
        device_id: str,
        command_name: str,
        freq_khz: int,
        duty: int,
        repeat: int,
        raw_data: list[int],
        command_label: str | None = None,
    ) -> bool:
        """Add or update a command for a device."""
        if device_id not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found in database", device_id)
            return False

        # CORRECTION ULTRA: Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()
        
        _LOGGER.info("Adding command '%s' (type: %s) to device '%s'", 
                    command_name, type(command_name).__name__, device_id)

        self._data["devices"][device_id]["commands"][command_name] = {
            "name": command_label or command_name,
            "freq_khz": freq_khz,
            "duty": duty,
            "repeat": repeat,
            "raw": raw_data,
            "learned_at": dt_util.utcnow().isoformat(),
        }
        self._save()
        _LOGGER.info(
            "Command '%s' added to device '%s'", command_name, device_id
        )
        return True

    def get_command(
        self, device_id: str, command_name: str
    ) -> dict[str, Any] | None:
        """Get a specific command."""
        if device_id not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_id)
            return None

        # CORRECTION ULTRA: Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()
        
        commands = self._data["devices"][device_id].get("commands", {})
        
        # CORRECTION ULTRA: Log pour debug
        _LOGGER.debug("Looking for command '%s' (type: %s) in device '%s'", 
                     command_name, type(command_name).__name__, device_id)
        _LOGGER.debug("Available commands: %s (types: %s)", 
                     list(commands.keys()),
                     [f"{k}:{type(k).__name__}" for k in commands.keys()])
        
        # Recherche directe avec la clé normalisée
        if command_name in commands:
            _LOGGER.debug("Command '%s' found directly", command_name)
            return commands[command_name]
        
        # Recherche de secours en normalisant toutes les clés
        for key, value in commands.items():
            normalized_key = str(key).strip()
            if normalized_key == command_name:
                _LOGGER.debug("Command '%s' found after normalization (original key: '%s')", 
                            command_name, key)
                return value
        
        _LOGGER.error(
            "Command '%s' not found for device '%s' (available: %s)", 
            command_name, device_id, list(commands.keys())
        )
        return None

    def get_device(self, device_id: str) -> dict[str, Any] | None:
        """Get device info."""
        return self._data["devices"].get(device_id)

    def list_devices(self) -> list[dict[str, Any]]:
        """List all devices."""
        devices = []
        for device_id, device_data in self._data["devices"].items():
            devices.append(
                {
                    "id": device_id,
                    "name": device_data.get("name", device_id),
                    "type": device_data.get("type", "Generic"),
                    "command_count": len(device_data.get("commands", {})),
                    "created_at": device_data.get("created_at"),
                }
            )
        return devices

    def list_commands(self, device_id: str) -> list[dict[str, Any]]:
        """List all commands for a device."""
        if device_id not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_id)
            return []

        commands = []
        for cmd_name, cmd_data in self._data["devices"][device_id].get(
            "commands", {}
        ).items():
            # CORRECTION ULTRA: S'assurer que cmd_name est toujours une string
            cmd_name_str = str(cmd_name).strip()
            commands.append(
                {
                    "name": cmd_name_str,
                    "label": cmd_data.get("name", cmd_name_str),
                    "freq_khz": cmd_data.get("freq_khz"),
                    "learned_at": cmd_data.get("learned_at"),
                }
            )
        return commands

    def delete_command(self, device_id: str, command_name: str) -> bool:
        """Delete a command from a device."""
        if device_id not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_id)
            return False

        # CORRECTION ULTRA: Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()

        commands = self._data["devices"][device_id].get("commands", {})
        
        # CORRECTION ULTRA: Chercher la clé en normalisant
        key_to_delete = None
        for key in list(commands.keys()):
            normalized_key = str(key).strip()
            if normalized_key == command_name:
                key_to_delete = key
                break
        
        if key_to_delete is not None:
            del commands[key_to_delete]
            self._save()
            _LOGGER.info(
                "Command '%s' deleted from device '%s'", command_name, device_id
            )
            return True

        _LOGGER.error(
            "Command '%s' not found for device '%s' (available: %s)", 
            command_name, device_id, list(commands.keys())
        )
        return False

    def delete_device(self, device_id: str) -> bool:
        """Delete a device and all its commands."""
        if device_id in self._data["devices"]:
            del self._data["devices"][device_id]
            self._save()
            _LOGGER.info("Device '%s' deleted from database", device_id)
            return True

        _LOGGER.error("Device '%s' not found", device_id)
        return False

    def export_device(self, device_id: str) -> dict[str, Any] | None:
        """Export device data for sharing."""
        return self.get_device(device_id)

    def import_device(self, device_data: dict[str, Any]) -> bool:
        """Import device data from export."""
        try:
            device_id = device_data.get("id")
            if not device_id:
                _LOGGER.error("Device ID missing in import data")
                return False

            # CORRECTION ULTRA: Normaliser les commandes importées
            commands = device_data.get("commands", {})
            normalized_commands = {}
            for key, value in commands.items():
                normalized_commands[str(key).strip()] = value

            self._data["devices"][device_id] = {
                "name": device_data.get("name", device_id),
                "type": device_data.get("type", "Generic"),
                "created_at": device_data.get("created_at", dt_util.utcnow().isoformat()),
                "commands": normalized_commands,
            }
            self._save()
            _LOGGER.info("Device '%s' imported successfully", device_id)
            return True
        except Exception as err:
            _LOGGER.error("Failed to import device: %s", err)
            return False