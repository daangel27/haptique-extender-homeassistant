# Changelog

All notable changes to the Haptique Extender Home Assistant integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-XX

### Added
- Initial public release
- Full IR learning and replay functionality
- JSON-based IR command database
- Automatic device discovery via Zeroconf/mDNS
- Real-time device monitoring sensors
- Learning mode with timeout handling
- Comprehensive notification system
- Pre-configured YAML packages for easy setup
- Complete dashboard example
- Service-based command management
- Database import/export functionality
- Auto-refresh automations for device and command lists

### Features
- **IR Learning**: Learn IR commands with visual feedback
- **Command Replay**: Send learned commands via selectors or services
- **Database Management**: Organize devices and commands
- **Smart Notifications**: User feedback for all operations
- **Connection Monitoring**: WiFi status tracking
- **Storage Monitoring**: Track firmware storage usage
- **Learning Mode Switch**: Manual learning mode control
- **Multiple Device Support**: Manage multiple IR devices
- **Device Types**: Categorize devices (TV, AC, Fan, etc.)
- **Command Labels**: Human-readable command names

### Sensors Created
- Firmware version
- MAC address
- WiFi SSID and signal strength
- WiFi IP address
- IR RX count and frequency
- IR commands stored (firmware)
- Storage usage percentage
- Learning mode status
- Last learned IR code with timestamp

### Binary Sensors
- WiFi connection status

### Switches
- IR Learning Mode toggle

### Services
- `learn_ir_command` - Learn and save IR commands
- `send_ir_command` - Send learned commands
- `send_ir_code` - Send raw IR codes
- `list_ir_devices` - List all devices
- `list_ir_commands` - List device commands
- `delete_ir_command` - Delete specific command
- `delete_ir_device` - Delete entire device

### Packages Included
- Input helpers (selectors, text fields, numbers)
- Scripts for learning, sending, and management
- Auto-refresh automations
- Comprehensive notification system
- REST commands for firmware API

### Documentation
- Complete README with usage examples
- Detailed installation guide
- Contributing guidelines
- Troubleshooting section
- Dashboard example

### Known Limitations
- RF (Radio Frequency) commands not yet supported
- Requires authentication token from Haptique Config mobile app
- Local API polling (WebSocket support planned)

## [Unreleased]

### Planned Features
- RF command support
- WebSocket integration for real-time updates
- Command macros and sequences
- Cloud backup/restore
- Advanced analytics
- Scene integration
- Enhanced mobile app integration

### Under Consideration
- Multi-device learning sessions
- Command templates
- IR code library integration
- Voice assistant integration
- Energy monitoring

## Development Roadmap

### Version 1.3.0 (Planned)
- RF command learning and transmission
- WebSocket support for real-time updates
- Enhanced error handling
- Performance optimizations

### Version 1.4.0 (Planned)
- Command macros (sequences)
- Scene integration
- Advanced automation helpers
- Command scheduling

### Version 2.0.0 (Future)
- Cloud backup/restore
- IR code library
- Multi-device coordination
- Advanced analytics

## Migration Guides

### Upgrading from Pre-Release Versions

If you were using a pre-release version:

1. Backup your IR database: `/config/haptique_ir_devices.json`
2. Remove the old integration
3. Delete the old custom_component folder
4. Install version 1.2.0 following the installation guide
5. Restore your database file
6. Reconfigure the integration with your token

## Breaking Changes

### Version 1.2.0
- Initial release - No breaking changes

## Bug Fixes

### Version 1.2.0
- Fixed command name normalization in database
- Fixed learning mode timeout handling
- Improved error handling for network issues
- Fixed entity naming with special characters
- Corrected polling interval for learning mode
- Fixed command lookup with string keys

## Deprecations

No deprecations in current version.

## Security

### Version 1.2.0
- Authentication token securely stored in Home Assistant config
- Local API communication only (no cloud dependencies)
- JSON database with proper file permissions

## Contributors

### Version 1.2.0
- **daangel27** - Integration development and maintenance

### Special Thanks
- Cantata Communication Solutions - Firmware development
- Home Assistant community
- Beta testers and early adopters

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/daangel27/haptique-extender-homeassistant/issues
- Discussions: https://github.com/daangel27/haptique-extender-homeassistant/discussions

---

**Note**: Dates will be updated upon official releases.
