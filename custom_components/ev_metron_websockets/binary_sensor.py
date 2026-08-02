"""Binary sensors for Metron EV vehicle connection/charging state."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import MetronEVBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add binary sensors for setup hub object."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            CarConnected(hub),
            CarCharging(hub),
            WifiToNetworkEnabled(hub),
            WifiToNetworkConnected(hub),
        ]
    )


class CarConnected(MetronEVBaseEntity, BinarySensorEntity):
    """Whether a vehicle is plugged into the charger."""

    def __init__(self, hub) -> None:
        """Initialize the binary sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_car_connected"
        self._attr_name = f"{hub.name} car connected"
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self) -> bool:
        """Return true if a vehicle is connected."""
        return int(self._hub.metron_ev_status) in [2, 3, 4, 7]


class CarCharging(MetronEVBaseEntity, BinarySensorEntity):
    """Whether the vehicle is actively charging."""

    def __init__(self, hub) -> None:
        """Initialize the binary sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_charging"
        self._attr_name = f"{hub.name} charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self) -> bool:
        """Return true if actively charging."""
        return int(self._hub.metron_ev_status) == 3 and int(self._hub.TCA0_cmp2) != 8000


class WifiToNetworkEnabled(MetronEVBaseEntity, BinarySensorEntity):
    """Whether WiFi-to-network is enabled. Diagnostic, disabled by default."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the binary sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_wifi_to_network_enable"
        self._attr_name = f"{hub.name} WiFi to network enabled"

    @property
    def is_on(self) -> bool:
        """Return true if WiFi-to-network is enabled."""
        return bool(self._hub.wifi_to_network_enable)


class WifiToNetworkConnected(MetronEVBaseEntity, BinarySensorEntity):
    """Whether WiFi-to-network is currently connected. Diagnostic, disabled by default."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the binary sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_wifi_to_network_state"
        self._attr_name = f"{hub.name} WiFi to network connected"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self) -> bool:
        """Return true if WiFi-to-network is currently connected."""
        return bool(self._hub.wifi_to_network_state)
