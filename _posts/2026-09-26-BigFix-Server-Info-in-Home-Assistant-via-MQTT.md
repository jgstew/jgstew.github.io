I wrote a BigFix server plugin that publishes info about a BigFix server to MQTT so that Home Assistant automatically adds it as a device.

----------

**The script is here:**  https://github.com/jgstew/besapi/blob/master/examples/bigfix_plugin_mqtt_homeassistant.py

Each run queries BigFix with **session relevance** and publishes the results to MQTT as **retained** messages:

- a Home Assistant **[MQTT discovery](https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery)** config per sensor, so the BigFix server shows up automatically as a single device, keyed by the masthead serial number and named after the masthead FQDN
- one JSON state message holding every sensor's current value, plus a **Last Update** timestamp

----------

### The result in Home Assistant:

![BigFix Server device in Home Assistant](https://jgstew.github.io/images/BigFix_HomeAssistant_MQTT_Device.png "BigFix Server device in Home Assistant")

The default sensors include Actions, Computers, Computers Not Reporting, Relevant Critical Patches, Users, and more. The sensors can be overridden with `sensors:` in the config file, where each one is just a name and a session relevance statement.

Once the data is in Home Assistant, it can be added to a dashboard or used to trigger automations, like a notification when the number of computers not reporting goes up.

### Setup:

Copy `bigfix_plugin_mqtt_homeassistant.config.example.yaml` to `bigfix_plugin_mqtt_homeassistant.config.yaml` next to the script and fill in the MQTT broker and credentials.

Then run it with [uv](https://docs.astral.sh/uv/), which handles the requirements automatically, using the inline script metadata at the top of the script:

    uv run bigfix_plugin_mqtt_homeassistant.py -r https://localhost:52311/api -u API_USER -p API_PASSWORD

Or leave off the `-r`, `-u`, and `-p` arguments to use a besapi config file instead. It can also be run as a **BigFix Server Plugin Service** on the root server, in which case a plaintext MQTT password in the config file is replaced with an encrypted one after the first successful publish.
