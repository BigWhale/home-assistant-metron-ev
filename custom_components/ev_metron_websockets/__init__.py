"""The Metron EV integration."""
from __future__ import annotations


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    Platform,
    CONF_PORT,
    CONF_HOST,
    CONF_FRIENDLY_NAME,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir

from .const import DOMAIN
from .hub import MetronEVHub


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SELECT,
]

# unique_id suffixes for entities moved from sensor.* to binary_sensor.* (#65)
_MOVED_TO_BINARY_SENSOR = ["car_connected", "charging"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Metron EV from a config entry."""

    hub = MetronEVHub(
        hass,
        entry.data[CONF_FRIENDLY_NAME],
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
    )

    _async_migrate_car_status_entities(hass, entry, hub)

    entry.async_create_background_task(hass, hub.update(), "ev_metron_update")
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


def _async_migrate_car_status_entities(hass: HomeAssistant, entry: ConfigEntry, hub: MetronEVHub) -> None:
    """Remove the old sensor.* car_connected/charging entities superseded by binary_sensor.*.

    They were booleans wrongly exposed as SensorEntity with a BinarySensorDeviceClass
    (#65). Domain is part of the registry key, so HA won't rename them on its own -
    left alone they'd sit as permanently-unavailable orphans once the sensor.py
    classes are removed. Raises a repair issue so the user knows to update any
    automations/dashboards pointing at the old entity_ids.
    """
    registry = er.async_get(hass)
    moved = []
    for suffix in _MOVED_TO_BINARY_SENSOR:
        unique_id = f"{hub.name}_{suffix}"
        old_entity_id = registry.async_get_entity_id(Platform.SENSOR, DOMAIN, unique_id)
        if old_entity_id is None:
            continue
        registry.async_remove(old_entity_id)
        new_entity_id = f"binary_sensor.{old_entity_id.split('.', 1)[1]}"
        moved.append((old_entity_id, new_entity_id))

    if not moved:
        return

    ir.async_create_issue(
        hass,
        DOMAIN,
        f"car_status_entities_moved_{entry.entry_id}",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="car_status_entities_moved",
        translation_placeholders={
            "changes": ", ".join(f"{old} -> {new}" for old, new in moved)
        },
    )

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
