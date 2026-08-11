"""Shared helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.util import dt as dt_util

from .const import (
    CONF_AZIMUTH,
    CONF_FORECAST_DAYS,
    CONF_GROUPS,
    CONF_MODELS,
    CONF_MODULES,
    CONF_PRECIPITATION_UNIT,
    CONF_PRESSURE_LEVELS,
    CONF_TEMPERATURE_UNIT,
    CONF_TILT,
    CONF_UPDATE_INTERVAL,
    CONF_WIND_SPEED_UNIT,
    DEFAULT_FORECAST_DAYS,
    DEFAULT_MODELS,
    DEFAULT_MODULES,
    DEFAULT_PRECIPITATION_UNIT,
    DEFAULT_PRESSURE_LEVELS,
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DEFAULT_WIND_SPEED_UNIT,
)
from .models.variables import DEFAULT_GROUPS


def location_unique_id(latitude: float, longitude: float) -> str:
    """Stable unique ID from coordinates."""
    return f"{latitude:.4f}_{longitude:.4f}"


def entry_name(entry: ConfigEntry) -> str:
    """Return the configured location name."""
    return str(entry.data.get(CONF_NAME) or entry.title)


def entry_latitude(entry: ConfigEntry) -> float:
    return float(entry.data[CONF_LATITUDE])


def entry_longitude(entry: ConfigEntry) -> float:
    return float(entry.data[CONF_LONGITUDE])


def opt(entry: ConfigEntry, key: str, default: Any) -> Any:
    """Read an option, falling back to data then default."""
    if key in entry.options:
        return entry.options[key]
    return entry.data.get(key, default)


def configured_modules(entry: ConfigEntry) -> list[str]:
    return list(opt(entry, CONF_MODULES, DEFAULT_MODULES))


def configured_groups(entry: ConfigEntry) -> dict[str, list[str]]:
    groups = opt(entry, CONF_GROUPS, {})
    if isinstance(groups, dict) and groups:
        return {str(key): list(value) for key, value in groups.items()}
    return dict(DEFAULT_GROUPS)


def configured_models(entry: ConfigEntry) -> list[str]:
    models = opt(entry, CONF_MODELS, DEFAULT_MODELS)
    return list(models) if models else list(DEFAULT_MODELS)


def configured_pressure_levels(entry: ConfigEntry) -> list[str]:
    levels = opt(entry, CONF_PRESSURE_LEVELS, DEFAULT_PRESSURE_LEVELS)
    return [str(level) for level in levels]


def configured_forecast_days(entry: ConfigEntry) -> int:
    return int(opt(entry, CONF_FORECAST_DAYS, DEFAULT_FORECAST_DAYS))


def configured_update_minutes(entry: ConfigEntry) -> int:
    return int(opt(entry, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES))


def configured_units(entry: ConfigEntry) -> tuple[str, str, str]:
    return (
        str(opt(entry, CONF_TEMPERATURE_UNIT, DEFAULT_TEMPERATURE_UNIT)),
        str(opt(entry, CONF_WIND_SPEED_UNIT, DEFAULT_WIND_SPEED_UNIT)),
        str(opt(entry, CONF_PRECIPITATION_UNIT, DEFAULT_PRECIPITATION_UNIT)),
    )


def configured_panel(entry: ConfigEntry) -> tuple[float, float]:
    return float(opt(entry, CONF_TILT, 0)), float(opt(entry, CONF_AZIMUTH, 0))


def parse_api_datetime(value: str | None) -> datetime | None:
    """Parse an Open-Meteo timestamp into an aware datetime."""
    if not value:
        return None
    parsed = dt_util.parse_datetime(str(value))
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.get_default_time_zone())
    return parsed


def nearest_index(times: list[str]) -> int | None:
    """Index of the latest timestep that is not in the future."""
    if not times:
        return None
    now = dt_util.now()
    index = 0
    for i, stamp in enumerate(times):
        parsed = parse_api_datetime(stamp)
        if parsed is None:
            continue
        if parsed <= now:
            index = i
        else:
            break
    return index
