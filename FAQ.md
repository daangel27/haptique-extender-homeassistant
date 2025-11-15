# Frequently Asked Questions (FAQ)

## Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Device & Connection](#device--connection)
- [IR Learning](#ir-learning)
- [Command Sending](#command-sending)
- [Database & Storage](#database--storage)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## General Questions

### What is Haptique Extender?

Haptique Extender is a Home Assistant integration for the KINCONY KC868-AG hardware device. It enables you to learn and replay infrared (IR) remote control commands, effectively turning your Home Assistant into a universal remote control.

### What devices does it work with?

The Haptique Extender works with any device that uses infrared (IR) remote controls:
- TVs
- Air conditioners
- Fans
- Audio systems
- Projectors
- Cable/satellite boxes
- And more!

### What firmware do I need?

You need the Haptique Extender firmware from [Cantata Communication Solutions](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW). This integration is specifically designed to work with this firmware.

### Does it support RF (Radio Frequency) commands?

**Not yet.** RF command support is planned for a future release. Currently, only IR (infrared) functionality is available.

### Is this integration cloud-based?

No! The integration communicates directly with your Haptique Extender device on your local network. No cloud services are required.

## Installation & Setup

### How do I get the authentication token?

The authentication token must be obtained from the **Haptique Config mobile app**:

1. Download the Haptique Config app on your smartphone
2. Connect to your Haptique Extender device
3. The token is automatically copied to your clipboard
4. Paste this token when setting up the integration in Home Assistant

**Important:** You cannot use the integration without this token.

### Do I need to install package files?

The package files are **optional but highly recommended**. They provide:
- Pre-configured input helpers
- Useful scripts and automations
- Smart notification system
- Dashboard integration

Without package files, you can still use the integration but you'll need to create your own UI and automations.

### Can I use this with Home Assistant OS?

Yes! The integration works with:
- Home Assistant OS (recommended)
- Home Assistant Container
- Home Assistant Supervised
- Home Assistant Core

### Should I assign a static IP to my device?

**Yes, highly recommended.** Use your router's DHCP reservation feature to assign a static IP to your Haptique Extender. This prevents connection issues when the DHCP lease renews.

### Why isn't my device auto-discovered?

Auto-discovery requires:
- Both devices on the same network (or with routing between networks)
- mDNS/Zeroconf enabled on your network
- Proper network firewall settings

If auto-discovery fails, you can always configure manually with the IP address.

## Device & Connection

### How often does the integration poll the device?

The integration polls the device every **10 seconds** for status updates. This provides a good balance between responsiveness and network load.

### My device keeps disconnecting. What should I do?

Common causes and solutions:

1. **WiFi signal strength**: Check `sensor.haptique_extender_wifi_signal`
   - Solution: Move device closer to router or use WiFi extender

2. **Network congestion**: Heavy network traffic can cause issues
   - Solution: Prioritize device in router QoS settings

3. **Power issues**: Inadequate power supply
   - Solution: Use recommended power adapter

4. **Firmware issue**: Outdated firmware
   - Solution: Update to latest firmware version

### Can I use multiple Haptique Extender devices?

Yes! You can add multiple devices to Home Assistant. Each device will have its own entities and database.

### How do I change the device IP address?

If your device's IP changes:
1. Go to **Settings** → **Devices & Services**
2. Find your Haptique Extender integration
3. Click the three dots → **Configure**
4. Update the IP address

## IR Learning

### How far should the remote be from the sensor?

**Recommended distance:** 6-24 inches (15-60 cm)

- Too close: May capture noise or overflow
- Too far: May not capture signal clearly

Point the remote directly at the IR sensor for best results.

### Why isn't my IR code being captured?

Common issues:

1. **Learning mode not active**: 
   - Verify `switch.haptique_extender_ir_learning_mode` is ON
   - Or use `learn_ir_command` service

2. **Remote battery low**:
   - Replace batteries in remote

3. **Infrared interference**:
   - Avoid direct sunlight on sensor
   - Turn off other IR devices nearby

4. **Timeout expired**:
   - Default timeout is 30 seconds
   - Restart learning mode

5. **Wrong button pressed**:
   - Make sure you press the correct button
   - Press firmly and hold for 1-2 seconds

### How long does learning mode stay active?

**Default: 30 seconds** (configurable)

You can change this in the service call:
```yaml
service: haptique_extender.learn_ir_command
data:
  timeout: 60  # 60 seconds
```

### Can I learn multiple commands at once?

No, you must learn commands one at a time. Each learning session captures one command. However, the process is quick and you can learn multiple commands in succession.

### What happens to manually captured IR codes?

When you use the learning mode switch (without the `learn_ir_command` service), captured codes:
- Are stored in `sensor.haptique_extender_last_learn_ir_code`
- Trigger a `haptique_ir_captured_manual` event
- Are NOT automatically saved to the database
- Can be sent using `send_ir_code` service with the raw data

### How do I save a manually captured code?

Use the `learn_ir_command` service instead of the switch. This automatically:
- Captures the code
- Saves it to the database
- Associates it with a device and command name

## Command Sending

### Why isn't my device responding to commands?

Troubleshooting steps:

1. **Check IR LED position**: Ensure line-of-sight to device
2. **Distance**: Device should be within 20-30 feet (6-9 meters)
3. **Verify command learned**: Use `list_ir_commands` to confirm
4. **Test with original remote**: Ensure device works normally
5. **Check repeat count**: Some devices need multiple repeats
6. **Frequency**: Verify frequency matches (usually 38 kHz)

### Can I send commands to multiple devices?

Yes! You can:
- Create automation to send multiple commands in sequence
- Use script to send commands to different devices
- Create scenes that include IR commands

Example:
```yaml
script:
  movie_mode:
    sequence:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv_living_room"
          command_name: "power"
      - delay: "00:00:01"
      - service: haptique_extender.send_ir_command
        data:
          device_id: "amplifier"
          command_name: "power"
```

### How fast can I send commands?

It's recommended to add a small delay (1-2 seconds) between commands to ensure the receiving device processes each command properly.

### Can I repeat a command automatically?

Yes! Use the `repeat` parameter:

```yaml
service: haptique_extender.send_ir_code
data:
  raw_data: [...]
  repeat: 3  # Send 3 times
```

## Database & Storage

### Where is the IR command database stored?

Location: `/config/haptique_ir_devices.json`

This is a JSON file that stores all your learned devices and commands.

### Should I backup the database?

**Yes, highly recommended!** Include `/config/haptique_ir_devices.json` in your regular Home Assistant backups.

### Can I edit the database manually?

While possible, it's **not recommended**. Use the integration's services instead:
- `list_ir_devices`
- `list_ir_commands`
- `delete_ir_command`
- `delete_ir_device`

If you must edit manually:
1. Backup first
2. Validate JSON syntax
3. Restart Home Assistant after changes

### How many commands can I store?

There's no hard limit in the integration's database. However:
- The firmware has storage limits (check `sensor.haptique_extender_ir_storage_max`)
- Large databases may slow down list operations
- Recommended: Organize commands logically by device

### Can I share my learned commands with others?

Yes! You can export device configurations:

```yaml
service: haptique_extender.list_ir_devices
```

Share the device data from the database file, and others can import it.

### What's the difference between integration database and firmware storage?

- **Integration database** (`haptique_ir_devices.json`): 
  - Stores commands learned through the integration
  - Unlimited storage
  - Organized by device
  - Managed through services

- **Firmware storage**:
  - Limited slots (typically 50)
  - Accessed via firmware API
  - Monitored by `sensor.haptique_extender_ir_commands_stored`

## Troubleshooting

### How do I enable debug logging?

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.haptique_extender: debug
```

Then restart Home Assistant and check logs.

### Where do I find the logs?

**Settings** → **System** → **Logs**

Or check the log file: `/config/home-assistant.log`

### The integration isn't loading. What should I check?

1. **Verify installation**:
   ```bash
   ls -la /config/custom_components/haptique_extender/
   ```

2. **Check manifest.json** exists

3. **Check Home Assistant logs** for errors

4. **Clear browser cache** (Ctrl+F5)

5. **Restart Home Assistant**

### Notifications aren't appearing. Why?

Ensure you have:
1. Installed the notification package file
2. Restarted after installing packages
3. No errors in automation configuration

Check: **Settings** → **Automations & Scenes** → Look for "Haptique" automations

### Entity names don't match the examples. Why?

Entity names are based on your device's **hostname**. If your device hostname is "haptique-extender-2", entities will be:
- `sensor.haptique_extender_2_firmware_version`
- `switch.haptique_extender_2_ir_learning_mode`

This is normal and expected.

## Advanced Usage

### Can I use this in Node-RED?

Yes! You can call all services from Node-RED using the "call service" node with `haptique_extender.*` services.

### Can I integrate with voice assistants?

Yes! Create scripts that call the services, then expose those scripts to:
- Google Assistant (via Home Assistant Cloud or manual setup)
- Alexa (via Home Assistant Cloud)
- Siri (via HomeKit integration)

Example:
```yaml
script:
  turn_on_tv:
    alias: "Turn On TV"
    sequence:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "living_room_tv"
          command_name: "power"
```

Then: "Hey Google, turn on TV"

### Can I create command macros/sequences?

Yes! Use scripts or automations:

```yaml
script:
  netflix_mode:
    sequence:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "power"
      - delay: "00:00:02"
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "input_hdmi1"
      - delay: "00:00:01"
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "netflix"
```

### How do I create conditional automations?

Example: Only turn on AC if temperature > 25°C

```yaml
automation:
  - alias: "Auto AC On"
    trigger:
      - platform: numeric_state
        entity_id: sensor.living_room_temperature
        above: 25
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "ac_living_room"
          command_name: "power_on"
```

### Can I schedule commands?

Yes! Use time-based automations:

```yaml
automation:
  - alias: "Turn off TV at midnight"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "power"
```

### How do I monitor command success/failure?

Listen to events in automations:

```yaml
automation:
  - alias: "Command Success Notification"
    trigger:
      - platform: event
        event_type: haptique_command_sent
    action:
      - service: notify.mobile_app
        data:
          message: "Command {{ trigger.event.data.command_name }} sent!"
```

## Still Have Questions?

- Check the [Troubleshooting](README.md#troubleshooting) section
- Browse [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
- Search [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- Create a new discussion or issue if needed

---

**This FAQ is community-maintained. Contributions welcome!**
