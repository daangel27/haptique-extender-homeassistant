"""Switch platform for Haptique Extender."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers import entity_registry as er

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
        HaptiqueNotificationSwitch(coordinator, entry, "learning", "Learning Notifications", "mdi:school"),
        HaptiqueNotificationSwitch(coordinator, entry, "send", "Send Notifications", "mdi:send"),
        HaptiqueNotificationSwitch(coordinator, entry, "connection", "Connection Notifications", "mdi:lan-connect"),
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
        clean_hostname = hostname.replace("-", "_")
        
        self._attr_name = "IR Learning Mode"
        self._attr_unique_id = f"{entry.entry_id}_ir_learning"
        self._attr_icon = "mdi:remote-tv"
        self._attr_has_entity_name = True
        
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


class HaptiqueNotificationSwitch(CoordinatorEntity[HaptiqueCoordinator], SwitchEntity):
    """Switch to enable/disable specific notification types."""

    def __init__(
        self,
        coordinator: HaptiqueCoordinator,
        entry: ConfigEntry,
        notification_type: str,
        name: str,
        icon: str,
    ) -> None:
        """Initialize the notification switch."""
        super().__init__(coordinator)
        
        # Use hostname for entity naming
        hostname = coordinator.device_info.get("hostname", "haptique_extender")
        
        self._notification_type = notification_type
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_notify_{notification_type}"
        self._attr_icon = icon
        self._attr_has_entity_name = True
        self._attr_entity_category = EntityCategory.CONFIG
        
        # Link corresponding input_boolean
        self._input_boolean_entity = f"input_boolean.haptique_notify_{notification_type}_enabled"
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_info["mac"])},
            "name": hostname,
            "manufacturer": "KINCONY",
            "model": "KC868-AG",
            "sw_version": coordinator.device_info["fw_ver"],
        }

    @property
    def is_on(self) -> bool:
        """Return true if notifications are enabled."""
        # Get state from the corresponding input_boolean
        state = self.hass.states.get(self._input_boolean_entity)
        if state is None:
            return True  # Default to enabled if input_boolean doesn't exist yet
        return state.state == "on"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on notifications."""
        await self.hass.services.async_call(
            "input_boolean",
            "turn_on",
            {"entity_id": self._input_boolean_entity},
            blocking=True,
        )
        self.async_write_ha_state()
        _LOGGER.info("%s notifications enabled", self._notification_type.capitalize())

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off notifications."""
        await self.hass.services.async_call(
            "input_boolean",
            "turn_off",
            {"entity_id": self._input_boolean_entity},
            blocking=True,
        )
        self.async_write_ha_state()
        _LOGGER.info("%s notifications disabled", self._notification_type.capitalize())

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        
        # Listen to input_boolean state changes to update this switch
        self.async_on_remove(
            self.hass.bus.async_listen(
                "state_changed",
                self._handle_input_boolean_change,
            )
        )

    async def _handle_input_boolean_change(self, event) -> None:
        """Handle input_boolean state changes."""
        if event.data.get("entity_id") == self._input_boolean_entity:
            self.async_write_ha_state()
