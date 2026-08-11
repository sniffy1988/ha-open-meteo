"""Historical weather and climate projection services."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import OpenMeteoApiError, OpenMeteoClient
from .api import endpoints
from .const import (
    CONF_MODELS,
    DEFAULT_CLIMATE_MODELS,
    DEFAULT_PRECIPITATION_UNIT,
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_WIND_SPEED_UNIT,
    DOMAIN,
    LOGGER,
    SERVICE_GET_CLIMATE,
    SERVICE_GET_HISTORICAL,
)
from .helpers import configured_units, entry_latitude, entry_longitude

ATTR_CONFIG_ENTRY_ID = "config_entry_id"
ATTR_START_DATE = "start_date"
ATTR_END_DATE = "end_date"
ATTR_HOURLY = "hourly"
ATTR_DAILY = "daily"

DEFAULT_HISTORICAL_HOURLY = ["temperature_2m", "precipitation", "weather_code"]
DEFAULT_HISTORICAL_DAILY = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "weather_code",
]
DEFAULT_CLIMATE_DAILY = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
]


HISTORICAL_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_CONFIG_ENTRY_ID): cv.string,
        vol.Optional(CONF_LATITUDE): cv.latitude,
        vol.Optional(CONF_LONGITUDE): cv.longitude,
        vol.Required(ATTR_START_DATE): cv.string,
        vol.Required(ATTR_END_DATE): cv.string,
        vol.Optional(ATTR_HOURLY): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_DAILY): vol.All(cv.ensure_list, [cv.string]),
    }
)

CLIMATE_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_CONFIG_ENTRY_ID): cv.string,
        vol.Optional(CONF_LATITUDE): cv.latitude,
        vol.Optional(CONF_LONGITUDE): cv.longitude,
        vol.Required(ATTR_START_DATE): cv.string,
        vol.Required(ATTR_END_DATE): cv.string,
        vol.Optional(ATTR_DAILY): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_MODELS): vol.All(cv.ensure_list, [cv.string]),
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register domain services once."""
    if hass.services.has_service(DOMAIN, SERVICE_GET_HISTORICAL):
        return

    client = OpenMeteoClient(async_get_clientsession(hass))

    async def _historical(call: ServiceCall) -> ServiceResponse:
        latitude, longitude, temp_unit, wind_unit, precip_unit = _resolve_location(hass, call)
        hourly = call.data.get(ATTR_HOURLY) or DEFAULT_HISTORICAL_HOURLY
        daily = call.data.get(ATTR_DAILY) or DEFAULT_HISTORICAL_DAILY
        url, params = endpoints.archive_request(
            latitude,
            longitude,
            start_date=_as_date(call.data[ATTR_START_DATE]),
            end_date=_as_date(call.data[ATTR_END_DATE]),
            hourly=list(hourly),
            daily=list(daily),
            temperature_unit=temp_unit,
            wind_speed_unit=wind_unit,
            precipitation_unit=precip_unit,
        )
        return await _fetch(client, url, params)

    async def _climate(call: ServiceCall) -> ServiceResponse:
        latitude, longitude, temp_unit, wind_unit, precip_unit = _resolve_location(hass, call)
        daily = call.data.get(ATTR_DAILY) or DEFAULT_CLIMATE_DAILY
        models = call.data.get(CONF_MODELS) or DEFAULT_CLIMATE_MODELS
        url, params = endpoints.climate_request(
            latitude,
            longitude,
            start_date=_as_date(call.data[ATTR_START_DATE]),
            end_date=_as_date(call.data[ATTR_END_DATE]),
            daily=list(daily),
            models=list(models),
            temperature_unit=temp_unit,
            wind_speed_unit=wind_unit,
            precipitation_unit=precip_unit,
        )
        return await _fetch(client, url, params)

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_HISTORICAL,
        _historical,
        schema=HISTORICAL_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_CLIMATE,
        _climate,
        schema=CLIMATE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )


def async_unload_services(hass: HomeAssistant) -> None:
    """Remove domain services."""
    hass.services.async_remove(DOMAIN, SERVICE_GET_HISTORICAL)
    hass.services.async_remove(DOMAIN, SERVICE_GET_CLIMATE)


def _resolve_location(
    hass: HomeAssistant, call: ServiceCall
) -> tuple[float, float, str, str, str]:
    entry_id = call.data.get(ATTR_CONFIG_ENTRY_ID)
    latitude = call.data.get(CONF_LATITUDE)
    longitude = call.data.get(CONF_LONGITUDE)
    temp_unit = DEFAULT_TEMPERATURE_UNIT
    wind_unit = DEFAULT_WIND_SPEED_UNIT
    precip_unit = DEFAULT_PRECIPITATION_UNIT

    if entry_id:
        entry = hass.config_entries.async_get_entry(entry_id)
        if entry is None or entry.domain != DOMAIN:
            raise ServiceValidationError(f"Unknown Open-Meteo config entry: {entry_id}")
        latitude = entry_latitude(entry)
        longitude = entry_longitude(entry)
        temp_unit, wind_unit, precip_unit = configured_units(entry)
    elif latitude is None or longitude is None:
        raise ServiceValidationError(
            "Provide config_entry_id or both latitude and longitude"
        )

    return float(latitude), float(longitude), temp_unit, wind_unit, precip_unit


def _as_date(value: Any) -> str:
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


async def _fetch(client: OpenMeteoClient, url: str, params: dict[str, Any]) -> dict[str, Any]:
    try:
        return await client.get(url, params)
    except OpenMeteoApiError as err:
        LOGGER.error("Open-Meteo service request failed: %s", err)
        raise HomeAssistantError(str(err)) from err
