"""TalentMonitor Inverter."""

import json
import logging

from custom_components.tsun.pyTalentMonitor.data_provider import DataProvider, Entity

# Configure logging
_LOGGER: logging.Logger = logging.getLogger(__name__)


class Inverter(Entity):
    """Class for TalentMonitor inverter."""

    def __init__(self, entity_id: str, name: str) -> None:
        """Initialize the inverter."""
        super().__init__(entity_id, name)


class InverterDataProvider:
    """Data provider for inverter."""

    def __init__(self, data_provider: DataProvider) -> None:
        """Initialize the data provider."""
        self._data_provider = data_provider
        self._inverters = {}

    @property
    def inverters(self) -> list[Inverter]:
        """Returns the inverters read from TalentMonitor."""
        result: list[Inverter] = []
        for data in self._inverters.values():
            result.append(data)

        return result

    async def fetch_data(self):
        """Fetch the data of the inverter."""
        data = await self._data_provider.get_data(
            endpoint="tools/device/selectDeviceInverter"
        )
        if data and "rows" in data:
            for index, inverter_data in enumerate(data["rows"], start=1):
                if "deviceGuid" in inverter_data:
                    device_guid = inverter_data["deviceGuid"]
                    inverter_name = (
                        "Inverter"  # TODO get a better name from inverter_data
                    )

                    _LOGGER.debug(
                        "Data for inverter GUID %s: %s",
                        device_guid,
                        json.dumps(inverter_data),
                    )

                    if device_guid not in self._inverters:
                        self._inverters[device_guid] = Inverter(
                            device_guid, inverter_name + " " + str(index)
                        )

                    inverter = self._inverters[device_guid]

                    inverter_info = await self._data_provider.get_data(
                        endpoint=f"tools/device/selectDeviceInverterInfo?deviceGuid={device_guid}"
                    )

                    _LOGGER.debug(
                        "Details for inverter GUID %s: %s",
                        device_guid,
                        json.dumps(inverter_info),
                    )
                    if inverter_info and "data" in inverter_info:
                        inverter.data = inverter_info["data"]
