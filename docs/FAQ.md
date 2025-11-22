# Frequently Asked Questions (FAQ)

## Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Learning & Commands](#learning--commands)
- [Database & Storage](#database--storage)
- [Dashboard & Interface](#dashboard--interface)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

---

## General Questions

### What is Haptique Extender?

Haptique Extender is a comprehensive Home Assistant integration for the Kincony KC868-AG device, enabling you to learn, store, and replay infrared (IR) remote control commands for home automation.

### What devices can I control?

Any device that uses infrared (IR) remote control:
- TVs (all brands)
- Set-top boxes
- Soundbars and audio systems
- Air conditioners
- DVD/Blu-ray players
- Media streaming devices
- And much more!

### Does it support RF (Radio Frequency)?

Not yet. RF support is planned for future versions. Current version only supports IR.

### Do I need the Kincony mobile app?

The mobile app is only needed during initial setup to:
- Get the authentication token
- Update firmware (if needed)

After configuration, you control everything through Home Assistant.

### Is internet connection required?

No. The integration works entirely on your local network. Internet is only needed for:
- HACS installation
- Firmware updates

---

## Installation & Setup

### What firmware version do I need?

**Minimum required**: Firmware 1.1.2

Check your current version:
1. Open Kincony mobile app
2. Connect to device
3. Check firmware version in settings

Update if needed: [KinkonyAGFW Repository](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)

### Can I install without HACS?

Yes, manual installation is possible. See [Installation Guide](INSTALLATION.md#manual-installation).

However, HACS is recommended for:
- Easy updates
- Version management
- Automatic dependency handling

### How do I get the authentication token?

1. Open Kincony mobile app
2. Connect to your KC868-AG device
3. The token is automatically copied to clipboard
4. Paste it during Home Assistant setup

**Note**: Token is device-specific and doesn't change unless you reset the device.

### Can I have multiple KC868-AG devices?

Yes! Add each device as a separate integration:
- Each will have its own database
- Separate dashboards recommended
- Commands don't overlap

### Do I need to restart HA after installation?

Yes, restart is required:
- After HACS installation
- After adding YAML files
- After changing configuration files

---

## Learning & Commands

### How does learning work?

The KC868-AG captures raw IR signals from your remote:

1. You activate learning mode
2. Point your remote at the IR sensor
3. Press the button you want to learn
4. Signal is captured and stored

The raw signal is stored, so it works even with "unknown" remotes.

### How close should I be when learning?

**Optimal distance**: 10-30 cm (4-12 inches)

- Too close (< 5 cm): May saturate sensor
- Too far (> 50 cm): May not capture reliably
- Direct line of sight required

### Why didn't it capture my button?

Common reasons:

1. **Too far**: Move closer (10-20 cm)
2. **Wrong angle**: Point directly at sensor
3. **Timeout**: Default 30 seconds, try again
4. **Interference**: Turn off other IR sources
5. **Button not held long enough**: Short, firm press

### Can I learn the same command twice?

Yes, but with caveats:

- **Same name**: Will replace the existing command
- **Different name**: Will create a new entry
- **Tip**: Use descriptive names to avoid confusion

### How many commands can I store?

**Home Assistant Database**: Unlimited (disk space limited)
**Device Firmware**: 50 commands (not used in current version)

### What's the difference between Database and Hub storage?

**Database (Home Assistant)**:
- Location: `/config/haptique_ir_database.json`
- Capacity: Unlimited
- Used for: Learning, sending, management
- Backup: Recommended

**Hub (Device Firmware)**:
- Location: KC868-AG internal memory
- Capacity: 50 commands
- Used for: Future standalone operation
- Note: Not actively used in v1.5.0

### Can I edit commands after learning?

Not directly in the UI. Options:

1. **Re-learn**: Learn again with same name
2. **Manual edit**: Edit `/config/haptique_ir_database.json` (advanced)
3. **Delete and re-learn**: Safest option

### Can I backup my commands?

Yes! **Highly recommended**:

```bash
# Backup database
cp /config/haptique_ir_database.json /config/backups/haptique_backup_$(date +%Y%m%d).json
```

Automate with a script or Home Assistant backup.

### Can I share commands with others?

Yes! The database is a JSON file containing raw IR data.

**To share**:
1. Export device from database
2. Share JSON snippet
3. Others import to their database

**Note**: Raw IR codes are device-specific but brand/model agnostic.

---

## Database & Storage

### Where is the database stored?

`/config/haptique_ir_database.json`

### What's in the database file?

JSON structure:
```json
{
  "devices": {
    "Samsung TV": {
      "created_at": "2025-01-15T10:30:00",
      "commands": {
        "power": {
          "freq_khz": 38,
          "duty": 33,
          "repeat": 1,
          "raw": [9000, 4500, ...],
          "learned_at": "2025-01-15T10:31:00"
        }
      }
    }
  }
}
```

### Can I manually edit the database?

Yes, but carefully:

1. **Backup first!**
2. Valid JSON required
3. Respect field types
4. Restart integration after editing

**Safer alternative**: Use integration services.

### What happens if I delete the database?

All learned commands are lost! **Always backup**.

To reset:
1. Stop Home Assistant
2. Delete or rename file
3. Start Home Assistant
4. Empty database created automatically

### How do I migrate to a new HA instance?

1. **Backup database**:
   ```bash
   cp /config/haptique_ir_database.json ~/
   ```

2. **Install integration on new instance**

3. **Restore database**:
   ```bash
   cp ~/haptique_ir_database.json /config/
   ```

4. **Restart Home Assistant**

---

## Dashboard & Interface

### Why are my toggles resetting?

This is **intentional behavior** for certain modes:

- **Send mode**: Both toggles → ON (must select existing)
- **Delete modes**: Toggles → ON (must select existing)
- **Learn mode**: Toggles stay as you set them (flexible)

Disable automations if you want manual control:
- `Haptique - Mode Send: Enable Existing Toggles`
- `Haptique - Mode Delete Command: Enable Existing Toggles`
- etc.

### How do I add new command to existing device?

1. Mode: **Learn**
2. **Device toggle**: ON → Select your device
3. **Command toggle**: OFF → Enter new command name
4. Execute

This is the most common workflow!

### Why don't I see my learned command?

Check:

1. **Refresh**: Click "🔄 Refresh" button
2. **Device selected**: Commands sensor needs device selected
3. **Wait**: Auto-refresh takes 2-5 seconds
4. **Verify in Database view**: Go to Database tab

### Can I customize the dashboard?

Yes! Options:

1. **Move cards**: Drag and drop in edit mode
2. **Hide sections**: Remove unwanted views
3. **Add cards**: Add your own custom cards
4. **Change colors**: Modify YAML directly

### Why don't I see the IR Learning switch?

**Intentional**: Switch is disabled by default.

The switch is for internal use. Use the dashboard for learning.

**To enable** (if needed):
1. Settings → Devices & Services → Entities
2. Search: "IR Learning Mode"
3. Enable the entity

### How do I see notifications?

Notifications appear:
- Top right corner (🔔 bell icon)
- Persistent notifications
- Mobile app (if configured)

**To enable**:
```yaml
service: input_boolean.turn_on
target:
  entity_id: input_boolean.haptique_notify_enabled
```

---

## Troubleshooting

### Integration doesn't appear after HACS install

**Try**:
1. Hard refresh browser (Ctrl+F5)
2. Restart Home Assistant
3. Check `/config/custom_components/haptique_extender/` exists
4. Verify `manifest.json` is valid

### "Cannot connect to device" error

**Check**:
1. ✅ Device powered on
2. ✅ Device on same network as HA
3. ✅ Correct IP address
4. ✅ Valid authentication token
5. ✅ Firewall not blocking port 80

**Test manually**:
```bash
curl http://DEVICE_IP/api/status
```

### Sensors show "Unavailable"

**Solutions**:
1. Check device is online: `ping DEVICE_IP`
2. Reload integration: Integrations → Haptique Extender → ⋮ → Reload
3. Check logs: Settings → System → Logs
4. Restart Home Assistant

### "Template Error" in logs

**Common cause**: Sensor attributes are None

**Solution**: Already fixed in v1.5.0. Update to latest version.

### Commands list is empty but I have devices

**Solution**:
```yaml
# Update commands sensor to show first device
service: haptique_extender.set_commands_device
data:
  device_name: "Your Device Name"
```

Or use the dashboard refresh button.

### Database file is huge

**Cause**: Many learned commands

**Solutions**:
- Delete unused commands
- Delete unused devices
- Archive old commands
- Clean raw data (advanced)

Normal size: < 1MB for 100 commands

### Learning timeout too short

**Default**: 30 seconds

**To change** (requires automation edit):
```yaml
# In learn_ir_command service call
timeout: 60  # seconds
```

---

## Advanced Usage

### Can I use this in automations?

**Yes!** All services are automation-ready:

```yaml
# Example: Turn on TV at 8 PM
automation:
  - alias: "TV On at Evening"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_name: "Living Room TV"
          command_name: "power"
```

### Can I send raw IR codes?

Yes, using `send_ir_code` service:

```yaml
service: haptique_extender.send_ir_code
data:
  raw_data: [9000, 4500, 560, 560, ...]
  freq_khz: 38
  duty: 33
  repeat: 1
```

### Can I capture IR without saving?

Yes, use the manual learning mode:
1. Enable IR Learning switch
2. Listen for `haptique_ir_captured` event
3. Process raw data as needed

### Can I create virtual remotes?

Yes! Use the `send_ir_command` service in scripts:

```yaml
script:
  tv_watch_netflix:
    sequence:
      - service: haptique_extender.send_ir_command
        data:
          device_name: "Samsung TV"
          command_name: "power"
      - delay: "00:00:02"
      - service: haptique_extender.send_ir_command
        data:
          device_name: "Samsung TV"
          command_name: "input"
      # ... more commands
```

### Can I use with Node-RED?

Yes! Call services from Node-RED:

```json
{
  "domain": "haptique_extender",
  "service": "send_ir_command",
  "data": {
    "device_name": "TV",
    "command_name": "power"
  }
}
```

### Can I integrate with voice assistants?

Yes! Create scripts/automations triggered by voice:

```yaml
# In configuration.yaml
intent_script:
  TurnOnTV:
    speech:
      text: "Turning on the TV"
    action:
      - service: haptique_extender.send_ir_command
        data:
          device_name: "Living Room TV"
          command_name: "power"
```

Then: "Hey Google, activate Turn On TV"

### Can I export/import commands between devices?

**Manual method**:
1. Copy device section from `/config/haptique_ir_database.json`
2. Paste to another installation
3. Restart integration

**Script method** (future feature):
- Export device to YAML
- Import from YAML

---

## Still Have Questions?

- 📖 [Full Documentation](DOCUMENTATION_INDEX.md)
- 💬 [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
- 🐛 [Report Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 📧 Contact: [Project Repository](https://github.com/daangel27/haptique-extender-homeassistant)

---

**Can't find your question?** [Ask in GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions) and help improve this FAQ!
