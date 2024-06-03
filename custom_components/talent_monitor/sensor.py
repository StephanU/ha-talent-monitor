"""Sensor platform for TalentMonitor."""
from datetime import datetime
import logging
from custom_components.talent_monitor.entity import TalentMonitorEntity
from custom_components.talent_monitor.pyTalentMonitor.power_station import PowerStation
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfPower

from .const import DOMAIN


_LOGGER: logging.Logger = logging.getLogger(__name__)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="totalActivePower",
        translation_key="talentmonitor_powerstation_totalActivePower",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="dayEnergy",
        translation_key="talentmonitor_powerstation_dayEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="monthEnergy",
        translation_key="talentmonitor_powerstation_monthEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="yearEnergy",
        translation_key="talentmonitor_powerstation_yearEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="lastDataUpdateTime",
        translation_key="talentmonitor_powerstation_lastDataUpdateTime",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATE,
    ),
)

SENSORS = {desc.key: desc for desc in SENSOR_TYPES}

SENSOR_UNIT_MAPPING = {
    "Wh": UnitOfEnergy.WATT_HOUR,
    "kWh": UnitOfEnergy.KILO_WATT_HOUR,
    "kW": UnitOfPower.KILO_WATT,
    "W": UnitOfPower.WATT,
}


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    power_stations: list[PowerStation] = coordinator.api.get_power_stations()
    for power_station in power_stations:
        for _, value in enumerate(power_station.data):
            _LOGGER.debug("Iterate data for powerstation %s", value)
            if value and value in SENSORS:
                async_add_devices(
                    [
                        TalentMonitorPowerStationSensor(
                            coordinator,
                            power_station,
                            SENSORS[value],
                        )
                    ]
                )

class TalentMonitorPowerStationSensor(TalentMonitorEntity, SensorEntity):
    """TalentMonitor PowerStation Sensor class."""

    def __init__(
        self,
        coordinator,
        power_station: PowerStation,
        sensorEntityDescription: SensorEntityDescription,
    ):
        """Initialize a TalentMonitor PowerStation sensor."""
        super().__init__(
            coordinator,
            power_station,
            sensorEntityDescription.key
        )

        self._power_station = power_station
        self.entity_description = sensorEntityDescription

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if (self.entity_description.key == "lastDataUpdateTime"):
            return datetime.fromisoformat(self._power_station.data[self.entity_description.key])
        else:
            return self._power_station.data[self.entity_description.key]

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        key_for_value_with_unit = self.entity_description.key + "Named"

        if (key_for_value_with_unit in self._power_station.data and self._power_station.data[key_for_value_with_unit]):
            value_split = self._power_station.data[key_for_value_with_unit].split(" ")
            if (value_split and len(value_split) == 2):
                unit = value_split[1]
                return SENSOR_UNIT_MAPPING[unit]

        return None

