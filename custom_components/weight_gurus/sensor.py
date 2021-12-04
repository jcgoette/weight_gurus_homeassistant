"""Platform for Weight Gurus sensor integration."""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import requests
import stringcase
import voluptuous as vol
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, MASS_KILOGRAMS, MASS_POUNDS
from homeassistant.helpers.entity import Entity

from .const import (
    ATTR_ACCESS_TOKEN,
    ATTR_DECIMAL_VALUES,
    ATTR_DEFAULT_NAME,
    ATTR_ENTRY_TIMESTAMP,
    ATTR_ICON,
    ATTR_OPERATIONS,
    ATTR_URL,
    ATTR_WEIGHT,
    DOMAIN,
)

# TODO: add error logging
_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup Weight Gurus sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    unit_system = hass.config.units.is_metric
    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]

    weight_gurus_data = WeightGurusData(email, password)

    async_add_entities(
        [WeightGurusSensor(unit_system, weight_gurus_data)], update_before_add=True
    )


class WeightGurusSensor(Entity):
    """Representation of a Weight Gurus Sensor."""

    def __init__(self, unit_system, weight_gurus_data):
        """Initialize the Weight Gurus sensor."""
        self._state = None
        self._unit_system = unit_system
        self._weight_gurus_data = weight_gurus_data
        self._data = self._weight_gurus_data._data

    @property
    def name(self):
        """Return the name of the Weight Gurus sensor."""
        return ATTR_DEFAULT_NAME

    @property
    def state(self):
        """Return the state of the Weight Gurus sensor."""
        # TODO: better way to handle significant digits
        if self._unit_system:
            return round(
                self._data.get(ATTR_DECIMAL_VALUES).get(ATTR_WEIGHT) * 0.45359, 1
            )
        return self._data.get(ATTR_DECIMAL_VALUES).get(ATTR_WEIGHT)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the Weight Gurus sensor state."""
        if self._unit_system:
            return MASS_KILOGRAMS
        return MASS_POUNDS

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes for Weight Gurus."""
        self._extra_state_attributes = self._data.get(ATTR_DECIMAL_VALUES)

        entry_timestamp = self._data.get(ATTR_ENTRY_TIMESTAMP)
        entry_timestamp = dt_util.parse_datetime(entry_timestamp)
        localized_timestamp = dt_util.as_local(entry_timestamp)

        self._extra_state_attributes[ATTR_ENTRY_TIMESTAMP] = localized_timestamp

        self._extra_state_attributes = {
            stringcase.snakecase(key): value
            for (key, value) in sorted(
                self._extra_state_attributes.items(), key=lambda item: item[0]
            )
            if key != ATTR_WEIGHT
        }
        return self._extra_state_attributes

    @property
    def icon(self):
        """Return the icon to use in Weight Gurus frontend."""
        return ATTR_ICON

    def update(self):
        """Update data from Weight Gurus for the sensor."""
        self._weight_gurus_data.update()
        self._data = self._weight_gurus_data._data


# TODO: PYPI package
class WeightGurusData:
    """Coordinate retrieving and updating data from Weight Gurus."""

    def __init__(self, email, password):
        """Initialize the WeightGurusData object."""
        self._data = None
        self._email = email
        self._password = password

    def WeightGurusQuery(self, email, password):
        """Query Weight Gurus for data via hidden API."""
        data_account = {CONF_EMAIL: email, CONF_PASSWORD: password}
        account_response = requests.post(f"{ATTR_URL}/account/login", data=data_account)
        account_json = account_response.json()

        account_access_token = account_json[ATTR_ACCESS_TOKEN]

        headers_operation = {
            "Authorization": f"Bearer {account_access_token}",
            "Accept": "application/json, text/plain, */*",
        }
        operation_response = requests.get(
            f"{ATTR_URL}/operation/", headers=headers_operation
        )
        operation_json = sorted(
            operation_response.json().get(ATTR_OPERATIONS),
            key=lambda x: x[ATTR_ENTRY_TIMESTAMP],
        )

        # TODO: account for deleted entries
        for entry in operation_json[-1:]:
            entry_data = {}

            entry_data[ATTR_ENTRY_TIMESTAMP] = entry.get(ATTR_ENTRY_TIMESTAMP)

            entry_data[ATTR_DECIMAL_VALUES] = {
                key: value / 10
                for (key, value) in entry.items()
                if isinstance(value, int)
            }

        return entry_data

    def update(self):
        """Update data from Weight Gurus via WeightGurusQuery."""
        self._data = self.WeightGurusQuery(self._email, self._password)
