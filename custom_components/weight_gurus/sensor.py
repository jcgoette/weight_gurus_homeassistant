"""weight_gurus sensor."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.dt import as_local, parse_datetime
from voluptuous.validators import Datetime

from .const import (
    ATTR_ACTIVITY_LEVEL,
    ATTR_BMI,
    ATTR_BODY_FAT,
    ATTR_ENTRY_TIMESTAMP,
    ATTR_FIRST_NAME,
    ATTR_HEIGHT,
    ATTR_LAST_NAME,
    ATTR_MUSCLE_MASS,
    ATTR_WATER,
    ATTR_WEIGHT,
    DOMAIN,
    NAME,
)
from .coordinator import WeightGurusDataUpdateCoordinator
from .entity import WeightGurusEntity


@dataclass
class WeightGurusEntityDescription(SensorEntityDescription):
    """WeightGurusEntityDescription."""

    pretty_key: str = ""


SENSOR_TYPES: tuple[WeightGurusEntityDescription, ...] = (
    WeightGurusEntityDescription(
        icon="mdi:percent",
        key=ATTR_BODY_FAT,
        native_unit_of_measurement="%",
        pretty_key="Body Fat",
    ),
    WeightGurusEntityDescription(
        icon="mdi:scale-bathroom",
        key=ATTR_BMI,
        native_unit_of_measurement="kg/m2",
        pretty_key="BMI",
    ),
    WeightGurusEntityDescription(
        icon="mdi:scale-bathroom",
        key="goalWeight",
        pretty_key="Goal Weight",
    ),
    WeightGurusEntityDescription(
        icon="mdi:scale-bathroom",
        key="initialWeight",
        pretty_key="Initial Weight",
    ),
    WeightGurusEntityDescription(
        icon="mdi:percent",
        key=ATTR_MUSCLE_MASS,
        native_unit_of_measurement="%",
        pretty_key="Muscle Mass",
    ),
    WeightGurusEntityDescription(
        icon="mdi:water-percent",
        key=ATTR_WATER,
        native_unit_of_measurement="%",
        pretty_key="Water",
    ),
    WeightGurusEntityDescription(
        icon="mdi:scale-bathroom",
        key=ATTR_WEIGHT,
        pretty_key="Weight",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for description in SENSOR_TYPES:
        if description.key in coordinator.data and coordinator.data[description.key]:
            entities.append(WeightGurusSensor(coordinator, description))

    async_add_devices(entities)


class WeightGurusSensor(WeightGurusEntity, SensorEntity):
    """WeightGurus sensor."""

    def __init__(
        self,
        coordinator: WeightGurusDataUpdateCoordinator,
        description: WeightGurusEntityDescription,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._description = description

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data[self._description.key]

    @property
    def extra_state_attributes(self) -> dict[str, str | Datetime]:
        """Return the extra state attributes."""
        extra_state_attributes = {
            ATTR_FIRST_NAME: str(self.coordinator.data.get(ATTR_FIRST_NAME)),
            ATTR_LAST_NAME: str(self.coordinator.data.get(ATTR_LAST_NAME)),
            ATTR_HEIGHT: str(self.coordinator.data.get(ATTR_HEIGHT) / 10),
            ATTR_ACTIVITY_LEVEL: str(self.coordinator.data.get(ATTR_ACTIVITY_LEVEL)),
        }
        if self.coordinator.data.get(f"{self._description.key}_{ATTR_ENTRY_TIMESTAMP}"):
            timestamp_str = self.coordinator.data[
                f"{self._description.key}_{ATTR_ENTRY_TIMESTAMP}"
            ]
            timestamp_dt = parse_datetime(timestamp_str)
            timestamp_local = as_local(timestamp_dt)
            extra_state_attributes[ATTR_ENTRY_TIMESTAMP] = timestamp_local
        return extra_state_attributes

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        return self._description.icon

    @property
    def name(self) -> str:
        """Return the name."""
        name_builder = {
            key: value
            for key, value in self.coordinator.data.items()
            if key in [ATTR_FIRST_NAME, ATTR_LAST_NAME]
        }
        name_builder = {
            "name": NAME,
            **name_builder,
            "pretty_key": self._description.pretty_key,
        }
        name_builder = " ".join(
            {value: key for key, value in name_builder.items() if value}
        )

        return name_builder

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        return self.coordinator.data[self._description.key] / 10

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the native unit of measurement."""
        if self._description.native_unit_of_measurement:
            return self._description.native_unit_of_measurement
        return self.coordinator.data["weightUnit"]

    @property
    def unique_id(self) -> str:
        """Return a unique, HASS-friendly identifier for this entity."""
        return f"{self.device_id}_{self._description.key}"
