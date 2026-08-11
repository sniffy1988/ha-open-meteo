"""Sensors for selected Open-Meteo variable groups."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    EntityCategory,
    UnitOfLength,
    UnitOfPrecipitationDepth,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from .const import (
    MODULE_ELEVATION,
    PRECIP_UNIT_INCH,
    TEMP_UNIT_FAHRENHEIT,
    WIND_UNIT_KN,
    WIND_UNIT_MPH,
    WIND_UNIT_MS,
)
from .coordinator import HaOpenMeteoCoordinator
from .entity import HaOpenMeteoEntity
from .helpers import configured_units, parse_api_datetime
from .models.variables import BUCKET_CURRENT, VariableDef

PARALLEL_UPDATES = 0


@dataclass(kw_only=True, frozen=True)
class OpenMeteoSensorEntityDescription(SensorEntityDescription):
    """Sensor description that knows which API field to read."""

    module: str
    bucket: str
    api_key: str


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create sensors for every selected variable."""
    entities: list[HaOpenMeteoSensor] = []
    temp_unit, wind_unit, precip_unit = configured_units(entry)

    for module, coordinator in entry.runtime_data.coordinators.items():
        if module == MODULE_ELEVATION:
            entities.append(
                HaOpenMeteoSensor(
                    coordinator,
                    entry,
                    _elevation_description(),
                )
            )
            continue
        for variable in coordinator.selected_variables():
            entities.append(
                HaOpenMeteoSensor(
                    coordinator,
                    entry,
                    _description_from_variable(module, variable, temp_unit, wind_unit, precip_unit),
                )
            )

    async_add_entities(entities)


class HaOpenMeteoSensor(HaOpenMeteoEntity, SensorEntity):
    """One Open-Meteo variable as a scalar sensor."""

    entity_description: OpenMeteoSensorEntityDescription

    def __init__(
        self,
        coordinator: HaOpenMeteoCoordinator,
        entry: ConfigEntry,
        description: OpenMeteoSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator, entry)
        self.entity_description = description
        unique = entry.unique_id or entry.entry_id
        self._attr_unique_id = (
            f"{unique}_{description.module}_{description.bucket}_{description.api_key}"
        )

    @property
    def native_value(self) -> StateType | datetime | date:
        data = self.coordinator.data
        if data is None:
            return None
        raw = data.value(self.entity_description.bucket, self.entity_description.api_key)
        if raw is None:
            return None
        if self.entity_description.device_class == SensorDeviceClass.TIMESTAMP:
            return parse_api_datetime(str(raw))
        if isinstance(raw, bool):
            return raw
        if isinstance(raw, (int, float)):
            return raw
        if isinstance(raw, str):
            try:
                if "." in raw:
                    return float(raw)
                return int(raw)
            except ValueError:
                return raw
        return raw


def _elevation_description() -> OpenMeteoSensorEntityDescription:
    return OpenMeteoSensorEntityDescription(
        key="elevation",
        name="Elevation",
        module=MODULE_ELEVATION,
        bucket=BUCKET_CURRENT,
        api_key="elevation",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfLength.METERS,
        icon="mdi:image-filter-hdr",
        entity_category=EntityCategory.DIAGNOSTIC,
    )


_BUCKET_SUFFIX = {
    "hourly": "hourly",
    "daily": "daily",
    "minutely_15": "15-min",
    "weekly": "weekly",
    "monthly": "monthly",
}


def _sensor_name(variable: VariableDef) -> str:
    suffix = _BUCKET_SUFFIX.get(variable.bucket)
    if not suffix:
        return variable.name
    lowered = variable.name.lower()
    if suffix in lowered or "daily" in lowered or "weekly" in lowered or "monthly" in lowered:
        return variable.name
    return f"{variable.name} ({suffix})"


def _description_from_variable(
    module: str,
    variable: VariableDef,
    temp_unit: str,
    wind_unit: str,
    precip_unit: str,
) -> OpenMeteoSensorEntityDescription:
    unit = _native_unit(variable, temp_unit, wind_unit, precip_unit)
    return OpenMeteoSensorEntityDescription(
        key=f"{module}_{variable.bucket}_{variable.key}",
        name=_sensor_name(variable),
        module=module,
        bucket=variable.bucket,
        api_key=variable.key,
        device_class=variable.device_class,
        state_class=variable.state_class,
        native_unit_of_measurement=unit,
        icon=variable.icon,
    )


def _native_unit(
    variable: VariableDef,
    temp_unit: str,
    wind_unit: str,
    precip_unit: str,
) -> str | None:
    if variable.device_class == SensorDeviceClass.TEMPERATURE:
        return (
            UnitOfTemperature.FAHRENHEIT
            if temp_unit == TEMP_UNIT_FAHRENHEIT
            else UnitOfTemperature.CELSIUS
        )
    if variable.device_class in (SensorDeviceClass.WIND_SPEED, SensorDeviceClass.SPEED):
        return {
            WIND_UNIT_MS: UnitOfSpeed.METERS_PER_SECOND,
            WIND_UNIT_MPH: UnitOfSpeed.MILES_PER_HOUR,
            WIND_UNIT_KN: UnitOfSpeed.KNOTS,
        }.get(wind_unit, UnitOfSpeed.KILOMETERS_PER_HOUR)
    if variable.device_class == SensorDeviceClass.PRECIPITATION:
        return (
            UnitOfPrecipitationDepth.INCHES
            if precip_unit == PRECIP_UNIT_INCH
            else UnitOfPrecipitationDepth.MILLIMETERS
        )
    if variable.unit == UnitOfLength.CENTIMETERS and precip_unit == PRECIP_UNIT_INCH:
        return UnitOfLength.INCHES
    return variable.unit
