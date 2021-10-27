"""
Script file: const.py
Created on: Oct 19, 2021
Last modified on: Oct 27, 2021

Comments:
    Constants for the KCS TraceME N1Cx integration
"""

DOMAIN = "kcs_n1cx"
DATA_LISTENER = "listener"

# config options
CONF_GAS = "gas"
CONF_TEMPERATURE = "temperature"
CONF_HUMIDITY = "humidity"
CONF_PRESSURE = "pressure"
CONF_AIR_QUALITY = "air_quality"
CONF_BATTERY = "battery"
CONF_ALL = "all"

# properties
PLATFORM = "sensor"
ATTRIBUTION = "CO2 gas PPM data from https://trace.me, delivered by KCS."
SENSOR_TYPE = "usage"
ICON = "mdi:flash"

# default values
DEFAULT_NAME = "CO2 Level"
DEFAULT_DEVICE_TYPE = "Not specified"
DEFAULT_GAS = True
DEFAULT_TEMPERATURE = False
DEFAULT_HUMIDITY = False
DEFAULT_PRESSURE = False
DEFAULT_AIR_QUALITY = False
DEFAULT_BATTERY = False
DEFAULT_ALL = False

# attributes
ATTR_DEVICE_TYPE = "Device type"

