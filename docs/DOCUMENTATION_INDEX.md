# Documentation Index

Complete documentation for Haptique Extender integration.

## 📚 Documentation Structure

### Getting Started
- [README](../README.md) - Overview and features
- [Installation Guide](INSTALLATION.md) - Complete setup instructions
- [Quick Start Guide](QUICK_START.md) - Get running in 10 minutes
- [FAQ](FAQ.md) - Frequently Asked Questions

### User Guides
- [Dashboard Guide](DASHBOARD_GUIDE.md) - Using the control interface
- [Learning Guide](LEARNING_GUIDE.md) - How to learn IR commands
- [Command Management](COMMAND_MANAGEMENT.md) - Managing your IR database
- [Automation Examples](AUTOMATION_EXAMPLES.md) - Home automation ideas

### Technical Documentation
- [Architecture](ARCHITECTURE.md) - System design and components
- [API Reference](API_REFERENCE.md) - Services and entities
- [Events Reference](EVENTS_REFERENCE.md) - Event system documentation
- [Database Schema](DATABASE_SCHEMA.md) - Database structure

### Advanced Topics
- [Advanced Features](ADVANCED_FEATURES.md) - Power user features
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Development Guide](DEVELOPMENT.md) - Contributing to the project
- [Changelog](CHANGELOG.md) - Version history

---

## 🎯 Quick Navigation

### I want to...

#### Install the Integration
→ [Installation Guide](INSTALLATION.md)

#### Learn my first command
→ [Quick Start Guide](QUICK_START.md) → Section: "Your First IR Command"

#### Control my TV
→ [Quick Start Guide](QUICK_START.md) → Section: "Common Workflows"

#### Fix a problem
→ [FAQ](FAQ.md) → Section: "Troubleshooting"

#### Create automations
→ [Automation Examples](AUTOMATION_EXAMPLES.md)

#### Understand the dashboard
→ [Dashboard Guide](DASHBOARD_GUIDE.md)

#### Learn about services
→ [API Reference](API_REFERENCE.md) → Section: "Services"

#### Backup my commands
→ [FAQ](FAQ.md) → Section: "Database & Storage"

#### Contribute code
→ [Development Guide](DEVELOPMENT.md)

---

## 📖 Documentation by Topic

### Installation & Setup

