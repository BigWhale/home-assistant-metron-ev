"""Tests for the binary_sensor platform (moved out of sensor.py per issue #65)."""

import types

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from custom_components.ev_metron_websockets.binary_sensor import CarConnected, CarCharging


def _fake_hub(**attrs):
    attrs.setdefault("name", "test")
    return types.SimpleNamespace(**attrs)


def test_car_connected_inherits_binary_sensor_entity():
    assert issubclass(CarConnected, BinarySensorEntity)


def test_car_connected_is_on_for_connected_statuses():
    for status in (2, 3, 4, 7):
        entity = CarConnected(_fake_hub(metron_ev_status=status))
        assert entity.is_on is True
    entity = CarConnected(_fake_hub(metron_ev_status=1))
    assert entity.is_on is False
    assert entity.device_class == BinarySensorDeviceClass.PLUG


def test_car_charging_is_on_only_while_status_3_and_not_full():
    entity = CarCharging(_fake_hub(metron_ev_status=3, TCA0_cmp2=100))
    assert entity.is_on is True

    entity = CarCharging(_fake_hub(metron_ev_status=3, TCA0_cmp2=8000))
    assert entity.is_on is False

    entity = CarCharging(_fake_hub(metron_ev_status=2, TCA0_cmp2=100))
    assert entity.is_on is False
    assert entity.device_class == BinarySensorDeviceClass.BATTERY_CHARGING
