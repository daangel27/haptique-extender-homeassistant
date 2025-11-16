"""Haptique Extender integration - Version 2.0 with COMPLETE Cleanup."""
from __future__ import annotations

import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN
from .coordinator import HaptiqueCoordinator
from .ir_database import IRDatabase

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]

# Liste des entités créées par les packages qui doivent être supprimées
PACKAGE_ENTITIES = [
    # Input Select
    "input_select.haptique_replay_device",
    "input_select.haptique_replay_command",
    "input_select.haptique_services_device",
    "input_select.haptique_services_command",
    "input_select.haptique_delete_device_selector",
    # Input Text
    "input_text.haptique_last_rf_code",
    "input_text.haptique_new_device_name",
    "input_text.haptique_new_command_name",
    # Input Number
    "input_number.haptique_ir_freq",
    "input_number.haptique_ir_repeat",
    "input_number.haptique_rf_bits",
    "input_number.haptique_rf_protocol",
    # Input Boolean
    "input_boolean.haptique_ir_learning_active",
    # Scripts
    "script.haptique_learn_from_helpers",
    "script.haptique_clear_helpers",
    "script.haptique_send_from_selectors",
    "script.haptique_update_device_list",
    "script.haptique_update_command_list",
    "script.haptique_update_all_services_lists",
    "script.haptique_update_services_command_list",
    "script.haptique_list_all_devices",
    "script.haptique_list_commands_from_services",
    "script.haptique_delete_command_from_services",
    "script.haptique_delete_device_from_services",
    # Automations (IDs)
    "automation.haptique_auto_update_commands_on_device_change",
    "automation.haptique_auto_update_commands_services_db",
    "automation.haptique_auto_update_commands_replay",
    "automation.haptique_auto_refresh_on_startup",
    "automation.haptique_notify_command_sent",
    "automation.haptique_notify_command_delete_error",    
    "automation.haptique_notify_device_delete_error",    
    "automation.haptique_notify_device_delete_error",    
    "automation.haptique_notify_save_error",    
    "automation.haptique_auto_refresh_after_learn",
    "automation.haptique_auto_refresh_after_learning",
    "automation.haptique_notify_learning_mode_activated",
    "automation.haptique_notify_learning_timeout",
    "automation.haptique_notify_ir_code_learned_and_saved",
    "automation.haptique_notify_ir_code_captured_manual",
    "automation.haptique_notify_learning_save_error",
    "automation.haptique_notify_command_sent_success",
    "automation.haptique_notify_command_send_error",
    "automation.haptique_notify_command_not_found",
    "automation.haptique_notify_command_deleted",
    "automation.haptique_notify_device_deleted",
    "automation.haptique_notify_delete_command_error",
    "automation.haptique_notify_delete_device_error",
    "automation.haptique_notify_connection_lost",
    "automation.haptique_notify_connection_restored",
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

    # Initialize IR Database
    if "ir_database" not in hass.data[DOMAIN]:
        ir_db = IRDatabase(hass)
        await ir_db.async_load()
        hass.data[DOMAIN]["ir_database"] = ir_db
        _LOGGER.info("IR Database initialized")

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

    # Register services
    async def handle_send_ir_code(call):
        """Handle send_ir_code service."""
        device_id = call.data.get("device_id")
        if not device_id:
            raw_data = call.data.get("raw_data", [])
            freq_khz = call.data.get("freq_khz", 38)
            duty = call.data.get("duty", 33)
            repeat = call.data.get("repeat", 1)
            
            success = await coordinator.send_ir_code(raw_data, freq_khz, duty, repeat)
            if success:
                _LOGGER.info("IR code sent successfully")
            else:
                _LOGGER.error("Failed to send IR code")

    async def handle_learn_ir_command(call):
        """Handle learn_ir_command service."""
        device_name = call.data.get("device_name")
        command_name = call.data.get("command_name")
        timeout = call.data.get("timeout", 30)

        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        ir_db.add_device(device_name)
        
        coordinator._learning_context = {
            "device_name": device_name,
            "command_name": command_name,
        }
        
        coordinator.set_learning_mode(True)
        
        _LOGGER.info(
            "Learning mode activated for device '%s', command '%s'",
            device_name,
            command_name,
        )
        
        hass.bus.async_fire(
            "haptique_learning_activated",
            {
                "device_name": device_name,
                "command_name": command_name,
                "timeout": timeout,
            }
        )

    async def handle_send_ir_command(call):
        """Handle send_ir_command service."""
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
            hass.bus.async_fire(
                "haptique_command_not_found",
                {
                    "device_name": device_name,
                    "command_name": command_name,
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
            hass.bus.async_fire(
                "haptique_command_sent",
                {
                    "device_name": device_name,
                    "command_name": command_name,
                }
            )
        else:
            _LOGGER.error("Failed to send command '%s' to device '%s'", command_name, device_name)
            hass.bus.async_fire(
                "haptique_command_error",
                {
                    "device_name": device_name,
                    "command_name": command_name,
                    "error": "Failed to send IR code"
                }
            )

    async def handle_list_ir_devices(call):
        """Handle list_ir_devices service."""
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        devices = ir_db.list_devices()
        return {"devices": devices}

    async def handle_list_ir_commands(call):
        """Handle list_ir_commands service."""
        device_name = call.data.get("device_name")
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        commands = ir_db.list_commands(device_name)
        return {"commands": commands}

    async def handle_delete_ir_command(call):
        """Handle delete_ir_command service."""
        device_name = call.data.get("device_name")
        command_name = call.data.get("command_name")
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        success = ir_db.delete_command(device_name, command_name)
        if success:
            _LOGGER.info("Command '%s' deleted from device '%s'", command_name, device_name)
            hass.bus.async_fire(
                "haptique_command_deleted",
                {
                    "device_name": device_name,
                    "command_name": command_name,
                }
            )
        else:
            _LOGGER.error("Failed to delete command '%s' from device '%s'", command_name, device_name)
            hass.bus.async_fire(
                "haptique_delete_command_error",
                {
                    "device_name": device_name,
                    "command_name": command_name,
                }
            )

    async def handle_delete_ir_device(call):
        """Handle delete_ir_device service."""
        device_name = call.data.get("device_name")
        ir_db: IRDatabase = hass.data[DOMAIN]["ir_database"]
        
        device = ir_db.get_device(device_name)
        command_count = len(device.get("commands", {})) if device else 0
        
        success = ir_db.delete_device(device_name)
        if success:
            _LOGGER.info("Device '%s' deleted", device_name)
            hass.bus.async_fire(
                "haptique_device_deleted",
                {
                    "device_name": device_name,
                    "command_count": command_count,
                }
            )
        else:
            _LOGGER.error("Failed to delete device '%s'", device_name)
            hass.bus.async_fire(
                "haptique_delete_device_error",
                {
                    "device_name": device_name,
                }
            )

    # Register services
    hass.services.async_register(DOMAIN, "send_ir_code", handle_send_ir_code)
    hass.services.async_register(DOMAIN, "learn_ir_command", handle_learn_ir_command)
    hass.services.async_register(DOMAIN, "send_ir_command", handle_send_ir_command)
    hass.services.async_register(
        DOMAIN, "list_ir_devices", handle_list_ir_devices, supports_response=True
    )
    hass.services.async_register(
        DOMAIN, "list_ir_commands", handle_list_ir_commands, supports_response=True
    )
    hass.services.async_register(DOMAIN, "delete_ir_command", handle_delete_ir_command)
    hass.services.async_register(DOMAIN, "delete_ir_device", handle_delete_ir_device)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
        
        remaining_entries = [
            e for e in hass.config_entries.async_entries(DOMAIN)
            if e.entry_id != entry.entry_id
        ]
        
        if not remaining_entries:
            _LOGGER.info("Last Haptique Extender device removed - unregistering services")
            
            services_to_remove = [
                "send_ir_code",
                "learn_ir_command",
                "send_ir_command",
                "list_ir_devices",
                "list_ir_commands",
                "delete_ir_command",
                "delete_ir_device",
            ]
            
            for service in services_to_remove:
                if hass.services.has_service(DOMAIN, service):
                    hass.services.async_remove(DOMAIN, service)
                    _LOGGER.debug("Service %s.%s removed", DOMAIN, service)
            
            if "ir_database" in hass.data[DOMAIN]:
                hass.data[DOMAIN].pop("ir_database")
                _LOGGER.info("IR database removed from memory")

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry - COMPLETE CLEANUP."""
    _LOGGER.info("=== Starting COMPLETE removal of Haptique Extender ===")
    
    # Get device MAC if available
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        coordinator = hass.data[DOMAIN][entry.entry_id]
        device_mac = coordinator.device_info.get("mac")
    else:
        device_mac = None
    
    # 1. Clean up integration entities (from entity registry)
    entity_registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(entity_registry, entry.entry_id)
    
    for entity in entities:
        entity_registry.async_remove(entity.entity_id)
        _LOGGER.debug("Removed integration entity: %s", entity.entity_id)
    
    _LOGGER.info("Removed %d integration entities", len(entities))
    
    # 2. Clean up device
    if device_mac:
        device_registry = dr.async_get(hass)
        device = device_registry.async_get_device(identifiers={(DOMAIN, device_mac)})
        
        if device:
            device_registry.async_remove_device(device.id)
            _LOGGER.info("Removed device: %s", device.name)
    
    # 3. Check if last entry
    remaining_entries = [
        e for e in hass.config_entries.async_entries(DOMAIN)
        if e.entry_id != entry.entry_id
    ]
    
    if not remaining_entries:
        _LOGGER.info("Last device - performing COMPLETE cleanup including package entities")
        
        # 4. Remove package-created entities (helpers, scripts, automations)
        removed_count = 0
        unavailable_count = 0
        
        for entity_id in PACKAGE_ENTITIES:
            try:
                # Try to get the entity from registry
                entity = entity_registry.async_get(entity_id)
                
                if entity:
                    # Entity exists in registry - remove it
                    entity_registry.async_remove(entity_id)
                    removed_count += 1
                    _LOGGER.debug("Removed package entity: %s", entity_id)
                else:
                    # Entity not in registry, check if it exists in state
                    state = hass.states.get(entity_id)
                    if state:
                        # Entity exists only in state - remove from state
                        hass.states.async_remove(entity_id)
                        unavailable_count += 1
                        _LOGGER.debug("Removed entity from state: %s", entity_id)
                        
            except Exception as err:
                _LOGGER.debug("Could not remove %s: %s", entity_id, err)
        
        _LOGGER.info(
            "Package cleanup: %d entities removed from registry, %d removed from state",
            removed_count,
            unavailable_count
        )
        
        # 5. Optional: Delete IR database file
        # Uncomment to enable automatic database deletion
        # db_path = os.path.join(hass.config.path(), "haptique_ir_devices.json")
        # if os.path.exists(db_path):
        #     try:
        #         # Create backup first
        #         backup_path = db_path + ".backup"
        #         import shutil
        #         shutil.copy2(db_path, backup_path)
        #         _LOGGER.info("Created database backup: %s", backup_path)
        #         
        #         # Delete original
        #         os.remove(db_path)
        #         _LOGGER.info("Deleted IR database file: %s", db_path)
        #     except Exception as err:
        #         _LOGGER.error("Failed to delete IR database file: %s", err)
        
        # 6. Clean up hass.data
        if DOMAIN in hass.data:
            hass.data.pop(DOMAIN)
            _LOGGER.info("Cleaned up integration data from hass.data")
        
        _LOGGER.info("=== COMPLETE removal finished ===")
        _LOGGER.warning(
            "Package files still present in /config/packages/. "
            "Delete haptique_extender_*.yaml files and restart HA to prevent recreation."
        )


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    return True
