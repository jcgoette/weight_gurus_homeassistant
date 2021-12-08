"""weight_gurus API."""
import asyncio
import socket

import aiohttp
import async_timeout
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from .const import LOGGER

TIMEOUT = 10


class ApiClientException(Exception):
    """Api Client Exception."""


class WeightGurusApiClient:
    # TODO: refactor this class so functions live in appropriate method subnodes
    def __init__(
        self, email: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Initialize the API client."""
        self._email = email
        self._password = password
        self._session = session
        self._account_login_dict: dict = {}
        self._token_expires_at: str = ""

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "https://api.weightgurus.com/v3/operation/"
        headers = await self.async_build_headers()
        data = await self.api_wrapper("get", url, {}, headers)
        return await self.get_last_entry_and_merge_dicts(data)

    async def async_build_headers(self) -> dict:
        """Build headers for the API."""
        account_access_token = await self.async_get_token_and_save_account_dict()
        headers = {
            "Authorization": f"Bearer {account_access_token}",
            "Accept": "application/json, text/plain, */*",
        }
        return headers

    async def async_get_token_and_save_account_dict(self) -> str:
        """Get account access token and save account dict."""
        # TODO: check self._token_expires_at before requesting new token (but this might not be a good idea if goalType, goalWeight, and initialWeight change frequently)
        account_credentials = {CONF_EMAIL: self._email, CONF_PASSWORD: self._password}
        account_login_response = await self._session.post(
            f"https://api.weightgurus.com/v3/account/login", data=account_credentials
        )
        account_login_json = await account_login_response.json()
        self._token_expires_at = account_login_json["expiresAt"]
        self._account_login_dict = account_login_json["account"]
        account_access_token = account_login_json["accessToken"]
        return account_access_token

    async def get_last_entry_and_merge_dicts(self, data: dict) -> dict:
        """Get last entry and merge dicts."""
        sorted_data = sorted(
            data["operations"],
            key=lambda x: x["entryTimestamp"],
        )
        last_entry = sorted_data[-1:][0]
        merged_dicts = {**self._account_login_dict, **last_entry}
        return merged_dicts

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """API wrapper."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    await self._session.post(url, headers=headers, json=data)

        except asyncio.TimeoutError as exception:
            LOGGER.error(
                "Timeout error fetching information from %s - %s", url, exception
            )

        except (KeyError, TypeError) as exception:
            LOGGER.error("Error parsing information from %s - %s", url, exception)
        except (aiohttp.ClientError, socket.gaierror) as exception:
            LOGGER.error("Error fetching information from %s - %s", url, exception)
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.error("Something really wrong happened! - %s", exception)
