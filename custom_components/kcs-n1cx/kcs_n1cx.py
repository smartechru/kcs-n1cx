"""
Script file: kcs_n1cx.py
Created on: Jan Oct 19, 2021
Last modified on: Oct 21, 2021

Comments:
    KCS TraceME N1Cx data api functions
"""

import re
import json
import logging
import requests

_LOGGER = logging.getLogger(__name__)


class StatusCode:
    ST_OK = 200
    ST_CREATED = 201
    ST_BAD_REQUEST = 400
    ST_FORBIDDEN = 403
    ST_NOT_FOUND = 404


class KCSTraceMeN1CxDataClient:
    """
    Provides a RESTful API that can access the payload data
    processed into an easy to consume format.
    """

    def __init__(self):
        """
        Initialize data api client.
        :param: none
        :return: none
        """
        self.url = 'https://www.qontrol-vision.com/rak_forward_receive_7258/7cc6c42900010851.payloads'

    def call_api(self, gas_enabled=True, payload=None, tag=None):
        """
        KCS TraceME N1Cx API call base function.
        :param gas_enabled: CO2 gas PPM feature enable/disable flag
        :param payload: payload data for GET request
        :param tag: tag for debug
        :return: response of API request
        """
        # call api
        data = None
        response = requests.get(self.url, params=payload)

        # fetch data from response object
        if response.status_code in [StatusCode.ST_OK]:
            try:
                data = json.loads(response.text)
            except ValueError:
                data = response.text

            # logging response data
            if tag is not None:
                _LOGGER.debug(f"[{tag}] Response: {data}")
        else:
            # logging error
            if tag is not None:
                _LOGGER.warning(f"[{tag}] Invalid API request: {response.status_code}")

        return data

    def get_valid_date(self, start, end):
        """
        Validate given date/time objects using regex.
        :param start: start date/time of the period, in the format YYYYMMDDHHmm
        :param end: end date/time of the period, in the format YYYYMMDDHHmm
        :return: valid payload data
        """
        payload = None

        # with query params
        if start and end:
            # start date/time validation and exception handler
            if not re.search(r'[0-9]{12}', start):
                raise ValueError("Invalid value for `start`, must conform to the pattern `YYYYMMDDHHmm`")

            # end date/time validation and exception handler
            if not re.search(r'[0-9]{12}', end):
                raise ValueError("Invalid value for `end`, must conform to the pattern `YYYYMMDDHHmm`")

            # n3rgy data api request with query params
            payload = {
                "start": start,
                "end": end
            }

        # return valid payload
        return payload

    def read_data(self, gas_enabled, start, end):
        """
        Returns raw values of the payload published in the given URL.
        Accepts as optional parameters a start date/time, an end date/time.
        :param gas_enabled: CO2 gas PPM feature enable/disable flag
        :param start: start date/time of the period, in the format YYYYMMDDHHmm
        :param end: end date/time of the period, in the format YYYYMMDDHHmm
        :return: raw data
        """
        payload = self.get_valid_date(start, end)
        return self.call_api(gas_enabled, payload=payload)
