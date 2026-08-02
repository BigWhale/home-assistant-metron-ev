"""Tests for the diagnostic sensors added after inspecting a live charger payload (#65).

These fields were previously parsed by metron.py but never read by hub.py or
exposed as entities. All are disabled-by-default diagnostic entities since
several units/scales aren't confirmed from the protocol alone.
"""

import types

from homeassistant.const import EntityCategory
from custom_components.ev_metron_websockets.metron import get_parsed_variables
from custom_components.ev_metron_websockets.sensor import (
    CarPhases,
    ChargingCableMaxCurrent,
    DynamicChargingEnableFlag,
    FirmwareVersion,
    FrontButtonState,
    GridPowerLimit,
    GridSystem,
    HousePhases,
    InternalTemperature,
    KwhLimitSlider,
    NumberOfStations,
    SinceLastResetEnergy,
    SolarPhases,
    StationId,
    StationMaxChargingCurrent,
    Vreg1SetChargingCurrent,
    Vreg2SetChargingCurrent,
)
from custom_components.ev_metron_websockets.binary_sensor import (
    WifiToNetworkConnected,
    WifiToNetworkEnabled,
)

# Captured live from a real charger (idle / "Ready to charge") while investigating #65.
LIVE_PAYLOAD = (
    '{"a":1,"b":0,"c":0,"d":0,"e":2,"f":1,"g":0,"h":13,"i":10,"j":20,"k":20,'
    '"l":32,"m":32,"n":16,"o":10,"p":1,"q":1,"r":32,"s":1,"t":8000,"u":2,'
    '"A":0,"B":0,"C":0,"D":0,"E":0,"F":9359129,"G":9359129,"H":32,"I":1,'
    '"J":766,"K":28493302,"L":3,"M":3,"N":1,"O":8731,"P":30748422,"Q":7965,'
    '"R":1,"S":"10.10.10.147","T":0,"U":2,"V":1,"W":10,"X":1,"Y":1,"Z":0,'
    '"AA":0,"AB":"0.0.0.0","AC":320,"AD":"","AE":0,"AF":0,"AG":0,"AH":0,'
    '"AI":1,"AJ":"1.09","AK":"X.XX","AL":93,"AM":0,"AN":3,"AO":0,"AP":0,'
    '"AR":0,"AS":"","AT":0,"AU":0,"AV":0,"AW":0,"AX":"X.XX","AY":0,"AZ":0,'
    '"BA":"","BB":0,"BC":0,"BD":10,"BE":1}'
)

_HUB_FIELDS = (
    "Metron_Charge_Control_Version", "temperature_sens_read", "Solar_phases",
    "House_phases", "Car_phases", "WiFi_to_network_enable", "WiFi_to_network_state",
    "Since_last_reset_energy", "ID_station", "number_of_stations",
    "Charging_cable_max_current", "Vreg1_set_charging_current",
    "Vreg2_set_charging_current", "Station_max_charging_current", "Front_button",
    "Dynamic_Enable", "P_grid_limit", "Grid_system", "kWh_limit_slider",
)


def _hub_from_live_payload():
    """Build a fake hub the way MetronEVHub.update() would populate it from LIVE_PAYLOAD."""
    parsed, fmt = get_parsed_variables(LIVE_PAYLOAD)
    assert fmt == "json"
    return types.SimpleNamespace(
        name="Home Charger",
        metron_charge_control_version=parsed["Metron_Charge_Control_Version"],
        temperature_sens_read=parsed["temperature_sens_read"],
        solar_phases=parsed["Solar_phases"],
        house_phases=parsed["House_phases"],
        car_phases=parsed["Car_phases"],
        wifi_to_network_enable=parsed["WiFi_to_network_enable"],
        wifi_to_network_state=parsed["WiFi_to_network_state"],
        since_last_reset_energy=parsed["Since_last_reset_energy"],
        id_station=parsed["ID_station"],
        number_of_stations=parsed["number_of_stations"],
        charging_cable_max_current=parsed["Charging_cable_max_current"],
        vreg1_set_charging_current=parsed["Vreg1_set_charging_current"],
        vreg2_set_charging_current=parsed["Vreg2_set_charging_current"],
        station_max_charging_current=parsed["Station_max_charging_current"],
        front_button=parsed["Front_button"],
        dynamic_enable=parsed["Dynamic_Enable"],
        p_grid_limit=parsed["P_grid_limit"],
        grid_system=parsed["Grid_system"],
        kwh_limit_slider=parsed["kWh_limit_slider"],
    )


def test_sensors_read_correct_fields_from_live_payload():
    hub = _hub_from_live_payload()

    assert FirmwareVersion(hub).state == "1.09"
    assert InternalTemperature(hub).state == 93
    assert SolarPhases(hub).state == 3
    assert HousePhases(hub).state == 3
    assert CarPhases(hub).state == 1
    assert SinceLastResetEnergy(hub).state == 9359129
    assert StationId(hub).state == 1
    assert NumberOfStations(hub).state == 1
    assert ChargingCableMaxCurrent(hub).state == 20
    assert Vreg1SetChargingCurrent(hub).state == 32
    assert Vreg2SetChargingCurrent(hub).state == 32
    assert StationMaxChargingCurrent(hub).state == 16
    assert FrontButtonState(hub).state == 1
    assert DynamicChargingEnableFlag(hub).state == 2
    assert GridPowerLimit(hub).state == 10
    assert GridSystem(hub).state == 1
    assert KwhLimitSlider(hub).state == 0


def test_binary_sensors_read_correct_fields_from_live_payload():
    hub = _hub_from_live_payload()
    assert WifiToNetworkEnabled(hub).is_on is True
    assert WifiToNetworkConnected(hub).is_on is True


def test_all_new_sensors_are_disabled_diagnostic_by_default():
    for cls in (
        FirmwareVersion, InternalTemperature, SolarPhases, HousePhases, CarPhases,
        SinceLastResetEnergy, StationId, NumberOfStations, ChargingCableMaxCurrent,
        Vreg1SetChargingCurrent, Vreg2SetChargingCurrent, StationMaxChargingCurrent,
        FrontButtonState, DynamicChargingEnableFlag, GridPowerLimit, GridSystem,
        KwhLimitSlider, WifiToNetworkEnabled, WifiToNetworkConnected,
    ):
        assert cls._attr_entity_registry_enabled_default is False
        assert cls._attr_entity_category == EntityCategory.DIAGNOSTIC


def test_hub_update_keys_match_metron_parser_output():
    """Regression guard against key typos between hub.py and metron.py.

    Every new hub.py latest_message.get(key) must match a key metron.py's
    JSON parser actually produces, or the hub attribute would silently stay
    None forever — a real risk with ~19 fields added by hand.
    """
    parsed, _ = get_parsed_variables(LIVE_PAYLOAD)
    for key in _HUB_FIELDS:
        assert key in parsed
