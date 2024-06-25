"""TalentMonitorEntity class."""

import logging

from custom_components.tsun.pyTalentMonitor.data_provider import Entity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.tsun.pyTalentMonitor.inverter import Inverter

from .const import DOMAIN
from .const import NAME

_LOGGER: logging.Logger = logging.getLogger(__name__)


class TalentMonitorEntity(CoordinatorEntity):
    """Base Class for TalentMonitor entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entity: Entity, entity_suffix: str = ""):
        """Initialize a TalentMonitor entity."""
        CoordinatorEntity.__init__(self, coordinator)

        device_id = f"{entity.entity_id}"
        device_name = entity.name

        self._attr_unique_id = f"{device_id}{entity_suffix}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            manufacturer=NAME,
            name=device_name,
        )

        _LOGGER.debug("Added TalentMonitor entity id='%s'", self.unique_id)


class TalentMonitorInverterEntity(CoordinatorEntity):
    """Base Class for TalentMonitor inverter entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, inverter: Inverter, entity_suffix: str = ""):
        """Initialize a TalentMonitor inverter entity."""
        super().__init__(coordinator)

        device_id = f"{inverter.entity_id}"
        device_name = inverter.name

        self._attr_unique_id = f"{device_id}{entity_suffix}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            manufacturer=inverter.data.get("nameOfManufacturer", NAME),
            name=device_name,
            serial_number=inverter.data.get("serialNumber", None),
            sw_version=inverter.data.get("firmwareVersion1", None),
            model=inverter.data.get("model", None),
        )

        _LOGGER.debug("Added TalentMonitor entity id='%s'", self.unique_id)
