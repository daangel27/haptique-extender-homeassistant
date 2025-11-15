"""Binary sensor platform for Haptique Extender."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HaptiqueCoordinator


@dataclass
class HaptiqueBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Haptique binary sensor entity."""

    value_fn: Callable[[dict[str, Any]], bool] = None


BINARY_SENSOR_TYPES: tuple[HaptiqueBinarySensorEntityDescription, ...] = (
    HaptiqueBinarySensorEntityDescription(
        key="wifi_connected",
        name="WiFi Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        value_fn=lambda data: data.get("status", {}).get("sta_ok", False),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique binary sensors."""
    coordinator: HaptiqueCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        HaptiqueBinarySensor(coordinator, entry, description)
        for description in BINARY_SENSOR_TYPES
    ]
    
    async_add_entities(entities)


class HaptiqueBinarySensor(CoordinatorEntity[HaptiqueCoordinator], BinarySensorEntity):
    """Representation of a Haptique binary sensor."""

    entity_description: HaptiqueBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
        description: HaptiqueBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        
        # Use hostname for entity naming
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        clean_hostname = hostname.replace("-", "_")
        
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = f"{clean_hostname}_{description.name}".replace(" ", "_")
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        if self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return False
