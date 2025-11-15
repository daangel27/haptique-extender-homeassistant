"""Sensor platform for Haptique Extender - Version 2.0."""
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

    value_fn: Callable[[dict[str, Any]], StateType] = None
    attr_fn: Callable[[dict[str, Any]], dict[str, Any]] = None


SENSOR_TYPES: tuple[HaptiqueSensorEntityDescription, ...] = (
    # Device Info Sensors
    HaptiqueSensorEntityDescription(
        key="fw_version",
        name="Firmware Version",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("status", {}).get("fw_ver"),
    ),
    HaptiqueSensorEntityDescription(
        key="mac_address",
        name="MAC Address",
        icon="mdi:network",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("status", {}).get("mac"),
    ),
    
    # WiFi Sensors
    HaptiqueSensorEntityDescription(
        key="wifi_ssid",
        name="WiFi SSID",
        icon="mdi:wifi",
        value_fn=lambda data: data.get("status", {}).get("sta_ssid"),
    ),
    HaptiqueSensorEntityDescription(
        key="wifi_rssi",
        name="WiFi Signal",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("wifi", {}).get("sta", {}).get("rssi"),
    ),
    HaptiqueSensorEntityDescription(
        key="wifi_ip",
        name="WiFi IP",
        icon="mdi:ip",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("wifi", {}).get("sta", {}).get("ip"),
    ),
    
    # IR RX Info Sensors
    HaptiqueSensorEntityDescription(
        key="ir_rx_count",
        name="IR RX Count",
        icon="mdi:counter",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("ir_rx_info", {}).get("rx_count", 0),
    ),
    HaptiqueSensorEntityDescription(
        key="ir_last_freq",
        name="IR Last Frequency",
        icon="mdi:sine-wave",
        native_unit_of_measurement="kHz",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("ir_rx_info", {}).get("last_freq_khz"),
    ),
    
    # Storage Info Sensors
    HaptiqueSensorEntityDescription(
        key="ir_commands_stored",
        name="IR Commands Stored",
        icon="mdi:database",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("storage_info", {}).get("ir_count", 0),
    ),
    HaptiqueSensorEntityDescription(
        key="ir_storage_max",
        name="IR Storage Max",
        icon="mdi:database-settings",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("storage_info", {}).get("ir_max", 50),
    ),
    HaptiqueSensorEntityDescription(
        key="ir_storage_percent",
        name="IR Storage Usage",
        icon="mdi:database-check",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: int(
            (data.get("storage_info", {}).get("ir_count", 0) 
             / max(data.get("storage_info", {}).get("ir_max", 50), 1)) * 100
        ) if data.get("storage_info", {}).get("ir_max") else 0,
    ),
    
    # Learning Mode Sensor
    HaptiqueSensorEntityDescription(
        key="learning_mode",
        name="Learning Mode",
        icon="mdi:school",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: "Active" if data.get("learning_mode") else "Inactive",
    ),
    
    # Last Learn IR Code Sensor
    HaptiqueSensorEntityDescription(
        key="last_learn_ir_code",
        name="Last Learn IR Code",
        icon="mdi:remote-tv",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda data: (
            data.get("last_learn_ir_timestamp") 
            if data.get("last_learn_ir_code") 
            else None
        ),
        attr_fn=lambda data: (
            {
                "raw_data": data.get("last_learn_ir_code", {}).get("combined", []),
                "freq_khz": data.get("last_learn_ir_code", {}).get("freq_khz"),
                "frames": data.get("last_learn_ir_code", {}).get("frames"),
                "count": len(data.get("last_learn_ir_code", {}).get("combined", [])),
            }
            if data.get("last_learn_ir_code")
            else {}
        ),
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
        HaptiqueSensor(coordinator, entry, description) for description in SENSOR_TYPES
    ]
    
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
        # Clean hostname for entity_id (replace hyphens with underscores)
        clean_hostname = hostname.replace("-", "_")
        
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,  # Device name = hostname
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
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.entity_description.attr_fn:
            return self.entity_description.attr_fn(self.coordinator.data)
        return {}
