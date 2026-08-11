"""Data update coordinators for Open-Meteo modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import OpenMeteoApiError, OpenMeteoClient
from .api import endpoints
from .const import (
    ENSEMBLE_MODEL_CHOICES,
    LOGGER,
    MODULE_AIR_QUALITY,
    MODULE_ELEVATION,
    MODULE_ENSEMBLE,
    MODULE_FLOOD,
    MODULE_FORECAST,
    MODULE_MARINE,
    MODULE_SEASONAL,
    WEATHER_CURRENT_VARS,
    WEATHER_DAILY_VARS,
    WEATHER_HOURLY_VARS,
)
from .helpers import (
    configured_forecast_days,
    configured_groups,
    configured_models,
    configured_panel,
    configured_pressure_levels,
    configured_units,
    configured_update_minutes,
    entry_latitude,
    entry_longitude,
    nearest_index,
)
from .models.variables import VariableDef, expand_variables


@dataclass
class ModuleData:
    """Parsed payload for one Open-Meteo module."""

    raw: dict[str, Any]
    current: dict[str, Any] = field(default_factory=dict)
    series: dict[str, dict[str, list[Any]]] = field(default_factory=dict)
    times: dict[str, list[str]] = field(default_factory=dict)

    def value(self, bucket: str, key: str) -> Any:
        """Return the current/latest value for a variable."""
        if key in self.current and bucket == "current":
            return self.current.get(key)
        if bucket == "current" and key in self.current:
            return self.current.get(key)
        values = self.series.get(bucket, {}).get(key)
        times = self.times.get(bucket, [])
        if values is None:
            if key in self.current:
                return self.current.get(key)
            return None
        index = nearest_index(times)
        if index is None or index >= len(values):
            return None
        return values[index]


def parse_module_payload(payload: dict[str, Any]) -> ModuleData:
    """Normalize an Open-Meteo JSON payload."""
    current_raw = payload.get("current") or {}
    current = {
        key: value
        for key, value in current_raw.items()
        if key not in {"time", "interval"}
    }
    if "elevation" in payload and "elevation" not in current:
        elevation = payload["elevation"]
        if isinstance(elevation, list):
            current["elevation"] = elevation[0] if elevation else None
        else:
            current["elevation"] = elevation

    series: dict[str, dict[str, list[Any]]] = {}
    times: dict[str, list[str]] = {}
    for bucket in ("hourly", "daily", "minutely_15", "weekly", "monthly"):
        block = payload.get(bucket)
        if not isinstance(block, dict):
            continue
        bucket_times = [str(item) for item in block.get("time") or []]
        times[bucket] = bucket_times
        series[bucket] = {
            key: list(values)
            for key, values in block.items()
            if key != "time" and isinstance(values, list)
        }
    return ModuleData(raw=payload, current=current, series=series, times=times)


class HaOpenMeteoCoordinator(DataUpdateCoordinator[ModuleData]):
    """Fetch one Open-Meteo API module for a config entry."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: OpenMeteoClient,
        module: str,
    ) -> None:
        self.entry = entry
        self.client = client
        self.module = module
        super().__init__(
            hass,
            LOGGER,
            name=f"Open-Meteo {module}",
            config_entry=entry,
            update_interval=_interval_for_module(module, configured_update_minutes(entry)),
        )

    async def _async_update_data(self) -> ModuleData:
        try:
            url, params = self._build_request()
            payload = await self.client.get(url, params)
        except OpenMeteoApiError as err:
            raise UpdateFailed(str(err)) from err
        return parse_module_payload(payload)

    def selected_variables(self) -> list[VariableDef]:
        """Variable defs enabled for this module."""
        groups = configured_groups(self.entry).get(self.module, [])
        return expand_variables(
            self.module,
            groups,
            configured_pressure_levels(self.entry),
        )

    def _build_request(self) -> tuple[str, dict[str, Any]]:
        latitude = entry_latitude(self.entry)
        longitude = entry_longitude(self.entry)
        temp_unit, wind_unit, precip_unit = configured_units(self.entry)
        forecast_days = configured_forecast_days(self.entry)
        models = configured_models(self.entry)
        tilt, azimuth = configured_panel(self.entry)
        buckets = _keys_by_bucket(self.selected_variables())

        if self.module == MODULE_FORECAST:
            current = _merge(WEATHER_CURRENT_VARS, buckets.get("current", []))
            hourly = _merge(WEATHER_HOURLY_VARS, buckets.get("hourly", []))
            daily = _merge(WEATHER_DAILY_VARS, buckets.get("daily", []))
            return endpoints.forecast_request(
                latitude,
                longitude,
                current=current,
                hourly=hourly,
                daily=daily,
                minutely_15=buckets.get("minutely_15") or None,
                forecast_days=min(forecast_days, 16),
                models=models,
                temperature_unit=temp_unit,
                wind_speed_unit=wind_unit,
                precipitation_unit=precip_unit,
                tilt=tilt,
                azimuth=azimuth,
            )

        if self.module == MODULE_AIR_QUALITY:
            current = buckets.get("current", [])
            hourly = buckets.get("hourly", [])
            if not hourly and current:
                hourly = list(current)
            return endpoints.air_quality_request(
                latitude,
                longitude,
                current=current or None,
                hourly=hourly or None,
                forecast_days=min(forecast_days, 7),
            )

        if self.module == MODULE_MARINE:
            return endpoints.marine_request(
                latitude,
                longitude,
                current=buckets.get("current") or None,
                hourly=buckets.get("hourly") or buckets.get("current") or None,
                daily=buckets.get("daily") or None,
                forecast_days=min(forecast_days, 8),
                wind_speed_unit=wind_unit,
            )

        if self.module == MODULE_FLOOD:
            return endpoints.flood_request(
                latitude,
                longitude,
                daily=buckets.get("daily") or ["river_discharge"],
                forecast_days=min(max(forecast_days, 7), 210),
            )

        if self.module == MODULE_ENSEMBLE:
            ensemble_models = [model for model in models if model in ENSEMBLE_MODEL_CHOICES]
            return endpoints.ensemble_request(
                latitude,
                longitude,
                current=buckets.get("current") or None,
                hourly=buckets.get("hourly") or None,
                daily=buckets.get("daily") or None,
                forecast_days=min(forecast_days, 35),
                models=ensemble_models or ["icon_seamless"],
                temperature_unit=temp_unit,
                wind_speed_unit=wind_unit,
                precipitation_unit=precip_unit,
            )

        if self.module == MODULE_SEASONAL:
            return endpoints.seasonal_request(
                latitude,
                longitude,
                hourly=buckets.get("hourly") or None,
                daily=buckets.get("daily") or None,
                weekly=buckets.get("weekly") or None,
                monthly=buckets.get("monthly") or None,
                forecast_days=min(max(forecast_days, 30), 210),
                temperature_unit=temp_unit,
                wind_speed_unit=wind_unit,
                precipitation_unit=precip_unit,
            )

        if self.module == MODULE_ELEVATION:
            return endpoints.elevation_request(latitude, longitude)

        raise UpdateFailed(f"Unsupported module: {self.module}")


def _interval_for_module(module: str, minutes: int) -> timedelta | None:
    if module == MODULE_ELEVATION:
        return None
    if module == MODULE_SEASONAL:
        return timedelta(hours=6)
    if module == MODULE_ENSEMBLE:
        return timedelta(minutes=max(minutes, 60))
    return timedelta(minutes=max(minutes, 5))


def _keys_by_bucket(variables: list[VariableDef]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    for variable in variables:
        keys = buckets.setdefault(variable.bucket, [])
        if variable.key not in keys:
            keys.append(variable.key)
    return buckets


def _merge(*lists: list[str]) -> list[str]:
    merged: list[str] = []
    for items in lists:
        for item in items:
            if item not in merged:
                merged.append(item)
    return merged