| Document | Description | Difficulty |
|----------|-------------|------------|
| [Installation Guide](INSTALLATION.md) | Complete installation walkthrough | Beginner |
| [HACS Setup](INSTALLATION.md#hacs-installation) | Installing via HACS | Beginner |
| [Manual Setup](INSTALLATION.md#manual-installation) | Manual installation method | Intermediate |
| [YAML Configuration](INSTALLATION.md#yaml-files-setup) | Setting up YAML files | Beginner |
| [Dashboard Setup](INSTALLATION.md#dashboard-installation) | Installing the dashboard | Beginner |

### Basic Usage

| Document | Description | Difficulty |
|----------|-------------|------------|
| [Quick Start](QUICK_START.md) | Get started in 10 minutes | Beginner |
| [Learning Commands](LEARNING_GUIDE.md) | How to capture IR signals | Beginner |
| [Sending Commands](QUICK_START.md#step-3-send-the-command) | How to control devices | Beginner |
| [Dashboard Overview](DASHBOARD_GUIDE.md) | Understanding the interface | Beginner |
| [Operation Modes](QUICK_START.md#understanding-operation-modes) | Different modes explained | Beginner |

### Command Management

| Document | Description | Difficulty |
|----------|-------------|------------|
| [Command Management](COMMAND_MANAGEMENT.md) | Organize your commands | Beginner |
| [Deleting Commands](COMMAND_MANAGEMENT.md#deleting-commands) | Remove unwanted commands | Beginner |
| [Database Backup](FAQ.md#can-i-backup-my-commands) | Protecting your data | Intermediate |
| [Import/Export](FAQ.md#can-i-share-commands-with-others) | Sharing commands | Advanced |

### Automation & Integration

| Document | Description | Difficulty |
|----------|-------------|------------|
| [Automation Examples](AUTOMATION_EXAMPLES.md) | Ready-to-use automations | Intermediate |
| [Script Templates](AUTOMATION_EXAMPLES.md#script-templates) | Reusable scripts | Intermediate |
| [Voice Control](FAQ.md#can-i-integrate-with-voice-assistants) | Alexa/Google integration | Intermediate |
| [Node-RED](FAQ.md#can-i-use-with-node-red) | Node-RED integration | Advanced |

### Troubleshooting

| Document | Description | Difficulty |
|----------|-------------|------------|
| [FAQ](FAQ.md) | Common questions & answers | Beginner |
| [Troubleshooting Guide](TROUBLESHOOTING.md) | Detailed problem solving | Intermediate |
| [Connection Issues](TROUBLESHOOTING.md#connection-problems) | Network troubleshooting | Intermediate |
| [Learning Issues](TROUBLESHOOTING.md#learning-problems) | IR capture problems | Intermediate |

### Technical Reference

| Document | Description | Difficulty |
|----------|-------------|------------|
| [Architecture](ARCHITECTURE.md) | System design overview | Advanced |
| [API Reference](API_REFERENCE.md) | Complete API documentation | Advanced |
| [Database Schema](DATABASE_SCHEMA.md) | Database structure | Advanced |
| [Events Reference](EVENTS_REFERENCE.md) | Event system details | Advanced |
| [Development Guide](DEVELOPMENT.md) | Contributing guidelines | Advanced |

---

## 🔢 Component Reference

### Integration Components

#### Sensors (13 total)

**Device Information**:
- `sensor.haptique_extender_firmware_version` - Firmware version
- `sensor.haptique_extender_hostname` - Device hostname
- `sensor.haptique_extender_mac_address` - MAC address
- `sensor.haptique_extender_ip_address` - IP address

**Network Status**:
- `sensor.haptique_extender_wifi_ssid` - Connected WiFi network
- `sensor.haptique_extender_wifi_signal` - Signal strength (dBm)

**Storage Monitoring**:
- `sensor.haptique_extender_hub_ir_commands_stored` - Commands in firmware
- `sensor.haptique_extender_hub_ir_storage_max` - Max firmware capacity
- `sensor.haptique_extender_hub_ir_storage_usage` - Usage percentage

**Database Tracking**:
- `sensor.haptique_extender_database_ir_devices` - Device count
- `sensor.haptique_extender_database_ir_commands` - Command count (per device)

**Learning Info**:
- `sensor.haptique_extender_last_learn_ir_code` - Last captured timestamp

#### Binary Sensors (1 total)
- `binary_sensor.haptique_extender_wifi_connected` - WiFi connectivity

#### Switches (1 total)
- `switch.haptique_extender_ir_learning_mode` - Manual learning mode (disabled by default)

### YAML Components

#### Input Helpers (4 files)

**haptique_extender_input.yaml** (10 helpers):
- `input_text.haptique_device_name` - Device name input
- `input_text.haptique_command_name` - Command name input
- `input_boolean.haptique_notify_enabled` - Notifications toggle
- `input_boolean.haptique_use_existing_device` - Device selection mode
- `input_boolean.haptique_use_existing_command` - Command selection mode
- `input_select.haptique_device_selector` - Device dropdown
- `input_select.haptique_command_selector` - Command dropdown
- `input_select.haptique_operation_mode` - Operation mode selector

#### Scripts (8 total)

**haptique_extender_script.yaml**:
- `script.haptique_execute_operation` - Main operation executor
- `script.haptique_refresh_device_list` - Refresh device list
- `script.haptique_refresh_command_list` - Refresh command list
- `script.haptique_refresh_all` - Refresh all lists
- `script.haptique_clear_learn_helpers` - Clear input fields

#### Automations (7 total)

**haptique_extender_automation.yaml**:
- `automation.haptique_auto_refresh_on_device_change` - Auto-refresh on selection
- `automation.haptique_auto_refresh_on_startup` - Refresh at startup
- `automation.haptique_auto_refresh_on_db_change` - Refresh after operations
- `automation.haptique_mode_send_adjust_toggles` - Send mode toggle management
- `automation.haptique_mode_delete_command_adjust_toggles` - Delete command mode
- `automation.haptique_mode_delete_device_adjust_toggles` - Delete device mode
- `automation.haptique_mode_list_commands_adjust_toggles` - List mode

#### Templates (1 total)

**haptique_extender_template.yaml**:
- `binary_sensor.haptique_extender_notifications_enabled` - Notification status

#### Notifications

**haptique_extender_notifications.yaml**:
- Learn notifications (success, error, timeout)
- Send notifications (success, error)
- Delete notifications (success, error)
- Connection notifications (lost, restored)

### Services (7 total)

| Service | Description |
|---------|-------------|
| `send_ir_code` | Send raw IR code |
| `learn_ir_command` | Learn new IR command |
| `send_ir_command` | Send learned command |
| `delete_ir_command` | Delete specific command |
| `delete_ir_device` | Delete device and all commands |
| `set_commands_device` | Update commands sensor |
| `list_device_commands` | List device commands |

### Events (2 total)

| Event | Description |
|-------|-------------|
| `haptique_operation` | All operations (learn, send, delete, list) |
| `haptique_ir_captured` | Manual IR capture |

### Dashboard Views (5 total)

| View | Purpose |
|------|---------|
| Control | Main operation interface |
| Database | View IR command database |
| Sensors | Monitor device status |
| Settings | Configure integration |
| Help | Documentation and examples |

---

## 📊 Statistics Summary

### Component Counts

| Category | Count |
|----------|-------|
| **Sensors** | 13 |
| **Binary Sensors** | 1 |
| **Switches** | 1 |
| **Input Helpers** | 10 |
| **Scripts** | 8 |
| **Automations** | 7 |
| **Templates** | 1 |
| **Services** | 7 |
| **Events** | 2 |
| **Dashboard Views** | 5 |
| **YAML Files** | 5 |
| **Documentation Files** | 15+ |

### Code Statistics

| Metric | Value |
|--------|-------|
| Python files | 9 |
| YAML files | 5 |
| JSON files | 4 |
| Lines of code (Python) | ~3000 |
| Lines of config (YAML) | ~1200 |
| Supported devices | Any IR device |
| Database capacity | Unlimited |
| Firmware capacity | 50 commands |

---

## 🔄 Version History

### Version 1.5.0 (Current)
- Complete rewrite with unified interface
- Flexible toggle system
- Enhanced validation
- Improved naming
- Better error handling
- Template protection
- Switch hidden by default

[Full Changelog](CHANGELOG.md)

---

## 🛠️ Development Resources

### For Contributors
- [Development Setup](DEVELOPMENT.md#development-setup)
- [Coding Standards](DEVELOPMENT.md#coding-standards)
- [Testing Guidelines](DEVELOPMENT.md#testing)
- [Pull Request Process](DEVELOPMENT.md#pull-requests)

### For Users
- [Feature Requests](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- [Bug Reports](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- [Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

---

## 📞 Getting Help

### Support Channels

1. **Documentation** (Start here!)
   - Check relevant guide above
   - Search this index
   - Review FAQ

2. **GitHub Discussions**
   - Ask questions
   - Share tips
   - Get community help

3. **GitHub Issues**
   - Report bugs
   - Request features
   - Track progress

4. **Community Forums**
   - Home Assistant Community
   - Reddit r/homeassistant
   - Discord servers

### Before Asking

✅ Check these first:
1. Read relevant documentation
2. Search FAQ
3. Check existing issues/discussions
4. Review troubleshooting guide
5. Check logs for errors

### When Asking for Help

Include:
- Home Assistant version
- Integration version
- Firmware version
- Error messages (from logs)
- Steps to reproduce
- What you've already tried

---

## 📝 Documentation Contributions

Help improve this documentation!

### How to Contribute
1. Fork repository
2. Edit documentation
3. Submit pull request
4. Review and merge

### What to Add
- Missing information
- Better examples
- Clearer explanations
- Screenshots
- Translations

---

## 🔗 External Resources

### Official Links
- [GitHub Repository](https://github.com/daangel27/haptique-extender-homeassistant)
- [Firmware Repository](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)
- [Home Assistant Docs](https://www.home-assistant.io/)

### Community Resources
- [Home Assistant Community](https://community.home-assistant.io/)
- [HACS Documentation](https://hacs.xyz/)
- [Reddit r/homeassistant](https://www.reddit.com/r/homeassistant/)

---

**Documentation Version**: 1.5.0  
**Last Updated**: 2025-11-20  
**Maintained by**: [@daangel27](https://github.com/daangel27)
