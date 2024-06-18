"""Sensor platform for TalentMonitor."""

from datetime import datetime
import logging
import re
from custom_components.talent_monitor.entity import (
    TalentMonitorEntity,
    TalentMonitorInverterEntity,
)
from custom_components.talent_monitor.pyTalentMonitor.data_provider import Entity
from custom_components.talent_monitor.pyTalentMonitor.inverter import Inverter
from custom_components.talent_monitor.pyTalentMonitor.power_station import PowerStation
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.const import UnitOfElectricPotential
from homeassistant.const import UnitOfEnergy
from homeassistant.const import UnitOfFrequency
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfPower
from homeassistant.core import callback

from .const import DOMAIN


_LOGGER: logging.Logger = logging.getLogger(__name__)

camel_case_to_snake_case = re.compile(r'(?<!^)(?=[A-Z])')

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="totalActivePower",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="ratedPower",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="dayEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="monthEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="yearEnergy",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
    SensorEntityDescription(
        key="lastDataUpdateTime",
        device_class=SensorDeviceClass.DATE,
    ),
    SensorEntityDescription(
        key="inverterTemp",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    SensorEntityDescription(
        key="activePower",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="power",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
    ),
    SensorEntityDescription(
        key="current",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
    ),
    SensorEntityDescription(
        key="voltage",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SensorEntityDescription(
        key="frequency",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
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
            if value == "pv" and "pvCount" in inverter.data:
                for index, pv in enumerate(inverter.data[value]):
                    if index < inverter.data["pvCount"] - 1 and index < len(
                        inverter.data[value]
                    ): # it seems pvCount is not set correctly as it is set to 3 when there are only 2 panels, subtracting 1 is a solution for now but might result in a problem at some point
                        for _, pv_value in enumerate(pv):
                            _LOGGER.debug(
                                "Iterate pv %d for inverter %s", index, pv_value
                            )
                            if pv_value and pv_value in SENSORS:
                                async_add_devices(
                                    [
                                        TalentMonitorInverterPanelSensor(
                                            coordinator,
                                            inverter,
                                            SENSORS[pv_value],
                                            index,
                                        )
                                    ]
                                )

            if value == "phase" and "acPhaseCount" in inverter.data:
                for index, phase in enumerate(inverter.data[value]):
                    if index < inverter.data["acPhaseCount"] and index < len(
                        inverter.data[value]
                    ):
                        for _, phase_value in enumerate(phase):
                            _LOGGER.debug(
                                "Iterate phase %d for inverter %s", index, phase_value
                            )
                            if phase_value and phase_value in SENSORS:
                                async_add_devices(
                                    [
                                        TalentMonitorInverterPhaseSensor(
                                            coordinator,
                                            inverter,
                                            SENSORS[phase_value],
                                            index,
                                        )
                                    ]
                                )


class TalentMonitorSensor(SensorEntity):
    """TalentMonitor Sensor class."""

    def __init__(
        self,
        entity: Entity,
    ):
        """Initialize a TalentMonitor sensor."""
        self._entity = entity

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def data(self):
        """Return the data of this sensor."""
        return self._entity.data

    @property
    def native_value(self):
        """Return the state of the sensor."""

        if self.entity_description.key == "lastDataUpdateTime":
            return datetime.fromisoformat(self.data[self.entity_description.key])
        else:
            key_for_value_with_unit = self.entity_description.key + "Named"

            if (
                key_for_value_with_unit in self.data
                and self.data[key_for_value_with_unit]
            ):
                value_split = self.data[key_for_value_with_unit].split(" ")

                if value_split and len(value_split) == 2:
                    value = value_split[0]
                    return value
                else:
                    return self.data[self.entity_description.key]
            else:
                return self.data[self.entity_description.key]

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        key_for_value_with_unit = self.entity_description.key + "Named"

        if key_for_value_with_unit in self.data and self.data[key_for_value_with_unit]:
            value_split = self.data[key_for_value_with_unit].split(" ")
            if value_split and len(value_split) == 2:
                unit = value_split[1]
                return SENSOR_UNIT_MAPPING[unit]
        return self.entity_description.native_unit_of_measurement

class TalentMonitorPowerStationSensor(TalentMonitorEntity, TalentMonitorSensor):
    """TalentMonitor PowerStation Sensor class."""

    def __init__(
        self,
        coordinator,
        power_station: PowerStation,
        sensorEntityDescription: SensorEntityDescription,
    ):
        """Initialize a TalentMonitor PowerStation sensor."""
        TalentMonitorEntity.__init__(
            self, coordinator, power_station, sensorEntityDescription.key
        )
        TalentMonitorSensor.__init__(self, power_station)

        self.entity_description = sensorEntityDescription
        self.translation_key = 'talentmonitor_powerstation_' + camel_case_to_snake_case.sub('_', sensorEntityDescription.key).lower()


class TalentMonitorInverterSensor(TalentMonitorInverterEntity, TalentMonitorSensor):
    """TalentMonitor Inverter Sensor class."""

    def __init__(
        self,
        coordinator,
        inverter: Inverter,
        sensorEntityDescription: SensorEntityDescription,
    ):
        """Initialize a TalentMonitor Inverter sensor."""
        TalentMonitorInverterEntity.__init__(
            self, coordinator, inverter, sensorEntityDescription.key
        )
        TalentMonitorSensor.__init__(self, inverter)

        self.entity_description = sensorEntityDescription
        self.translation_key = 'talentmonitor_inverter_' + camel_case_to_snake_case.sub('_', sensorEntityDescription.key).lower()

class TalentMonitorInverterPhaseSensor(
    TalentMonitorInverterEntity, TalentMonitorSensor
):
    """TalentMonitor Inverter Phase Sensor class."""

    def __init__(
        self,
        coordinator,
        inverter: Inverter,
        sensorEntityDescription: SensorEntityDescription,
        phase_index,
    ):
        """Initialize a TalentMonitor Inverter sensor."""
        TalentMonitorInverterEntity.__init__(
            self,
            coordinator,
            inverter,
            "phase" + str(phase_index) + sensorEntityDescription.key,
        )
        TalentMonitorSensor.__init__(self, inverter)
        phase_name = inverter.data["acPhaseExpress"].split(",")[phase_index] if "acPhaseExpress" in inverter.data else phase_index
        self._attr_translation_placeholders = {"phase_id": phase_name }
        self.entity_description = sensorEntityDescription
        self.translation_key = 'talentmonitor_inverter_phase_' + camel_case_to_snake_case.sub('_', sensorEntityDescription.key).lower()
        self._phase_index = phase_index

    @property
    def data(self):
        """Return the data of this sensor."""
        return self._entity.data["phase"][self._phase_index]

class TalentMonitorInverterPanelSensor(
    TalentMonitorInverterEntity, TalentMonitorSensor
):
    """TalentMonitor Inverter Panel Sensor class."""

    def __init__(
        self,
        coordinator,
        inverter: Inverter,
        sensorEntityDescription: SensorEntityDescription,
        panel_index,
    ):
        """Initialize a TalentMonitor Inverter sensor."""
        TalentMonitorInverterEntity.__init__(
            self,
            coordinator,
            inverter,
            "panel" + str(panel_index) + sensorEntityDescription.key,
        )
        TalentMonitorSensor.__init__(self, inverter)

        self._attr_translation_placeholders = {"panel_id": panel_index}
        self.entity_description = sensorEntityDescription
        self.translation_key = 'talentmonitor_inverter_panel_' + sensorEntityDescription.key
        self._panel_index = panel_index

    @property
    def data(self):
        """Return the data of this sensor."""
        return self._entity.data["pv"][self._panel_index]
