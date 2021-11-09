"""
Script file: const.py
Created on: Oct 19, 2021
Last modified on: Nov 6, 2021

Comments:
    Constants for the KCS TraceME N1Cx integration
"""

DOMAIN = "kcs_n1cx"
DATA_LISTENER = "listener"

# config options
CONF_DEV_EUI = "dev_eui"
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
DEFAULT_DEV_EUI = "7CC6C42900010851"
DEFAULT_DEVICE_TYPE = "Not specified"
DEFAULT_GAS = True
DEFAULT_TEMPERATURE = False
DEFAULT_HUMIDITY = False
DEFAULT_PRESSURE = False
DEFAULT_AIR_QUALITY = False
DEFAULT_BATTERY = False
DEFAULT_ALL = False

# attributes
ATTR_DEVICE_TYPE = "Device Type"
ATTR_TEMPERATURE = "Temperature"
ATTR_HUMIDITY = "Humidity"
ATTR_PRESSURE = "Pressure"
ATTR_AIR_QUALITY = "Air Quality"
ATTR_BATTERY = "Battery"
