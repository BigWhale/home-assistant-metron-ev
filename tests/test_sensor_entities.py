"""Regression tests for GitHub issue #65: sensor state_class/unit not exposed to HA.

Sensor entities only inherited from MetronEVBaseEntity(Entity), never from
SensorEntity, so _attr_state_class / _attr_native_unit_of_measurement were
set but never surfaced through HA's state_class/native_unit_of_measurement
properties.
"""

import types

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from custom_components.ev_metron_websockets.sensor import LifetimeEnergy, L1CurrentStation, MetronName


def _fake_hub(**attrs):
    attrs.setdefault("name", "test")
    return types.SimpleNamespace(**attrs)


def test_sensor_entities_inherit_sensor_entity():
    assert issubclass(LifetimeEnergy, SensorEntity)
    assert issubclass(L1CurrentStation, SensorEntity)


def test_state_class_and_unit_exposed():
    entity = LifetimeEnergy(_fake_hub(lifetime_energy=42))
    assert entity.state_class == SensorStateClass.TOTAL_INCREASING
    assert entity.native_unit_of_measurement == "Wh"
    assert entity.device_class == SensorDeviceClass.ENERGY


def test_measurement_sensor_exposes_current_unit():
    entity = L1CurrentStation(_fake_hub(L1_current_station=6))
    assert entity.state_class == SensorStateClass.MEASUREMENT
    assert entity.native_unit_of_measurement == "A"
    assert entity.device_class == SensorDeviceClass.CURRENT


def test_sensor_without_state_class_defaults_to_none():
    entity = MetronName(_fake_hub(name="Charger"))
    assert entity.state_class is None
    assert entity.native_unit_of_measurement is None
    assert entity.state == "Charger"
