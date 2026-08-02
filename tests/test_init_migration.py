"""Tests for the sensor.* -> binary_sensor.* registry migration (issue #65)."""

import types

import homeassistant.helpers.issue_registry as ir
from custom_components.ev_metron_websockets import _async_migrate_car_status_entities
from tests.conftest import FakeEntityRegistry


def _fake_hass():
    hass = types.SimpleNamespace()
    hass._fake_entity_registry = FakeEntityRegistry()
    return hass


def _fake_entry(entry_id="abc123"):
    return types.SimpleNamespace(entry_id=entry_id)


def _fake_hub(name="test"):
    return types.SimpleNamespace(name=name)


def test_removes_old_sensor_entities_and_raises_issue(monkeypatch):
    hass = _fake_hass()
    registry = hass._fake_entity_registry
    registry.add("sensor", "ev_metron_websockets", "test_car_connected", "sensor.test_car_connected")
    registry.add("sensor", "ev_metron_websockets", "test_charging", "sensor.test_charging")

    created_issues = []
    monkeypatch.setattr(ir, "async_create_issue", lambda hass, domain, issue_id, **kw: created_issues.append((domain, issue_id, kw)))

    _async_migrate_car_status_entities(hass, _fake_entry(), _fake_hub())

    assert sorted(registry.removed) == ["sensor.test_car_connected", "sensor.test_charging"]
    assert len(created_issues) == 1
    domain, issue_id, kwargs = created_issues[0]
    assert domain == "ev_metron_websockets"
    assert issue_id == "car_status_entities_moved_abc123"
    assert "sensor.test_car_connected -> binary_sensor.test_car_connected" in kwargs["translation_placeholders"]["changes"]
    assert "sensor.test_charging -> binary_sensor.test_charging" in kwargs["translation_placeholders"]["changes"]


def test_no_op_when_nothing_to_migrate(monkeypatch):
    hass = _fake_hass()

    created_issues = []
    monkeypatch.setattr(ir, "async_create_issue", lambda *a, **kw: created_issues.append((a, kw)))

    _async_migrate_car_status_entities(hass, _fake_entry(), _fake_hub())

    assert hass._fake_entity_registry.removed == []
    assert created_issues == []
