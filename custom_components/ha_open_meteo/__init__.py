"""Open-Meteo Full custom integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import OpenMeteoClient
from .const import DOMAIN, LIVE_MODULES, LOGGER, MODULE_FORECAST
from .coordinator import HaOpenMeteoCoordinator
from .helpers import configured_modules
from .services import async_setup_services, async_unload_services


@dataclass
class HaOpenMeteoRuntimeData:
    """Runtime objects attached to a config entry."""

    client: OpenMeteoClient
    coordinators: dict[str, HaOpenMeteoCoordinator]
    platforms: list[Platform]


type HaOpenMeteoConfigEntry = ConfigEntry[HaOpenMeteoRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: HaOpenMeteoConfigEntry) -> bool:
    """Set up a location from a config entry."""
    client = OpenMeteoClient(async_get_clientsession(hass))
    coordinators: dict[str, HaOpenMeteoCoordinator] = {}
    errors: list[str] = []

    for module in configured_modules(entry):
        if module not in LIVE_MODULES:
            continue
        coordinator = HaOpenMeteoCoordinator(hass, entry, client, module)
        try:
            await coordinator.async_config_entry_first_refresh()
        except ConfigEntryNotReady as err:
            LOGGER.warning("Initial %s fetch failed for %s: %s", module, entry.title, err)
            errors.append(f"{module}: {err}")
            # Keep the coordinator so other modules and later retries still work.
            coordinators[module] = coordinator
            continue
        coordinators[module] = coordinator

    live_requested = [module for module in configured_modules(entry) if module in LIVE_MODULES]
    if live_requested and not any(
        coordinator.last_update_success for coordinator in coordinators.values()
    ):
        raise ConfigEntryNotReady("; ".join(errors) or "Open-Meteo unavailable")

    platforms: list[Platform] = [Platform.SENSOR]
    if MODULE_FORECAST in coordinators:
        platforms.append(Platform.WEATHER)

    entry.runtime_data = HaOpenMeteoRuntimeData(
        client=client,
        coordinators=coordinators,
        platforms=platforms,
    )
    await hass.config_entries.async_forward_entry_setups(entry, platforms)
    await async_setup_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HaOpenMeteoConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, entry.runtime_data.platforms
    )
    remaining = [
        item
        for item in hass.config_entries.async_entries(DOMAIN)
        if item.entry_id != entry.entry_id and item.state is ConfigEntryState.LOADED
    ]
    if unload_ok and not remaining:
        async_unload_services(hass)
    return unload_ok
