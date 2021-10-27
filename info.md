## CONFIGURATION

**KCS TraceME N1Cx** can be configured on the integrations menu or in configuration.yaml

### Config flow

In Configuration/Integrations click on the **<+>** button, select **KCS TraceME N1Cx** and configure the options on the form.

### Example configuration.yaml

Add **KCS TraceME N1Cx** sensor in your `configuration.yaml`.

```yaml
# Example configuration.yaml entry

kcs_n1cx:
  name: 'CO2 Level'
  gas: true

```

Optional arguments (Not implemented yet):

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

### Parameters

| Parameter | Optional | Description |
|:--------- | -------- | ----------- |
| `name` | Yes | Sensor name |
| `gas` | No | CO2 gas PPM feature enable/disable flag (default: `true`) |
| `temperature` | Yes | Temperature feature enable/disable flag (default: `false`) |
| `humidity` | Yes | Humidity feature enable/disable flag (default: `false`) |
| `pressure` | Yes | Pressure feature enable/disable flag (default: `false`) |
| `air_quality` | Yes | Air quality feature enable/disable flag (default: `false`) |
| `battery` | Yes | Battery level feature enable/disable flag (default: `false`) |
| `all` | Yes | All features enable/disable flag (default: `false`) |
