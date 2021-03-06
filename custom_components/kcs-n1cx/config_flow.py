"""
Script file: config_flow.py
Created on: Oct 19, 2021
Last modified on: Nov 2, 2021

Comments:
    Config flow for KCS TraceME N1Cx
"""

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (
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

    DEFAULT_NAME,
    DEFAULT_DEV_EUI,
    DEFAULT_GAS,

    DOMAIN
)

_LOGGER = logging.getLogger(__name__)


class KCSTraceMeN1CxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for KCS TraceME N1Cx"""

    VERSION = 1.0
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """
        Handle a flow initialized by the user
        :param user_input: user input
        :return: config form
        """
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            try:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # schema
        config = {
            vol.Required(CONF_DEV_EUI, default=DEFAULT_DEV_EUI): str,
            vol.Required(CONF_GAS, default=DEFAULT_GAS): bool,
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(config),
            errors=errors
        )

    async def async_step_import(self, import_config):
        """
        Import from config
        :param import_config: import config values
        :return: config form
        """
        # validate config values
        return await self.async_step_user(user_input=import_config)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """
        Options callback for KCS TraceME N1Cx data
        :param config_entry: config entry
        :return: option form
        """
        return KCSTraceMeN1CxOptionsFlow(config_entry)


class KCSTraceMeN1CxOptionsFlow(config_entries.OptionsFlow):
    """Config flow options for KCS TraceME N1Cx"""

    def __init__(self, config_entry):
        """
        Initialize KCS TraceME N1Cx options flow
        :param config_entry: config entry
        :return: none
        """
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """
        Manage the options
        :param user_input: user input
        :return: option form
        """
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """
        Handle a flow initialized by the user
        :param user_input: user input
        :return: option form
        """
        errors = {}

        if user_input is not None:
            try:
                return self.async_create_entry(
                    title="",
                    data=user_input
                )
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # schema
        config = {
            vol.Optional(CONF_DEV_EUI, default=self.config_entry.options.get(CONF_DEV_EUI)): str,
            vol.Optional(CONF_TEMPERATURE, default=self.config_entry.options.get(CONF_TEMPERATURE)): bool,
            vol.Optional(CONF_HUMIDITY, default=self.config_entry.options.get(CONF_HUMIDITY)): bool,
            vol.Optional(CONF_PRESSURE, default=self.config_entry.options.get(CONF_PRESSURE)): bool,
            vol.Optional(CONF_AIR_QUALITY, default=self.config_entry.options.get(CONF_AIR_QUALITY)): bool,
            vol.Optional(CONF_BATTERY, default=self.config_entry.options.get(CONF_BATTERY)): bool,
            vol.Optional(CONF_ALL, default=self.config_entry.options.get(CONF_ALL)): bool,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(config),
            errors=errors
        )
