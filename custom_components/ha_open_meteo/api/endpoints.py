"""URL and query builders for Open-Meteo endpoints."""

from __future__ import annotations

from typing import Any

from ..const import (
    AIR_QUALITY_URL,
    ARCHIVE_URL,
    CLIMATE_URL,
    ELEVATION_URL,
    ENSEMBLE_URL,
    FLOOD_URL,
    FORECAST_URL,
    GEOCODING_URL,
    MARINE_URL,
    SEASONAL_URL,
)


def _base_params(
    latitude: float,
    longitude: float,
    *,
    timezone: str = "auto",
    temperature_unit: str | None = None,
    wind_speed_unit: str | None = None,
    precipitation_unit: str | None = None,
    forecast_days: int | None = None,
    models: list[str] | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
    }
    if temperature_unit:
        params["temperature_unit"] = temperature_unit
    if wind_speed_unit:
        params["wind_speed_unit"] = wind_speed_unit
    if precipitation_unit:
        params["precipitation_unit"] = precipitation_unit
    if forecast_days is not None:
        params["forecast_days"] = forecast_days
    if models:
        params["models"] = models
    return params


def forecast_request(
    latitude: float,
    longitude: float,
    *,
    current: list[str] | None = None,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    minutely_15: list[str] | None = None,
    forecast_days: int = 7,
    models: list[str] | None = None,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
    tilt: float | None = None,
    azimuth: float | None = None,
) -> tuple[str, dict[str, Any]]:
    """Build a Weather Forecast API request."""
    params = _base_params(
        latitude,
        longitude,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
        precipitation_unit=precipitation_unit,
        forecast_days=forecast_days,
        models=models,
    )
    if current:
        params["current"] = current
    if hourly:
        params["hourly"] = hourly
    if daily:
        params["daily"] = daily
    if minutely_15:
        params["minutely_15"] = minutely_15
    if tilt is not None:
        params["tilt"] = tilt
    if azimuth is not None:
        params["azimuth"] = azimuth
    return FORECAST_URL, params


def air_quality_request(
    latitude: float,
    longitude: float,
    *,
    current: list[str] | None = None,
    hourly: list[str] | None = None,
    forecast_days: int = 5,
) -> tuple[str, dict[str, Any]]:
    """Build an Air Quality API request."""
    params = _base_params(latitude, longitude, forecast_days=forecast_days)
    if current:
        params["current"] = current
    if hourly:
        params["hourly"] = hourly
    return AIR_QUALITY_URL, params


def marine_request(
    latitude: float,
    longitude: float,
    *,
    current: list[str] | None = None,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    forecast_days: int = 7,
    wind_speed_unit: str = "kmh",
) -> tuple[str, dict[str, Any]]:
    """Build a Marine API request."""
    params = _base_params(
        latitude,
        longitude,
        wind_speed_unit=wind_speed_unit,
        forecast_days=forecast_days,
    )
    params["cell_selection"] = "sea"
    if current:
        params["current"] = current
    if hourly:
        params["hourly"] = hourly
    if daily:
        params["daily"] = daily
    return MARINE_URL, params


def flood_request(
    latitude: float,
    longitude: float,
    *,
    daily: list[str] | None = None,
    forecast_days: int = 92,
) -> tuple[str, dict[str, Any]]:
    """Build a Flood API request."""
    params = _base_params(latitude, longitude, forecast_days=forecast_days)
    if daily:
        params["daily"] = daily
    return FLOOD_URL, params


def ensemble_request(
    latitude: float,
    longitude: float,
    *,
    current: list[str] | None = None,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    forecast_days: int = 7,
    models: list[str] | None = None,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
) -> tuple[str, dict[str, Any]]:
    """Build an Ensemble API request."""
    params = _base_params(
        latitude,
        longitude,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
        precipitation_unit=precipitation_unit,
        forecast_days=forecast_days,
        models=models,
    )
    if current:
        params["current"] = current
    if hourly:
        params["hourly"] = hourly
    if daily:
        params["daily"] = daily
    return ENSEMBLE_URL, params


def seasonal_request(
    latitude: float,
    longitude: float,
    *,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    weekly: list[str] | None = None,
    monthly: list[str] | None = None,
    forecast_days: int = 183,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
) -> tuple[str, dict[str, Any]]:
    """Build a Seasonal Forecast API request."""
    params = _base_params(
        latitude,
        longitude,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
        precipitation_unit=precipitation_unit,
        forecast_days=forecast_days,
    )
    if hourly:
        params["hourly"] = hourly
    if daily:
        params["daily"] = daily
    if weekly:
        params["weekly"] = weekly
    if monthly:
        params["monthly"] = monthly
    return SEASONAL_URL, params


def archive_request(
    latitude: float,
    longitude: float,
    *,
    start_date: str,
    end_date: str,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
) -> tuple[str, dict[str, Any]]:
    """Build a Historical Weather API request."""
    params = _base_params(
        latitude,
        longitude,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
        precipitation_unit=precipitation_unit,
    )
    params["start_date"] = start_date
    params["end_date"] = end_date
    if hourly:
        params["hourly"] = hourly
    if daily:
        params["daily"] = daily
    return ARCHIVE_URL, params


def climate_request(
    latitude: float,
    longitude: float,
    *,
    start_date: str,
    end_date: str,
    daily: list[str],
    models: list[str],
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
) -> tuple[str, dict[str, Any]]:
    """Build a Climate API request."""
    params = _base_params(
        latitude,
        longitude,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
        precipitation_unit=precipitation_unit,
        models=models,
    )
    params.pop("timezone", None)
    params["start_date"] = start_date
    params["end_date"] = end_date
    params["daily"] = daily
    return CLIMATE_URL, params


def elevation_request(latitude: float, longitude: float) -> tuple[str, dict[str, Any]]:
    """Build an Elevation API request."""
    return ELEVATION_URL, {"latitude": latitude, "longitude": longitude}


def geocoding_request(name: str, count: int = 8) -> tuple[str, dict[str, Any]]:
    """Build a Geocoding search request."""
    return GEOCODING_URL, {"name": name, "count": count, "language": "en", "format": "json"}
