"""
Script file: sensor.py
Created on: Oct 19, 2021
Last modified on: Oct 21, 2021

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
    CONF_GAS,
    CONF_START,
    CONF_END,

    PLATFORM,
    ATTRIBUTION,
    SENSOR_TYPE,
    ICON,

    DEFAULT_NAME,
    DEFAULT_GAS,
    DEFAULT_DEVICE_TYPE,

    INPUT_DATETIME_FORMAT,
    ATTR_DATETIME_FORMAT,

    ATTR_START_DATETIME,
    ATTR_END_DATETIME,
    ATTR_DEVICE_TYPE,
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
        :return: CO2 gas PPM data
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
    device_type = None
    api = KCSTraceMeN1CxDataClient()
    coordinator, sensor_name, device_type = await async_initialize()

    # add sensor
    async_add_entities([KCSTraceMeN1CxSensor(coordinator, sensor_name, device_type)], False)


def get_device_info(api, config_entry):
    """
    Get sensor information
    :param api: KCS TraceME N1Cx client
    :param config_entry: config entry
    :return: (device name, smarte meter type)
    """
    gas_enabled = False
    sensor_name = DEFAULT_NAME

    # check the input data
    if config_entry.data:
        gas_enabled = config_entry.data.get(CONF_GAS)
        sensor_name = config_entry.data.get(CONF_NAME)

    # get device type
    device_type = None
    return (sensor_name, device_type)


def decode_payload(api, config_entry):
    """
    List consumption values for an utility type on the provided accessible property, within a certain time frame
    :param api: KCS TraceME N1Cx api client
    :param config_entry: config entry
    :return: consumption data list
    """
    # read the configuration data
    gas_enabled = DEFAULT_GAS
    start = None
    end = None

    # check options
    if config_entry.options:
        gas_enabled = config_entry.options.get(CONF_GAS)
        start = config_entry.options.get(CONF_START)
        end = config_entry.options.get(CONF_END)

    # get power consumption data
    data = None
    try:
        data = api.parse_data(gas_enabled, start, end)
        _LOGGER.info(f"[READ_CONSUMPTION] Grabbed CO2 gas PPM data: ({start}-{end})")
    except ValueError as err:
        _LOGGER.warning(f"[READ_CONSUMPTION] Error: {str(err)}")
    finally:
        return data


class KCSTraceMeN1CxSensor(Entity):
    """Implementation of a sensor"""

    def __init__(self, coordinator, sensor_name, device_type):
        """
        Initialize sensor class
        :param coordinator: data coordinator object
        :param sensor_name: device name
        :param device_type: device type
        :return: none
        """
        self._name = sensor_name
        self._type = SENSOR_TYPE
        self._state = None
        self._coordinator = coordinator
        self._device_type = DEFAULT_DEVICE_TYPE

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
        if self._coordinator.data:
            return self._coordinator.data['unit']
        return None

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

        if not self._coordinator.data:
            return attributes

        # reformat date/time
        try:
            str_start = self._coordinator.data['start']
            str_end = self._coordinator.data['end']
            dt_start = datetime.strptime(str_start, INPUT_DATETIME_FORMAT)
            dt_end = datetime.strptime(str_end, INPUT_DATETIME_FORMAT)
            attributes[ATTR_START_DATETIME] = datetime.strftime(dt_start, ATTR_DATETIME_FORMAT)
            attributes[ATTR_END_DATETIME] = datetime.strftime(dt_end, ATTR_DATETIME_FORMAT)
        except:
            _LOGGER.warning("Failed to reformat datetime object")

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
            value_list = self._coordinator.data['values']
            values = [v['value'] for v in value_list]
            self._state = f"{sum(values):.2f}"

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
