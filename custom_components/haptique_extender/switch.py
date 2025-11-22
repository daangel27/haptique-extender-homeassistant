"""Switch platform for Haptique Extender - Simplified."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HaptiqueCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique switches."""
    coordinator: HaptiqueCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        HaptiqueIRLearningSwitch(coordinator, entry),
    ]
    
    async_add_entities(entities)


class HaptiqueIRLearningSwitch(CoordinatorEntity[HaptiqueCoordinator], SwitchEntity):
    """Switch to enable/disable IR learning mode."""

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        
        # Use hostname for entity naming
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        
        self._attr_name = "IR Learning Mode"
        self._attr_unique_id = f"{entry.entry_id}_ir_learning"
        self._attr_icon = "mdi:remote-tv"
        self._attr_has_entity_name = True
        self._attr_entity_registry_enabled_default = False  # Disabled by default, hidden from panel
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def is_on(self) -> bool:
        """Return true if learning mode is on."""
        return self.coordinator.learning_mode

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on learning mode."""
        self.coordinator.set_learning_mode(True)
        self.async_write_ha_state()
        _LOGGER.info("IR Learning Mode enabled")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off learning mode."""
        self.coordinator.set_learning_mode(False)
        self.async_write_ha_state()
        _LOGGER.info("IR Learning Mode disabled")
