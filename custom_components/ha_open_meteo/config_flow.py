"""Config and options flows for Open-Meteo Full."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

try:
    from homeassistant.config_entries import OptionsFlowWithReload
except ImportError:  # HA < 2024.11
    from homeassistant.config_entries import OptionsFlow as OptionsFlowWithReload
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    LocationSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from .api import OpenMeteoApiError, OpenMeteoClient
from .api.endpoints import geocoding_request
from .const import (
    ALL_MODULES,
    CONF_AZIMUTH,
    CONF_FORECAST_DAYS,
    CONF_GROUPS,
    CONF_LOCATION_MODE,
    CONF_MODELS,
    CONF_MODULES,
    CONF_PLACE,
    CONF_PRECIPITATION_UNIT,
    CONF_PRESSURE_LEVELS,
    CONF_SEARCH,
    CONF_TEMPERATURE_UNIT,
    CONF_TILT,
    CONF_UPDATE_INTERVAL,
    CONF_WIND_SPEED_UNIT,
    DEFAULT_FORECAST_DAYS,
    DEFAULT_GROUPS,
    DEFAULT_MODELS,
    DEFAULT_MODULES,
    DEFAULT_NAME,
    DEFAULT_PRECIPITATION_UNIT,
    DEFAULT_PRESSURE_LEVELS,
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DEFAULT_WIND_SPEED_UNIT,
    DOMAIN,
    FORECAST_MODEL_CHOICES,
    LIVE_MODULES,
    LOCATION_MODE_COORDINATES,
    LOCATION_MODE_SEARCH,
    MODULE_FORECAST,
    PRECIP_UNIT_INCH,
    PRECIP_UNIT_MM,
    PRESSURE_LEVEL_CHOICES,
    TEMP_UNIT_CELSIUS,
    TEMP_UNIT_FAHRENHEIT,
    WIND_UNIT_KMH,
    WIND_UNIT_KN,
    WIND_UNIT_MPH,
    WIND_UNIT_MS,
    group_options,
)
from .helpers import location_unique_id

MODULE_LABELS = {
    "forecast": "Weather Forecast",
    "air_quality": "Air Quality",
    "marine": "Marine",
    "flood": "Flood",
    "ensemble": "Ensemble",
    "seasonal": "Seasonal Forecast",
    "elevation": "Elevation",
    "historical": "Historical Weather (service)",
    "climate": "Climate Projections (service)",
}


class HaOpenMeteoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle adding a location."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._options: dict[str, Any] = {}
        self._results: list[dict[str, Any]] = []

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> HaOpenMeteoOptionsFlow:
        return HaOpenMeteoOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Name and how to pick coordinates."""
        if user_input is not None:
            self._data[CONF_NAME] = user_input[CONF_NAME]
            if user_input[CONF_LOCATION_MODE] == LOCATION_MODE_SEARCH:
                return await self.async_step_search()
            return await self.async_step_coordinates()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=DEFAULT_NAME): TextSelector(),
                    vol.Required(
                        CONF_LOCATION_MODE, default=LOCATION_MODE_COORDINATES
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=LOCATION_MODE_COORDINATES, label="Coordinates"),
                                SelectOptionDict(value=LOCATION_MODE_SEARCH, label="Search place name"),
                            ],
                            mode=SelectSelectorMode.LIST,
                        )
                    ),
                }
            ),
        )

    async def async_step_coordinates(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect latitude and longitude."""
        if user_input is not None:
            location = user_input["location"]
            return await self._async_store_location(
                float(location[CONF_LATITUDE]),
                float(location[CONF_LONGITUDE]),
            )

        return self.async_show_form(
            step_id="coordinates",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "location",
                        default={
                            CONF_LATITUDE: self.hass.config.latitude,
                            CONF_LONGITUDE: self.hass.config.longitude,
                        },
                    ): LocationSelector(),
                }
            ),
        )

    async def async_step_search(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Search Open-Meteo geocoding."""
        errors: dict[str, str] = {}
        if user_input is not None:
            client = OpenMeteoClient(async_get_clientsession(self.hass))
            url, params = geocoding_request(user_input[CONF_SEARCH])
            try:
                payload = await client.get(url, params)
            except OpenMeteoApiError:
                errors["base"] = "cannot_connect"
            else:
                self._results = list(payload.get("results") or [])
                if not self._results:
                    errors["base"] = "no_results"
                else:
                    return await self.async_step_place()

        return self.async_show_form(
            step_id="search",
            data_schema=vol.Schema({vol.Required(CONF_SEARCH): TextSelector()}),
            errors=errors,
        )

    async def async_step_place(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pick a geocoding result."""
        if user_input is not None:
            result = self._results[int(user_input[CONF_PLACE])]
            if not self._data.get(CONF_NAME) or self._data[CONF_NAME] == DEFAULT_NAME:
                self._data[CONF_NAME] = result.get("name") or DEFAULT_NAME
            return await self._async_store_location(
                float(result["latitude"]),
                float(result["longitude"]),
            )

        options = [
            SelectOptionDict(value=str(index), label=_format_place(result))
            for index, result in enumerate(self._results)
        ]
        return self.async_show_form(
            step_id="place",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PLACE, default="0"): SelectSelector(
                        SelectSelectorConfig(options=options, mode=SelectSelectorMode.LIST)
                    )
                }
            ),
        )

    async def _async_store_location(self, latitude: float, longitude: float) -> ConfigFlowResult:
        unique_id = location_unique_id(latitude, longitude)
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()
        self._data[CONF_LATITUDE] = latitude
        self._data[CONF_LONGITUDE] = longitude
        return await self.async_step_modules()

    async def async_step_modules(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select API modules."""
        if user_input is not None:
            self._options[CONF_MODULES] = user_input[CONF_MODULES]
            return await self.async_step_groups()

        return self.async_show_form(
            step_id="modules",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MODULES, default=DEFAULT_MODULES): _modules_selector(),
                }
            ),
        )

    async def async_step_groups(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select variable groups for live modules."""
        modules = list(self._options.get(CONF_MODULES, DEFAULT_MODULES))
        schema = _groups_schema(modules, DEFAULT_GROUPS)
        if schema is None:
            self._options[CONF_GROUPS] = {}
            return await self.async_step_settings()

        if user_input is not None:
            self._options[CONF_GROUPS] = _unpack_groups(user_input, modules)
            return await self.async_step_settings()

        return self.async_show_form(step_id="groups", data_schema=vol.Schema(schema))

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Units, models, and polling."""
        if user_input is not None:
            self._options.update(user_input)
            return self.async_create_entry(
                title=self._data[CONF_NAME],
                data=self._data,
                options=self._options,
            )

        return self.async_show_form(
            step_id="settings",
            data_schema=_settings_schema(
                include_forecast=MODULE_FORECAST in self._options.get(CONF_MODULES, [])
            ),
        )


class HaOpenMeteoOptionsFlow(OptionsFlowWithReload):
    """Change modules, groups, and settings without re-adding the location."""

    def __init__(self) -> None:
        self._options: dict[str, Any] = {}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        self._options = dict(self.config_entry.options)
        return await self.async_step_modules()

    async def async_step_modules(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            self._options[CONF_MODULES] = user_input[CONF_MODULES]
            return await self.async_step_groups()

        return self.async_show_form(
            step_id="modules",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MODULES,
                        default=self._options.get(CONF_MODULES, DEFAULT_MODULES),
                    ): _modules_selector(),
                }
            ),
        )

    async def async_step_groups(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        modules = list(self._options.get(CONF_MODULES, DEFAULT_MODULES))
        current_groups = self._options.get(CONF_GROUPS, DEFAULT_GROUPS)
        schema = _groups_schema(modules, current_groups)
        if schema is None:
            self._options[CONF_GROUPS] = {}
            return await self.async_step_settings()

        if user_input is not None:
            self._options[CONF_GROUPS] = _unpack_groups(user_input, modules)
            return await self.async_step_settings()

        return self.async_show_form(step_id="groups", data_schema=vol.Schema(schema))

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            self._options.update(user_input)
            return self.async_create_entry(title="", data=self._options)

        return self.async_show_form(
            step_id="settings",
            data_schema=_settings_schema(
                include_forecast=MODULE_FORECAST in self._options.get(CONF_MODULES, []),
                options=self._options,
            ),
        )


def _modules_selector() -> SelectSelector:
    return SelectSelector(
        SelectSelectorConfig(
            options=[
                SelectOptionDict(value=module, label=MODULE_LABELS[module])
                for module in ALL_MODULES
            ],
            multiple=True,
            mode=SelectSelectorMode.LIST,
        )
    )


def _groups_schema(
    modules: list[str], current: dict[str, list[str]]
) -> dict[Any, Any] | None:
    schema: dict[Any, Any] = {}
    for module in modules:
        if module not in LIVE_MODULES or module == "elevation":
            continue
        options = [
            SelectOptionDict(value=group_id, label=label)
            for group_id, label in group_options(module)
        ]
        if not options:
            continue
        default = current.get(module) or DEFAULT_GROUPS.get(module) or [options[0]["value"]]
        schema[
            vol.Required(f"groups_{module}", default=default)
        ] = SelectSelector(
            SelectSelectorConfig(
                options=options,
                multiple=True,
                mode=SelectSelectorMode.LIST,
            )
        )
    return schema or None


def _unpack_groups(user_input: dict[str, Any], modules: list[str]) -> dict[str, list[str]]:
    packed: dict[str, list[str]] = {}
    for module in modules:
        key = f"groups_{module}"
        if key in user_input:
            packed[module] = list(user_input[key])
    return packed


def _settings_schema(
    *,
    include_forecast: bool,
    options: dict[str, Any] | None = None,
) -> vol.Schema:
    options = options or {}
    fields: dict[Any, Any] = {
        vol.Required(
            CONF_TEMPERATURE_UNIT,
            default=options.get(CONF_TEMPERATURE_UNIT, DEFAULT_TEMPERATURE_UNIT),
        ): SelectSelector(
            SelectSelectorConfig(
                options=[
                    SelectOptionDict(value=TEMP_UNIT_CELSIUS, label="Celsius"),
                    SelectOptionDict(value=TEMP_UNIT_FAHRENHEIT, label="Fahrenheit"),
                ]
            )
        ),
        vol.Required(
            CONF_WIND_SPEED_UNIT,
            default=options.get(CONF_WIND_SPEED_UNIT, DEFAULT_WIND_SPEED_UNIT),
        ): SelectSelector(
            SelectSelectorConfig(
                options=[
                    SelectOptionDict(value=WIND_UNIT_KMH, label="km/h"),
                    SelectOptionDict(value=WIND_UNIT_MS, label="m/s"),
                    SelectOptionDict(value=WIND_UNIT_MPH, label="mph"),
                    SelectOptionDict(value=WIND_UNIT_KN, label="knots"),
                ]
            )
        ),
        vol.Required(
            CONF_PRECIPITATION_UNIT,
            default=options.get(CONF_PRECIPITATION_UNIT, DEFAULT_PRECIPITATION_UNIT),
        ): SelectSelector(
            SelectSelectorConfig(
                options=[
                    SelectOptionDict(value=PRECIP_UNIT_MM, label="Millimeters"),
                    SelectOptionDict(value=PRECIP_UNIT_INCH, label="Inches"),
                ]
            )
        ),
        vol.Required(
            CONF_FORECAST_DAYS,
            default=options.get(CONF_FORECAST_DAYS, DEFAULT_FORECAST_DAYS),
        ): NumberSelector(
            NumberSelectorConfig(min=1, max=16, step=1, mode=NumberSelectorMode.BOX)
        ),
        vol.Required(
            CONF_UPDATE_INTERVAL,
            default=options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES),
        ): NumberSelector(
            NumberSelectorConfig(min=5, max=180, step=5, mode=NumberSelectorMode.BOX)
        ),
        vol.Required(
            CONF_TILT,
            default=options.get(CONF_TILT, 0),
        ): NumberSelector(
            NumberSelectorConfig(min=0, max=90, step=1, mode=NumberSelectorMode.BOX)
        ),
        vol.Required(
            CONF_AZIMUTH,
            default=options.get(CONF_AZIMUTH, 0),
        ): NumberSelector(
            NumberSelectorConfig(min=-180, max=180, step=1, mode=NumberSelectorMode.BOX)
        ),
    }
    if include_forecast:
        fields[
            vol.Required(CONF_MODELS, default=options.get(CONF_MODELS, DEFAULT_MODELS))
        ] = SelectSelector(
            SelectSelectorConfig(
                options=[SelectOptionDict(value=model, label=model) for model in FORECAST_MODEL_CHOICES],
                multiple=True,
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
        fields[
            vol.Required(
                CONF_PRESSURE_LEVELS,
                default=options.get(CONF_PRESSURE_LEVELS, DEFAULT_PRESSURE_LEVELS),
            )
        ] = SelectSelector(
            SelectSelectorConfig(
                options=[SelectOptionDict(value=level, label=f"{level} hPa") for level in PRESSURE_LEVEL_CHOICES],
                multiple=True,
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
    return vol.Schema(fields)


def _format_place(result: dict[str, Any]) -> str:
    parts = [result.get("name") or "Unknown"]
    admin = result.get("admin1")
    country = result.get("country") or result.get("country_code")
    if admin:
        parts.append(str(admin))
    if country:
        parts.append(str(country))
    return ", ".join(parts)
