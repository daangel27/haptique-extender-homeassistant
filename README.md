# Haptique Extender - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/daangel27/haptique-extender-homeassistant.svg)](https://github.com/daangel27/haptique-extender-homeassistant/releases)
[![License](https://img.shields.io/github/license/daangel27/haptique-extender-homeassistant.svg)](LICENSE)

![alt text](image.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-1.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)


A Home Assistant integration for the **Haptique Extender** (KINCONY KC868-AG) device, enabling comprehensive infrared (IR) remote control management directly from Home Assistant.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Services](#services)
- [Dashboard Example](#dashboard-example)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## 🌟 Overview

This integration provides seamless control of IR devices through the Haptique Extender hardware. It features an intelligent IR command database, learning capabilities, and an intuitive interface for managing your infrared-controlled devices.

**Hardware:** KINCONY KC868-AG  
**Firmware:** [Haptique Extender Firmware](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)

## ✨ Features

### Core Functionality
- 🔍 **Automatic device discovery** via Zeroconf/mDNS
- 📡 **IR code learning** with visual feedback
- 💾 **Local database storage** for learned commands (JSON-based)
- 🎮 **Command replay** through intuitive selectors
- 📊 **Real-time monitoring** of device status and statistics
- 🔄 **API polling** for reliable state updates (10-second interval)

### Entities Created
- **Sensors:**
  - Firmware version
  - MAC address
  - WiFi SSID and signal strength (RSSI)
  - WiFi IP address
  - IR RX count and last frequency
  - IR commands stored (firmware storage)
  - Storage usage percentage
  - Learning mode status
  - Last learned IR code (with timestamp)

- **Binary Sensors:**
  - WiFi connection status

- **Switches:**
  - IR Learning Mode toggle

### Smart Notifications
- 🎓 Learning mode activation/timeout
- ✅ Command learned and saved confirmation
- 📤 Command sent confirmation
- ⚠️ Error handling (connection lost, command not found, etc.)
- 🔌 Connection status changes

### Database Management
- Create and organize devices by type (TV, AC, Fan, Light, Audio, Projector, Generic)
- Learn and store IR commands with custom labels
- List all devices and commands
- Delete individual commands or entire devices
- Export/import device configurations

## 📋 Prerequisites

### Required
1. **Haptique Extender device** (KINCONY KC868-AG) with firmware installed
2. **Haptique Config mobile app** - Required to obtain the authentication token
3. **Home Assistant** 2023.1 or later

### Important Notes
- ⚠️ **RF functionality is not currently supported** - Only IR (infrared) control is available
- 🔑 **Authentication token required** - Must be obtained from the Haptique Config mobile app before adding the integration

### Getting Your Authentication Token
1. Download and install the **Haptique Config** mobile app
2. Connect to your Haptique Extender device through the app
3. The authentication token will be automatically copied to your clipboard
4. Use this token when setting up the integration in Home Assistant

## 🚀 Installation

### Method 1: HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/daangel27/haptique-extender-homeassistant`
6. Select category: "Integration"
7. Click "Add"
8. Search for "Haptique Extender" and install
9. Restart Home Assistant

### Method 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/daangel27/haptique-extender-homeassistant/releases)
2. Extract the `haptique_extender` folder from the archive
3. Copy the folder to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

### Installing Package Files

The integration includes pre-configured YAML packages for easy setup:

1. Ensure you have a `packages` folder in your Home Assistant configuration directory
2. If not, create it: `mkdir /config/packages`
3. Add to your `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
4. Copy all package files to `/config/packages/`:
   - `haptique_extender_input_en.yaml` - Input helpers (selectors, text fields)
   - `haptique_extender_script_en.yaml` - Scripts for automation
   - `haptique_extender_automation_en.yaml` - Auto-refresh automations
   - `haptique_extender_notifications_en.yaml` - Smart notifications
   - `haptique_extender_rest_en.yaml` - REST commands (optional)
5. Restart Home Assistant

## ⚙️ Configuration

### Adding the Integration

#### Automatic Discovery (Recommended)
1. Go to **Settings** → **Devices & Services**
2. If your Haptique Extender is on the same network, it should be auto-discovered
3. Click **Configure** on the discovered device
4. Enter your authentication token (obtained from Haptique Config app)
5. Click **Submit**

#### Manual Setup
1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Haptique Extender"
4. Enter:
   - **IP Address**: Your device's IP address
   - **Authentication Token**: Token from Haptique Config app
   - **Name** (optional): Custom name for the device
5. Click **Submit**

### Configuration Options

| Parameter | Required | Description |
|-----------|----------|-------------|
| IP Address | Yes | Static IP address of your Haptique Extender |
| Authentication Token | Yes | Token obtained from Haptique Config mobile app |
| Name | No | Custom device name (defaults to hostname) |

**Recommendation:** Assign a static IP address to your Haptique Extender in your router for reliable operation.

## 📖 Usage

### Learning IR Commands

There are two ways to learn IR commands:

#### Method 1: Using the Service (Recommended)

```yaml
service: haptique_extender.learn_ir_command
data:
  device_id: "tv_samsung_living_room"
  device_name: "Samsung TV Living Room"
  device_type: "TV"
  command_name: "power"
  command_label: "Power On/Off"
  timeout: 30
```

#### Method 2: Using the Dashboard

1. Open your Haptique Extender dashboard
2. Fill in the learning form:
   - Device name
   - Device type
   - Command name
   - Command label (optional)
3. Click "Learn Command"
4. Point your remote at the IR sensor
5. Press the button on your remote
6. Wait for confirmation notification

### Sending IR Commands

#### Using Selectors (Dashboard)
1. Select device from dropdown
2. Select command from dropdown
3. Click "Send Command"

#### Using Service Call

```yaml
service: haptique_extender.send_ir_command
data:
  device_id: "tv_samsung_living_room"
  command_name: "power"
```

#### Direct IR Code Sending

```yaml
service: haptique_extender.send_ir_code
data:
  raw_data: [9000, 4500, 560, 560, 560, 1680, 560, 560]
  freq_khz: 38
  duty: 33
  repeat: 1
```

## 🔧 Services

### IR Learning Services

#### `haptique_extender.learn_ir_command`
Learn and save an IR command to the database.

**Parameters:**
- `device_id` (required): Unique identifier (e.g., "tv_samsung_salon")
- `device_name` (optional): Human-readable name
- `device_type` (optional): TV, AC, Fan, Light, Audio, Projector, Generic
- `command_name` (required): Command identifier (e.g., "power")
- `command_label` (optional): Display label (e.g., "Power On/Off")
- `timeout` (optional): Learning timeout in seconds (default: 30)

### IR Sending Services

#### `haptique_extender.send_ir_command`
Send a learned IR command from the database.

**Parameters:**
- `device_id` (required): Device identifier
- `command_name` (required): Command identifier

#### `haptique_extender.send_ir_code`
Send a raw IR code directly.

**Parameters:**
- `raw_data` (required): List of timing values in microseconds
- `freq_khz` (optional): Carrier frequency (default: 38)
- `duty` (optional): PWM duty cycle (default: 33)
- `repeat` (optional): Repeat count (default: 1)

### Database Management Services

#### `haptique_extender.list_ir_devices`
List all devices in the IR database.

**Returns:** JSON with device list

#### `haptique_extender.list_ir_commands`
List all commands for a specific device.

**Parameters:**
- `device_id` (required): Device identifier

**Returns:** JSON with command list

#### `haptique_extender.delete_ir_command`
Delete a command from the database.

**Parameters:**
- `device_id` (required): Device identifier
- `command_name` (required): Command to delete

#### `haptique_extender.delete_ir_device`
Delete a device and all its commands.

**Parameters:**
- `device_id` (required): Device identifier to delete

## 🎨 Dashboard Example

A complete dashboard configuration is provided in `dashboard_example.yaml`. This includes:

- **Learning section** with input helpers
- **Command replay** with device/command selectors
- **Database management** interface
- **Device monitoring** cards
- **Statistics** and status displays

To use the example dashboard:
1. Copy the contents of `dashboard_example.yaml`
2. Create a new dashboard in Home Assistant
3. Paste the configuration in YAML mode
4. Customize entity IDs if needed

## 🐛 Troubleshooting

### Device Not Discovered
- Ensure the device and Home Assistant are on the same network
- Check that mDNS/Zeroconf is enabled on your network
- Try manual configuration with IP address

### Cannot Connect / Authentication Failed
- Verify the authentication token is correct
- Get a fresh token from the Haptique Config mobile app
- Check network connectivity between Home Assistant and the device
- Ensure the device firmware is up to date

### IR Commands Not Learning
- Ensure the IR sensor is not obstructed
- Hold the remote close to the sensor (within 6 feet / 2 meters)
- Press the button firmly and hold for 1-2 seconds
- Check that learning mode timeout hasn't expired (default: 30s)

### Commands Not Sending
- Verify the device is powered on and connected
- Check WiFi signal strength (sensor.haptique_extender_wifi_signal)
- Ensure the command exists in the database
- Try learning the command again

### Database Issues
- Location: `/config/haptique_ir_devices.json`
- Check file permissions
- Verify JSON syntax if manually edited
- Backup before making manual changes

### Logs and Debugging

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.haptique_extender: debug
```

Check logs at: **Settings** → **System** → **Logs**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test thoroughly
5. Submit PR with detailed description

## 🙏 Credits

### Firmware
This integration is built for the Haptique Extender firmware developed by:
- **Cantata Communication Solutions**
- Firmware Repository: [KinkonyAGFW](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)

### Hardware
- **KINCONY KC868-AG** - IR/RF Universal Controller

### Integration Development
- **daangel27** - Home Assistant integration development

### Special Thanks
- Home Assistant community
- HACS project
- All contributors and testers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
- **Documentation**: [Wiki](https://github.com/daangel27/haptique-extender-homeassistant/wiki)

## 🔮 Future Plans

- 📻 RF (Radio Frequency) command support
- 🌐 WebSocket support for real-time updates
- 📱 Enhanced mobile app integration
- 🎯 Command macros and sequences
- 🔄 Cloud backup/restore functionality
- 🏠 Scene integration
- 📊 Advanced analytics and usage statistics

---

**Note:** This integration is not officially affiliated with KINCONY or Cantata Communication Solutions. It is an independent community project.

**Version:** 1.2.0  
**Last Updated:** 2025
