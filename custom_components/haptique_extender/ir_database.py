"""IR Device Database Manager for Haptique Extender - VERSION SIMPLIFIÉE."""
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
                
                # Normaliser TOUTES les clés de commandes en strings
                for device_name in self._data.get("devices", {}):
                    commands = self._data["devices"][device_name].get("commands", {})
                    normalized_commands = {}
                    for key, value in commands.items():
                        # Force la clé en string
                        normalized_commands[str(key)] = value
                    self._data["devices"][device_name]["commands"] = normalized_commands
                
                _LOGGER.info("IR database loaded and normalized from %s", self.db_file)
            except Exception as err:
                _LOGGER.error("Failed to load IR database: %s", err)
                self._data = {"version": "1.0", "devices": {}}
        else:
            _LOGGER.info("IR database file not found, creating new one")
            self._data = {"version": "1.0", "devices": {}}
            await self._async_save()

    async def _async_save(self) -> None:
        """Save database to JSON file asynchronously."""
        try:
            # Avant de sauvegarder, s'assurer que toutes les clés sont des strings
            for device_name in self._data.get("devices", {}):
                commands = self._data["devices"][device_name].get("commands", {})
                normalized_commands = {}
                for key, value in commands.items():
                    normalized_commands[str(key)] = value
                self._data["devices"][device_name]["commands"] = normalized_commands
            
            data_str = json.dumps(self._data, indent=2, ensure_ascii=False)
            
            # Utiliser async_add_executor_job pour l'écriture du fichier
            await self.hass.async_add_executor_job(
                write_utf8_file, self.db_file, data_str
            )
            _LOGGER.debug("IR database saved to %s", self.db_file)
        except Exception as err:
            _LOGGER.error("Failed to save IR database: %s", err)

    def _save(self) -> None:
        """Save database to JSON file (non-blocking, synchronous)."""
        try:
            # Avant de sauvegarder, s'assurer que toutes les clés sont des strings
            for device_name in self._data.get("devices", {}):
                commands = self._data["devices"][device_name].get("commands", {})
                normalized_commands = {}
                for key, value in commands.items():
                    normalized_commands[str(key)] = value
                self._data["devices"][device_name]["commands"] = normalized_commands
            
            data_str = json.dumps(self._data, indent=2, ensure_ascii=False)
            write_utf8_file(self.db_file, data_str)
            _LOGGER.debug("IR database saved to %s", self.db_file)
        except Exception as err:
            _LOGGER.error("Failed to save IR database: %s", err)

    def add_device(self, device_name: str) -> bool:
        """Add or update a device."""
        if device_name not in self._data["devices"]:
            self._data["devices"][device_name] = {
                "created_at": dt_util.utcnow().isoformat(),
                "commands": {},
            }
            self._save()
            _LOGGER.info("Device '%s' added to database", device_name)
            return True
        else:
            _LOGGER.info("Device '%s' already exists", device_name)
            return True

    def add_command(
        self,
        device_name: str,
        command_name: str,
        freq_khz: int,
        duty: int,
        repeat: int,
        raw_data: list[int],
    ) -> bool:
        """Add or update a command for a device."""
        if device_name not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found in database", device_name)
            return False

        # Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()
        
        _LOGGER.info("Adding command '%s' (type: %s) to device '%s'", 
                    command_name, type(command_name).__name__, device_name)

        self._data["devices"][device_name]["commands"][command_name] = {
            "freq_khz": freq_khz,
            "duty": duty,
            "repeat": repeat,
            "raw": raw_data,
            "learned_at": dt_util.utcnow().isoformat(),
        }
        self._save()
        _LOGGER.info(
            "Command '%s' added to device '%s'", command_name, device_name
        )
        return True

    def get_command(
        self, device_name: str, command_name: str
    ) -> dict[str, Any] | None:
        """Get a specific command."""
        if device_name not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_name)
            return None

        # Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()
        
        commands = self._data["devices"][device_name].get("commands", {})
        
        # Log pour debug
        _LOGGER.debug("Looking for command '%s' (type: %s) in device '%s'", 
                     command_name, type(command_name).__name__, device_name)
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
            command_name, device_name, list(commands.keys())
        )
        return None

    def get_device(self, device_name: str) -> dict[str, Any] | None:
        """Get device info."""
        return self._data["devices"].get(device_name)

    def list_devices(self) -> list[dict[str, Any]]:
        """List all devices."""
        devices = []
        for device_name, device_data in self._data["devices"].items():
            devices.append(
                {
                    "name": device_name,
                    "command_count": len(device_data.get("commands", {})),
                    "created_at": device_data.get("created_at"),
                }
            )
        return devices

    def list_commands(self, device_name: str) -> list[dict[str, Any]]:
        """List all commands for a device."""
        if device_name not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_name)
            return []

        commands = []
        for cmd_name, cmd_data in self._data["devices"][device_name].get(
            "commands", {}
        ).items():
            # S'assurer que cmd_name est toujours une string
            cmd_name_str = str(cmd_name).strip()
            commands.append(
                {
                    "name": cmd_name_str,
                    "freq_khz": cmd_data.get("freq_khz"),
                    "learned_at": cmd_data.get("learned_at"),
                }
            )
        return commands

    def delete_command(self, device_name: str, command_name: str) -> bool:
        """Delete a command from a device."""
        if device_name not in self._data["devices"]:
            _LOGGER.error("Device '%s' not found", device_name)
            return False

        # Force command_name à string ET strip whitespace
        command_name = str(command_name).strip()

        commands = self._data["devices"][device_name].get("commands", {})
        
        # Chercher la clé en normalisant
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
                "Command '%s' deleted from device '%s'", command_name, device_name
            )
            return True

        _LOGGER.error(
            "Command '%s' not found for device '%s' (available: %s)", 
            command_name, device_name, list(commands.keys())
        )
        return False

    def delete_device(self, device_name: str) -> bool:
        """Delete a device and all its commands."""
        if device_name in self._data["devices"]:
            del self._data["devices"][device_name]
            self._save()
            _LOGGER.info("Device '%s' deleted from database", device_name)
            return True

        _LOGGER.error("Device '%s' not found", device_name)
        return False

    def export_device(self, device_name: str) -> dict[str, Any] | None:
        """Export device data for sharing."""
        return self.get_device(device_name)

    def import_device(self, device_data: dict[str, Any]) -> bool:
        """Import device data from export."""
        try:
            device_name = device_data.get("name")
            if not device_name:
                _LOGGER.error("Device name missing in import data")
                return False

            # Normaliser les commandes importées
            commands = device_data.get("commands", {})
            normalized_commands = {}
            for key, value in commands.items():
                normalized_commands[str(key).strip()] = value

            self._data["devices"][device_name] = {
                "created_at": device_data.get("created_at", dt_util.utcnow().isoformat()),
                "commands": normalized_commands,
            }
            self._save()
            _LOGGER.info("Device '%s' imported successfully", device_name)
            return True
        except Exception as err:
            _LOGGER.error("Failed to import device: %s", err)
            return False
