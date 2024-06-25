"""PyTalentMonitor script (to be added to PyPi)."""

import argparse
import asyncio
import logging

from aiohttp import ClientSession
from custom_components.tsun.pyTalentMonitor.inverter import (
    Inverter,
    InverterDataProvider,
)
from custom_components.tsun.pyTalentMonitor.data_provider import DataProvider
from custom_components.tsun.pyTalentMonitor.power_station import (
    PowerStation,
    PowerStationDataProvider,
)

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)


class TalentSolarMonitor:
    """TalentSolarMonitor API client."""

    def __init__(
        self,
        username: str = None,
        password: str = None,
        session: ClientSession = None,
    ):
        """Construct the TalentSolarMonitor API client."""
        self._data_provider = DataProvider(username, password, session)
        self._inverter_data_provider = InverterDataProvider(self._data_provider)
        self._power_station_data_provider = PowerStationDataProvider(
            self._data_provider
        )

    def get_power_stations(self) -> list[PowerStation]:
        """Return the power stations."""
        return self._power_station_data_provider.power_stations

    def get_inverters(self) -> list[Inverter]:
        """Return the inverters."""
        return self._inverter_data_provider.inverters

    async def fetch_data(self):
        """Fetch data from the TalentMonitor."""
        await self._inverter_data_provider.fetch_data()
        await self._power_station_data_provider.fetch_data()

    async def fetch_solar_data(self):
        """Fetch the solar data and return it as json."""
        await self.fetch_data()

    async def login(self):
        """Log in to the TalentMonitor API."""
        await self._data_provider.login()


async def main(username: str, password: str):
    """Connect to the TalentSolarMonitor API and fetch the solar data."""
    async with ClientSession() as session:
        talent_monitor = TalentSolarMonitor(username, password, session)
        result = await talent_monitor.fetch_solar_data()
        if result:
            _LOGGER.info("Solar data received: %s", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pyTalent - Talent Solar Monitoring Script"
    )
    parser.add_argument("-u", "--username", required=False, help="Username to log in")
    parser.add_argument("-p", "--password", required=False, help="Password to log in")
    args = parser.parse_args()

    asyncio.run(main(args.username, args.password))
