"""Sensor platform for TalentMonitor."""
from custom_components.talent_monitor.entity import TalentMonitorEntity
from custom_components.talent_monitor.pyTalentMonitor.power_station import PowerStation
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfPower

from .const import DOMAIN

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="totalActivePower",
        translation_key="talentmonitor_powerstation_totalActivePower",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    )
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
        for index, value in enumerate(power_station.data):
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
        )

        self._power_station = power_station
        self.entity_description = sensorEntityDescription

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._power_station.data[self.entity_description.key]

