"""Constants for the Open-Meteo Full integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Final

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SUNNY,
)

DOMAIN: Final = "ha_open_meteo"
LOGGER = logging.getLogger(__package__)

DEFAULT_NAME: Final = "Open-Meteo"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=30)
DEFAULT_FORECAST_DAYS: Final = 7
DEFAULT_UPDATE_INTERVAL_MINUTES: Final = 30

# API hosts
FORECAST_URL: Final = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL: Final = "https://air-quality-api.open-meteo.com/v1/air-quality"
MARINE_URL: Final = "https://marine-api.open-meteo.com/v1/marine"
FLOOD_URL: Final = "https://flood-api.open-meteo.com/v1/flood"
ENSEMBLE_URL: Final = "https://ensemble-api.open-meteo.com/v1/ensemble"
SEASONAL_URL: Final = "https://seasonal-api.open-meteo.com/v1/seasonal"
ARCHIVE_URL: Final = "https://archive-api.open-meteo.com/v1/archive"
CLIMATE_URL: Final = "https://climate-api.open-meteo.com/v1/climate"
ELEVATION_URL: Final = "https://api.open-meteo.com/v1/elevation"
GEOCODING_URL: Final = "https://geocoding-api.open-meteo.com/v1/search"

# Modules
MODULE_FORECAST: Final = "forecast"
MODULE_AIR_QUALITY: Final = "air_quality"
MODULE_MARINE: Final = "marine"
MODULE_FLOOD: Final = "flood"
MODULE_ENSEMBLE: Final = "ensemble"
MODULE_SEASONAL: Final = "seasonal"
MODULE_ELEVATION: Final = "elevation"
MODULE_HISTORICAL: Final = "historical"
MODULE_CLIMATE: Final = "climate"

LIVE_MODULES: Final = (
    MODULE_FORECAST,
    MODULE_AIR_QUALITY,
    MODULE_MARINE,
    MODULE_FLOOD,
    MODULE_ENSEMBLE,
    MODULE_SEASONAL,
    MODULE_ELEVATION,
)

SERVICE_MODULES: Final = (MODULE_HISTORICAL, MODULE_CLIMATE)

ALL_MODULES: Final = LIVE_MODULES + SERVICE_MODULES

DEFAULT_MODULES: Final = [MODULE_FORECAST, MODULE_AIR_QUALITY]

# Config / options keys
CONF_MODULES: Final = "modules"
CONF_GROUPS: Final = "groups"
CONF_MODELS: Final = "models"
CONF_FORECAST_DAYS: Final = "forecast_days"
CONF_UPDATE_INTERVAL: Final = "update_interval"
CONF_TEMPERATURE_UNIT: Final = "temperature_unit"
CONF_WIND_SPEED_UNIT: Final = "wind_speed_unit"
CONF_PRECIPITATION_UNIT: Final = "precipitation_unit"
CONF_PRESSURE_LEVELS: Final = "pressure_levels"
CONF_TILT: Final = "tilt"
CONF_AZIMUTH: Final = "azimuth"
CONF_LOCATION_MODE: Final = "location_mode"
CONF_SEARCH: Final = "search"
CONF_PLACE: Final = "place"

LOCATION_MODE_COORDINATES: Final = "coordinates"
LOCATION_MODE_SEARCH: Final = "search"

TEMP_UNIT_CELSIUS: Final = "celsius"
TEMP_UNIT_FAHRENHEIT: Final = "fahrenheit"
WIND_UNIT_KMH: Final = "kmh"
WIND_UNIT_MS: Final = "ms"
WIND_UNIT_MPH: Final = "mph"
WIND_UNIT_KN: Final = "kn"
PRECIP_UNIT_MM: Final = "mm"
PRECIP_UNIT_INCH: Final = "inch"

DEFAULT_TEMPERATURE_UNIT: Final = TEMP_UNIT_CELSIUS
DEFAULT_WIND_SPEED_UNIT: Final = WIND_UNIT_KMH
DEFAULT_PRECIPITATION_UNIT: Final = PRECIP_UNIT_MM

DEFAULT_PRESSURE_LEVELS: Final = ["850", "700", "500"]
PRESSURE_LEVEL_CHOICES: Final = [
    "1000",
    "975",
    "950",
    "925",
    "900",
    "850",
    "800",
    "700",
    "600",
    "500",
    "400",
    "300",
    "250",
    "200",
    "150",
    "100",
    "70",
    "50",
    "30",
]

DEFAULT_MODELS: Final = ["best_match"]

FORECAST_MODEL_CHOICES: Final = [
    "best_match",
    "ecmwf_ifs",
    "ecmwf_ifs025",
    "ecmwf_aifs025",
    "cma_grapes_global",
    "bom_access_global",
    "gfs_seamless",
    "gfs_global",
    "gfs_hrrr",
    "ncep_nbm_conus",
    "nam_conus",
    "jma_seamless",
    "jma_msm",
    "jma_gsm",
    "kma_seamless",
    "icon_seamless",
    "icon_global",
    "icon_eu",
    "icon_d2",
    "gem_seamless",
    "gem_global",
    "gem_regional",
    "gem_hrdps_continental",
    "meteofrance_seamless",
    "meteofrance_arpege_world",
    "meteofrance_arpege_europe",
    "meteofrance_arome_france",
    "meteofrance_arome_france_hd",
    "metno_nordic",
    "knmi_seamless",
    "dmi_seamless",
    "ukmo_seamless",
    "ukmo_global_deterministic_10km",
    "ukmo_uk_deterministic_2km",
    "meteoswiss_icon_seamless",
]

ENSEMBLE_MODEL_CHOICES: Final = [
    "icon_seamless",
    "gfs_seamless",
    "ecmwf_ifs025",
    "ecmwf_aifs025",
    "ukmo_global_ensemble_20km",
    "gem_global",
]

CLIMATE_MODEL_CHOICES: Final = [
    "CMCC_CM2_VHR4",
    "FGOALS_f3_H",
    "HiRAM_SIT_HR",
    "MRI_AGCM3_2_S",
    "EC_Earth3P_HR",
    "MPI_ESM1_2_XR",
    "NICAM16_8S",
]

DEFAULT_CLIMATE_MODELS: Final = ["MRI_AGCM3_2_S"]

# Services
SERVICE_GET_HISTORICAL: Final = "get_historical_weather"
SERVICE_GET_CLIMATE: Final = "get_climate_projection"

# Weather entity always requests these so the weather card works
WEATHER_CURRENT_VARS: Final = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "dew_point_2m",
    "is_day",
    "precipitation",
    "rain",
    "showers",
    "snowfall",
    "weather_code",
    "cloud_cover",
    "pressure_msl",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    "visibility",
]
WEATHER_HOURLY_VARS: Final = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "dew_point_2m",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "pressure_msl",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
]
WEATHER_DAILY_VARS: Final = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "precipitation_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    "sunrise",
    "sunset",
    "uv_index_max",
]

WMO_TO_HA_CONDITION_MAP = {
    0: ATTR_CONDITION_SUNNY,
    1: ATTR_CONDITION_SUNNY,
    2: ATTR_CONDITION_PARTLYCLOUDY,
    3: ATTR_CONDITION_CLOUDY,
    45: ATTR_CONDITION_FOG,
    48: ATTR_CONDITION_FOG,
    51: ATTR_CONDITION_RAINY,
    53: ATTR_CONDITION_RAINY,
    55: ATTR_CONDITION_RAINY,
    56: ATTR_CONDITION_RAINY,
    57: ATTR_CONDITION_RAINY,
    61: ATTR_CONDITION_RAINY,
    63: ATTR_CONDITION_RAINY,
    65: ATTR_CONDITION_POURING,
    66: ATTR_CONDITION_RAINY,
    67: ATTR_CONDITION_POURING,
    71: ATTR_CONDITION_SNOWY,
    73: ATTR_CONDITION_SNOWY,
    75: ATTR_CONDITION_SNOWY,
    77: ATTR_CONDITION_SNOWY,
    80: ATTR_CONDITION_RAINY,
    81: ATTR_CONDITION_RAINY,
    82: ATTR_CONDITION_POURING,
    85: ATTR_CONDITION_SNOWY,
    86: ATTR_CONDITION_SNOWY,
    95: ATTR_CONDITION_LIGHTNING,
    96: ATTR_CONDITION_LIGHTNING,
    99: ATTR_CONDITION_LIGHTNING,
}

CLEAR_NIGHT = ATTR_CONDITION_CLEAR_NIGHT
