"""Weight Gurus integration"""
from .const import DOMAIN


async def async_setup_entry(hass, entry):
    """Set up Weight Gurus platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True
