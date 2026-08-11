"""Shared entity helpers."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HaOpenMeteoCoordinator
from .helpers import entry_name


def device_info_for_entry(entry: ConfigEntry) -> DeviceInfo:
    """One service device per location/config entry."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry_name(entry),
        manufacturer="Open-Meteo",
        model="Open-Meteo Full",
        entry_type=DeviceEntryType.SERVICE,
        configuration_url="https://open-meteo.com/",
    )


class HaOpenMeteoEntity(CoordinatorEntity[HaOpenMeteoCoordinator]):
    """Base entity tied to a module coordinator and location device."""

    _attr_attribution = "Weather data by Open-Meteo.com"
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HaOpenMeteoCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self._attr_device_info = device_info_for_entry(entry)
