"""weight_gurus coordinator."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiClientException, WeightGurusApiClient
from .const import DATA_COORDINATOR_UPDATE_INTERVAL, DOMAIN, LOGGER


class WeightGurusDataUpdateCoordinator(DataUpdateCoordinator):
    """WeightGurus data update coordinator."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, api: WeightGurusApiClient) -> None:
        """Initialize the data update coordinator."""
        self.api = api
        self.platforms: list[str] = []

        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=DATA_COORDINATOR_UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            return await self.api.async_get_data()
        except ApiClientException as exception:
            raise UpdateFailed(exception) from exception
