# Open-Meteo Full

A HACS custom integration that brings the full [Open-Meteo](https://open-meteo.com/en/docs) API surface into Home Assistant.

Core Home Assistant already ships a basic Open-Meteo weather entity. This integration is a separate domain (`ha_open_meteo`) with selectable API modules, variable groups, multiple locations, and historical/climate actions.

## Features

- **Multiple places** — add the integration once per location (home, cottage, city, …). Each place has its own device, entities, and options.
- **Weather Forecast** — `weather` entity with current conditions plus daily and hourly forecasts (`weather.get_forecasts`).
- **Selectable variable groups** — sensors are created only for the groups you enable (current, hourly, 15-minutely, daily, solar, soil, pressure levels, and more).
- **Air Quality** — pollutants, European/US AQI, pollen.
- **Marine** — waves, swell, currents, sea surface temperature.
- **Flood** — GloFAS river discharge.
- **Ensemble** and **Seasonal** forecasts.
- **Elevation** — diagnostic height from the 90 m DEM.
- **Actions** — `ha_open_meteo.get_historical_weather` (ERA5 archive) and `ha_open_meteo.get_climate_projection` (CMIP6). These return JSON; they are not polled sensors.

No API key is required for non-commercial Open-Meteo use.

## Install with HACS

1. HACS → Integrations → Custom repositories.
2. Add this repository URL as an **Integration**.
3. Install **Open-Meteo Full**.
4. Restart Home Assistant.
5. Settings → Devices & services → Add integration → **Open-Meteo Full**.

Copy `custom_components/ha_open_meteo` into your Home Assistant `custom_components` folder if you are not using HACS.

## Configuration

1. Name the location and set coordinates (map) or search by place name (Open-Meteo Geocoding).
2. Pick API modules.
3. Pick variable groups for each live module.
4. Set units, forecast length, models, pressure levels, and update interval.

Change modules and groups later via the integration’s **Configure** options. To add another place, add the integration again.

## Actions

Both actions support `response_variable` in automations/scripts.

| Action | Purpose |
| --- | --- |
| `ha_open_meteo.get_historical_weather` | Archive API, `start_date` / `end_date`, optional `hourly` / `daily` variable lists |
| `ha_open_meteo.get_climate_projection` | Climate API, date range, `daily` variables, CMIP6 `models` |

Pass `config_entry_id` to reuse a configured place, or `latitude` and `longitude`.

## License and attribution

This integration is MIT licensed. Weather data comes from [Open-Meteo](https://open-meteo.com/) and the national weather services they redistribute. Open-Meteo’s public API is free for non-commercial use; see their [license and pricing](https://open-meteo.com/en/pricing) if you need commercial access.
