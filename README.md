# KCS TraceME N1Cx

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub](https://img.shields.io/github/license/smartechru/kcs-n1cx)](LICENSE)
[![GitHub Release (latest by date)](https://img.shields.io/github/v/release/smartechru/kcs-n1cx)](https://github.com/smartechru/kcs-n1cx/releases)
![GitHub Release Date](https://img.shields.io/github/release-date/smartechru/kcs-n1cx)
[![GitHub Issues](https://img.shields.io/github/issues/smartechru/kcs-n1cx)](https://github.com/smartechru/kcs-n1cx/issues)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg)](https://github.com/smartechru/kcs-n1cx/graphs/commit-activity)

The **KCS TraceME N1Cx** component is a Home Assistant custom sensor which provides access to historic CO2 gas PPM data and other information.

## TABLE OF CONTENTS

* [Installation](#installation)
* [Configuration](#configuration)
  * [Config Flow](#config-flow)
  * [Configuration Parameters](#configuration-parameters)
* [State](#state)

## INSTALLATION

This integration is able to install via HACS.

1. Ensure that [HACS](https://custom-components.github.io/hacs/) is installed.
2. Search for and install the **KCS TraceME N1Cx** integration.
3. Configure the **KCS TraceME N1Cx** sensor.
4. Restart Home Assistant.

## CONFIGURATION

**KCS TraceME N1Cx** can be configured on the integrations menu or in configuration.yaml

### CONFIG FLOW

In Configuration/Integrations click on the **<+>** button, select **KCS TraceME N1Cx** and configure the options on the form.

### configuration.yaml

Add **KCS TraceME N1Cx** sensor in your `configuration.yaml`.

```yaml
# Example configuration.yaml entry

kcs_n1cx:
  name: 'CO2 Level'
  dev_eui: '7CC6C42900010851'
  gas: true

```

Optional arguments (Future version):

```yaml
kcs_n1cx:
  name: 'CO2 Level'
  ...
  tempertaure: false    # temperature disabled
  humidity: false       # humidity disabled
  pressure: true        # pressure enabled
  air_quality: false    # air quality disabled
  battery: true         # battery level enabled
  all: false            # all features disabled

```

### CONFIGURATION PARAMETERS

| Parameter | Optional | Description |
|:--------- | -------- | ----------- |
| `name` | Yes | Sensor name |
| `dev_eui` | No | LoraWAN DevEUI |
| `gas` | No | CO2 gas ppm feature enable/disable flag (default: `true`) |
| `temperature` | Yes | Temperature feature enable/disable flag (default: `false`) |
| `humidity` | Yes | Humidity feature enable/disable flag (default: `false`) |
| `pressure` | Yes | Pressure feature enable/disable flag (default: `false`) |
| `air_quality` | Yes | Air quality feature enable/disable flag (default: `false`) |
| `battery` | Yes | Battery level feature enable/disable flag (default: `false`) |
| `all` | Yes | All features enable/disable flag (default: `false`) |

## STATE

Returns values for the specified utility (e.g. CO2 gas, temperature, humitidy, etc.)
