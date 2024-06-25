"""Adds config flow for TalentMonitor."""

import logging

from custom_components.tsun.pyTalentMonitor import TalentSolarMonitor
from custom_components.tsun.pyTalentMonitor.data_provider import AuthenticationError
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from aiohttp import ClientConnectorError
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__name__)

CLOUD_CONNECTION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class TalentMonitorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for TalentMonitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}
        _LOGGER.debug("Config flow async_step_user %s", user_input)

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        return await self.async_step_connection_talent_monitor_cloud(user_input)

    async def async_step_connection_talent_monitor_cloud(self, user_input):
        """Show the configuration form to edit location data."""
        _LOGGER.debug(
            "Config flow async_step_connection_talent_monitor_cloud %s", user_input
        )

        if user_input is not None:
            if CONF_USERNAME in user_input and CONF_PASSWORD in user_input:
                valid = await self._test_credentials_cloud_talent_monitor(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
                if valid:
                    return self.async_create_entry(
                        title=user_input[CONF_USERNAME], data=user_input
                    )
                else:
                    self._errors["base"] = "auth_cloud"

        return self.async_show_form(
            step_id="connection_talent_monitor_cloud",
            data_schema=CLOUD_CONNECTION_SCHEMA,
            errors=self._errors,
        )

    async def _test_credentials_cloud_talent_monitor(self, username, password):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = TalentSolarMonitor(username, password, session)
            await client.login()
            return True
        except ClientConnectorError:
            _LOGGER.exception("ClientConnectorError")
        except AuthenticationError:
            _LOGGER.exception("TalentMonitorError")
        return False
