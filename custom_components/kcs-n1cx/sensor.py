"""
Script file: sensor.py
Created on: Oct 19, 2021
Last modified on: Nov 8, 2021

Comments:
    Support for KCS TraceME N1Cx sensor
"""

import logging

from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from homeassistant.const import(
    ATTR_ATTRIBUTION,
    CONF_NAME
)
from .const import (
    CONF_DEV_EUI,
    CONF_GAS,
    CONF_TEMPERATURE,
    CONF_HUMIDITY,
    CONF_PRESSURE,
    CONF_AIR_QUALITY,
    CONF_BATTERY,
    CONF_ALL,

    PLATFORM,
    ATTRIBUTION,
    SENSOR_TYPE,
    ICON,

    DEFAULT_NAME,
    DEFAULT_DEV_EUI,
    DEFAULT_GAS,
    DEFAULT_DEVICE_TYPE,
    DEFAULT_TEMPERATURE,
    DEFAULT_HUMIDITY,
    DEFAULT_PRESSURE,
    DEFAULT_AIR_QUALITY,
    DEFAULT_BATTERY,
    DEFAULT_ALL,

    ATTR_DEVICE_TYPE,
    ATTR_TEMPERATURE,
    ATTR_HUMIDITY,
    ATTR_PRESSURE,
    ATTR_AIR_QUALITY,
    ATTR_BATTERY
)
from .kcs_n1cx import KCSTraceMeN1CxDataClient

# set scan interval as 10 mins
SCAN_INTERVAL = timedelta(seconds=600)
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """
    Set up KCS TraceME N1Cx sensor
    :param hass: hass object
    :param entry: config entry
    :return: none
    """
    # in-line function
    async def async_update_data():
        """
        Fetch data from KCS TraceME N1Cx API
        This is the place to pre-process the data to lookup tables so entities can quickly look up their data
        :param: none
        :return: json data decoded
        """
        return await hass.async_add_executor_job(decode_payload, api, entry)

    async def async_initialize():
        """
        Initialize objects from KCS TraceME N1Cx API
        :param: none
        :return: data coordinator, device type
        """
        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=PLATFORM,
            update_method=async_update_data
        )

        # fetch initial data so we have data when entities subscribe
        sensor_name, device_type = await hass.async_add_executor_job(get_device_info, api, entry)
        await coordinator.async_refresh()
        return (coordinator, sensor_name, device_type)

    # initialize KCS TraceME N1Cx API
    dev_eui = None
    if entry.data:
        dev_eui = entry.data.get(CONF_DEV_EUI, DEFAULT_DEV_EUI)

    api = KCSTraceMeN1CxDataClient(dev_eui)
    coordinator, sensor_name, device_type = await async_initialize()

    # get options
    options = None
    if entry.data:
        options = {
            "temperature": entry.data.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE),
            "humidity": entry.data.get(CONF_HUMIDITY, DEFAULT_HUMIDITY),
            "pressure": entry.data.get(CONF_PRESSURE, DEFAULT_PRESSURE),
            "air_quality": entry.data.get(CONF_AIR_QUALITY, DEFAULT_AIR_QUALITY),
            "battery": entry.data.get(CONF_BATTERY, DEFAULT_BATTERY),
            "all": entry.data.get(CONF_ALL, DEFAULT_ALL)
        }

    # add sensor
    async_add_entities([KCSTraceMeN1CxSensor(coordinator, sensor_name, device_type, options)], False)


def get_device_info(api, config_entry):
    """
    Get sensor information
    :param api: KCS TraceME N1Cx client
    :param config_entry: config entry
    :return: (device name, smarte meter type)
    """
    sensor_name = None

    # check the input data
    if config_entry.data:
        sensor_name = config_entry.data.get(CONF_NAME, DEFAULT_NAME)

    # get device type
    device_type = None
    return (sensor_name, device_type)


