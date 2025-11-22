"""Sensor platform for Haptique Extender - With DB Sensors."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HaptiqueCoordinator


@dataclass
class HaptiqueSensorEntityDescription(SensorEntityDescription):
    """Describes Haptique sensor entity."""

    value_fn: Callable[[dict[str, Any]], StateType] | None = None


SENSOR_TYPES: tuple[HaptiqueSensorEntityDescription, ...] = (
    # Device Info Sensors
    HaptiqueSensorEntityDescription(
        key="firmware_version",
        name="Firmware Version",
        icon="mdi:chip",
        value_fn=lambda data: data.get("status", {}).get("fw_ver", "unknown"),
    ),
    HaptiqueSensorEntityDescription(
        key="hostname",
        name="Hostname",
        icon="mdi:network",
        value_fn=lambda data: data.get("status", {}).get("hostname", "unknown"),
    ),
    HaptiqueSensorEntityDescription(
        key="mac_address",
        name="MAC Address",
        icon="mdi:identifier",
        value_fn=lambda data: data.get("status", {}).get("mac", "unknown"),
    ),
    HaptiqueSensorEntityDescription(
        key="sta_ip",
        name="IP Address",
        icon="mdi:ip-network",
        value_fn=lambda data: data.get("status", {}).get("sta_ip", "unknown"),
    ),
    
    # WiFi Sensors
    HaptiqueSensorEntityDescription(
        key="wifi_ssid",
        name="WiFi SSID",
        icon="mdi:wifi",
        value_fn=lambda data: data.get("status", {}).get("sta_ssid", "unknown"),
    ),
    HaptiqueSensorEntityDescription(
        key="wifi_signal",
        name="WiFi Signal",
        icon="mdi:wifi-strength-2",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wifi", {}).get("sta", {}).get("rssi"),
    ),
    
    # Hub Storage Info Sensors (firmware)
    HaptiqueSensorEntityDescription(
        key="ir_commands_stored",
        name="Hub IR Commands Stored",
        icon="mdi:database",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("storage_info", {}).get("ir_count", 0),
    ),
    HaptiqueSensorEntityDescription(
        key="ir_storage_max",
        name="Hub IR Storage Max",
        icon="mdi:database-settings",
        value_fn=lambda data: data.get("storage_info", {}).get("ir_max", 50),
    ),
    HaptiqueSensorEntityDescription(
        key="ir_storage_percent",
        name="Hub IR Storage Usage",
        icon="mdi:database-check",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            round((data.get("storage_info", {}).get("ir_count", 0) / 
                   data.get("storage_info", {}).get("ir_max", 50)) * 100, 1)
            if data.get("storage_info", {}).get("ir_max", 50) > 0 else 0
        ),
    ),
    
    # Last Learned IR Code Sensor
    HaptiqueSensorEntityDescription(
        key="last_learn_ir_code",
        name="Last Learn IR Code",
        icon="mdi:remote-tv",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: data.get("last_learn_ir_timestamp"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique sensors."""
    coordinator: HaptiqueCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        HaptiqueSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
    ]
    
    # Add DB sensors
    entities.append(HaptiqueDevicesSensor(coordinator, entry))
    entities.append(HaptiqueCommandsSensor(coordinator, entry))

    async_add_entities(entities)


class HaptiqueSensor(CoordinatorEntity[HaptiqueCoordinator], SensorEntity):
    """Representation of a Haptique sensor."""

    entity_description: HaptiqueSensorEntityDescription

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
        description: HaptiqueSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        
        # Use hostname for entity naming
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra state attributes for last_learn_ir_code sensor."""
        if self.entity_description.key == "last_learn_ir_code":
            last_ir_code = self.coordinator.data.get("last_learn_ir_code")
            if last_ir_code:
                return {
                    "count": len(last_ir_code.get("combined", [])),
                    "freq_khz": last_ir_code.get("freq_khz"),
                    "frames": last_ir_code.get("frames", 1),
                    "raw_data": last_ir_code.get("combined", []),
                }
        return None


class HaptiqueDevicesSensor(CoordinatorEntity[HaptiqueCoordinator], SensorEntity):
    """Sensor that lists all devices in the IR database."""

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the devices sensor."""
        super().__init__(coordinator)
        
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        
        self._attr_name = "Database IR Devices"
        self._attr_unique_id = f"{entry.entry_id}_ir_devices"
        self._attr_icon = "mdi:database"
        self._attr_has_entity_name = True
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def native_value(self) -> int:
        """Return the number of devices."""
        from .ir_database import IRDatabase
        
        ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
        devices = ir_db.list_devices()
        return len(devices)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the list of devices as attributes."""
        from .ir_database import IRDatabase
        
        ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
        devices = ir_db.list_devices()
        
        return {
            "devices": devices,
            "device_names": [d["name"] for d in devices],
        }


class HaptiqueCommandsSensor(CoordinatorEntity[HaptiqueCoordinator], SensorEntity):
    """Sensor that lists commands (requires device selection via service call)."""

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the commands sensor."""
        super().__init__(coordinator)
        
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        
        self._attr_name = "Database IR Commands"
        self._attr_unique_id = f"{entry.entry_id}_ir_commands"
        self._attr_icon = "mdi:code-braces"
        self._attr_has_entity_name = True
        self._selected_device: str | None = None
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def native_value(self) -> int:
        """Return the number of commands for selected device."""
        if not self._selected_device:
            return 0
        
        from .ir_database import IRDatabase
        
        ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
        commands = ir_db.list_commands(self._selected_device)
        return len(commands)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the list of commands as attributes."""
        if not self._selected_device:
            return {
                "selected_device": None,
                "commands": [],
                "command_names": [],
            }
        
        from .ir_database import IRDatabase
        
        ir_db: IRDatabase = self.hass.data[DOMAIN]["ir_database"]
        commands = ir_db.list_commands(self._selected_device)
        
        return {
            "selected_device": self._selected_device,
            "commands": commands,
            "command_names": [c["name"] for c in commands],
        }
    
    def set_device(self, device_name: str) -> None:
        """Set the device to query commands for."""
        self._selected_device = device_name
        self.async_write_ha_state()
