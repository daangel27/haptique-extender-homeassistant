# Installation Guide - Haptique Extender Integration

This guide provides detailed step-by-step instructions for installing and configuring the Haptique Extender integration for Home Assistant.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Package Files Setup](#package-files-setup)
4. [Initial Configuration](#initial-configuration)
5. [Verification](#verification)
6. [Post-Installation](#post-installation)

## Prerequisites

### Hardware Requirements
- ✅ Haptique Extender device (KINCONY KC868-AG) with firmware installed
- ✅ WiFi network connectivity
- ✅ Home Assistant instance (version 2023.1 or later)

### Software Requirements
- ✅ **Haptique Config mobile app** (iOS/Android) - Required for initial setup
- ✅ Home Assistant with network access to the device
- ✅ (Optional) HACS installed for easier updates

### Network Requirements
- Both Home Assistant and Haptique Extender on the same network (or with routing between networks)
- mDNS/Zeroconf enabled for automatic discovery
- Recommended: Static IP address for the Haptique Extender

## Installation Methods

### Method 1: HACS Installation (Recommended)

HACS (Home Assistant Community Store) makes installation and updates easier.

#### Step 1: Add Custom Repository

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Click the **three dots menu** (⋮) in the top right
4. Select **Custom repositories**
5. Add the repository:
   - **Repository URL**: `https://github.com/daangel27/haptique-extender-homeassistant`
   - **Category**: Integration
6. Click **Add**

#### Step 2: Install Integration

1. In HACS, search for "Haptique Extender"
2. Click on the integration
3. Click **Download**
4. Select the latest version
5. Click **Download** again to confirm

#### Step 3: Restart Home Assistant

1. Go to **Settings** → **System**
2. Click **Restart**
3. Wait for Home Assistant to restart (1-2 minutes)

### Method 2: Manual Installation

If you prefer not to use HACS or want more control:

#### Step 1: Download Files

1. Go to the [Releases page](https://github.com/daangel27/haptique-extender-homeassistant/releases)
2. Download the latest `haptique_extender.zip` file
3. Extract the archive on your computer

#### Step 2: Copy Files

**Option A: Using File Editor Add-on**
1. Install the "File editor" add-on if not already installed
2. Navigate to `/config/custom_components/`
3. Create a `haptique_extender` folder if it doesn't exist
4. Upload all files from the extracted folder

**Option B: Using SSH/Terminal**
```bash
cd /config/custom_components
wget https://github.com/daangel27/haptique-extender-homeassistant/releases/latest/download/haptique_extender.zip
unzip haptique_extender.zip
rm haptique_extender.zip
```

**Option C: Using Samba/SMB**
1. Connect to your Home Assistant via network share
2. Navigate to `config/custom_components/`
3. Copy the `haptique_extender` folder

#### Step 3: Verify Installation

Check that files are in the correct location:
```
/config/custom_components/haptique_extender/
├── __init__.py
├── manifest.json
├── config_flow.py
├── const.py
├── coordinator.py
├── sensor.py
├── binary_sensor.py
├── switch.py
├── ir_database.py
├── firmware_storage.py
├── services.yaml
├── strings.json
└── translations/
    └── en.json
```

#### Step 4: Restart Home Assistant

1. Go to **Settings** → **System**
2. Click **Restart**
3. Wait for restart to complete

## Package Files Setup

The integration includes pre-configured YAML packages for enhanced functionality.

### Step 1: Enable Packages

Edit your `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

### Step 2: Create Packages Directory

If you don't have a `packages` folder:

**Via SSH/Terminal:**
```bash
mkdir -p /config/packages
```

**Via File Editor:**
1. Create a new folder named `packages` in `/config/`

### Step 3: Copy Package Files

Copy the following files to `/config/packages/`:

1. **haptique_extender_input_en.yaml**
   - Input helpers (text fields, selectors, numbers)
   - Required for dashboard functionality

2. **haptique_extender_script_en.yaml**
   - Scripts for learning, sending, and database management
   - Required for automation

3. **haptique_extender_automation_en.yaml**
   - Auto-refresh automations
   - Keeps device and command lists updated

4. **haptique_extender_notifications_en.yaml**
   - Smart notifications for all operations
   - Provides user feedback

5. **haptique_extender_rest_en.yaml** (Optional)
   - REST commands for advanced firmware features

### Step 4: Validate Configuration

1. Go to **Developer Tools** → **YAML**
2. Click **Check Configuration**
3. Ensure no errors are reported

### Step 5: Restart Home Assistant

After adding package files, restart Home Assistant.

## Initial Configuration

### Getting Your Authentication Token

**Important:** You must obtain the token from the Haptique Config mobile app before proceeding.

1. Download **Haptique Config** app:
   - iOS: Search in App Store
   - Android: Search in Play Store

2. Open the app and connect to your device:
   - Follow the in-app connection wizard
   - Connect to your Haptique Extender's WiFi network if needed

3. Copy the authentication token:
   - The token is automatically copied to your clipboard upon connection
   - Or find it in the app's settings/info section
   - Save this token securely

### Adding the Integration

#### Option 1: Automatic Discovery (Easiest)

1. After installation and restart, go to **Settings** → **Devices & Services**
2. Look for a discovered "Haptique Extender" device
3. Click **Configure**
4. Paste your authentication token
5. Click **Submit**

The integration will automatically:
- Configure the device
- Create all entities
- Set up the device name based on hostname

#### Option 2: Manual Configuration

If automatic discovery doesn't work:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Haptique Extender"
4. Click on it
5. Fill in the form:
   - **IP Address**: Your device's IP (e.g., `192.168.1.100`)
   - **Authentication Token**: Paste the token from mobile app
   - **Name** (optional): Custom name (e.g., "Living Room IR")
6. Click **Submit**

### Configuration Tips

**Static IP Recommendation:**
Assign a static IP to your Haptique Extender in your router to prevent connection issues after DHCP lease renewal.

**Token Security:**
The authentication token is stored securely in Home Assistant's configuration. Do not share it publicly.

## Verification

### Check Integration Status

1. Go to **Settings** → **Devices & Services**
2. Find "Haptique Extender" in the list
3. Status should show:
   - ✅ Device connected
   - Entity count (typically 15+ entities)

### Verify Entities Created

Go to **Developer Tools** → **States** and look for:

**Sensors:**
- `sensor.haptique_extender_firmware_version`
- `sensor.haptique_extender_wifi_ssid`
- `sensor.haptique_extender_wifi_signal`
- `sensor.haptique_extender_ir_commands_stored`
- `sensor.haptique_extender_learning_mode`
- `sensor.haptique_extender_last_learn_ir_code`
- And more...

**Binary Sensors:**
- `binary_sensor.haptique_extender_wifi_connected`

**Switches:**
- `switch.haptique_extender_ir_learning_mode`

**Note:** Entity names may vary based on your device's hostname.

### Test Basic Functionality

1. Check WiFi connectivity:
   ```yaml
   # Should show 'on'
   binary_sensor.haptique_extender_wifi_connected
   ```

2. View firmware version:
   ```yaml
   # Should show version number
   sensor.haptique_extender_firmware_version
   ```

3. Test learning mode switch:
   - Turn on: `switch.haptique_extender_ir_learning_mode`
   - Should activate learning mode
   - Turn off to deactivate

### Check Services

Go to **Developer Tools** → **Services** and verify these services exist:

- `haptique_extender.learn_ir_command`
- `haptique_extender.send_ir_command`
- `haptique_extender.send_ir_code`
- `haptique_extender.list_ir_devices`
- `haptique_extender.list_ir_commands`
- `haptique_extender.delete_ir_command`
- `haptique_extender.delete_ir_device`

### Check Package Helpers

If you installed package files, verify these exist in **Settings** → **Devices & Services** → **Helpers**:

**Input Select:**
- `input_select.haptique_replay_device`
- `input_select.haptique_replay_command`
- `input_select.haptique_new_device_type`
- `input_select.haptique_services_device`
- `input_select.haptique_services_command`

**Input Text:**
- `input_text.haptique_new_device_name`
- `input_text.haptique_new_command_name`
- `input_text.haptique_new_command_label`

**Scripts:**
- `script.haptique_learn_from_helpers`
- `script.haptique_send_from_selectors`
- `script.haptique_update_device_list`

## Post-Installation

### 1. Import Dashboard

1. Copy the contents of `dashboard_example.yaml`
2. Create a new dashboard in Home Assistant:
   - Go to **Settings** → **Dashboards**
   - Click **+ Add Dashboard**
   - Name it "Haptique Extender" or similar
3. Edit the dashboard in YAML mode
4. Paste the configuration
5. Adjust entity IDs if your hostname differs

### 2. Learn Your First Command

Test the learning functionality:

```yaml
service: haptique_extender.learn_ir_command
data:
  device_id: "test_tv"
  device_name: "Test TV"
  device_type: "TV"
  command_name: "power"
  command_label: "Power On/Off"
```

1. Run the service
2. Point your TV remote at the IR sensor
3. Press the power button
4. Wait for confirmation notification

### 3. Send a Test Command

After learning a command:

```yaml
service: haptique_extender.send_ir_command
data:
  device_id: "test_tv"
  command_name: "power"
```

### 4. Configure Notifications (Optional)

If you want mobile notifications instead of persistent notifications:

Edit `haptique_extender_notifications_en.yaml` and replace:
```yaml
service: persistent_notification.create
```

With:
```yaml
service: notify.mobile_app_your_phone
```

### 5. Set Up Automations (Optional)

Create automations based on your needs:
- Turn on TV when arriving home
- Control AC based on temperature
- Create scenes with multiple IR commands

### 6. Backup Configuration

Important files to backup:
- `/config/haptique_ir_devices.json` - IR command database
- `/config/packages/haptique_extender_*.yaml` - Package files
- Integration configuration (backed up with Home Assistant)

## Troubleshooting Installation

### Integration Not Showing Up

**Check 1:** Verify files are in correct location
```bash
ls -la /config/custom_components/haptique_extender/
```

**Check 2:** Check Home Assistant logs
- Go to **Settings** → **System** → **Logs**
- Look for errors containing "haptique_extender"

**Check 3:** Clear browser cache
- Press Ctrl+F5 (Windows/Linux) or Cmd+Shift+R (Mac)
- Try a different browser

### Package Files Not Loading

**Check 1:** Verify configuration.yaml syntax
```yaml
homeassistant:
  packages: !include_dir_named packages
```

**Check 2:** Check YAML syntax in package files
- Use **Developer Tools** → **YAML** → **Check Configuration**

**Check 3:** Check file permissions
```bash
ls -la /config/packages/
```

### Device Won't Connect

See main [Troubleshooting section](README.md#troubleshooting) in README.md

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](README.md#troubleshooting) section
2. Review [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues)
3. Enable debug logging and check logs
4. Post in [Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

## Next Steps

- Read the [Usage Guide](README.md#usage)
- Explore available [Services](README.md#services)
- Set up your [Dashboard](README.md#dashboard-example)
- Learn your devices' IR commands
- Create automations

---

**Congratulations!** Your Haptique Extender integration is now installed and ready to use.
