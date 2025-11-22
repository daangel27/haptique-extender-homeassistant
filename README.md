# Haptique Extender for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/daangel27/haptique-extender-homeassistant.svg)](https://github.com/daangel27/haptique-extender-homeassistant/releases)
[![License](https://img.shields.io/github/license/daangel27/haptique-extender-homeassistant.svg)](LICENSE)

A comprehensive Home Assistant integration for the **Kincony KC868-AG** (Haptique Extender), enabling powerful infrared (IR) remote control management with an intuitive interface.

## 📸 Screenshots

<!-- Example syntax for adding images from the images directory -->
![Dashboard Overview](images/dashboard-overview.png)
![Device Panel](images/device-panel.png)
![Learning Mode](images/learning-mode.png)

## ✨ Features

### Core Capabilities
- 🎯 **IR Learning Mode**: Capture commands from any IR remote control
- 📤 **Command Transmission**: Send learned IR commands to control devices
- 💾 **Dual Storage System**: 
  - Home Assistant local database (unlimited commands)
  - Device firmware storage (50 commands max)
- 🔍 **Device Discovery**: Automatic Zeroconf detection on local network
- 🎛️ **Intuitive Dashboard**: Complete control interface with conditional displays
- 🔔 **Smart Notifications**: Configurable alerts for all operations

### Advanced Features
- ✅ **Name Validation**: Automatic validation of device and command names
- 🔄 **Auto-refresh**: Lists update automatically after operations
- 🎚️ **Flexible Input**: Toggle between existing items or create new ones
- 📊 **Real-time Monitoring**: Track storage usage, WiFi signal, and more
- 🚫 **Duplicate Prevention**: Smart detection of unchanged IR codes

## 📦 What's Included

### Integration Components
- **13 Sensors**:
  - Device information (Firmware, Hostname, MAC, IP)
  - Network status (WiFi SSID, Signal strength)
  - Storage monitoring (Hub commands, usage percentage)
  - Database tracking (Devices count, Commands count)
  - Last learned IR code with metadata
  
- **1 Binary Sensor**: WiFi connection status

- **1 Switch**: IR Learning Mode (disabled by default)

### YAML Configuration Files
- **4 Input Helpers** (`haptique_extender_input.yaml`):
  - 2 text inputs (device name, command name)
  - 3 boolean toggles (notifications, use existing device/command)
  - 3 select dropdowns (operation mode, device selector, command selector)

- **7 Services**:
  - `send_ir_code` - Send raw IR code
  - `learn_ir_command` - Learn and save IR command
  - `send_ir_command` - Send learned command
  - `delete_ir_command` - Delete specific command
  - `delete_ir_device` - Delete device and all commands
  - `set_commands_device` - Update commands sensor
  - `list_device_commands` - List all device commands

- **8 Scripts** (`haptique_extender_script.yaml`):
  - Main operation execution
  - Device list refresh
  - Command list refresh
  - Full refresh (devices + commands)
  - Clear input helpers

- **7 Automations** (`haptique_extender_automation.yaml`):
  - Auto-refresh on device change
  - Auto-refresh on startup
  - Auto-refresh on database changes
  - Mode-based toggle management (4 automations)

- **1 Template** (`haptique_extender_template.yaml`):
  - Binary sensor for notifications status

- **1 Dashboard** (`dashboard.yaml`):
  - 4 views (Control, Database, Sensors, Settings, Help)
  - Conditional displays based on operation mode
  - Comprehensive help and examples

### Events System
- `haptique_operation` - Unified event for all operations (learn, send, delete, list)
- `haptique_ir_captured` - Manual IR capture event

## 🚀 Quick Start

### Prerequisites
- Home Assistant 2025.2.0 or later
- Kincony KC868-AG device with **firmware 1.1.2** or later
  - Firmware available at: [KinkonyAGFW Repository](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)
- Device and Home Assistant on the same local network
- HACS (Home Assistant Community Store) installed

### Installation

1. **Add Custom Repository in HACS**:
   - Open HACS in Home Assistant
   - Click on "Integrations"
   - Click the three dots (⋮) in top right
   - Select "Custom repositories"
   - Add URL: `https://github.com/daangel27/haptique-extender-homeassistant`
   - Category: Integration
   - Click "Add"

2. **Install via HACS**:
   - Search for "Haptique Extender"
   - Click "Download"
   - Restart Home Assistant

3. **Configure Integration**:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Haptique Extender"
   - Follow the configuration flow (IP address + authentication token)

4. **Install YAML Files**:
   - Copy all files from `packages/` to `/config/packages/`
   - Ensure packages are enabled in `configuration.yaml`:
     ```yaml
     homeassistant:
       packages: !include_dir_named packages
     ```
   - Restart Home Assistant

5. **Add Dashboard**:
   - Copy `dashboard/dashboard.yaml` content
   - Create a new dashboard or add to existing one
   - Enjoy!

📖 **Detailed instructions**: See [INSTALLATION.md](docs/INSTALLATION.md)

## 🎯 Usage Example

### Learning a TV Power Command

1. Set operation mode to **"Learn"**
2. Toggle "Use Existing Device" OFF, enter "Samsung TV"
3. Toggle "Use Existing Command" OFF, enter "power"
4. Click **"Execute"**
5. Point your TV remote at the KC868-AG sensor
6. Press the power button
7. Command automatically saved! ✅

### Sending the Command

1. Set operation mode to **"Send"**
2. Toggle "Use Existing Device" ON, select "Samsung TV"
3. Toggle "Use Existing Command" ON, select "power"
4. Click **"Execute"**
5. Your TV turns on/off! ✅

## 📚 Documentation

- [📖 Full Documentation Index](docs/DOCUMENTATION_INDEX.md)
- [🚀 Quick Start Guide](docs/QUICK_START.md)
- [💾 Installation Guide](docs/INSTALLATION.md)
- [❓ Frequently Asked Questions](docs/FAQ.md)
- [🔧 Troubleshooting](docs/TROUBLESHOOTING.md)

## 🎛️ Supported Devices

The Haptique Extender can control any device that uses **infrared (IR)** remote control:

- 📺 **TVs** (all brands)
- 📦 **Set-top boxes** (Cable, Satellite, IPTV)
- 🔊 **Audio systems** (Amplifiers, Soundbars, Receivers)
- ❄️ **Air conditioners** (all IR-controlled models)
- 🎮 **Media players** (Blu-ray, DVD, Streaming boxes)
- 💡 **IR-controlled lighting**
- 🪟 **Motorized blinds/curtains** (IR models)
- And much more!

**Note**: RF (Radio Frequency) support is not yet implemented in this version.

## 🔧 Technical Details

### Database Storage
- **Location**: `/config/haptique_ir_database.json`
- **Format**: JSON with timestamps
- **Capacity**: Unlimited (limited only by disk space)
- **Backup**: Recommended to backup this file regularly

### Firmware Storage
- **Capacity**: 50 commands maximum
- **Purpose**: Standalone operation without Home Assistant
- **Note**: Not used in current version (reserved for future features)

### Network Configuration
- **Protocol**: HTTP/REST API
- **Port**: 80 (default)
- **Authentication**: Bearer token
- **Discovery**: mDNS/Zeroconf (`_http._tcp.local.`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### Version 1.5.0 (Current)
- ✅ Complete rewrite with unified control panel
- ✅ Flexible toggle system (new/existing devices and commands)
- ✅ Smart name validation and duplicate prevention
- ✅ Improved sensor naming (Database/Hub distinction)
- ✅ Mode-based automatic toggle management
- ✅ Enhanced error handling and notifications
- ✅ Template protection against None values
- ✅ Switch hidden by default from device panel

### Version 1.3.0
- Initial public release
- Basic IR learning and sending
- Database storage
- Dashboard interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kincony** for the KC868-AG hardware
- **Cantata Communication Solutions** for the firmware
- Home Assistant community for testing and feedback

## 💬 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 📖 **Documentation**: [docs/](docs/)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

## ⚠️ Disclaimer

This integration is not affiliated with or endorsed by Kincony or Cantata Communication Solutions. Use at your own risk.

---

**Made with ❤️ for the Home Assistant community**
