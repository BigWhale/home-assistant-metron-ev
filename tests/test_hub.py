"""Tests for MetronEVHub: public accessors, connection testing, update resilience."""

import asyncio
import types

import websockets
from websockets.protocol import State

from custom_components.ev_metron_websockets.hub import MetronEVHub


def _make_hub():
    return MetronEVHub(types.SimpleNamespace(), "Home Charger", "192.168.1.50", 80)


def test_public_accessors_expose_hub_identity():
    hub = _make_hub()
    assert hub.name == "Home Charger"
    assert hub.host == "192.168.1.50"
    assert hub.id == "192.168.1.50"


class _FakeWebSocket:
    def __init__(self, state):
        self.state = state


class _FakeConnectCtx:
    """Stand-in for the object returned by websockets.connect()."""

    def __init__(self, state=None, exc=None):
        self._state = state
        self._exc = exc

    async def __aenter__(self):
        if self._exc:
            raise self._exc
        return _FakeWebSocket(self._state)

    async def __aexit__(self, *args):
        return False


def test_endpoint_returns_true_when_open(monkeypatch):
    hub = _make_hub()
    monkeypatch.setattr(websockets, "connect", lambda uri: _FakeConnectCtx(state=State.OPEN))
    assert asyncio.run(hub.test_endpoint()) is True


def test_endpoint_returns_false_on_connection_error(monkeypatch):
    """Real connection failures (host down, refused, ...) must not raise out of test_endpoint."""
    hub = _make_hub()
    monkeypatch.setattr(websockets, "connect", lambda uri: _FakeConnectCtx(exc=ConnectionRefusedError()))
    assert asyncio.run(hub.test_endpoint()) is False


def test_endpoint_returns_false_on_websocket_exception(monkeypatch):
    hub = _make_hub()
    monkeypatch.setattr(websockets, "connect", lambda uri: _FakeConnectCtx(exc=websockets.WebSocketException()))
    assert asyncio.run(hub.test_endpoint()) is False


def test_publish_updates_isolates_callback_errors():
    """One entity failing to compute state must not stop other entities updating."""
    hub = _make_hub()
    calls = []

    def bad_callback():
        raise RuntimeError("boom")

    def good_callback():
        calls.append("ok")

    hub.register_callback(bad_callback)
    hub.register_callback(good_callback)

    asyncio.run(hub.publish_updates())  # must not raise

    assert calls == ["ok"]
