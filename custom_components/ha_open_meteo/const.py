"""Constants for the Open-Meteo Full integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Final

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

# Keep these as literals so const.py never imports homeassistant.components.weather
# (that circular import makes custom config flows fail with "Invalid handler specified").
WMO_TO_HA_CONDITION_MAP = {
    0: "sunny",
    1: "sunny",
    2: "partlycloudy",
    3: "cloudy",
    45: "fog",
    48: "fog",
    51: "rainy",
    53: "rainy",
    55: "rainy",
    56: "rainy",
    57: "rainy",
    61: "rainy",
    63: "rainy",
    65: "pouring",
    66: "rainy",
    67: "pouring",
    71: "snowy",
    73: "snowy",
    75: "snowy",
    77: "snowy",
    80: "rainy",
    81: "rainy",
    82: "pouring",
    85: "snowy",
    86: "snowy",
    95: "lightning",
    96: "lightning",
    99: "lightning",
}

CLEAR_NIGHT = "clear-night"

GROUP_LABELS: Final[dict[str, str]] = {
    "current": "Current conditions",
    "hourly_core": "Hourly (core)",
    "hourly_extra": "Hourly (additional)",
    "minutely_15": "15-minutely",
    "daily_core": "Daily (core)",
    "daily_extra": "Daily (additional)",
    "solar": "Solar radiation",
    "soil": "Soil",
    "pressure_levels": "Pressure levels",
    "pollutants": "Pollutants",
    "aqi": "Air quality index",
    "pollen": "Pollen",
    "extra": "Additional air quality",
    "hourly": "Hourly",
    "waves": "Waves",
    "swell": "Swell",
    "currents": "Currents and sea level",
    "sst": "Sea surface temperature",
    "daily": "Daily",
    "discharge": "River discharge",
    "weekly": "Weekly",
    "monthly": "Monthly",
}

MODULE_GROUP_IDS: Final[dict[str, tuple[str, ...]]] = {
    MODULE_FORECAST: (
        "current",
        "hourly_core",
        "hourly_extra",
        "minutely_15",
        "daily_core",
        "daily_extra",
        "solar",
        "soil",
        "pressure_levels",
    ),
    MODULE_AIR_QUALITY: ("pollutants", "aqi", "pollen", "extra", "hourly"),
    MODULE_MARINE: ("waves", "swell", "currents", "sst", "daily"),
    MODULE_FLOOD: ("discharge",),
    MODULE_ENSEMBLE: ("hourly_core", "daily_core"),
    MODULE_SEASONAL: ("hourly_core", "daily", "weekly", "monthly"),
}

DEFAULT_GROUPS: Final[dict[str, list[str]]] = {
    MODULE_FORECAST: ["current", "hourly_core", "daily_core"],
    MODULE_AIR_QUALITY: ["pollutants", "aqi"],
    MODULE_MARINE: ["waves", "sst"],
    MODULE_FLOOD: ["discharge"],
    MODULE_ENSEMBLE: ["hourly_core"],
    MODULE_SEASONAL: ["daily"],
}


def group_options(module: str) -> list[tuple[str, str]]:
    """Return (value, label) pairs for a module's groups."""
    return [
        (group_id, GROUP_LABELS.get(group_id, group_id))
        for group_id in MODULE_GROUP_IDS.get(module, ())
    ]
