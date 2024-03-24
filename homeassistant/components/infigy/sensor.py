"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]
    # TODO: remove the loop
    sensor = hub.sensors[0]
    # async_add_entities(InfigySensorBoilerTemp(sensor) for sensor in hub.sensors)
    async_add_entities(
        [
            InfigySensorBoilerTemp(sensor),
            InfigySensorBoilerPower(sensor),
            InfigySensorBoilerEnergy(sensor),
        ]
    )


class InfigySensorBoilerTemp(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Boiler Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1

    def __init__(self, sensor) -> None:
        """Initialize the sensor."""
        # Usual setup is done here. Callbacks are added in async_added_to_hass.
        self._hub = sensor.hub
        self._name = sensor.name

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self._hub.online:
            self._attr_native_value = self._hub.data["HW_TEMP"]
        else:
            self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "100.100.1.2_2")},
            # If desired, the name for the device could be different to the entity
            "name": self._attr_name,
        }


class InfigySensorBoilerPower(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Boiler Power"
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1

    def __init__(self, sensor) -> None:
        """Initialize the sensor."""
        # Usual setup is done here. Callbacks are added in async_added_to_hass.
        self._hub = sensor.hub
        self._name = sensor.name

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self._hub.online:
            self._attr_native_value = self._hub.data.get("HW_ACTUAL_POWER", 0)
        else:
            self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "100.100.1.2_1")},
            # If desired, the name for the device could be different to the entity
            "name": self._attr_name,
        }


class InfigySensorBoilerEnergy(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Boiler Total Energy"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL
    _attr_suggested_display_precision = 1

    def __init__(self, sensor) -> None:
        """Initialize the sensor."""
        # Usual setup is done here. Callbacks are added in async_added_to_hass.
        self._hub = sensor.hub
        self._name = sensor.name

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self._hub.online:
            self._attr_native_value = self._hub.data.get(
                "HW_ENERGY_PRODUCED_TOTAL", None
            )
        else:
            self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "100.100.1.2_3")},
            # If desired, the name for the device could be different to the entity
            "name": self._attr_name,
        }
