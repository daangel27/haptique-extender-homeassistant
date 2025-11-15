# Quick Start Guide - Haptique Extender

Get up and running with Haptique Extender in minutes!

## Prerequisites Checklist

- [ ] Haptique Extender (KC868-AG) with firmware installed
- [ ] Device connected to your WiFi network
- [ ] **Haptique Config mobile app** installed
- [ ] Authentication token copied from mobile app
- [ ] Home Assistant 2023.1+ running

## 5-Minute Setup

### Step 1: Install Integration (2 minutes)

**Via HACS (Recommended):**
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/daangel27/haptique-extender-homeassistant`
3. Search "Haptique Extender" → Download
4. Restart Home Assistant

**Or Manual:**
1. Download latest release
2. Extract to `/config/custom_components/haptique_extender/`
3. Restart Home Assistant

### Step 2: Get Your Token (1 minute)

1. Open **Haptique Config** app on your phone
2. Connect to your device
3. Token is auto-copied to clipboard
4. Keep it handy for next step

### Step 3: Add Device (1 minute)

1. **Settings** → **Devices & Services**
2. Click discovered device (or + Add Integration)
3. Paste your token
4. Click Submit

✅ **Done!** Your device is now connected.

### Step 4: Install Packages (1 minute) - Optional but Recommended

1. Edit `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

2. Create `/config/packages/` folder

3. Copy these files to packages:
   - `haptique_extender_input_en.yaml`
   - `haptique_extender_script_en.yaml`
   - `haptique_extender_automation_en.yaml`
   - `haptique_extender_notifications_en.yaml`

4. Restart Home Assistant

## Quick Learning Tutorial

### Learn Your First Command (30 seconds)

**Method 1: Using Service (Recommended)**

1. Go to **Developer Tools** → **Services**
2. Select: `haptique_extender.learn_ir_command`
3. Fill in:
   ```yaml
   device_id: "living_room_tv"
   device_name: "Living Room TV"
   device_type: "TV"
   command_name: "power"
   command_label: "Power On/Off"
   ```
4. Click **Call Service**
5. **Point remote at sensor** → **Press button**
6. Wait for success notification

**Method 2: Using Dashboard (if packages installed)**

1. Open your Haptique dashboard
2. Fill in the learning form
3. Click "Learn Command"
4. Point remote → Press button
5. Done!

### Send Your First Command (10 seconds)

**Via Service:**
```yaml
service: haptique_extender.send_ir_command
data:
  device_id: "living_room_tv"
  command_name: "power"
```

**Via Dashboard (if packages installed):**
1. Select device from dropdown
2. Select command from dropdown
3. Click "Send Command"

## Essential Services Quick Reference

### Learn a Command
```yaml
service: haptique_extender.learn_ir_command
data:
  device_id: "tv_samsung"
  device_name: "Samsung TV"
  device_type: "TV"
  command_name: "volume_up"
```

### Send a Command
```yaml
service: haptique_extender.send_ir_command
data:
  device_id: "tv_samsung"
  command_name: "volume_up"
```

### List All Devices
```yaml
service: haptique_extender.list_ir_devices
```

### List Device Commands
```yaml
service: haptique_extender.list_ir_commands
data:
  device_id: "tv_samsung"
```

### Delete a Command
```yaml
service: haptique_extender.delete_ir_command
data:
  device_id: "tv_samsung"
  command_name: "old_command"
```

## Key Entities

After setup, you'll have these entities (names vary by hostname):

**Monitoring:**
- `sensor.haptique_extender_firmware_version`
- `sensor.haptique_extender_wifi_signal`
- `binary_sensor.haptique_extender_wifi_connected`

**Learning:**
- `switch.haptique_extender_ir_learning_mode`
- `sensor.haptique_extender_learning_mode`
- `sensor.haptique_extender_last_learn_ir_code`

**Storage:**
- `sensor.haptique_extender_ir_commands_stored`
- `sensor.haptique_extender_ir_storage_usage`

## Quick Tips

### ✅ Best Practices

- **Assign static IP** to your device in router
- **Backup** `/config/haptique_ir_devices.json` regularly
- **Name commands clearly** (e.g., "volume_up" not "btn2")
- **Add delays** between multiple commands (1-2 seconds)
- **Hold remote close** to sensor when learning (6-24 inches)

### ⚠️ Common Mistakes to Avoid

- ❌ Don't use spaces in `device_id` (use underscores)
- ❌ Don't point remote too close or too far
- ❌ Don't learn in direct sunlight
- ❌ Don't forget to enable packages in configuration.yaml
- ❌ Don't manually edit database without backup

## Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Device not discovered | Add manually with IP address |
| Learning timeout | Move remote closer, try again |
| Command not working | Check device is in line-of-sight |
| No notifications | Install notification package |
| Connection lost | Check WiFi signal, assign static IP |

## Quick Examples

### Example 1: Simple Automation
Turn on TV when arriving home:

```yaml
automation:
  - alias: "Welcome Home TV"
    trigger:
      - platform: state
        entity_id: person.your_name
        to: "home"
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "living_room_tv"
          command_name: "power"
```

### Example 2: Command Macro
Create a "Movie Mode" script:

```yaml
script:
  movie_mode:
    sequence:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "power"
      - delay: "00:00:02"
      - service: haptique_extender.send_ir_command
        data:
          device_id: "amplifier"
          command_name: "power"
      - delay: "00:00:01"
      - service: haptique_extender.send_ir_command
        data:
          device_id: "tv"
          command_name: "input_hdmi1"
```

### Example 3: Temperature-Based AC Control
Auto-start AC when hot:

```yaml
automation:
  - alias: "Auto AC"
    trigger:
      - platform: numeric_state
        entity_id: sensor.temperature
        above: 25
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_id: "bedroom_ac"
          command_name: "power_on"
```

## What's Next?

### Immediate Next Steps:
1. ✅ Learn commands for all your IR devices
2. ✅ Create a dashboard using the example
3. ✅ Set up your first automation

### Explore More:
- 📖 Read the [full README](README.md) for detailed features
- 🔧 Check [Installation Guide](INSTALLATION.md) for advanced setup
- ❓ Browse [FAQ](FAQ.md) for common questions
- 💡 Share your setups in [Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

## Need Help?

- 📚 [Full Documentation](README.md)
- ❓ [FAQ](FAQ.md)
- 🐛 [Report Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 💬 [Community Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

## Support the Project

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🤝 Contribute code

---

**Ready to learn more?** Check out the complete [README](README.md) for advanced features and detailed documentation.

**Having issues?** See [Troubleshooting](README.md#troubleshooting) or [FAQ](FAQ.md).
