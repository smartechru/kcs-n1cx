"""
Script file: const.py
Created on: Oct 19, 2021
Last modified on: Oct 21, 2021

Comments:
    Constants for the KCS TraceME N1Cx integration
"""

DOMAIN = "kcs_n1cx"
DATA_LISTENER = "listener"

# config options
CONF_GAS = "gas"
CONF_START = "start"
CONF_END = "end"

# properties
PLATFORM = "sensor"
ATTRIBUTION = "CO2 gas PPM data from https://trace.me, delivered by KCS."
SENSOR_TYPE = "usage"
ICON = "mdi:flash"

# default values
DEFAULT_NAME = "CO2 Level"
DEFAULT_GAS = True
DEFAULT_DEVICE_TYPE = "Not specified"

# attributes
ATTR_START_DATETIME = "Start datetime"
ATTR_END_DATETIME = "End datetime"
ATTR_DEVICE_TYPE = "Smart meter type"

# date/time formatter
INPUT_DATETIME_FORMAT = "%Y%m%d%H%M"
ATTR_DATETIME_FORMAT = "%m/%d/%Y %H:%M"
