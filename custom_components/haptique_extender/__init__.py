"""Haptique Extender integration - Simplified with Unified Events."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .coordinator import HaptiqueCoordinator
from .firmware_storage import FirmwareIRStorage
from .ir_database import IRDatabase, InvalidNameError

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Haptique Extender from a config entry."""
    host = entry.data[CONF_HOST]
    token = entry.data.get(CONF_TOKEN, "")

    # Initialize coordinator
    coordinator = HaptiqueCoordinator(hass, host, token)
    
    # Initial data fetch
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Initialize IR Database (shared across all entries)
    if "ir_database" not in hass.data[DOMAIN]:
        ir_db = IRDatabase(hass)
        await ir_db.async_load()
        hass.data[DOMAIN]["ir_database"] = ir_db
        _LOGGER.info("IR Database initialized")

    # Initialize Firmware Storage
    firmware_storage = FirmwareIRStorage(host, token, coordinator.session)
    hass.data[DOMAIN][f"{entry.entry_id}_firmware"] = firmware_storage
    _LOGGER.info("Firmware Storage initialized")

    # Register device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, coordinator.device_info["mac"])},
        name=coordinator.device_info.get("hostname", "Haptique Extender"),
        manufacturer="KINCONY",
        model="KC868-AG",
        sw_version=coordinator.device_info.get("fw_ver", "unknown"),
    )

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services (only once)
    if not hass.services.has_service(DOMAIN, "send_ir_code"):
        _register_services(hass)
        _LOGGER.info("Services registered")

    return True


def _register_services(hass: HomeAssistant) -> None:
    """Register all integration services."""

    async def handle_send_ir_code(call):
        """Handle send_ir_code service (raw IR code)."""
        # Get coordinator from any entry
        coordinator = _get_any_coordinator(hass)
        if not coordinator:
            _LOGGER.error("No coordinator available")
            return
        
        raw_data = call.data.get("raw_data", [])
        freq_khz = call.data.get("freq_khz", 38)
        duty = call.data.get("duty", 33)
        repeat = call.data.get("repeat", 1)
        
        success = await coordinator.send_ir_code(raw_data, freq_khz, duty, repeat)
        
        if not success:
            _LOGGER.error("Failed to send IR code")

    async def handle_learn_ir_command(call):
        """Handle learn_ir_command service."""
        coordinator = _get_any_coordinator(hass)
        if not coordinator:
            _LOGGER.error("No coordinator available")
            return
        
        device_name = call.data.get("device_name", "").strip()
        command_name = call.data.get("command_name", "").strip()
        timeout = call.data.get("timeout", 30)

        # Validation: device_name and command_name must not be empty
        if not device_name:
            _LOGGER.error("device_name cannot be empty")
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "learn",
                    "status": "error",
                    "entity_type": "command",
                    "error": "Device name cannot be empty"
                }
            )
            return
        
        if not command_name:
            _LOGGER.error("command_name cannot be empty")
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "learn",
                    "status": "error",
                    "entity_type": "command",
                    "device_name": device_name,
                    "error": "Command name cannot be empty"
                }
            )
            return

        # Validate names
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        try:
            from .ir_database import validate_name
            device_name = validate_name(device_name)
            command_name = validate_name(command_name)
        except InvalidNameError as err:
            _LOGGER.error("Invalid name: %s", err)
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "learn",
                    "status": "error",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                    "error": str(err)
                }
            )
            return

        await ir_db.add_device(device_name)
        
        coordinator.set_learning_context(device_name, command_name)
        coordinator.set_learning_mode(True)
        
        _LOGGER.info(
            "Learning mode activated for device '%s', command '%s'",
            device_name,
            command_name,
        )
        
        # Fire unified event - STARTED
        hass.bus.async_fire(
            "haptique_operation",
            {
                "operation": "learn",
                "status": "started",
                "entity_type": "command",
                "device_name": device_name,
                "command_name": command_name,
                "data": {"timeout": timeout}
            }
        )

    async def handle_send_ir_command(call):
        """Handle send_ir_command service (from database)."""
        coordinator = _get_any_coordinator(hass)
        if not coordinator:
            _LOGGER.error("No coordinator available")
            return
        
        device_name = call.data.get("device_name")
        command_name = call.data.get("command_name")
        
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        command = ir_db.get_command(device_name, command_name)
        if not command:
            _LOGGER.error(
                "Command '%s' not found for device '%s'",
                command_name,
                device_name,
            )
            
            # Fire unified event - ERROR (not found)
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "send",
                    "status": "error",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                    "error": "Command not found in database"
                }
            )
            return
        
        success = await coordinator.send_ir_code(
            command["raw"],
            command["freq_khz"],
            command["duty"],
            command["repeat"],
        )
        
        if success:
            _LOGGER.info("Command '%s' sent to device '%s'", command_name, device_name)
            
            # Fire unified event - SUCCESS
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "send",
                    "status": "success",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                }
            )
        else:
            _LOGGER.error("Failed to send command '%s' to device '%s'", command_name, device_name)
            
            # Fire unified event - ERROR
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "send",
                    "status": "error",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                    "error": "Failed to send IR code"
                }
            )

    async def handle_delete_ir_command(call):
        """Handle delete_ir_command service."""
        device_name = call.data.get("device_name")
        command_name = call.data.get("command_name")
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        success = await ir_db.delete_command(device_name, command_name)
        
        if success:
            _LOGGER.info("Command '%s' deleted from device '%s'", command_name, device_name)
            
            # Fire unified event - SUCCESS
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "delete",
                    "status": "success",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                }
            )
        else:
            _LOGGER.error("Failed to delete command '%s' from device '%s'", command_name, device_name)
            
            # Fire unified event - ERROR
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "delete",
                    "status": "error",
                    "entity_type": "command",
                    "device_name": device_name,
                    "command_name": command_name,
                    "error": "Command not found or delete failed"
                }
            )

    async def handle_delete_ir_device(call):
        """Handle delete_ir_device service."""
        device_name = call.data.get("device_name")
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        success = await ir_db.delete_device(device_name)
        
        if success:
            _LOGGER.info("Device '%s' deleted", device_name)
            
            # Fire unified event - SUCCESS
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "delete",
                    "status": "success",
                    "entity_type": "device",
                    "device_name": device_name,
                }
            )
        else:
            _LOGGER.error("Failed to delete device '%s'", device_name)
            
            # Fire unified event - ERROR
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "delete",
                    "status": "error",
                    "entity_type": "device",
                    "device_name": device_name,
                    "error": "Device not found or delete failed"
                }
            )

    async def handle_set_commands_device(call):
        """Handle set_commands_device service (to update commands sensor)."""
        device_name = call.data.get("device_name")
        
        # Find the commands sensor and update it
        from homeassistant.helpers import entity_registry as er
        ent_reg = er.async_get(hass)
        
        # Find the commands sensor entity
        for entity_entry in ent_reg.entities.values():
            if entity_entry.domain == "sensor" and "ir_commands" in entity_entry.unique_id:
                # Get the actual entity object from the state machine
                entity_id = entity_entry.entity_id
                
                # Access the entity through the component
                component = hass.data.get("entity_components", {}).get("sensor")
                if component:
                    entity_obj = component.get_entity(entity_id)
                    if entity_obj and hasattr(entity_obj, "set_device"):
                        entity_obj.set_device(device_name)
                        _LOGGER.info("Commands sensor updated for device: %s", device_name)
                        break
    
    async def handle_list_device_commands(call):
        """Handle list_device_commands service - List commands for a specific device."""
        device_name = call.data.get("device_name")
        
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        commands = ir_db.list_commands(device_name)
        
        if commands:
            _LOGGER.info(
                "Device '%s' has %d command(s): %s",
                device_name,
                len(commands),
                [c["name"] for c in commands]
            )
            
            # Fire unified event - SUCCESS
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "list_commands",
                    "status": "success",
                    "entity_type": "device",
                    "device_name": device_name,
                    "data": {
                        "command_count": len(commands),
                        "commands": commands
                    }
                }
            )
        else:
            _LOGGER.warning("No commands found for device '%s'", device_name)
            
            # Fire unified event - ERROR (no commands)
            hass.bus.async_fire(
                "haptique_operation",
                {
                    "operation": "list_commands",
                    "status": "error",
                    "entity_type": "device",
                    "device_name": device_name,
                    "error": "No commands found for this device"
                }
            )

    # Register all services
    hass.services.async_register(DOMAIN, "send_ir_code", handle_send_ir_code)
    hass.services.async_register(DOMAIN, "learn_ir_command", handle_learn_ir_command)
    hass.services.async_register(DOMAIN, "send_ir_command", handle_send_ir_command)
    hass.services.async_register(DOMAIN, "delete_ir_command", handle_delete_ir_command)
    hass.services.async_register(DOMAIN, "delete_ir_device", handle_delete_ir_device)
    hass.services.async_register(DOMAIN, "set_commands_device", handle_set_commands_device)
    hass.services.async_register(DOMAIN, "list_device_commands", handle_list_device_commands)


