"""Contains the Entity classes."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import EntityCategory, UnitOfElectricCurrent, UnitOfEnergy, UnitOfPower, UnitOfTime
from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from .const import DOMAIN
from .entity import MetronEVBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for setup hub object."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            MetronStatus(hub),
            MetronActive(hub),
            MetronName(hub),
            L1CurrentStation(hub),
            L2CurrentStation(hub),
            L3CurrentStation(hub),
            L1CurrentBuilding(hub),
            L2CurrentBuilding(hub),
            L3CurrentBuilding(hub),
            HouseEnergy(hub),
            L1CurrentSolar(hub),
            ButtonSetChargingCurrent(hub),
            MainFuseRating(hub),
            DynamicChargingCurrentLimit(hub),
            SolarChargingEnable(hub),
            SolarChargingEnableShort(hub),
            TotalChargingPower(hub),
            TotalHousePower(hub),
            TotalSolarPower(hub),
            ThisChargeEnergy(hub),
            ChargingTime(hub),
            PreviousChargeEnergy(hub),
            LifetimeEnergy(hub),
            SolarEnergy(hub),
            SolarSURPLUSPower(hub),
            LocalNetworkIPString(hub),
            TimerDelay(hub),
            SignalPresent(hub),
            MessageFormat(hub),
            FirmwareVersion(hub),
            InternalTemperature(hub),
            SolarPhases(hub),
            HousePhases(hub),
            CarPhases(hub),
            SinceLastResetEnergy(hub),
            StationId(hub),
            NumberOfStations(hub),
            ChargingCableMaxCurrent(hub),
            Vreg1SetChargingCurrent(hub),
            Vreg2SetChargingCurrent(hub),
            StationMaxChargingCurrent(hub),
            FrontButtonState(hub),
            DynamicChargingEnableFlag(hub),
            GridPowerLimit(hub),
            GridSystem(hub),
            KwhLimitSlider(hub),
        ]
    )

class MetronStatus(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_station_status"
        self._attr_name = f"{hub.name} station status"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.metron_ev_status) == 1 and int(self._hub.ESP32_timer_delay) == 0:
            return "Ready to charge"
        elif int(self._hub.metron_ev_status) == 1 and int(self._hub.ESP32_timer_delay) != 0:
            return "Charging start delayed"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub.TCA0_cmp2) != 8000:
            return "FULLY CHARGED or charging postponed"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub.TCA0_cmp2) == 8000 and int(self._hub.ESP32_timer_delay) == 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 2 and int(self._hub.TCA0_cmp2) == 8000 and int(self._hub.ESP32_timer_delay) != 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub.TCA0_cmp2) != 8000:
            return "CHARGING"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub.TCA0_cmp2) == 8000 and int(self._hub.ESP32_timer_delay) == 0:
            return "Charging stopped"
        elif int(self._hub.metron_ev_status) == 3 and int(self._hub.TCA0_cmp2) == 8000 and int(self._hub.ESP32_timer_delay) != 0:
            return "Charging start delayed"
        elif int(self._hub.metron_ev_status) == 4:
            return "Room ventilation required by the vehicle, charging stopped"
        elif int(self._hub.metron_ev_status) == 5:
            return "STATION BOOTING"
        elif int(self._hub.metron_ev_status) == 6:
            return "Waiting for charging activation"
        elif int(self._hub.metron_ev_status) == 7:
            return "Waiting for charging activation"
        else:
            return "Station or vehicle error"

class MetronActive(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_station_active"
        self._attr_name = f"{hub.name} station active"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self._hub.available is True:
            return "Connected"
        else:
            return "Disconnected"

class MetronName(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_station_name"
        self._attr_name = f"{hub.name} station name"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.name

class L1CurrentStation(MetronEVBaseEntity, SensorEntity):
    """Metron station phase 1 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L1_current_station"
        self._attr_name = f"{hub.name} L1 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self):
        """Return the state of the sensor."""

        return self._hub.L1_current_station

class L2CurrentStation(MetronEVBaseEntity, SensorEntity):
    """Metron station phase 2 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L2_current_station"
        self._attr_name = f"{hub.name} L2 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L2_current_station

class L3CurrentStation(MetronEVBaseEntity, SensorEntity):
    """Metron station phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L3_current_station"
        self._attr_name = f"{hub.name} L3 current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L3_current_station

class L1CurrentBuilding(MetronEVBaseEntity, SensorEntity):
    """Metron station building phase 1 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L1_current_building"
        self._attr_name = f"{hub.name} L1 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L1_current_building

class L2CurrentBuilding(MetronEVBaseEntity, SensorEntity):
    """Metron station building phase 2 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L2_current_building"
        self._attr_name = f"{hub.name} L2 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L2_current_building

