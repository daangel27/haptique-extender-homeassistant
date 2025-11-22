# Installation Guide

Complete step-by-step installation guide for Haptique Extender integration.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Firmware Update](#firmware-update)
3. [HACS Installation](#hacs-installation)
4. [Manual Installation](#manual-installation)
5. [Configuration](#configuration)
6. [YAML Files Setup](#yaml-files-setup)
7. [Dashboard Installation](#dashboard-installation)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements
- **Kincony KC868-AG** device (Haptique Extender)
- Network connection (WiFi or Ethernet)
- IR sensor connected to the device

### Software Requirements
- **Home Assistant**: Version 2025.2.0 or later
- **HACS**: Home Assistant Community Store installed
- **Network**: Device and HA on same local network

### Before You Start
1. Ensure your KC868-AG is powered on and connected to your network
2. Note the device's IP address (check your router or use network scanner)
3. Have your authentication token ready (from Kincony mobile app)

---

## Firmware Update

⚠️ **IMPORTANT**: Your KC868-AG must run firmware version **1.1.2** or later.

### Check Current Firmware Version
1. Open the Kincony mobile app
2. Connect to your KC868-AG
3. Check firmware version in device settings

### Update Firmware (if needed)
1. Visit the firmware repository: [KinkonyAGFW](https://github.com/Cantata-Communication-Solutions/KinkonyAGFW)
2. Download firmware version 1.1.2 or later
3. Follow the update instructions in the repository
4. Reboot the device after update

---

## HACS Installation

### Step 1: Add Custom Repository

1. Open **Home Assistant**
2. Go to **HACS** (sidebar)
3. Click on **"Integrations"**
4. Click the **three dots (⋮)** in the top right corner
5. Select **"Custom repositories"**
6. Add the following:
   - **Repository**: `https://github.com/daangel27/haptique-extender-homeassistant`
   - **Category**: `Integration`
7. Click **"Add"**

![Add Custom Repository](images/hacs-custom-repo.png)

### Step 2: Install Integration

1. In HACS, search for **"Haptique Extender"**
2. Click on the integration
3. Click **"Download"**
4. Select the latest version
5. Click **"Download"** again to confirm

![Install from HACS](images/hacs-install.png)

### Step 3: Restart Home Assistant

1. Go to **Settings** → **System**
2. Click **"Restart"** (top right)
3. Choose **"Restart Home Assistant"**
4. Wait for restart to complete (~1-2 minutes)

---

## Manual Installation

If you prefer manual installation or HACS is not available:

### Step 1: Download Files

```bash
cd /config
git clone https://github.com/daangel27/haptique-extender-homeassistant.git temp_haptique
```

### Step 2: Copy Integration Files

```bash
mkdir -p custom_components/haptique_extender
cp -r temp_haptique/custom_components/haptique_extender/* custom_components/haptique_extender/
```

### Step 3: Verify Installation

```bash
ls -la custom_components/haptique_extender/
```

You should see:
- `__init__.py`
- `manifest.json`
- `coordinator.py`
- `sensor.py`
- `switch.py`
- `binary_sensor.py`
- `config_flow.py`
- `const.py`
- `firmware_storage.py`
- `ir_database.py`
- `services.yaml`
- `strings.json`
- `translations/` directory

### Step 4: Restart Home Assistant

---

## Configuration

### Step 1: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"** (bottom right)
3. Search for **"Haptique Extender"**
4. Click on the integration

![Add Integration](images/add-integration.png)

### Step 2: Configuration Flow

#### Option A: Automatic Discovery (Zeroconf)

If your device is discovered automatically:

1. **Confirm Device**:
   - Name: Haptique Extender (or custom name)
   - IP Address: (auto-detected)
   - Model: KC868-AG
   - Firmware: (detected version)

2. **Enter Authentication Token**:
   - Open Kincony mobile app
   - Connect to your device
   - Copy the token (automatically copied to clipboard)
   - Paste in Home Assistant
   - Click **"Submit"**

![Zeroconf Discovery](images/config-zeroconf.png)

#### Option B: Manual Configuration

If automatic discovery doesn't work:

1. **Enter Device Information**:
   - **IP Address**: `192.168.1.xxx` (your device IP)
   - **Authentication Token**: (from mobile app)
   - **Name** (optional): Custom name for the device
   - Click **"Submit"**

![Manual Configuration](images/config-manual.png)

### Step 3: Verify Device

After successful configuration, you should see:

- ✅ New device "Haptique Extender" (or your custom name)
- ✅ 13 sensors
- ✅ 1 binary sensor
- ✅ 1 switch (disabled by default)

![Device Panel](images/device-panel-complete.png)

---

## YAML Files Setup

The integration requires YAML configuration files for the dashboard and automation.

### Step 1: Enable Packages

Edit your `configuration.yaml`:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

### Step 2: Copy Package Files

```bash
# Create packages directory if it doesn't exist
mkdir -p /config/packages

# Copy all package files
cp temp_haptique/packages/*.yaml /config/packages/
```

Files to copy:
- ✅ `haptique_extender_input.yaml` (4 input helpers)
- ✅ `haptique_extender_script.yaml` (8 scripts)
- ✅ `haptique_extender_automation.yaml` (7 automations)
- ✅ `haptique_extender_template.yaml` (1 template sensor)
- ✅ `haptique_extender_notifications.yaml` (notification templates)

### Step 3: Verify Files

```bash
ls -la /config/packages/haptique_extender_*
```

### Step 4: Check Configuration

1. Go to **Developer Tools** → **YAML**
2. Click **"Check Configuration"**
3. Verify no errors
4. Click **"Restart"** if all is OK

![Check Configuration](images/check-config.png)

---

## Dashboard Installation

### Method 1: New Dashboard (Recommended)

1. Go to **Settings** → **Dashboards**
2. Click **"+ Add Dashboard"** (bottom right)
3. Enter details:
   - **Title**: `Haptique Manager`
   - **Icon**: `mdi:remote`
   - **Show in sidebar**: ✅
4. Click **"Create"**
5. Click on the new dashboard
6. Click **⋮** (top right) → **"Edit Dashboard"**
7. Click **⋮** again → **"Raw configuration editor"**
8. Copy entire content from `dashboard/dashboard.yaml`
9. Paste into editor
10. Click **"Save"**

![Create Dashboard](images/dashboard-create.png)

### Method 2: Add to Existing Dashboard

1. Open your existing dashboard
2. Enter edit mode (pencil icon)
3. Click **"+ Add View"**
4. Choose **"Panel (1 card)"**
5. Copy sections from `dashboard/dashboard.yaml`
6. Paste and adapt to your layout

### Dashboard Structure

The dashboard includes 5 views:

1. **Control** 🎮
   - Unified control panel
   - Operation mode selector
   - Device/Command input (toggle system)
   - Execution buttons
   - Mode-specific help

2. **Database** 💾
   - Database statistics
   - Device list with command counts
   - Storage usage visualization

3. **Sensors** 📊
   - Network information
   - Storage monitoring
   - Device details

4. **Settings** ⚙️
   - Notification toggle
   - Configuration options

5. **Help** ❓
   - Service examples
   - Tips and features
   - Quick workflows

---

## Verification

### Check Integration Status

1. **Devices & Services**:
   - Go to Settings → Devices & Services
   - Find "Haptique Extender"
   - Status should be "Configured"

2. **Device Panel**:
   - Click on the device
   - Verify all sensors are visible
   - Check values are updating

3. **Entities**:
   - Go to Settings → Devices & Services → Entities
   - Filter by "haptique"
   - All entities should be "Available" (not "Unavailable")

### Test Basic Functionality

#### Test 1: Refresh Lists
```yaml
service: script.haptique_refresh_all
```
- Should execute without errors
- Check logs for completion

#### Test 2: Check Database
1. Navigate to Haptique Manager dashboard
2. Go to "Database" view
3. Should show "0 devices" if fresh install

#### Test 3: Learning Mode
1. Go to "Control" view
2. Select mode: "Learn"
3. Enter device name: "Test Device"
4. Enter command name: "test_command"
5. Click "Execute"
6. Verify notification appears
7. Press any IR remote button near sensor
8. Should capture and save command

---

## Troubleshooting

### Integration Not Found

**Problem**: Can't find "Haptique Extender" in Add Integration

**Solutions**:
1. Verify HACS installation completed
2. Restart Home Assistant again
3. Check `/config/custom_components/haptique_extender/` exists
4. Check `/config/custom_components/haptique_extender/manifest.json` is valid JSON

### Connection Failed

**Problem**: "Cannot connect to device" during configuration

**Solutions**:
1. Verify device IP address is correct
2. Ping device: `ping 192.168.1.xxx`
3. Check device is powered on
4. Verify device and HA on same network
5. Check authentication token is valid
6. Try accessing `http://DEVICE_IP/api/status` in browser

### Entities Unavailable

**Problem**: All entities show "Unavailable"

**Solutions**:
1. Check device is online
2. Verify network connectivity
3. Restart integration: Configuration → Integrations → Haptique Extender → ⋮ → Reload
4. Check logs: Settings → System → Logs

### YAML Errors

**Problem**: Configuration check fails with YAML errors

**Solutions**:
1. Verify packages are enabled in `configuration.yaml`
2. Check YAML syntax (indentation, colons, quotes)
3. Validate files: [YAML Validator](http://www.yamllint.com/)
4. Check file permissions: `chmod 644 /config/packages/*.yaml`

### Dashboard Not Appearing

**Problem**: Dashboard doesn't show up

**Solutions**:
1. Verify you clicked "Save" after pasting YAML
2. Check for YAML syntax errors in dashboard editor
3. Try creating a new dashboard instead
4. Clear browser cache (Ctrl+F5)

### Services Not Available

**Problem**: Services like `haptique_extender.learn_ir_command` not found

**Solutions**:
1. Verify integration is loaded
2. Restart Home Assistant
3. Check `/config/custom_components/haptique_extender/services.yaml` exists
4. Check Developer Tools → Services for `haptique_extender.*`

---

## Post-Installation Steps

### 1. Configure Notifications
```yaml
# Enable notifications
service: input_boolean.turn_on
target:
  entity_id: input_boolean.haptique_notify_enabled
```

### 2. Test Learning
Follow the Quick Start guide to learn your first command.

### 3. Backup Database
```bash
# Backup IR database
cp /config/haptique_ir_database.json /config/backups/
```

### 4. Create Automations
Use the dashboard or create your own automations for common tasks.

---

## Next Steps

- 📖 Read the [Quick Start Guide](QUICK_START.md)
- ❓ Check the [FAQ](FAQ.md)
- 🎯 Learn about [Advanced Features](ADVANCED_FEATURES.md)
- 💬 Join [GitHub Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

---

## Need Help?

- 🐛 Found a bug? [Report it](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 💡 Have an idea? [Suggest a feature](https://github.com/daangel27/haptique-extender-homeassistant/issues)
- 💬 Questions? [Start a discussion](https://github.com/daangel27/haptique-extender-homeassistant/discussions)
