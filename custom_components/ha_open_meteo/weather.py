"""Weather entity backed by the Forecast API."""

from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_FORECAST_CLOUD_COVERAGE,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_HUMIDITY,
    ATTR_FORECAST_NATIVE_APPARENT_TEMP,
    ATTR_FORECAST_NATIVE_PRECIPITATION,
    ATTR_FORECAST_NATIVE_PRESSURE,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_NATIVE_WIND_GUST_SPEED,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_WIND_BEARING,
    CoordinatorWeatherEntity,
    Forecast,
    WeatherEntityFeature,
)
from homeassistant.const import (
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util
from .const import (
    CLEAR_NIGHT,
    MODULE_FORECAST,
    PRECIP_UNIT_INCH,
    TEMP_UNIT_FAHRENHEIT,
    WIND_UNIT_KN,
    WIND_UNIT_MPH,
    WIND_UNIT_MS,
    WMO_TO_HA_CONDITION_MAP,
)
from .coordinator import HaOpenMeteoCoordinator
from .entity import device_info_for_entry
from .helpers import configured_units, parse_api_datetime

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the weather entity for this location."""
    coordinator = entry.runtime_data.coordinators.get(MODULE_FORECAST)
    if coordinator is None:
        return
    async_add_entities([HaOpenMeteoWeatherEntity(coordinator, entry)])


class HaOpenMeteoWeatherEntity(
    CoordinatorWeatherEntity[HaOpenMeteoCoordinator]
):
    """Current conditions plus daily and hourly forecasts."""

    _attr_attribution = "Weather data by Open-Meteo.com"
    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
    )
    _attr_native_pressure_unit = UnitOfPressure.HPA
    _attr_native_visibility_unit = UnitOfLength.METERS

    def __init__(
        self,
        coordinator: HaOpenMeteoCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_weather"
        self._attr_device_info = device_info_for_entry(entry)
        temp_unit, wind_unit, precip_unit = configured_units(entry)
        self._attr_native_temperature_unit = (
            UnitOfTemperature.FAHRENHEIT
            if temp_unit == TEMP_UNIT_FAHRENHEIT
            else UnitOfTemperature.CELSIUS
        )
        self._attr_native_wind_speed_unit = {
            WIND_UNIT_MS: UnitOfSpeed.METERS_PER_SECOND,
            WIND_UNIT_MPH: UnitOfSpeed.MILES_PER_HOUR,
            WIND_UNIT_KN: UnitOfSpeed.KNOTS,
        }.get(wind_unit, UnitOfSpeed.KILOMETERS_PER_HOUR)
        self._attr_native_precipitation_unit = (
            UnitOfPrecipitationDepth.INCHES
            if precip_unit == PRECIP_UNIT_INCH
            else UnitOfPrecipitationDepth.MILLIMETERS
        )

    def _current(self) -> dict:
        data = self.coordinator.data
        if data is None:
            return {}
        return data.current

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data is not None

    @property
    def condition(self) -> str | None:
        current = self._current()
        code = current.get("weather_code")
        if code is None:
            return None
        condition = WMO_TO_HA_CONDITION_MAP.get(int(code))
        if condition == WMO_TO_HA_CONDITION_MAP.get(0) and current.get("is_day") == 0:
            return CLEAR_NIGHT
        return condition

    @property
    def native_temperature(self) -> float | None:
        return _float(self._current().get("temperature_2m"))

    @property
    def native_apparent_temperature(self) -> float | None:
        return _float(self._current().get("apparent_temperature"))

    @property
    def native_dew_point(self) -> float | None:
        return _float(self._current().get("dew_point_2m"))

    @property
    def humidity(self) -> float | None:
        return _float(self._current().get("relative_humidity_2m"))

    @property
    def native_pressure(self) -> float | None:
        return _float(self._current().get("pressure_msl"))

    @property
    def native_wind_speed(self) -> float | None:
        return _float(self._current().get("wind_speed_10m"))

    @property
    def native_wind_gust_speed(self) -> float | None:
        return _float(self._current().get("wind_gusts_10m"))

    @property
    def wind_bearing(self) -> float | None:
        return _float(self._current().get("wind_direction_10m"))

    @property
    def cloud_coverage(self) -> float | None:
        return _float(self._current().get("cloud_cover"))

    @property
    def native_visibility(self) -> float | None:
        return _float(self._current().get("visibility"))

    @callback
    def _async_forecast_daily(self) -> list[Forecast] | None:
        data = self.coordinator.data
        if data is None:
            return None
        times = data.times.get("daily") or []
        daily = data.series.get("daily") or {}
        forecasts: list[Forecast] = []
        for index, stamp in enumerate(times):
            parsed = parse_api_datetime(stamp)
            forecast = Forecast(datetime=(parsed.isoformat() if parsed else stamp))
            code = _series_at(daily, "weather_code", index)
            if code is not None:
                forecast[ATTR_FORECAST_CONDITION] = WMO_TO_HA_CONDITION_MAP.get(int(code))
            _put(forecast, ATTR_FORECAST_NATIVE_TEMP, daily, "temperature_2m_max", index)
            _put(forecast, ATTR_FORECAST_NATIVE_TEMP_LOW, daily, "temperature_2m_min", index)
            _put(forecast, ATTR_FORECAST_NATIVE_APPARENT_TEMP, daily, "apparent_temperature_max", index)
            _put(forecast, ATTR_FORECAST_NATIVE_PRECIPITATION, daily, "precipitation_sum", index)
            _put(forecast, ATTR_FORECAST_NATIVE_WIND_SPEED, daily, "wind_speed_10m_max", index)
            _put(forecast, ATTR_FORECAST_NATIVE_WIND_GUST_SPEED, daily, "wind_gusts_10m_max", index)
            _put(forecast, ATTR_FORECAST_WIND_BEARING, daily, "wind_direction_10m_dominant", index)
            forecasts.append(forecast)
        return forecasts

    @callback
    def _async_forecast_hourly(self) -> list[Forecast] | None:
        data = self.coordinator.data
        if data is None:
            return None
        now = dt_util.now()
        times = data.times.get("hourly") or []
        hourly = data.series.get("hourly") or {}
        forecasts: list[Forecast] = []
        for index, stamp in enumerate(times):
            parsed = parse_api_datetime(stamp)
            if parsed is not None and parsed < now:
                continue
            forecast = Forecast(datetime=(parsed.isoformat() if parsed else stamp))
            code = _series_at(hourly, "weather_code", index)
            if code is not None:
                forecast[ATTR_FORECAST_CONDITION] = WMO_TO_HA_CONDITION_MAP.get(int(code))
            _put(forecast, ATTR_FORECAST_NATIVE_TEMP, hourly, "temperature_2m", index)
            _put(forecast, ATTR_FORECAST_NATIVE_APPARENT_TEMP, hourly, "apparent_temperature", index)
            _put(forecast, ATTR_FORECAST_NATIVE_PRECIPITATION, hourly, "precipitation", index)
            _put(forecast, ATTR_FORECAST_NATIVE_WIND_SPEED, hourly, "wind_speed_10m", index)
            _put(forecast, ATTR_FORECAST_NATIVE_WIND_GUST_SPEED, hourly, "wind_gusts_10m", index)
            _put(forecast, ATTR_FORECAST_WIND_BEARING, hourly, "wind_direction_10m", index)
            _put(forecast, ATTR_FORECAST_HUMIDITY, hourly, "relative_humidity_2m", index)
            _put(forecast, ATTR_FORECAST_CLOUD_COVERAGE, hourly, "cloud_cover", index)
            _put(forecast, ATTR_FORECAST_NATIVE_PRESSURE, hourly, "pressure_msl", index)
            forecasts.append(forecast)
        return forecasts


def _float(value) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _series_at(series: dict, key: str, index: int):
    values = series.get(key)
    if not values or index >= len(values):
        return None
    return values[index]


def _put(forecast: Forecast, attr: str, series: dict, key: str, index: int) -> None:
    value = _series_at(series, key, index)
    if value is not None:
        forecast[attr] = value
