import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import ATTR_DEFAULT_NAME, DOMAIN


# TODO: better validation of data
# TODO: translations
class WeightGurusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input):
        if user_input is not None:
            return self.async_create_entry(title=ATTR_DEFAULT_NAME, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): cv.string,
                    vol.Required(CONF_PASSWORD): cv.string,
                }
            ),
        )
