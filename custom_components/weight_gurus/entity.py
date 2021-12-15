"""weight_gurus entity."""
from __future__ import annotations

from typing import Any

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
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the extra state attributes."""
        return {
            ATTR_FIRST_NAME: str(self.coordinator.data.get(ATTR_FIRST_NAME)),
            ATTR_LAST_NAME: str(self.coordinator.data.get(ATTR_LAST_NAME)),
            ATTR_HEIGHT: str(self.coordinator.data.get(ATTR_HEIGHT) / 10),
            ATTR_ACTIVITY_LEVEL: str(self.coordinator.data.get(ATTR_ACTIVITY_LEVEL)),
        }

    @property
    def state_class(self) -> str:
        """Return the state class."""
        return ATTR_MEASUREMENT
