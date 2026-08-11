"""Variable group catalogs for every Open-Meteo live API."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DEGREE,
    PERCENTAGE,
    UnitOfIrradiance,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolumeFlowRate,
)

from ..const import (
    MODULE_AIR_QUALITY,
    MODULE_ENSEMBLE,
    MODULE_FLOOD,
    MODULE_FORECAST,
    MODULE_MARINE,
    MODULE_SEASONAL,
)

try:
    from homeassistant.const import UV_INDEX
except ImportError:  # pragma: no cover - older/newer HA
    UV_INDEX = "UV index"

# Removed from SensorDeviceClass in HA 2026; keep a fallback so the catalog still imports.
_UV_DEVICE_CLASS: SensorDeviceClass | None = getattr(SensorDeviceClass, "UV_INDEX", None)

BUCKET_CURRENT = "current"
BUCKET_HOURLY = "hourly"
BUCKET_DAILY = "daily"
BUCKET_MINUTELY = "minutely_15"
BUCKET_WEEKLY = "weekly"
BUCKET_MONTHLY = "monthly"


@dataclass(frozen=True, kw_only=True)
class VariableDef:
    """One Open-Meteo variable mapped onto a Home Assistant sensor."""

    key: str
    name: str
    bucket: str
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT
    unit: str | None = None
    icon: str | None = None


def _v(
    key: str,
    name: str,
    bucket: str,
    *,
    dc: SensorDeviceClass | None = None,
    sc: SensorStateClass | None = SensorStateClass.MEASUREMENT,
    unit: str | None = None,
    icon: str | None = None,
) -> VariableDef:
    return VariableDef(
        key=key,
        name=name,
        bucket=bucket,
        device_class=dc,
        state_class=sc,
        unit=unit,
        icon=icon,
    )


def _temp(key: str, name: str, bucket: str) -> VariableDef:
    return _v(key, name, bucket, dc=SensorDeviceClass.TEMPERATURE, unit=UnitOfTemperature.CELSIUS)


def _hum(key: str, name: str, bucket: str) -> VariableDef:
    return _v(key, name, bucket, dc=SensorDeviceClass.HUMIDITY, unit=PERCENTAGE)


def _precip(key: str, name: str, bucket: str) -> VariableDef:
    return _v(
        key,
        name,
        bucket,
        dc=SensorDeviceClass.PRECIPITATION,
        unit=UnitOfPrecipitationDepth.MILLIMETERS,
    )


def _speed(key: str, name: str, bucket: str) -> VariableDef:
    return _v(key, name, bucket, dc=SensorDeviceClass.WIND_SPEED, unit=UnitOfSpeed.KILOMETERS_PER_HOUR)


def _dir(key: str, name: str, bucket: str) -> VariableDef:
    return _v(
        key,
        name,
        bucket,
        dc=SensorDeviceClass.WIND_DIRECTION,
        sc=SensorStateClass.MEASUREMENT_ANGLE,
        unit=DEGREE,
        icon="mdi:compass",
    )


def _press(key: str, name: str, bucket: str) -> VariableDef:
    return _v(key, name, bucket, dc=SensorDeviceClass.ATMOSPHERIC_PRESSURE, unit=UnitOfPressure.HPA)


def _cloud(key: str, name: str, bucket: str) -> VariableDef:
    return _v(key, name, bucket, unit=PERCENTAGE, icon="mdi:cloud")


def _rad(key: str, name: str, bucket: str) -> VariableDef:
    return _v(
        key,
        name,
        bucket,
        dc=SensorDeviceClass.IRRADIANCE,
        unit=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
    )


def _pct(key: str, name: str, bucket: str, icon: str | None = None) -> VariableDef:
    return _v(key, name, bucket, unit=PERCENTAGE, icon=icon)


def _idx(key: str, name: str, bucket: str, icon: str = "mdi:numeric") -> VariableDef:
    return _v(key, name, bucket, unit=None, icon=icon, sc=SensorStateClass.MEASUREMENT)


# --- Forecast -----------------------------------------------------------------

FORECAST_CURRENT = [
    _temp("temperature_2m", "Temperature", BUCKET_CURRENT),
    _hum("relative_humidity_2m", "Relative humidity", BUCKET_CURRENT),
    _temp("dew_point_2m", "Dew point", BUCKET_CURRENT),
    _temp("apparent_temperature", "Apparent temperature", BUCKET_CURRENT),
    _precip("precipitation", "Precipitation", BUCKET_CURRENT),
    _precip("rain", "Rain", BUCKET_CURRENT),
    _precip("showers", "Showers", BUCKET_CURRENT),
    _v("snowfall", "Snowfall", BUCKET_CURRENT, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _idx("weather_code", "Weather code", BUCKET_CURRENT, "mdi:weather-partly-cloudy"),
    _cloud("cloud_cover", "Cloud cover", BUCKET_CURRENT),
    _press("pressure_msl", "Sea level pressure", BUCKET_CURRENT),
    _press("surface_pressure", "Surface pressure", BUCKET_CURRENT),
    _speed("wind_speed_10m", "Wind speed", BUCKET_CURRENT),
    _dir("wind_direction_10m", "Wind direction", BUCKET_CURRENT),
    _speed("wind_gusts_10m", "Wind gusts", BUCKET_CURRENT),
    _v("is_day", "Is day", BUCKET_CURRENT, icon="mdi:weather-sunset", sc=None),
]

FORECAST_HOURLY_CORE = [
    _temp("temperature_2m", "Temperature", BUCKET_HOURLY),
    _hum("relative_humidity_2m", "Relative humidity", BUCKET_HOURLY),
    _temp("dew_point_2m", "Dew point", BUCKET_HOURLY),
    _temp("apparent_temperature", "Apparent temperature", BUCKET_HOURLY),
    _pct("precipitation_probability", "Precipitation probability", BUCKET_HOURLY, "mdi:water-percent"),
    _precip("precipitation", "Precipitation", BUCKET_HOURLY),
    _precip("rain", "Rain", BUCKET_HOURLY),
    _precip("showers", "Showers", BUCKET_HOURLY),
    _v("snowfall", "Snowfall", BUCKET_HOURLY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _v("snow_depth", "Snow depth", BUCKET_HOURLY, unit=UnitOfLength.METERS, icon="mdi:snowflake"),
    _idx("weather_code", "Weather code", BUCKET_HOURLY, "mdi:weather-partly-cloudy"),
    _press("pressure_msl", "Sea level pressure", BUCKET_HOURLY),
    _press("surface_pressure", "Surface pressure", BUCKET_HOURLY),
    _cloud("cloud_cover", "Cloud cover", BUCKET_HOURLY),
    _speed("wind_speed_10m", "Wind speed", BUCKET_HOURLY),
    _dir("wind_direction_10m", "Wind direction", BUCKET_HOURLY),
    _speed("wind_gusts_10m", "Wind gusts", BUCKET_HOURLY),
    _v("visibility", "Visibility", BUCKET_HOURLY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
]

FORECAST_HOURLY_EXTRA = [
    _cloud("cloud_cover_low", "Cloud cover low", BUCKET_HOURLY),
    _cloud("cloud_cover_mid", "Cloud cover mid", BUCKET_HOURLY),
    _cloud("cloud_cover_high", "Cloud cover high", BUCKET_HOURLY),
    _v("evapotranspiration", "Evapotranspiration", BUCKET_HOURLY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:water-plus"),
    _v("et0_fao_evapotranspiration", "Reference evapotranspiration", BUCKET_HOURLY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:water-plus"),
    _v("vapour_pressure_deficit", "Vapour pressure deficit", BUCKET_HOURLY, unit=UnitOfPressure.KPA, icon="mdi:gauge"),
    _speed("wind_speed_80m", "Wind speed 80 m", BUCKET_HOURLY),
    _speed("wind_speed_120m", "Wind speed 120 m", BUCKET_HOURLY),
    _speed("wind_speed_180m", "Wind speed 180 m", BUCKET_HOURLY),
    _dir("wind_direction_80m", "Wind direction 80 m", BUCKET_HOURLY),
    _dir("wind_direction_120m", "Wind direction 120 m", BUCKET_HOURLY),
    _dir("wind_direction_180m", "Wind direction 180 m", BUCKET_HOURLY),
    _temp("temperature_80m", "Temperature 80 m", BUCKET_HOURLY),
    _temp("temperature_120m", "Temperature 120 m", BUCKET_HOURLY),
    _temp("temperature_180m", "Temperature 180 m", BUCKET_HOURLY),
    _v("uv_index", "UV index", BUCKET_HOURLY, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
    _v("uv_index_clear_sky", "UV index clear sky", BUCKET_HOURLY, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
    _v("is_day", "Is day", BUCKET_HOURLY, icon="mdi:weather-sunset", sc=None),
    _v("sunshine_duration", "Sunshine duration", BUCKET_HOURLY, dc=SensorDeviceClass.DURATION, unit=UnitOfTime.SECONDS),
    _temp("wet_bulb_temperature_2m", "Wet bulb temperature", BUCKET_HOURLY),
    _v("total_column_integrated_water_vapour", "Integrated water vapour", BUCKET_HOURLY, unit="kg/m²", icon="mdi:water"),
    _v("cape", "CAPE", BUCKET_HOURLY, unit="J/kg", icon="mdi:lightning-bolt"),
    _v("lifted_index", "Lifted index", BUCKET_HOURLY, unit="K", icon="mdi:chart-line"),
    _v("convective_inhibition", "Convective inhibition", BUCKET_HOURLY, unit="J/kg", icon="mdi:lightning-bolt-outline"),
    _v("freezing_level_height", "Freezing level height", BUCKET_HOURLY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("boundary_layer_height", "Boundary layer height", BUCKET_HOURLY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
]

FORECAST_SOLAR = [
    _rad("shortwave_radiation", "Shortwave radiation GHI", BUCKET_HOURLY),
    _rad("direct_radiation", "Direct radiation", BUCKET_HOURLY),
    _rad("diffuse_radiation", "Diffuse radiation DHI", BUCKET_HOURLY),
    _rad("direct_normal_irradiance", "Direct normal irradiance", BUCKET_HOURLY),
    _rad("global_tilted_irradiance", "Global tilted irradiance", BUCKET_HOURLY),
    _rad("terrestrial_radiation", "Terrestrial radiation", BUCKET_HOURLY),
    _rad("shortwave_radiation_instant", "Shortwave radiation instant", BUCKET_HOURLY),
    _rad("direct_radiation_instant", "Direct radiation instant", BUCKET_HOURLY),
    _rad("diffuse_radiation_instant", "Diffuse radiation instant", BUCKET_HOURLY),
    _rad("direct_normal_irradiance_instant", "Direct normal irradiance instant", BUCKET_HOURLY),
    _rad("global_tilted_irradiance_instant", "Global tilted irradiance instant", BUCKET_HOURLY),
    _rad("terrestrial_radiation_instant", "Terrestrial radiation instant", BUCKET_HOURLY),
]

FORECAST_SOIL = [
    _temp("soil_temperature_0cm", "Soil temperature 0 cm", BUCKET_HOURLY),
    _temp("soil_temperature_6cm", "Soil temperature 6 cm", BUCKET_HOURLY),
    _temp("soil_temperature_18cm", "Soil temperature 18 cm", BUCKET_HOURLY),
    _temp("soil_temperature_54cm", "Soil temperature 54 cm", BUCKET_HOURLY),
    _v("soil_moisture_0_to_1cm", "Soil moisture 0-1 cm", BUCKET_HOURLY, unit="m³/m³", icon="mdi:water"),
    _v("soil_moisture_1_to_3cm", "Soil moisture 1-3 cm", BUCKET_HOURLY, unit="m³/m³", icon="mdi:water"),
    _v("soil_moisture_3_to_9cm", "Soil moisture 3-9 cm", BUCKET_HOURLY, unit="m³/m³", icon="mdi:water"),
    _v("soil_moisture_9_to_27cm", "Soil moisture 9-27 cm", BUCKET_HOURLY, unit="m³/m³", icon="mdi:water"),
    _v("soil_moisture_27_to_81cm", "Soil moisture 27-81 cm", BUCKET_HOURLY, unit="m³/m³", icon="mdi:water"),
]

FORECAST_MINUTELY = [
    _temp("temperature_2m", "Temperature 15-min", BUCKET_MINUTELY),
    _hum("relative_humidity_2m", "Relative humidity 15-min", BUCKET_MINUTELY),
    _temp("dew_point_2m", "Dew point 15-min", BUCKET_MINUTELY),
    _temp("apparent_temperature", "Apparent temperature 15-min", BUCKET_MINUTELY),
    _precip("precipitation", "Precipitation 15-min", BUCKET_MINUTELY),
    _precip("rain", "Rain 15-min", BUCKET_MINUTELY),
    _v("snowfall", "Snowfall 15-min", BUCKET_MINUTELY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _v("snowfall_height", "Snowfall height 15-min", BUCKET_MINUTELY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("freezing_level_height", "Freezing level 15-min", BUCKET_MINUTELY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("sunshine_duration", "Sunshine duration 15-min", BUCKET_MINUTELY, dc=SensorDeviceClass.DURATION, unit=UnitOfTime.SECONDS),
    _idx("weather_code", "Weather code 15-min", BUCKET_MINUTELY, "mdi:weather-partly-cloudy"),
    _speed("wind_speed_10m", "Wind speed 15-min", BUCKET_MINUTELY),
    _speed("wind_speed_80m", "Wind speed 80 m 15-min", BUCKET_MINUTELY),
    _dir("wind_direction_10m", "Wind direction 15-min", BUCKET_MINUTELY),
    _dir("wind_direction_80m", "Wind direction 80 m 15-min", BUCKET_MINUTELY),
    _speed("wind_gusts_10m", "Wind gusts 15-min", BUCKET_MINUTELY),
    _v("visibility", "Visibility 15-min", BUCKET_MINUTELY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("cape", "CAPE 15-min", BUCKET_MINUTELY, unit="J/kg", icon="mdi:lightning-bolt"),
    _v("lightning_potential", "Lightning potential", BUCKET_MINUTELY, unit="J/kg", icon="mdi:flash"),
    _v("is_day", "Is day 15-min", BUCKET_MINUTELY, icon="mdi:weather-sunset", sc=None),
    _rad("shortwave_radiation", "Shortwave radiation 15-min", BUCKET_MINUTELY),
    _rad("direct_radiation", "Direct radiation 15-min", BUCKET_MINUTELY),
    _rad("diffuse_radiation", "Diffuse radiation 15-min", BUCKET_MINUTELY),
    _rad("direct_normal_irradiance", "DNI 15-min", BUCKET_MINUTELY),
    _rad("global_tilted_irradiance", "GTI 15-min", BUCKET_MINUTELY),
    _rad("terrestrial_radiation", "Terrestrial radiation 15-min", BUCKET_MINUTELY),
    _rad("shortwave_radiation_instant", "Shortwave radiation instant 15-min", BUCKET_MINUTELY),
    _rad("direct_radiation_instant", "Direct radiation instant 15-min", BUCKET_MINUTELY),
    _rad("diffuse_radiation_instant", "Diffuse radiation instant 15-min", BUCKET_MINUTELY),
    _rad("direct_normal_irradiance_instant", "DNI instant 15-min", BUCKET_MINUTELY),
    _rad("global_tilted_irradiance_instant", "GTI instant 15-min", BUCKET_MINUTELY),
    _rad("terrestrial_radiation_instant", "Terrestrial radiation instant 15-min", BUCKET_MINUTELY),
]

FORECAST_DAILY_CORE = [
    _idx("weather_code", "Daily weather code", BUCKET_DAILY, "mdi:weather-partly-cloudy"),
    _temp("temperature_2m_max", "Maximum temperature", BUCKET_DAILY),
    _temp("temperature_2m_min", "Minimum temperature", BUCKET_DAILY),
    _temp("apparent_temperature_max", "Maximum apparent temperature", BUCKET_DAILY),
    _temp("apparent_temperature_min", "Minimum apparent temperature", BUCKET_DAILY),
    _v("uv_index_max", "UV index max", BUCKET_DAILY, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
    _v("uv_index_clear_sky_max", "UV index clear sky max", BUCKET_DAILY, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
    _v("sunrise", "Sunrise", BUCKET_DAILY, dc=SensorDeviceClass.TIMESTAMP, sc=None, icon="mdi:weather-sunset-up"),
    _v("sunset", "Sunset", BUCKET_DAILY, dc=SensorDeviceClass.TIMESTAMP, sc=None, icon="mdi:weather-sunset-down"),
    _v("daylight_duration", "Daylight duration", BUCKET_DAILY, dc=SensorDeviceClass.DURATION, unit=UnitOfTime.SECONDS),
    _v("sunshine_duration", "Sunshine duration daily", BUCKET_DAILY, dc=SensorDeviceClass.DURATION, unit=UnitOfTime.SECONDS),
    _precip("rain_sum", "Rain sum", BUCKET_DAILY),
    _precip("showers_sum", "Showers sum", BUCKET_DAILY),
    _v("snowfall_sum", "Snowfall sum", BUCKET_DAILY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _precip("precipitation_sum", "Precipitation sum", BUCKET_DAILY),
    _v("precipitation_hours", "Precipitation hours", BUCKET_DAILY, unit=UnitOfTime.HOURS, icon="mdi:weather-rainy"),
    _pct("precipitation_probability_max", "Precipitation probability max", BUCKET_DAILY, "mdi:water-percent"),
    _speed("wind_speed_10m_max", "Maximum wind speed", BUCKET_DAILY),
    _speed("wind_gusts_10m_max", "Maximum wind gusts", BUCKET_DAILY),
    _dir("wind_direction_10m_dominant", "Dominant wind direction", BUCKET_DAILY),
    _v("shortwave_radiation_sum", "Shortwave radiation sum", BUCKET_DAILY, unit="MJ/m²", icon="mdi:solar-power"),
    _v("et0_fao_evapotranspiration", "Daily ET₀", BUCKET_DAILY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:water-plus"),
]

FORECAST_DAILY_EXTRA = [
    _temp("temperature_2m_mean", "Mean temperature", BUCKET_DAILY),
    _temp("apparent_temperature_mean", "Mean apparent temperature", BUCKET_DAILY),
    _v("cape_mean", "Mean CAPE", BUCKET_DAILY, unit="J/kg", icon="mdi:lightning-bolt"),
    _v("cape_max", "Maximum CAPE", BUCKET_DAILY, unit="J/kg", icon="mdi:lightning-bolt"),
    _v("cape_min", "Minimum CAPE", BUCKET_DAILY, unit="J/kg", icon="mdi:lightning-bolt"),
    _cloud("cloud_cover_mean", "Mean cloud cover", BUCKET_DAILY),
    _cloud("cloud_cover_max", "Maximum cloud cover", BUCKET_DAILY),
    _cloud("cloud_cover_min", "Minimum cloud cover", BUCKET_DAILY),
    _temp("dew_point_2m_mean", "Mean dew point", BUCKET_DAILY),
    _temp("dew_point_2m_max", "Maximum dew point", BUCKET_DAILY),
    _temp("dew_point_2m_min", "Minimum dew point", BUCKET_DAILY),
    _v("growing_degree_days_base_0_limit_50", "Growing degree days", BUCKET_DAILY, unit="K", icon="mdi:sprout"),
    _pct("leaf_wetness_probability_mean", "Mean leaf wetness probability", BUCKET_DAILY, "mdi:leaf"),
    _pct("precipitation_probability_mean", "Mean precipitation probability", BUCKET_DAILY, "mdi:water-percent"),
    _pct("precipitation_probability_min", "Minimum precipitation probability", BUCKET_DAILY, "mdi:water-percent"),
    _hum("relative_humidity_2m_mean", "Mean relative humidity", BUCKET_DAILY),
    _hum("relative_humidity_2m_max", "Maximum relative humidity", BUCKET_DAILY),
    _hum("relative_humidity_2m_min", "Minimum relative humidity", BUCKET_DAILY),
    _v("snowfall_water_equivalent_sum", "Snowfall water equivalent", BUCKET_DAILY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:snowflake"),
    _press("pressure_msl_mean", "Mean sea level pressure", BUCKET_DAILY),
    _press("pressure_msl_max", "Maximum sea level pressure", BUCKET_DAILY),
    _press("pressure_msl_min", "Minimum sea level pressure", BUCKET_DAILY),
    _press("surface_pressure_mean", "Mean surface pressure", BUCKET_DAILY),
    _press("surface_pressure_max", "Maximum surface pressure", BUCKET_DAILY),
    _press("surface_pressure_min", "Minimum surface pressure", BUCKET_DAILY),
    _v("updraft_max", "Maximum updraft", BUCKET_DAILY, unit=UnitOfSpeed.METERS_PER_SECOND, icon="mdi:arrow-up-bold"),
    _v("visibility_mean", "Mean visibility", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("visibility_min", "Minimum visibility", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _v("visibility_max", "Maximum visibility", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _speed("wind_gusts_10m_mean", "Mean wind gusts", BUCKET_DAILY),
    _speed("wind_speed_10m_mean", "Mean wind speed", BUCKET_DAILY),
    _speed("wind_gusts_10m_min", "Minimum wind gusts", BUCKET_DAILY),
    _speed("wind_speed_10m_min", "Minimum wind speed", BUCKET_DAILY),
    _temp("wet_bulb_temperature_2m_mean", "Mean wet bulb temperature", BUCKET_DAILY),
    _temp("wet_bulb_temperature_2m_max", "Maximum wet bulb temperature", BUCKET_DAILY),
    _temp("wet_bulb_temperature_2m_min", "Minimum wet bulb temperature", BUCKET_DAILY),
    _v("vapour_pressure_deficit_max", "Maximum vapour pressure deficit", BUCKET_DAILY, unit=UnitOfPressure.KPA, icon="mdi:gauge"),
    _v("moonrise", "Moonrise", BUCKET_DAILY, dc=SensorDeviceClass.TIMESTAMP, sc=None, icon="mdi:moon-waning-crescent"),
    _v("moonset", "Moonset", BUCKET_DAILY, dc=SensorDeviceClass.TIMESTAMP, sc=None, icon="mdi:moon-waning-crescent"),
    _idx("moon_phase", "Moon phase", BUCKET_DAILY, "mdi:moon-waning-crescent"),
]

PRESSURE_KINDS: tuple[tuple[str, str, SensorDeviceClass | None, str | None], ...] = (
    ("temperature", "Temperature", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ("relative_humidity", "Relative humidity", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ("cloud_cover", "Cloud cover", None, PERCENTAGE),
    ("wind_speed", "Wind speed", SensorDeviceClass.WIND_SPEED, UnitOfSpeed.KILOMETERS_PER_HOUR),
    ("wind_direction", "Wind direction", SensorDeviceClass.WIND_DIRECTION, DEGREE),
    ("geopotential_height", "Geopotential height", SensorDeviceClass.DISTANCE, UnitOfLength.METERS),
)


def pressure_level_variables(levels: list[str]) -> list[VariableDef]:
    """Expand pressure-level variables for the selected hPa levels."""
    variables: list[VariableDef] = []
    for level in levels:
        for kind, label, device_class, unit in PRESSURE_KINDS:
            state_class = SensorStateClass.MEASUREMENT
            icon = None
            if kind == "wind_direction":
                state_class = SensorStateClass.MEASUREMENT_ANGLE
                icon = "mdi:compass"
            elif kind == "cloud_cover":
                icon = "mdi:cloud"
            variables.append(
                _v(
                    f"{kind}_{level}hPa",
                    f"{label} {level} hPa",
                    BUCKET_HOURLY,
                    dc=device_class,
                    sc=state_class,
                    unit=unit,
                    icon=icon,
                )
            )
    return variables


# --- Air quality --------------------------------------------------------------

_UG = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

AQ_POLLUTANTS = [
    _v("pm10", "PM10", BUCKET_CURRENT, dc=SensorDeviceClass.PM10, unit=_UG),
    _v("pm2_5", "PM2.5", BUCKET_CURRENT, dc=SensorDeviceClass.PM25, unit=_UG),
    _v("carbon_monoxide", "Carbon monoxide", BUCKET_CURRENT, dc=SensorDeviceClass.CO, unit=_UG),
    _v("carbon_dioxide", "Carbon dioxide", BUCKET_CURRENT, dc=SensorDeviceClass.CO2, unit=CONCENTRATION_PARTS_PER_MILLION),
    _v("nitrogen_dioxide", "Nitrogen dioxide", BUCKET_CURRENT, dc=SensorDeviceClass.NITROGEN_DIOXIDE, unit=_UG),
    _v("sulphur_dioxide", "Sulphur dioxide", BUCKET_CURRENT, dc=SensorDeviceClass.SULPHUR_DIOXIDE, unit=_UG),
    _v("ozone", "Ozone", BUCKET_CURRENT, dc=SensorDeviceClass.OZONE, unit=_UG),
    _v("dust", "Dust", BUCKET_CURRENT, unit=_UG, icon="mdi:weather-dust"),
    _v("ammonia", "Ammonia", BUCKET_CURRENT, unit=_UG, icon="mdi:chemical-weapon"),
    _v("methane", "Methane", BUCKET_CURRENT, unit=_UG, icon="mdi:molecule"),
]

AQ_AQI = [
    _v("european_aqi", "European AQI", BUCKET_CURRENT, dc=SensorDeviceClass.AQI, icon="mdi:air-filter"),
    _v("european_aqi_pm2_5", "European AQI PM2.5", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("european_aqi_pm10", "European AQI PM10", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("european_aqi_nitrogen_dioxide", "European AQI NO₂", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("european_aqi_ozone", "European AQI ozone", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("european_aqi_sulphur_dioxide", "European AQI SO₂", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi", "US AQI", BUCKET_CURRENT, dc=SensorDeviceClass.AQI, icon="mdi:air-filter"),
    _v("us_aqi_pm2_5", "US AQI PM2.5", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi_pm10", "US AQI PM10", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi_nitrogen_dioxide", "US AQI NO₂", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi_ozone", "US AQI ozone", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi_sulphur_dioxide", "US AQI SO₂", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
    _v("us_aqi_carbon_monoxide", "US AQI CO", BUCKET_CURRENT, dc=SensorDeviceClass.AQI),
]

AQ_POLLEN = [
    _v("alder_pollen", "Alder pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:tree"),
    _v("birch_pollen", "Birch pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:tree"),
    _v("grass_pollen", "Grass pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:grass"),
    _v("mugwort_pollen", "Mugwort pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:flower-pollen"),
    _v("olive_pollen", "Olive pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:tree"),
    _v("ragweed_pollen", "Ragweed pollen", BUCKET_CURRENT, unit="grains/m³", icon="mdi:flower-pollen"),
]

AQ_EXTRA = [
    _v("aerosol_optical_depth", "Aerosol optical depth", BUCKET_CURRENT, icon="mdi:blur"),
    _v("uv_index", "UV index", BUCKET_CURRENT, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
    _v("uv_index_clear_sky", "UV index clear sky", BUCKET_CURRENT, dc=_UV_DEVICE_CLASS, unit=UV_INDEX),
]

AQ_HOURLY = [
    _v("pm10", "PM10 hourly", BUCKET_HOURLY, dc=SensorDeviceClass.PM10, unit=_UG),
    _v("pm2_5", "PM2.5 hourly", BUCKET_HOURLY, dc=SensorDeviceClass.PM25, unit=_UG),
    _v("carbon_monoxide", "Carbon monoxide hourly", BUCKET_HOURLY, dc=SensorDeviceClass.CO, unit=_UG),
    _v("nitrogen_dioxide", "Nitrogen dioxide hourly", BUCKET_HOURLY, dc=SensorDeviceClass.NITROGEN_DIOXIDE, unit=_UG),
    _v("ozone", "Ozone hourly", BUCKET_HOURLY, dc=SensorDeviceClass.OZONE, unit=_UG),
    _v("european_aqi", "European AQI hourly", BUCKET_HOURLY, dc=SensorDeviceClass.AQI),
    _v("us_aqi", "US AQI hourly", BUCKET_HOURLY, dc=SensorDeviceClass.AQI),
]


# --- Marine -------------------------------------------------------------------

MARINE_WAVES = [
    _v("wave_height", "Wave height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("wave_direction", "Wave direction", BUCKET_CURRENT),
    _v("wave_period", "Wave period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("wave_peak_period", "Wave peak period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("wind_wave_height", "Wind wave height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("wind_wave_direction", "Wind wave direction", BUCKET_CURRENT),
    _v("wind_wave_period", "Wind wave period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("wind_wave_peak_period", "Wind wave peak period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
]

MARINE_SWELL = [
    _v("swell_wave_height", "Swell wave height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("swell_wave_direction", "Swell wave direction", BUCKET_CURRENT),
    _v("swell_wave_period", "Swell wave period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("swell_wave_peak_period", "Swell wave peak period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("secondary_swell_wave_height", "Secondary swell height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _v("secondary_swell_wave_period", "Secondary swell period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _dir("secondary_swell_wave_direction", "Secondary swell direction", BUCKET_CURRENT),
    _v("tertiary_swell_wave_height", "Tertiary swell height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _v("tertiary_swell_wave_period", "Tertiary swell period", BUCKET_CURRENT, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _dir("tertiary_swell_wave_direction", "Tertiary swell direction", BUCKET_CURRENT),
]

MARINE_CURRENTS = [
    _v("ocean_current_velocity", "Ocean current velocity", BUCKET_CURRENT, dc=SensorDeviceClass.SPEED, unit=UnitOfSpeed.KILOMETERS_PER_HOUR, icon="mdi:current-ac"),
    _dir("ocean_current_direction", "Ocean current direction", BUCKET_CURRENT),
    _v("sea_level_height_msl", "Sea level height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves-arrow-up"),
    _v("invert_barometer_height", "Inverted barometer height", BUCKET_CURRENT, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
]

MARINE_SST = [
    _temp("sea_surface_temperature", "Sea surface temperature", BUCKET_CURRENT),
]

MARINE_DAILY = [
    _v("wave_height_max", "Maximum wave height", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("wave_direction_dominant", "Dominant wave direction", BUCKET_DAILY),
    _v("wave_period_max", "Maximum wave period", BUCKET_DAILY, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("wind_wave_height_max", "Maximum wind wave height", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("wind_wave_direction_dominant", "Dominant wind wave direction", BUCKET_DAILY),
    _v("wind_wave_period_max", "Maximum wind wave period", BUCKET_DAILY, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("wind_wave_peak_period_max", "Maximum wind wave peak period", BUCKET_DAILY, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("swell_wave_height_max", "Maximum swell height", BUCKET_DAILY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS, icon="mdi:waves"),
    _dir("swell_wave_direction_dominant", "Dominant swell direction", BUCKET_DAILY),
    _v("swell_wave_period_max", "Maximum swell period", BUCKET_DAILY, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
    _v("swell_wave_peak_period_max", "Maximum swell peak period", BUCKET_DAILY, unit=UnitOfTime.SECONDS, icon="mdi:waves"),
]


# --- Flood --------------------------------------------------------------------

FLOOD_DISCHARGE = [
    _v("river_discharge", "River discharge", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_mean", "River discharge mean", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_median", "River discharge median", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_max", "River discharge max", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_min", "River discharge min", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_p25", "River discharge p25", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
    _v("river_discharge_p75", "River discharge p75", BUCKET_DAILY, dc=SensorDeviceClass.VOLUME_FLOW_RATE, unit=UnitOfVolumeFlowRate.CUBIC_METERS_PER_SECOND, icon="mdi:waves"),
]


# --- Ensemble -----------------------------------------------------------------

ENSEMBLE_HOURLY = [
    _temp("temperature_2m", "Ensemble temperature", BUCKET_HOURLY),
    _hum("relative_humidity_2m", "Ensemble relative humidity", BUCKET_HOURLY),
    _temp("dew_point_2m", "Ensemble dew point", BUCKET_HOURLY),
    _temp("apparent_temperature", "Ensemble apparent temperature", BUCKET_HOURLY),
    _precip("precipitation", "Ensemble precipitation", BUCKET_HOURLY),
    _precip("rain", "Ensemble rain", BUCKET_HOURLY),
    _v("snowfall", "Ensemble snowfall", BUCKET_HOURLY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _v("snow_depth", "Ensemble snow depth", BUCKET_HOURLY, unit=UnitOfLength.METERS, icon="mdi:snowflake"),
    _idx("weather_code", "Ensemble weather code", BUCKET_HOURLY, "mdi:weather-partly-cloudy"),
    _press("pressure_msl", "Ensemble sea level pressure", BUCKET_HOURLY),
    _press("surface_pressure", "Ensemble surface pressure", BUCKET_HOURLY),
    _cloud("cloud_cover", "Ensemble cloud cover", BUCKET_HOURLY),
    _speed("wind_speed_10m", "Ensemble wind speed", BUCKET_HOURLY),
    _dir("wind_direction_10m", "Ensemble wind direction", BUCKET_HOURLY),
    _speed("wind_gusts_10m", "Ensemble wind gusts", BUCKET_HOURLY),
    _v("visibility", "Ensemble visibility", BUCKET_HOURLY, dc=SensorDeviceClass.DISTANCE, unit=UnitOfLength.METERS),
    _rad("shortwave_radiation", "Ensemble shortwave radiation", BUCKET_HOURLY),
]

ENSEMBLE_DAILY = [
    _temp("temperature_2m_max", "Ensemble max temperature", BUCKET_DAILY),
    _temp("temperature_2m_min", "Ensemble min temperature", BUCKET_DAILY),
    _precip("precipitation_sum", "Ensemble precipitation sum", BUCKET_DAILY),
    _speed("wind_speed_10m_max", "Ensemble max wind speed", BUCKET_DAILY),
    _idx("weather_code", "Ensemble daily weather code", BUCKET_DAILY, "mdi:weather-partly-cloudy"),
]


# --- Seasonal -----------------------------------------------------------------

SEASONAL_HOURLY = [
    _temp("temperature_2m", "Seasonal temperature", BUCKET_HOURLY),
    _temp("temperature_2m_max", "Seasonal 6h max temperature", BUCKET_HOURLY),
    _temp("temperature_2m_min", "Seasonal 6h min temperature", BUCKET_HOURLY),
    _temp("dew_point_2m", "Seasonal dew point", BUCKET_HOURLY),
    _hum("relative_humidity_2m", "Seasonal relative humidity", BUCKET_HOURLY),
    _temp("apparent_temperature", "Seasonal apparent temperature", BUCKET_HOURLY),
    _press("pressure_msl", "Seasonal sea level pressure", BUCKET_HOURLY),
    _idx("weather_code", "Seasonal weather code", BUCKET_HOURLY, "mdi:weather-partly-cloudy"),
    _precip("precipitation", "Seasonal precipitation", BUCKET_HOURLY),
    _precip("rain", "Seasonal rain", BUCKET_HOURLY),
    _v("snowfall", "Seasonal snowfall", BUCKET_HOURLY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _cloud("cloud_cover", "Seasonal cloud cover", BUCKET_HOURLY),
    _speed("wind_speed_10m", "Seasonal wind speed", BUCKET_HOURLY),
    _dir("wind_direction_10m", "Seasonal wind direction", BUCKET_HOURLY),
    _temp("sea_surface_temperature", "Seasonal sea surface temperature", BUCKET_HOURLY),
]

SEASONAL_DAILY = [
    _temp("temperature_2m_mean", "Seasonal mean temperature", BUCKET_DAILY),
    _temp("temperature_2m_max", "Seasonal max temperature", BUCKET_DAILY),
    _temp("temperature_2m_min", "Seasonal min temperature", BUCKET_DAILY),
    _precip("precipitation_sum", "Seasonal precipitation sum", BUCKET_DAILY),
    _precip("rain_sum", "Seasonal rain sum", BUCKET_DAILY),
    _v("snowfall_sum", "Seasonal snowfall sum", BUCKET_DAILY, unit=UnitOfLength.CENTIMETERS, icon="mdi:snowflake"),
    _cloud("cloud_cover_mean", "Seasonal mean cloud cover", BUCKET_DAILY),
    _speed("wind_speed_10m_mean", "Seasonal mean wind speed", BUCKET_DAILY),
    _idx("weather_code", "Seasonal daily weather code", BUCKET_DAILY, "mdi:weather-partly-cloudy"),
]

SEASONAL_WEEKLY = [
    _temp("temperature_2m_mean", "Weekly mean temperature", BUCKET_WEEKLY),
    _v("temperature_2m_anomaly", "Weekly temperature anomaly", BUCKET_WEEKLY, dc=SensorDeviceClass.TEMPERATURE, unit=UnitOfTemperature.CELSIUS),
    _precip("precipitation_mean", "Weekly mean precipitation", BUCKET_WEEKLY),
    _v("precipitation_anomaly", "Weekly precipitation anomaly", BUCKET_WEEKLY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:weather-rainy"),
    _press("pressure_msl_mean", "Weekly mean pressure", BUCKET_WEEKLY),
    _cloud("cloud_cover_mean", "Weekly mean cloud cover", BUCKET_WEEKLY),
]

SEASONAL_MONTHLY = [
    _temp("temperature_2m_mean", "Monthly mean temperature", BUCKET_MONTHLY),
    _v("temperature_2m_anomaly", "Monthly temperature anomaly", BUCKET_MONTHLY, dc=SensorDeviceClass.TEMPERATURE, unit=UnitOfTemperature.CELSIUS),
    _precip("precipitation_mean", "Monthly mean precipitation", BUCKET_MONTHLY),
    _v("precipitation_anomaly", "Monthly precipitation anomaly", BUCKET_MONTHLY, unit=UnitOfPrecipitationDepth.MILLIMETERS, icon="mdi:weather-rainy"),
    _cloud("cloud_cover_mean", "Monthly mean cloud cover", BUCKET_MONTHLY),
    _speed("wind_speed_10m_mean", "Monthly mean wind speed", BUCKET_MONTHLY),
]


MODULE_GROUPS: dict[str, dict[str, list[VariableDef]]] = {
    MODULE_FORECAST: {
        "current": FORECAST_CURRENT,
        "hourly_core": FORECAST_HOURLY_CORE,
        "hourly_extra": FORECAST_HOURLY_EXTRA,
        "minutely_15": FORECAST_MINUTELY,
        "daily_core": FORECAST_DAILY_CORE,
        "daily_extra": FORECAST_DAILY_EXTRA,
        "solar": FORECAST_SOLAR,
        "soil": FORECAST_SOIL,
        "pressure_levels": [],  # expanded dynamically
    },
    MODULE_AIR_QUALITY: {
        "pollutants": AQ_POLLUTANTS,
        "aqi": AQ_AQI,
        "pollen": AQ_POLLEN,
        "extra": AQ_EXTRA,
        "hourly": AQ_HOURLY,
    },
    MODULE_MARINE: {
        "waves": MARINE_WAVES,
        "swell": MARINE_SWELL,
        "currents": MARINE_CURRENTS,
        "sst": MARINE_SST,
        "daily": MARINE_DAILY,
    },
    MODULE_FLOOD: {
        "discharge": FLOOD_DISCHARGE,
    },
    MODULE_ENSEMBLE: {
        "hourly_core": ENSEMBLE_HOURLY,
        "daily_core": ENSEMBLE_DAILY,
    },
    MODULE_SEASONAL: {
        "hourly_core": SEASONAL_HOURLY,
        "daily": SEASONAL_DAILY,
        "weekly": SEASONAL_WEEKLY,
        "monthly": SEASONAL_MONTHLY,
    },
}

def expand_variables(
    module: str,
    group_ids: list[str],
    pressure_levels: list[str] | None = None,
) -> list[VariableDef]:
    """Return variable defs for the selected groups, expanding pressure levels."""
    catalog = MODULE_GROUPS.get(module, {})
    selected: list[VariableDef] = []
    seen: set[tuple[str, str]] = set()
    for group_id in group_ids:
        variables = catalog.get(group_id, [])
        if group_id == "pressure_levels":
            variables = pressure_level_variables(pressure_levels or [])
        for variable in variables:
            marker = (variable.bucket, variable.key)
            if marker in seen:
                continue
            seen.add(marker)
            selected.append(variable)
    return selected