def decode_payload(api, config_entry):
    """
    List raw values from the given API
    :param api: KCS TraceME N1Cx api client
    :param config_entry: config entry
    :return: data list in json format
    """
    # get sensor readings
    data = None
    try:
        data = api.parse_data()
    except ValueError as err:
        _LOGGER.warning(f"[API] Error: {str(err)}")
    finally:
        return data


class KCSTraceMeN1CxSensor(Entity):
    """Implementation of a sensor"""

    def __init__(self, coordinator, sensor_name, device_type, options):
        """
        Initialize sensor class
        :param coordinator: data coordinator object
        :param sensor_name: device name
        :param device_type: device type
        :param options: option flags
        :return: none
        """
        self._name = sensor_name
        self._type = SENSOR_TYPE
        self._state = None
        self._coordinator = coordinator
        self._device_type = DEFAULT_DEVICE_TYPE
        self._options = options

        # parameter validation
        if device_type is not None:
            self._device_type = device_type

    @property
    def name(self):
        """
        Return the name of the sensor
        :param: none
        :return: sensor name
        """
        return self._name

    @property
    def unique_id(self):
        """
        Return sensor unique id
        :param: none
        :return: unique id
        """
        return self._type

    @property
    def state(self):
        """
        Return the state of the sensor
        :param: none
        :return: sensor state
        """
        return self._state

    @property
    def icon(self):
        """
        Icon for each sensor
        :param: none
        :return: sensor icon
        """
        return ICON

    @property
    def unit_of_measurement(self):
        """
        Return the unit of measurement of this entity, if any
        :param: none
        :return: data unit
        """
        return 'PPM'

    @property
    def should_poll(self):
        """
        Need to poll.
        Coordinator notifies entity of updates
        :param: none
        :return: false
        """
        return True

    @property
    def device_state_attributes(self):
        """
        Return the state attributes
        :param: none
        :return: state attributes
        """
        attributes = {
            ATTR_DEVICE_TYPE: self._device_type,
            ATTR_ATTRIBUTION: ATTRIBUTION
        }

        if self._coordinator.data and self._options:
            """
            if self._options.get('temperature'):
                attributes[ATTR_TEMPERATURE] = f"{self._coordinator.data.get('temperature'):.2f} °C",
            if self._options.get('humidity'):
                attributes[ATTR_HUMIDITY] = f"{self._coordinator.data.get('humidity'):.2f} %"
            if self._options.get('pressure'):
                attributes[ATTR_PRESSURE] = f"{self._coordinator.data.get('pressure'):.2f} hPa"
            if self._options.get('air_quality'):
                attributes[ATTR_AIR_QUALITY] = self._coordinator.data.get('air_quality')
            if self._options.get('battery'):
                attributes[ATTR_BATTERY] = f"{self._coordinator.data.get('battery'):.3f} V"
            """
            attributes[ATTR_TEMPERATURE] = f"{self._coordinator.data.get('temperature'):.2f} °C",
            attributes[ATTR_HUMIDITY] = f"{self._coordinator.data.get('humidity'):.2f} %"
            attributes[ATTR_PRESSURE] = f"{self._coordinator.data.get('pressure'):.2f} hPa"
            attributes[ATTR_AIR_QUALITY] = self._coordinator.data.get('air_quality')
            attributes[ATTR_BATTERY] = f"{self._coordinator.data.get('battery'):.3f} V"

        return attributes

    @property
    def available(self):
        """
        Return if entity is available
        :param: none
        :return: true is sensor is available, false otherwise
        """
        return self._coordinator.last_update_success

    def update_state(self):
        """
        Calculate the consumption data
        :param: none
        :return: none
        """
        if self._coordinator.data:
            # get consumption value
            value = self._coordinator.data.get('co2')
            self._state = f"{value:.2f}"

    async def async_added_to_hass(self):
        """
        When entity is added to hass
        :param: none
        :return: none
        """
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )
        self.update_state()

    async def async_update(self):
        """
        Update the entity
        Only used by the generic entity update service
        :param: none
        :return: none
        """
        _LOGGER.info("[ENTITY] Async updated")
        await self._coordinator.async_request_refresh()
        self.update_state()
