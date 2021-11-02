"""
Script file: kcs_n1cx.py
Created on: Jan Oct 19, 2021
Last modified on: Nov 2, 2021

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

    def __init__(self, dev_eui):
        """
        Initialize data api client.
        :param dev_eui: LoraWAN DevEUI (HEX)
        :return: none
        """
        self.url = f'https://www.qontrol-vision.com/rak_forward_receive_7258/{dev_eui.lower()}.payloads'

    def call_api(self, tag=None):
        """
        KCS TraceME N1Cx API call base function.
        :param tag: tag for debug
        :return: response of API request
        """
        # call api
        data = None
        response = requests.get(self.url)

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

    def parse_data(self):
        """
        Returns raw values of the payload published in the given URL.
        Accepts as optional parameters a start date/time, an end date/time.
        :param gas_enabled: CO2 gas PPM feature enable/disable flag
        :return: raw data
        """
        # payload = self.get_valid_date(start, end)
        raw_data = self.call_api()
        data_list = raw_data.splitlines()
        last_data = data_list[-1]
        raw_payload = last_data.split()[-1]

        # decode data
        payload = {
            "id": raw_payload[0:2],
            "temperature": (int(raw_payload[2:6], 16) // 100) / 10 - 15,
            "humidity": (int(raw_payload[2:6], 16) % 100),
            "co2": int(raw_payload[6:10], 16),
            "pressure": int(raw_payload[10:12], 16) + 900,
            "air_quality": int(raw_payload[12:14], 16),
            "io": int(raw_payload[14:16], 16),
            "battery": 100, # TODO
            "crc": int(raw_payload[18:22], 16),
            "fw_version": int(raw_payload[22:26], 16) / 10000.0,
            "pir_active": int(raw_payload[26:28], 16),
            "pir_bitfield": int(raw_payload[28:], 16),
        }
        return payload