class L3CurrentBuilding(MetronEVBaseEntity, SensorEntity):
    """Metron station building phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_L3_current_building"
        self._attr_name = f"{hub.name} L3 building current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L3_current_building

class HouseEnergy(MetronEVBaseEntity, SensorEntity):
    """Metron station building phase 3 current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_house_energy"
        self._attr_name = f"{hub.name} house energy"
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.House_energy

class L1CurrentSolar(MetronEVBaseEntity, SensorEntity):
    """Metron solar current."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_current"
        self._attr_name = f"{hub.name} solar current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.L1_current_solar

class ButtonSetChargingCurrent(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_button_set_current"
        self._attr_name = f"{hub.name} button set current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.button_set_charging_current

class MainFuseRating(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_main_fuse"
        self._attr_name = f"{hub.name} main fuse rating"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.main_fuse_rating

class DynamicChargingCurrentLimit(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_dynamic_charging_current_limit"
        self._attr_name = f"{hub.name} dynamic charging current limit"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.dynamic_charging_current_limit

class SolarChargingEnable(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_charging_enable"
        self._attr_name = f"{hub.name} solar charging enable"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 1:
            return "Solar charging OFF"
        elif int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 0:
            return "Solar charging activated"
        else:
            return "Solar charging activated by switch"

class SolarChargingEnableShort(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_charging_enable_short"
        self._attr_name = f"{hub.name} solar charging state"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 1:
            return "OFF"
        elif int(self._hub.solar_charging_enable) == 1 and int(self._hub.solar_charging_enable_esp) == 0:
            return "ON"
        else:
            return "ON"

class TotalChargingPower(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_total_charging_power"
        self._attr_name = f"{hub.name} total charging power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_charging_power

class TotalHousePower(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_total_house_power"
        self._attr_name = f"{hub.name} total house power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_house_power

class TotalSolarPower(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_total_solar_power"
        self._attr_name = f"{hub.name} total solar power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.total_solar_power

class ThisChargeEnergy(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_this_charge_energy"
        self._attr_name = f"{hub.name} this charge energy"
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.this_charge_energy

class ChargingTime(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_charging_time"
        self._attr_name = f"{hub.name} charging time"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        charging_time = (int(self._hub.hour_counter)*60)+int(self._hub.minute_counter)
        return charging_time

class PreviousChargeEnergy(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_previous_charge_energy"
        self._attr_name = f"{hub.name} previous charge energy"
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.previous_charge_energy

class LifetimeEnergy(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_lifetime_energy"
        self._attr_name = f"{hub.name} lifetime energy"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.lifetime_energy

class SolarEnergy(MetronEVBaseEntity, SensorEntity):
    """Metron solar energy lifetime counter."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_energy"
        self._attr_name = f"{hub.name} solar energy"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.solar_energy

