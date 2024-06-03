"""TalentMonitor Inverter."""

import json
import logging

from custom_components.talent_monitor.pyTalentMonitor.data_provider import DataProvider, Entity

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)

class Inverter(Entity):
    """Class for TalentMonitor inverter."""

    def __init__(
        self, entity_id: str, name: str
    ) -> None:
        """Initialize the inverter."""
        super().__init__(entity_id, name)
        self._data = {}

    @property
    def data(self):
        """Return the data of the inverter."""
        return self._data

    @data.setter
    def data(self, data):
        """Set the data of the inverter."""
        self._data = data


class InverterDataProvider:
    """Data provider for inverter."""

    def __init__(
        self, data_provider: DataProvider
    ) -> None:
        """Initialize the data provider."""
        self._data_provider = data_provider
        self._inverter = {}

    @property
    def inverters(self) -> list[Inverter]:
        """Returns the inverters read from TalentMonitor."""
        result: list[Inverter] = []
        for data in self._inverter.values():
            result.append(data)

        return result

    async def fetch_data(self):
        """Fetch the data of the inverter."""
        data = await self._data_provider.get_data(endpoint="tools/device/selectDeviceInverter")
        if data and "rows" in data:
            for inverter_data in data["rows"]:
                if "deviceGuid" in inverter_data:
                    deviceGuid = inverter_data["deviceGuid"]

                    _LOGGER.debug("Data for inverter GUID %s: %s", deviceGuid, json.dumps(inverter_data))

                    if deviceGuid not in self._inverters:
                        self._inverters["deviceGuid"] = Inverter()

                    inverter = self._inverters["deviceGuid"]

                    inverter_info = await self._data_provider.get_data(
                        endpoint=f"tools/device/selectDeviceInverterInfo?deviceGuid={deviceGuid}"
                    )

                    _LOGGER.debug("Details for inverter GUID %s: %s", deviceGuid, json.dumps(inverter_info))
                    if inverter_info and "data" in inverter_info:
                        inverter.data = inverter_info["data"]
