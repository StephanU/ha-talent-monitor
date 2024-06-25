"""Data Update Coordinator for the TalentMonitor integration."""

import logging
from datetime import timedelta

from custom_components.tsun.pyTalentMonitor import TalentSolarMonitor
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import DOMAIN


SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__name__)


class TalentMonitorDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize."""
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

        username = entry.data.get(CONF_USERNAME)
        password = entry.data.get(CONF_PASSWORD)

        session = async_get_clientsession(hass, verify_ssl=False)
        client = TalentSolarMonitor(username, password, session)

        if client is None:
            _LOGGER.exception(
                "Creating TalentMonitorDataUpdateCoordinator failed: client is None"
            )
            raise ConfigEntryError

        self.api = client

    async def _async_update_data(self):
        """Update data via library."""
        _LOGGER.debug("_async_update_data ")
        try:
            await self.api.fetch_data()
        except Exception as exception:
            _LOGGER.exception("_async_update_data failed")
            raise UpdateFailed() from exception