class SolarSURPLUSPower(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_SURPLUS_power"
        self._attr_name = f"{hub.name} solar SURPLUS power"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.solar_SURPLUS_power

class LocalNetworkIPString(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_local_network_IP_string"
        self._attr_name = f"{hub.name} local network IP string"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""

        return self._hub.local_network_IP_string

class TimerDelay(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_ESP32_timer_delay"
        self._attr_name = f"{hub.name} timer delay"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION

    @property
    def state(self) -> int:
        """Return the state of the sensor."""

        return int(self._hub.ESP32_timer_delay)

class SignalPresent(MetronEVBaseEntity, SensorEntity):
    """Metron station status entity."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_HC12_Signal_Present"
        self._attr_name = f"{hub.name} Telemetry Signal Present"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if int(self._hub.HC12_Signal_Present) == 1:
            return "Good"
        else:
            return "No signal"

class MessageFormat(MetronEVBaseEntity, SensorEntity):
    """Reports the websocket message format detected from the charger firmware."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_message_format"
        self._attr_name = f"{hub.name} message format"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def state(self) -> str:
        """Return the detected message format: json, legacy, or unknown."""
        return self._hub.message_format


# --- Diagnostic sensors below: parsed from the protocol but not yet exposed.
# Disabled by default (opt-in via entity settings) since usefulness/units of
# several of these are not fully confirmed. See issue #65 discussion.

class FirmwareVersion(MetronEVBaseEntity, SensorEntity):
    """Metron Charge Control firmware version."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_firmware_version"
        self._attr_name = f"{hub.name} firmware version"

    @property
    def state(self) -> str | None:
        """Return the firmware version, or None on legacy (pre-JSON) firmware."""
        return self._hub.metron_charge_control_version


class InternalTemperature(MetronEVBaseEntity, SensorEntity):
    """Raw internal temperature sensor reading; unit/scale not confirmed from the protocol."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_internal_temperature_raw"
        self._attr_name = f"{hub.name} internal temperature (raw)"

    @property
    def state(self) -> int | None:
        """Return the raw sensor value; unit unconfirmed from the protocol."""
        return self._hub.temperature_sens_read


class SolarPhases(MetronEVBaseEntity, SensorEntity):
    """Configured number of solar phases."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_solar_phases"
        self._attr_name = f"{hub.name} solar phases"

    @property
    def state(self) -> int:
        """Return the configured number of solar phases."""
        return self._hub.solar_phases


class HousePhases(MetronEVBaseEntity, SensorEntity):
    """Configured number of house phases."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_house_phases"
        self._attr_name = f"{hub.name} house phases"

    @property
    def state(self) -> int:
        """Return the configured number of house phases."""
        return self._hub.house_phases


class CarPhases(MetronEVBaseEntity, SensorEntity):
    """Configured number of car phases."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_car_phases"
        self._attr_name = f"{hub.name} car phases"

    @property
    def state(self) -> int:
        """Return the configured number of car phases."""
        return self._hub.car_phases


class SinceLastResetEnergy(MetronEVBaseEntity, SensorEntity):
    """Energy counter since its last reset."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_since_last_reset_energy"
        self._attr_name = f"{hub.name} energy since last reset"
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY

    @property
    def state(self) -> int:
        """Return the energy counter since its last reset."""
        return self._hub.since_last_reset_energy


class StationId(MetronEVBaseEntity, SensorEntity):
    """Station identifier."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_station_id"
        self._attr_name = f"{hub.name} station ID"

    @property
    def state(self) -> int | None:
        """Return the station identifier, or None on legacy (pre-JSON) firmware."""
        return self._hub.id_station


class NumberOfStations(MetronEVBaseEntity, SensorEntity):
    """Number of stations reported by the charger."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_number_of_stations"
        self._attr_name = f"{hub.name} number of stations"

    @property
    def state(self) -> int:
        """Return the number of stations reported by the charger."""
        return self._hub.number_of_stations


class ChargingCableMaxCurrent(MetronEVBaseEntity, SensorEntity):
    """Charging cable's maximum current rating."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_charging_cable_max_current"
        self._attr_name = f"{hub.name} charging cable max current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> int:
        """Return the charging cable's maximum current rating."""
        return self._hub.charging_cable_max_current


class Vreg1SetChargingCurrent(MetronEVBaseEntity, SensorEntity):
    """Vreg1 set charging current."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_vreg1_set_charging_current"
        self._attr_name = f"{hub.name} Vreg1 set charging current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> int:
        """Return the Vreg1 set charging current."""
        return self._hub.vreg1_set_charging_current


class Vreg2SetChargingCurrent(MetronEVBaseEntity, SensorEntity):
    """Vreg2 set charging current."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_vreg2_set_charging_current"
        self._attr_name = f"{hub.name} Vreg2 set charging current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> int:
        """Return the Vreg2 set charging current."""
        return self._hub.vreg2_set_charging_current


class StationMaxChargingCurrent(MetronEVBaseEntity, SensorEntity):
    """Station's maximum charging current."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_station_max_charging_current"
        self._attr_name = f"{hub.name} station max charging current"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def state(self) -> int:
        """Return the station's maximum charging current."""
        return self._hub.station_max_charging_current


class FrontButtonState(MetronEVBaseEntity, SensorEntity):
    """Front button raw value; exact semantics unconfirmed."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_front_button"
        self._attr_name = f"{hub.name} front button"

    @property
    def state(self) -> int | None:
        """Return the raw front button value; exact semantics unconfirmed."""
        return self._hub.front_button


class DynamicChargingEnableFlag(MetronEVBaseEntity, SensorEntity):
    """Dynamic charging enable flag; not a plain boolean, exact values unconfirmed."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_dynamic_enable"
        self._attr_name = f"{hub.name} dynamic charging enable flag"

    @property
    def state(self) -> int:
        """Return the raw flag value; exact meaning of each value unconfirmed."""
        return self._hub.dynamic_enable


class GridPowerLimit(MetronEVBaseEntity, SensorEntity):
    """Grid power limit setting; unit not confirmed from the protocol."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_p_grid_limit"
        self._attr_name = f"{hub.name} grid power limit"

    @property
    def state(self) -> int | None:
        """Return the raw grid power limit value; unit unconfirmed from the protocol."""
        return self._hub.p_grid_limit


class GridSystem(MetronEVBaseEntity, SensorEntity):
    """Grid system code; meaning unconfirmed from the protocol."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_grid_system"
        self._attr_name = f"{hub.name} grid system"

    @property
    def state(self) -> int | None:
        """Return the raw grid system code; meaning unconfirmed from the protocol."""
        return self._hub.grid_system


class KwhLimitSlider(MetronEVBaseEntity, SensorEntity):
    """kWh limit slider setting."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)
        self._attr_unique_id = f"{hub.name}_kwh_limit_slider"
        self._attr_name = f"{hub.name} kWh limit slider"
        self._attr_native_unit_of_measurement = "kWh"

    @property
    def state(self) -> int | None:
        """Return the raw kWh limit slider value."""
        return self._hub.kwh_limit_slider