def _get_any_coordinator(hass: HomeAssistant) -> HaptiqueCoordinator | None:
    """Get any available coordinator."""
    for entry_id in hass.data[DOMAIN]:
        if entry_id not in ["ir_database"]:
            if not entry_id.endswith("_firmware"):
                coordinator = hass.data[DOMAIN].get(entry_id)
                if coordinator:
                    return coordinator
    return None


def _get_any_firmware_storage(hass: HomeAssistant) -> FirmwareIRStorage | None:
    """Get any available firmware storage."""
    for entry_id in hass.data[DOMAIN]:
        if entry_id.endswith("_firmware"):
            firmware = hass.data[DOMAIN].get(entry_id)
            if firmware:
                return firmware
    return None


async def _refresh_db_sensors(hass: HomeAssistant) -> None:
    """Force refresh of database sensors."""
    coordinator = _get_any_coordinator(hass)
    if coordinator:
        await coordinator.async_request_refresh()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Remove firmware storage
        firmware_key = f"{entry.entry_id}_firmware"
        if firmware_key in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(firmware_key)

    # Remove services if this is the last entry
    loaded_entries = [
        entry
        for entry in hass.config_entries.async_entries(DOMAIN)
        if entry.state == ConfigEntry.State.LOADED
    ]
    
    if len(loaded_entries) == 1:
        # This is the last entry, remove services
        services_to_remove = [
            "send_ir_code",
            "learn_ir_command",
            "send_ir_command",
            "delete_ir_command",
            "delete_ir_device",
            "set_commands_device",
            "list_device_commands",
        ]
        
        for service_name in services_to_remove:
            if hass.services.has_service(DOMAIN, service_name):
                hass.services.async_remove(DOMAIN, service_name)

    return unload_ok
