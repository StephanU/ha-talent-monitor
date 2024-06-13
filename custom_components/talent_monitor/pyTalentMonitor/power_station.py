"""TalentMonitor PowerStation."""

import json
import logging

from custom_components.talent_monitor.pyTalentMonitor.data_provider import DataProvider, Entity

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)

TIMEZONE = "+02:00"

class PowerStation(Entity):
    """Class for TalentMonitor power station."""

    def __init__(
        self, entity_id: str, name: str
    ) -> None:
        """Initialize the power station."""
        super().__init__(entity_id, name)


class PowerStationDataProvider:
    """Data provider for power stations."""

    def __init__(
        self, data_provider: DataProvider
    ) -> None:
        """Initialize the data provider."""
        self._data_provider = data_provider
        self._power_stations = {}

    @property
    def power_stations(self) -> list[PowerStation]:
        """Returns the power stations read from TalentMonitor."""
        result: list[PowerStation] = []
        for data in self._power_stations.values():
            result.append(data)

        return result

    async def fetch_data(self):
        """Fetch the data of the power stations."""
        data = await self._data_provider.get_data(endpoint="system/station/list")
        if data and "rows" in data:
            for power_station_data in data["rows"]:
                if "powerStationGuid" in power_station_data:
                    power_station_guid = power_station_data["powerStationGuid"]
                    power_station_name = power_station_data["stationName"]

                    _LOGGER.debug("Data for powerstation GUID %s: %s", power_station_guid, json.dumps(power_station_data))

                    if power_station_guid not in self._power_stations:
                        self._power_stations[power_station_guid] = PowerStation(power_station_guid, power_station_name)

                    power_station = self._power_stations[power_station_guid]

                    power_station_info = await self._data_provider.get_data(
                        endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={power_station_guid}&timezone={TIMEZONE}"
                    )

                    _LOGGER.debug("Details for powerstation GUID %s: %s", power_station_guid, json.dumps(power_station_info))
                    if power_station_info and "data" in power_station_info:
                        power_station.data = power_station_info["data"]
