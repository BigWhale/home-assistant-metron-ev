"""Contains the MetronEVHub class."""

import asyncio
import logging

import websockets

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from websockets.protocol import State

from . import metron

_LOGGER = logging.getLogger(__name__)


class MetronEVHub:
    """Hub for connecting to the Metron EV websocket."""

    def __init__(
        self, hass: HomeAssistant, name: str, host: str, port: int
    ) -> None:
        """Initialise the class."""
        self._host = host
        self._hass = hass
        self._name = name
        self._port = port
        self._uri = f"ws://{host}:{port}/ws"
        self._id = host.lower()
        self._callbacks = set()
        self._is_active = False
        self._metron_ev_status = 0
        self._L1_current_station = 0
        self._L2_current_station = 0
        self._L3_current_station = 0
        self._L1_current_building = 0
        self._L2_current_building = 0
        self._L3_current_building = 0
        self._L1_current_solar = 0
        self._House_energy = 0
        self._button_set_charging_current = 0
        self._main_fuse_rating = 0
        self._dynamic_charging_current_limit = 0
        self._solar_charging_enable = 0
        self._solar_charging_enable_esp = 0
        self._total_charging_power = 0
        self._total_house_power = 0
        self._total_solar_power = 0
        self._this_charge_energy = 0
        self._hour_counter = 0
        self._minute_counter = 0
        self._previous_charge_energy = 0
        self._lifetime_energy = 0
        self._solar_energy = 0
        self._solar_SURPLUS_power = 0
        self._local_network_IP_string = 0
        self._ESP32_timer_delay = 0
        self._HC12_Signal_Present = 0
        self._TCA0_cmp2 = 0
        self._message_format = "unknown"
        self._metron_charge_control_version = None
        self._temperature_sens_read = None
        self._solar_phases = 0
        self._house_phases = 0
        self._car_phases = 0
        self._wifi_to_network_enable = 0
        self._wifi_to_network_state = 0
        self._since_last_reset_energy = 0
        self._id_station = None
        self._number_of_stations = 0
        self._charging_cable_max_current = 0
        self._vreg1_set_charging_current = 0
        self._vreg2_set_charging_current = 0
        self._station_max_charging_current = 0
        self._front_button = None
        self._dynamic_enable = 0
        self._p_grid_limit = None
        self._grid_system = None
        self._kwh_limit_slider = None

    async def test_endpoint(self) -> bool:
        """Test if we can subscribe to the websocket.

        Returns False (rather than raising) on any connection failure so the
        config flow can show "cannot connect" instead of an unhandled exception.
        """
        try:
            async with websockets.connect(self._uri) as websocket:
                return websocket.state is State.OPEN
        except (OSError, websockets.WebSocketException, TimeoutError):
            return False

    async def update(self) -> None:
        """Background task to loop websocket updates."""
        while True:
            try:
                async with websockets.connect(self._uri) as websocket:
                    self._is_active = websocket.state is State.OPEN
                    async for message in websocket:
                        latest_message, self._message_format = metron.get_parsed_variables(message)
                        self._metron_ev_status = latest_message.get("Status")
                        self._L1_current_station = latest_message.get("L1_current_station")
                        self._L2_current_station = latest_message.get("L2_current_station")
                        self._L3_current_station = latest_message.get("L3_current_station")
                        self._L1_current_building = latest_message.get("L1_current_building")
                        self._L2_current_building = latest_message.get("L2_current_building")
                        self._L3_current_building = latest_message.get("L3_current_building")
                        self._L1_current_solar = latest_message.get("L1_current_solar")
                        self._button_set_charging_current = latest_message.get("Button_set_charging_current")
                        self._main_fuse_rating = latest_message.get("Main_fuse_rating")
                        self._dynamic_charging_current_limit = latest_message.get("Dynamic_charging_current_limit")
                        self._solar_charging_enable_esp = latest_message.get("Solar_charging_enable_ESP32_reply")
                        self._solar_charging_enable = latest_message.get("Solar_charging_enable")
                        self._total_charging_power = latest_message.get("Total_charging_power")
                        self._total_house_power = latest_message.get("Total_house_power")
                        self._total_solar_power = latest_message.get("Total_solar_power")
                        self._this_charge_energy = latest_message.get("This_charge_energy")
                        self._hour_counter = latest_message.get("hour_counter")
                        self._minute_counter = latest_message.get("minute_counter")
                        self._previous_charge_energy = latest_message.get("Previous_charge_energy")
                        self._lifetime_energy = latest_message.get("Lifetime_energy")
                        self._solar_energy = latest_message.get("Solar_energy")
                        self._House_energy = latest_message.get("House_energy")
                        self._solar_SURPLUS_power = latest_message.get("Solar_SURPLUS_power")
                        self._local_network_IP_string = latest_message.get("Local_network_IP_string")
                        self._ESP32_timer_delay = latest_message.get("ESP32_timer_delay")
                        self._HC12_Signal_Present = latest_message.get("HC12_Signal_Present")
                        self._TCA0_cmp2 = latest_message.get("TCA0_cmp2")
                        self._metron_charge_control_version = latest_message.get("Metron_Charge_Control_Version")
                        self._temperature_sens_read = latest_message.get("temperature_sens_read")
                        self._solar_phases = latest_message.get("Solar_phases")
                        self._house_phases = latest_message.get("House_phases")
                        self._car_phases = latest_message.get("Car_phases")
                        self._wifi_to_network_enable = latest_message.get("WiFi_to_network_enable")
                        self._wifi_to_network_state = latest_message.get("WiFi_to_network_state")
                        self._since_last_reset_energy = latest_message.get("Since_last_reset_energy")
                        self._id_station = latest_message.get("ID_station")
                        self._number_of_stations = latest_message.get("number_of_stations")
                        self._charging_cable_max_current = latest_message.get("Charging_cable_max_current")
                        self._vreg1_set_charging_current = latest_message.get("Vreg1_set_charging_current")
                        self._vreg2_set_charging_current = latest_message.get("Vreg2_set_charging_current")
                        self._station_max_charging_current = latest_message.get("Station_max_charging_current")
                        self._front_button = latest_message.get("Front_button")
                        self._dynamic_enable = latest_message.get("Dynamic_Enable")
                        self._p_grid_limit = latest_message.get("P_grid_limit")
                        self._grid_system = latest_message.get("Grid_system")
                        self._kwh_limit_slider = latest_message.get("kWh_limit_slider")
                        await self.publish_updates()
                # Clean close: server ended the stream normally
                _LOGGER.debug("WebSocket closed cleanly, reconnecting in 5 s")
            except websockets.WebSocketException as e:
                _LOGGER.warning("WebSocket error, reconnecting in 5 s: %s", e)
            except Exception:
                _LOGGER.exception("Unexpected error in websocket loop, reconnecting in 5 s")
            finally:
                self._is_active = False
                await self.publish_updates()
                await asyncio.sleep(5)

    @property
    def name(self) -> str:
        """Return the configured friendly name."""
        return self._name

    @property
    def host(self) -> str:
        """Return the configured host."""
        return self._host

    @property
    def id(self) -> str:
        """Return the device identifier (lowercased host)."""
        return self._id

    @property
    def TCA0_cmp2(self) -> str:
        """Return status of station."""
        return self._TCA0_cmp2

    @property
    def metron_ev_status(self) -> str:
        """Return status of station."""
        return self._metron_ev_status

    @property
    def L1_current_station(self) -> str:
        """Return the value of L1_current_station."""
        return self._L1_current_station

    @property
    def L2_current_station(self) -> str:
        """Return the value of L2_current_station."""
        return self._L2_current_station

    @property
    def L3_current_station(self) -> str:
        """Return the value of L3_current_station."""
        return self._L3_current_station

    @property
    def L1_current_building(self) -> str:
        """Return the value of L1_current_building."""
        return self._L1_current_building

    @property
    def L2_current_building(self) -> str:
        """Return the value of L2_current_building."""
        return self._L2_current_building

    @property
    def L3_current_building(self) -> str:
        """Return the value of L3_current_building."""
        return self._L3_current_building

    @property
    def L1_current_solar(self) -> str:
        """Return the value of L1_current_solar."""
        return self._L1_current_solar

    @property
    def button_set_charging_current(self) -> str:
        """Return the value of button_set_charging_current."""
        return self._button_set_charging_current

    @property
    def main_fuse_rating(self) -> str:
        """Return the value of main_fuse_rating."""
        return self._main_fuse_rating

    @property
    def dynamic_charging_current_limit(self) -> str:
        """Return the value of dynamic_charging_current_limit."""
        return self._dynamic_charging_current_limit

    @property
    def solar_charging_enable(self) -> str:
        """Return the value of solar_charging_enable."""
        return self._solar_charging_enable

    @property
    def solar_charging_enable_esp(self) -> str:
        """Return the value of solar_charging_enable."""
        return self._solar_charging_enable_esp

    @property
    def total_charging_power(self) -> str:
        """Return the value of total_charging_power."""
        return self._total_charging_power

    @property
    def total_house_power(self) -> str:
        """Return the value of total_house_power."""
        return self._total_house_power

    @property
    def total_solar_power(self) -> str:
        """Return the value of total_solar_power."""
        return self._total_solar_power

    @property
    def this_charge_energy(self) -> str:
        """Return the value of this_charge_energy."""
        return self._this_charge_energy

    @property
    def hour_counter(self) -> str:
        """Return the value of hour_counter."""
        return self._hour_counter

    @property
    def minute_counter(self) -> str:
        """Return the value of minute_counter."""
        return self._minute_counter

    @property
    def previous_charge_energy(self) -> str:
        """Return the value of previous_charge_energy."""
        return self._previous_charge_energy

    @property
    def lifetime_energy(self) -> str:
        """Return the value of lifetime_energy."""
        return self._lifetime_energy

    @property
    def solar_energy(self) -> str:
        """Return the value of solar_energy."""
        return self._solar_energy

    @property
    def House_energy(self) -> str:
        """Return the value of solar_energy."""
        return self._House_energy

    @property
    def solar_SURPLUS_power(self) -> str:
        """Return the value of solar_SURPLUS_power."""
        return self._solar_SURPLUS_power

    @property
    def local_network_IP_string(self) -> str:
        """Return the value of local_network_IP_string."""
        return self._local_network_IP_string

    @property
    def ESP32_timer_delay(self) -> str:
        """Return the value of ESP32_timer_delay."""
        return self._ESP32_timer_delay

    @property
    def HC12_Signal_Present(self) -> str:
        """Return the value of HC12_Signal_Present."""
        return self._HC12_Signal_Present

    async def perform_action(self, message) -> None:
        """Send a constructed message to the websockets endpoint."""
        #message.update(const.ACTION_BASE_MESSAGE)
        #message["timestamp"] = datetime.now().timestamp()
        async with websockets.connect(self._uri) as websocket:
            await websocket.send(message)

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback called when the state changes."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Call all callbacks on update.

        A single entity failing to compute its state (e.g. a malformed message
        leaving one field un-coercible) must not stop the other entities from
        updating, or tear down the websocket connection the update loop runs in.
        """
        for callback in self._callbacks:
            try:
                callback()
            except Exception:
                _LOGGER.exception("Error notifying entity of update")

    @property
    def message_format(self) -> str:
        """Return the last detected websocket message format."""
        return self._message_format

    @property
    def metron_charge_control_version(self):
        """Return the firmware version string. None on legacy (pre-JSON) firmware."""
        return self._metron_charge_control_version

    @property
    def temperature_sens_read(self):
        """Return the raw internal temperature sensor reading. Scale/unit not confirmed."""
        return self._temperature_sens_read

    @property
    def solar_phases(self):
        """Return the configured number of solar phases."""
        return self._solar_phases

    @property
    def house_phases(self):
        """Return the configured number of house phases."""
        return self._house_phases

    @property
    def car_phases(self):
        """Return the configured number of car phases."""
        return self._car_phases

    @property
    def wifi_to_network_enable(self):
        """Return whether WiFi-to-network is enabled."""
        return self._wifi_to_network_enable

    @property
    def wifi_to_network_state(self):
        """Return whether WiFi-to-network is currently connected."""
        return self._wifi_to_network_state

    @property
    def since_last_reset_energy(self):
        """Return the energy counter since its last reset."""
        return self._since_last_reset_energy

    @property
    def id_station(self):
        """Return the station identifier. None on legacy (pre-JSON) firmware."""
        return self._id_station

    @property
    def number_of_stations(self):
        """Return the number of stations reported by the charger."""
        return self._number_of_stations

    @property
    def charging_cable_max_current(self):
        """Return the charging cable's maximum current rating, in amps."""
        return self._charging_cable_max_current

    @property
    def vreg1_set_charging_current(self):
        """Return the Vreg1 set charging current, in amps."""
        return self._vreg1_set_charging_current

    @property
    def vreg2_set_charging_current(self):
        """Return the Vreg2 set charging current, in amps."""
        return self._vreg2_set_charging_current

    @property
    def station_max_charging_current(self):
        """Return the station's maximum charging current, in amps."""
        return self._station_max_charging_current

    @property
    def front_button(self):
        """Return the front button state. None on legacy (pre-JSON) firmware."""
        return self._front_button

    @property
    def dynamic_enable(self):
        """Return the dynamic charging enable flag (not a plain boolean; meaning unconfirmed)."""
        return self._dynamic_enable

    @property
    def p_grid_limit(self):
        """Return the grid power limit setting. None on legacy (pre-JSON) firmware."""
        return self._p_grid_limit

    @property
    def grid_system(self):
        """Return the grid system code. None on legacy (pre-JSON) firmware."""
        return self._grid_system

    @property
    def kwh_limit_slider(self):
        """Return the kWh limit slider setting. None on legacy (pre-JSON) firmware."""
        return self._kwh_limit_slider

    @property
    def available(self) -> bool:
        """Available if the websockets connection has value and is not closed."""
        return self._is_active
