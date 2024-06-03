"""TalentMonitorEntity class."""
import logging

from custom_components.talent_monitor.pyTalentMonitor.data_provider import Entity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .const import NAME

_LOGGER: logging.Logger = logging.getLogger(__name__)


class TalentMonitorEntity(CoordinatorEntity):
    """Base Class for TalentMonitor entities."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator, entity: Entity, entity_suffix: str = ""
    ):
        """Initialize a TalentMonitor entity."""
        super().__init__(coordinator)

        device_id = f"{entity.entity_id}"
        device_name = entity.name

        self._attr_unique_id = f"{device_id}{entity_suffix}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            manufacturer=NAME,
            name=device_name,
        )

        _LOGGER.debug("Added TalentMonitor entity id='%s'", self.unique_id)
