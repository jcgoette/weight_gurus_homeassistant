"""weight_gurus entity."""
from __future__ import annotations

from homeassistant.const import CONF_EMAIL
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_MEASUREMENT, DOMAIN, NAME, VERSION
from .coordinator import WeightGurusDataUpdateCoordinator


class WeightGurusEntity(CoordinatorEntity):
    """WeightGurusEntity class"""

    coordinator: WeightGurusDataUpdateCoordinator

    @property
    def device_id(self) -> str | None:
        """Return the device id."""
        if not self.coordinator.config_entry:
            return None
        return self.coordinator.config_entry.entry_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.get(CONF_EMAIL))},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )

    @property
    def state_class(self) -> str:
        """Return the state class."""
        return ATTR_MEASUREMENT
