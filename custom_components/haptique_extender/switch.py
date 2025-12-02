"""Switch platform for Haptique Extender - No switches."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique switches - currently none."""
    # No switches to add - learning mode is now managed via services
    _LOGGER.debug("Switch platform loaded (no switches defined)")
    pass
