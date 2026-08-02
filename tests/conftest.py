"""Stub out homeassistant modules so tests run without a full HA install."""

import enum
import sys
import types


def _stub(name):
    """Ensure a dotted module path exists in sys.modules."""
    parts = name.split(".")
    for i in range(1, len(parts) + 1):
        key = ".".join(parts[:i])
        if key not in sys.modules:
            sys.modules[key] = types.ModuleType(key)


for _mod in [
    "homeassistant",
    "homeassistant.config_entries",
    "homeassistant.core",
    "homeassistant.helpers",
    "homeassistant.helpers.entity",
    "homeassistant.helpers.entity_platform",
    "homeassistant.helpers.entity_registry",
    "homeassistant.helpers.issue_registry",
    "homeassistant.components",
    "homeassistant.components.sensor",
    "homeassistant.components.binary_sensor",
    "homeassistant.const",
    "websockets",
    "websockets.protocol",
]:
    _stub(_mod)


# --- homeassistant.components.sensor ---

class SensorStateClass(str, enum.Enum):
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class SensorDeviceClass(str, enum.Enum):
    CURRENT = "current"
    ENERGY = "energy"
    POWER = "power"
    DURATION = "duration"


class SensorEntity:
    """Minimal stub mirroring the real SensorEntity's _attr_* fallback properties."""

    _attr_state_class = None
    _attr_native_unit_of_measurement = None
    _attr_device_class = None

    @property
    def state_class(self):
        return self._attr_state_class

    @property
    def native_unit_of_measurement(self):
        return self._attr_native_unit_of_measurement

    @property
    def device_class(self):
        return self._attr_device_class


_sensor = sys.modules["homeassistant.components.sensor"]
_sensor.SensorEntity = SensorEntity
_sensor.SensorStateClass = SensorStateClass
_sensor.SensorDeviceClass = SensorDeviceClass

# --- homeassistant.components.binary_sensor ---

class BinarySensorDeviceClass(str, enum.Enum):
    PLUG = "plug"
    BATTERY_CHARGING = "battery_charging"
    CONNECTIVITY = "connectivity"


class BinarySensorEntity:
    """Minimal stub mirroring the real BinarySensorEntity's _attr_* fallback properties."""

    _attr_is_on = None
    _attr_device_class = None

    @property
    def is_on(self):
        return self._attr_is_on

    @property
    def device_class(self):
        return self._attr_device_class


_binary_sensor = sys.modules["homeassistant.components.binary_sensor"]
_binary_sensor.BinarySensorDeviceClass = BinarySensorDeviceClass
_binary_sensor.BinarySensorEntity = BinarySensorEntity

# --- homeassistant.const ---

class EntityCategory(str, enum.Enum):
    DIAGNOSTIC = "diagnostic"


class Platform(str, enum.Enum):
    SENSOR = "sensor"
    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    NUMBER = "number"
    SELECT = "select"


_const = sys.modules["homeassistant.const"]
_const.EntityCategory = EntityCategory
_const.Platform = Platform
_const.UnitOfEnergy = types.SimpleNamespace(WATT_HOUR="Wh", KILO_WATT_HOUR="kWh")
_const.UnitOfPower = types.SimpleNamespace(WATT="W")
_const.UnitOfElectricCurrent = types.SimpleNamespace(AMPERE="A")
_const.UnitOfTime = types.SimpleNamespace(MINUTES="min")
_const.CONF_HOST = "host"
_const.CONF_PORT = "port"
_const.CONF_FRIENDLY_NAME = "friendly_name"

# --- homeassistant.config_entries ---

class ConfigEntry:
    """Minimal stub for ConfigEntry."""


sys.modules["homeassistant.config_entries"].ConfigEntry = ConfigEntry

# --- homeassistant.core ---

class HomeAssistant:
    """Minimal stub for HomeAssistant."""


sys.modules["homeassistant.core"].HomeAssistant = HomeAssistant

# --- homeassistant.helpers.entity ---

sys.modules["homeassistant.helpers.entity"].Entity = object
sys.modules["homeassistant.helpers.entity"].DeviceInfo = dict

# --- homeassistant.helpers.entity_platform ---

sys.modules["homeassistant.helpers.entity_platform"].AddEntitiesCallback = object

# --- homeassistant.helpers.entity_registry ---


class FakeEntityRegistry:
    """In-memory stand-in for HA's entity registry, for tests to pre-populate/inspect."""

    def __init__(self):
        """Initialize with an empty registry."""
        self._entity_ids: dict[tuple[str, str, str], str] = {}
        self.removed: list[str] = []

    def add(self, domain: str, platform: str, unique_id: str, entity_id: str) -> None:
        self._entity_ids[(domain, platform, unique_id)] = entity_id

    def async_get_entity_id(self, domain: str, platform: str, unique_id: str) -> str | None:
        return self._entity_ids.get((domain, platform, unique_id))

    def async_remove(self, entity_id: str) -> None:
        self.removed.append(entity_id)
        self._entity_ids = {k: v for k, v in self._entity_ids.items() if v != entity_id}


def _entity_registry_async_get(hass):
    return hass._fake_entity_registry


_entity_registry = sys.modules["homeassistant.helpers.entity_registry"]
_entity_registry.async_get = _entity_registry_async_get

# --- homeassistant.helpers.issue_registry ---


class IssueSeverity(str, enum.Enum):
    WARNING = "warning"
    ERROR = "error"


def _issue_registry_async_create_issue(hass, domain, issue_id, **kwargs) -> None:
    """No-op by default; tests monkeypatch this to capture calls."""


_issue_registry = sys.modules["homeassistant.helpers.issue_registry"]
_issue_registry.IssueSeverity = IssueSeverity
_issue_registry.async_create_issue = _issue_registry_async_create_issue

# --- websockets ---

sys.modules["websockets.protocol"].State = types.SimpleNamespace(OPEN="OPEN")
sys.modules["websockets"].connect = None
sys.modules["websockets"].WebSocketException = Exception
