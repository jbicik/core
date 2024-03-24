"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import logging

import socketio

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Hub:
    """Dummy hub for Hello World example."""

    manufacturer = "Infigy"

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Init dummy hub."""
        self._host = host

        self._hass = hass
        self.data = None
        self.online = False
        self._name = host
        self._id = host.lower()
        self.sensors = [
            Sensor(f"{self._id}_1", f"{self._name} 1", self),
        ]

        self.sio = socketio.AsyncClient()

        @self.sio.on("store:change")
        async def on_message(data):
            _LOGGER.debug(data)

            if data["payload"] is not None:
                self.data = data["payload"]

        @self.sio.event
        async def connect():
            _LOGGER.info("Infigy connected!")
            self.online = True

        @self.sio.event
        async def connect_error(data):
            _LOGGER.debug("The connection failed!")
            self.online = False

        @self.sio.event
        async def disconnect():
            _LOGGER.warning("Infigy disconnected!")
            self.online = False

    async def async_setup_entry(self) -> bool:
        """Async connection to the device."""
        _LOGGER.info("Connecting to %s", self._host)
        await self.sio.connect(f"http://{self._host}", socketio_path="core/socket.io")
        return True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        return True


class Sensor:
    """Dummy sensor."""

    def __init__(self, sensorid: str, name: str, hub: Hub) -> None:
        """Init dummy roller."""
        self._id = sensorid
        self.hub = hub
        self.name = name
