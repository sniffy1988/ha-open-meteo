"""Async HTTP client for Open-Meteo APIs."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession

from ..const import LOGGER


class OpenMeteoError(Exception):
    """Base Open-Meteo client error."""


class OpenMeteoApiError(OpenMeteoError):
    """Raised when the Open-Meteo API returns an error."""

    def __init__(self, reason: str, status: int | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.status = status


class OpenMeteoClient:
    """Thin aiohttp wrapper for Open-Meteo GET endpoints."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform a GET request and return JSON."""
        cleaned = _clean_params(params or {})
        LOGGER.debug("GET %s params=%s", url, cleaned)
        try:
            async with asyncio.timeout(30):
                async with self._session.get(url, params=cleaned) as response:
                    payload: dict[str, Any] = await response.json(content_type=None)
                    if response.status >= 400 or payload.get("error"):
                        reason = str(
                            payload.get("reason")
                            or payload.get("message")
                            or response.reason
                            or "Unknown Open-Meteo error"
                        )
                        raise OpenMeteoApiError(reason, response.status)
                    return payload
        except TimeoutError as err:
            raise OpenMeteoApiError("Timeout talking to Open-Meteo") from err
        except ClientError as err:
            raise OpenMeteoApiError(f"Error talking to Open-Meteo: {err}") from err


def _clean_params(params: dict[str, Any]) -> dict[str, str | int | float]:
    """Drop empty values and join list params with commas."""
    cleaned: dict[str, str | int | float] = {}
    for key, value in params.items():
        if value is None or value is False:
            continue
        if value is True:
            cleaned[key] = "true"
            continue
        if isinstance(value, (list, tuple, set)):
            items = [str(item) for item in value if item is not None and item != ""]
            if not items:
                continue
            cleaned[key] = ",".join(items)
            continue
        cleaned[key] = value
    return cleaned
