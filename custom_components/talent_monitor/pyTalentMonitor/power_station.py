"""TalentMonitor PowerStation"""

import json
import logging

from custom_components.talent_monitor.pyTalentMonitor.data_provider import DataProvider, Entity

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)

TIMEZONE = "+02:00"

class PowerStation(Entity):
    def __init__(
        self, entity_id: str, name: str
    ) -> None:
        super().__init__(entity_id, name)
        self._data = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data


class PowerStationDataProvider():
    def __init__(
        self, data_provider: DataProvider
    ) -> None:
        self._data_provider = data_provider
        self._power_stations = {}

    @property
    def power_stations(self) -> list[PowerStation]:
        """Returns the power stations read from TalentMonitor"""
        result: list[PowerStation] = []
        for key, data in self._power_stations.items():
            result.append(data)

        return result

    async def fetch_data(self):
        data = await self._data_provider.get_data(endpoint="system/station/list")
        if data and "rows" in data:
            for power_station_data in data["rows"]:
                if "powerStationGuid" in power_station_data:
                    powerStationGuid = power_station_data["powerStationGuid"]
                    powerStationName = power_station_data["stationName"]

                    _LOGGER.debug("Data for powerstation GUID %s: %s", powerStationGuid, json.dumps(power_station_data))

                    if not powerStationGuid in self._power_stations:
                        self._power_stations["powerStationGuid"] = PowerStation(powerStationGuid, powerStationName)

                    power_station = self._power_stations["powerStationGuid"]

                    power_station_info = await self._data_provider.get_data(
                        endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={powerStationGuid}&timezone={TIMEZONE}"
                    )

                    _LOGGER.debug("Details for powerstation GUID %s: %s", powerStationGuid, json.dumps(power_station_info))
                    if power_station_info and "data" in power_station_info:
                        power_station.data = power_station_info["data"]
