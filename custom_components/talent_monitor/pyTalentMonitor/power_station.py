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
        self._data = {}

    @property
    def data(self):
        """Return the data of the power station."""
        return self._data

    @data.setter
    def data(self, data):
        """Set the data of the power station."""
        self._data = data


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
                    powerStationGuid = power_station_data["powerStationGuid"]
                    powerStationName = power_station_data["stationName"]

                    _LOGGER.debug("Data for powerstation GUID %s: %s", powerStationGuid, json.dumps(power_station_data))

                    if powerStationGuid not in self._power_stations:
                        self._power_stations["powerStationGuid"] = PowerStation(powerStationGuid, powerStationName)

                    power_station = self._power_stations["powerStationGuid"]

                    power_station_info = await self._data_provider.get_data(
                        endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={powerStationGuid}&timezone={TIMEZONE}"
                    )

                    dummy_data = json.loads('{"yearBattDischargeEnergy": 0.0, "yearLoadEnergyNamed": "0.00 Wh","enableFitInApp": false,"monthEnergy": 44590.0,"yearBattChargeEnergy": 0.0,"totalEnergy": 301180.0,"peakHour": 0.14634146341463414,"stationType": "1","totalActivePower": 94.4,"gridSidePower": 0.0,"lastDataUpdateTime": "2024-05-26T06:52:41","statusNamed": "Online","yearEnergyNamed": "118.06 kWh","stationTypeNamed": "Household use","yearBattChargeEnergyNamed": "0.00 Wh","timezoneOffset": "+02:00","gridSidePowerNamed": "0.00 W","layoutMeta": "{}","locationLongitude": "[redacted]","dayEnergyNamed": "120.00 Wh","totalPeakPower": 94.4,"totalPeakPowerNamed": "94.40 W","dayEnergy": 120.0,"monthBattChargeEnergyNamed": "0.00 Wh","images": [],"deptId": 101,"timeZone": "Europe/Berlin","yearGridsellEnergyNamed": "0.00 Wh","monthBattDischargeEnergy": 0.0,"monthLoadEnergy": 0.0,"yearEnergy": 118060.0,"yearBattDischargeEnergyNamed": "0.00 Wh","monthLoadEnergyNamed": "0.00 Wh","electricityGain": 0.0,"deptCode": "[redacted]","yearGridbuyEnergyNamed": "0.00 Wh","status": "ready","isFavorite": 0,"totalActivePowerNamed": "94.40 W","monthBattChargeEnergy": 0.0,"gridConnectedType": "1","monthGridbuyEnergyNamed": "0.00 Wh","co2Reduced": "300.28 KG","yearGridsellEnergy": 0.0,"treesPlanted": "0.82","buildDate": "2023-06-17","monthGridsellEnergy": 0.0,"yearLoadEnergy": 0.0,"monthEnergyNamed": "44.59 kWh","installedCapacity": 820.0,"lightingHours": "23.19K","gridConnectedTypeNamed": "Full access to the Internet","powerStationId": "[redacted]","stationName": "priwatt priWall duo","monthGridbuyEnergy": 0.0,"currency": "EUR","monthGridsellEnergyNamed": "0.00 Wh","powerStationGuid": "[redacted]","owner": "User [redacted]","monthBattDischargeEnergyNamed": "0.00 Wh","locationLatitude": "[redacted]","battSidePowerNamed": "0.00 W","userId": "[redacted]","ownerEmail": "[redacted]","totalEnergyNamed": "301.18 kWh","earnings": "0.00","lastDataUpdateTimeOffseted": "2024-05-26T08:52:41","ownerUserId": "[redacted]","installedCapacityNamed": "820.00 Wp","guests": [],"location": "[redacted]","yearGridbuyEnergy": 0.0,"businessType": "1","battSidePower": 0.0}')

                    _LOGGER.debug("Details for powerstation GUID %s: %s", powerStationGuid, json.dumps(power_station_info))
                    if power_station_info and "data" in power_station_info:
                        #power_station.data = power_station_info["data"]
                        power_station.data = dummy_data
