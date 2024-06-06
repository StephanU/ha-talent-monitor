"""Sensor platform for TalentMonitor."""
from datetime import datetime
import logging
from custom_components.talent_monitor.entity import TalentMonitorEntity, TalentMonitorInverterEntity
from custom_components.talent_monitor.pyTalentMonitor.inverter import Inverter
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
        translation_key="talentmonitor_powerstation_total_active_power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="ratedPower",
        translation_key="talentmonitor_powerstation_rated_power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="dayEnergy",
        translation_key="talentmonitor_powerstation_day_energy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="monthEnergy",
        translation_key="talentmonitor_powerstation_month_energy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="yearEnergy",
        translation_key="talentmonitor_powerstation_year_energy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="lastDataUpdateTime",
        translation_key="talentmonitor_powerstation_last_data_update_time",
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

    inverters: list[Inverter] = coordinator.api.get_inverters()
    for inverter in inverters:
        for _, value in enumerate(inverter.data):
            _LOGGER.debug("Iterate data for inverter %s", value)
            if value and value in SENSORS:
                async_add_devices(
                    [
                        TalentMonitorInverterSensor(
                            coordinator,
                            inverter,
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


class TalentMonitorInverterSensor(TalentMonitorInverterEntity, SensorEntity):
    """TalentMonitor Inverter Sensor class."""

    def __init__(
        self,
        coordinator,
        inverter: Inverter,
        sensorEntityDescription: SensorEntityDescription,
    ):
        """Initialize a TalentMonitor Inverter sensor."""
        super().__init__(
            coordinator,
            inverter,
            sensorEntityDescription.key
        )

        self._inverter = inverter
        self.entity_description = sensorEntityDescription

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if (self.entity_description.key == "lastDataUpdateTime"):
            return datetime.fromisoformat(self._inverter.data[self.entity_description.key])
        else:
            return self._inverter.data[self.entity_description.key]

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        key_for_value_with_unit = self.entity_description.key + "Named"

        if (key_for_value_with_unit in self._inverter.data and self._inverter.data[key_for_value_with_unit]):
            value_split = self._inverter.data[key_for_value_with_unit].split(" ")
            if (value_split and len(value_split) == 2):
                unit = value_split[1]
                return SENSOR_UNIT_MAPPING[unit]

        return None

