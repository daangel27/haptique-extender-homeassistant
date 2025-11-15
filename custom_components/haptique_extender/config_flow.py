"""Config flow for Haptique Extender integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import zeroconf
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required("token"): str,
        vol.Optional(CONF_NAME): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Haptique Extender."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            token = user_input.get("token", "").strip()
            name = user_input.get(CONF_NAME, "")

            if not token:
                errors["token"] = "token_required"
            else:
                try:
                    # Validate the host and token by attempting to fetch device info
                    session = async_get_clientsession(self.hass)
                    device_info = await self._async_get_device_info(session, host, token)
                    
                    if device_info is None:
                        errors["base"] = "cannot_connect"
                    else:
                        # Use MAC address as unique ID
                        mac = device_info.get("mac", "")
                        if not mac:
                            errors["base"] = "invalid_device"
                        else:
                            await self.async_set_unique_id(mac)
                            self._abort_if_unique_id_configured()

                            # Use provided name or default to device name from API
                            final_name = name or device_info.get("name", f"Haptique Extender {mac[-8:]}")

                            return self.async_create_entry(
                                title=final_name,
                                data={
                                    CONF_HOST: host,
                                    CONF_NAME: final_name,
                                    "token": token,
                                },
                            )
                except aiohttp.ClientError:
                    errors["base"] = "cannot_connect"
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_zeroconf(
        self, discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        _LOGGER.debug("Zeroconf discovery info: %s", discovery_info)
        
        # Vérifier que c'est bien un appareil Haptique Extender
        # Le champ "dev" doit contenir "haptique-extender"
        properties = discovery_info.properties
        dev_field = properties.get("dev", "")
        
        if dev_field != "haptique-extender":
            _LOGGER.debug(
                "Ignoring device with dev='%s' (not 'haptique-extender')",
                dev_field
            )
            return self.async_abort(reason="not_haptique_device")

        # Récupérer l'adresse IP (pas le hostname)
        host = str(discovery_info.ip_addresses[0]) if discovery_info.ip_addresses else discovery_info.host
        
        # Récupérer le MAC depuis les propriétés
        mac = properties.get("mac", "")
        if not mac:
            _LOGGER.debug("No MAC address found in zeroconf properties")
            return self.async_abort(reason="no_mac_address")

        # Vérifier que l'appareil n'est pas déjà configuré
        await self.async_set_unique_id(mac)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        # Stocker les informations de découverte
        # Utiliser le nom depuis zeroconf ou un nom par défaut
        device_name = discovery_info.name.split(".")[0] if discovery_info.name else f"Haptique Extender {mac[-8:]}"
        
        self._discovery_info = {
            CONF_HOST: host,
            CONF_NAME: device_name,
            "mac": mac,
            "model": properties.get("model", ""),
            "fw": properties.get("fw", ""),
        }

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery and ask for token."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            token = user_input.get("token", "").strip()
            
            if not token:
                errors["token"] = "token_required"
            else:
                # Valider le token en tentant une connexion
                host = self._discovery_info[CONF_HOST]
                _LOGGER.info("Attempting to connect to %s with provided token", host)
                
                try:
                    session = async_get_clientsession(self.hass)
                    # Test de connexion avec le token
                    url = f"http://{host}/api/status"
                    headers = {"Authorization": f"Bearer {token}"}
                    
                    _LOGGER.debug("Request URL: %s", url)
                    _LOGGER.debug("Request headers: %s", {k: v[:20] + "..." if len(v) > 20 else v for k, v in headers.items()})
                    
                    async with session.get(
                        url, 
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        _LOGGER.debug("Response status: %s", response.status)
                        
                        if response.status == 200:
                            # Token valide, créer l'entrée
                            _LOGGER.info("Successfully connected to %s", host)
                            return self.async_create_entry(
                                title=self._discovery_info[CONF_NAME],
                                data={
                                    CONF_HOST: self._discovery_info[CONF_HOST],
                                    CONF_NAME: self._discovery_info[CONF_NAME],
                                    "token": token,
                                },
                            )
                        elif response.status == 401:
                            _LOGGER.error("Authentication failed for %s (status 401)", host)
                            errors["token"] = "invalid_token"
                        else:
                            _LOGGER.error("Unexpected status %s from %s", response.status, host)
                            response_text = await response.text()
                            _LOGGER.debug("Response body: %s", response_text[:200])
                            errors["base"] = "cannot_connect"
                            
                except aiohttp.ClientError as err:
                    _LOGGER.error("Client error connecting to %s: %s", host, err)
                    errors["base"] = "cannot_connect"
                except Exception as err:  # pylint: disable=broad-except
                    _LOGGER.exception("Unexpected exception connecting to %s: %s", host, err)
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="discovery_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required("token"): str,
                }
            ),
            errors=errors,
            description_placeholders={
                "name": self._discovery_info[CONF_NAME],
                "host": self._discovery_info[CONF_HOST],
                "model": self._discovery_info.get("model", "Unknown"),
                "fw": self._discovery_info.get("fw", "Unknown"),
            },
        )

    async def _async_get_device_info(
        self, session: aiohttp.ClientSession, host: str, token: str | None = None
    ) -> dict[str, Any] | None:
        """Get device info from the API."""
        try:
            url = f"http://{host}/api/status"
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
                
            async with session.get(
                url, 
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.debug("Device info from %s: %s", host, data)
                    return data
                elif response.status == 401:
                    _LOGGER.error("Authentication failed for %s", host)
                    return None
                _LOGGER.error("Failed to get device info from %s: status=%s", host, response.status)
                return None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to %s: %s", host, err)
            return None
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error getting device info from %s: %s", host, err)
            return None
