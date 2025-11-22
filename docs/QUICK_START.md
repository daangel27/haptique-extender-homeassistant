# Quick Start Guide

Get up and running with Haptique Extender in 10 minutes!

## Prerequisites ✅

Before starting, ensure you have:
- ✅ Haptique Extender integration installed ([Installation Guide](INSTALLATION.md))
- ✅ KC868-AG device configured and online
- ✅ Dashboard installed and accessible
- ✅ IR remote control ready for learning

---

## Your First IR Command (5 minutes)

### Step 1: Open the Dashboard

1. In Home Assistant sidebar, click **"Haptique Manager"**
2. You'll see the **Control** view by default

![Dashboard Control View](images/dashboard-control.png)

### Step 2: Learn a Command

Let's learn a TV power button:

1. **Set Operation Mode**:
   - Select **"Learn"** from dropdown

2. **Configure Device**:
   - Toggle **"Use Existing Device"** → **OFF**
   - Enter device name: **"Samsung TV"**

3. **Configure Command**:
   - Toggle **"Use Existing Command"** → **OFF**
   - Enter command name: **"power"**

4. **Execute Learning**:
   - Click **"Execute"** button
   - You'll receive a notification: "Learning mode activated"

5. **Capture IR Signal**:
   - Point your TV remote at the KC868-AG IR sensor
   - Press the **power** button
   - Distance: 5-50 cm (2-20 inches)
   - Wait for success notification

![Learning Process](images/learning-process.png)

✅ **Success!** Your command is now saved in the database.

### Step 3: Send the Command

Now let's test the command:

1. **Change Operation Mode**:
   - Select **"Send"** from dropdown
   - Notice: Both toggles automatically turn **ON**

2. **Select Device & Command**:
   - Device selector: **"Samsung TV"**
   - Command selector: **"power"**

3. **Execute**:
   - Click **"Execute"** button
   - Your TV should turn on/off!

![Send Command](images/send-command.png)

🎉 **Congratulations!** You've learned and sent your first IR command!

---

## Learning More Commands (3 minutes)

### Add Another Command to Same Device

Let's add a "volume_up" command:

1. **Set Mode**: **"Learn"**

2. **Select Existing Device**:
   - Toggle **"Use Existing Device"** → **ON**
   - Select: **"Samsung TV"**

3. **Enter New Command**:
   - Toggle **"Use Existing Command"** → **OFF**
   - Enter: **"volume_up"**

4. **Execute and Capture**:
   - Click **"Execute"**
   - Point remote and press **Volume Up**

5. **Repeat** for more commands:
   - volume_down
   - channel_up
   - channel_down
   - input
   - menu

💡 **Tip**: Keep "Use Existing Device" ON and "Use Existing Command" OFF to quickly add multiple commands to the same device.

---

## Learning a New Device (2 minutes)

Let's add a different device:

1. **Set Mode**: **"Learn"**

2. **New Device**:
   - Toggle **"Use Existing Device"** → **OFF**
   - Enter: **"Sony Soundbar"**

3. **New Command**:
   - Toggle **"Use Existing Command"** → **OFF**
   - Enter: **"power"**

4. **Execute and Capture**

5. **Add More Commands**:
   - Toggle **"Use Existing Device"** → **ON**
   - Select: **"Sony Soundbar"**
   - Add: volume_up, volume_down, input, etc.

---

## Exploring the Dashboard

### Control View 🎮

**Purpose**: Main interface for all operations

**Key Elements**:
- **Operation Mode**: Learn, Send, Delete Command, Delete Device, List Commands
- **Device Selection**: Toggle + Input/Selector
- **Command Selection**: Toggle + Input/Selector
- **Action Buttons**: Execute, Clear, Refresh
- **Mode Help**: Context-sensitive instructions

### Database View 💾

**Purpose**: View your IR command database

**Information Shown**:
- Total devices count
- Total commands per device
- Commands stored in firmware (Hub)
- Storage usage percentage

**Actions**:
- Click **"Refresh"** to update counters
- View device list with creation dates

![Database View](images/database-view.png)

### Sensors View 📊

**Purpose**: Monitor device status

**Information Available**:
- **Network**: WiFi status, signal strength, SSID, IP address
- **Storage**: Hub commands stored, max capacity, usage %
- **Device**: Firmware version, hostname, MAC address
- **Learning**: Last learned IR code timestamp and details

### Settings View ⚙️

**Purpose**: Configure integration behavior

**Options**:
- **Notifications**: Enable/disable all notifications
- **Future settings** (expandable)

---

## Understanding Operation Modes

### Learn Mode 🎓

**Purpose**: Capture IR commands from remote controls

**When to use**:
- Adding new device
- Adding command to existing device
- Replacing existing command

**Toggle Behavior**: Flexible
- Both OFF: New device + new command
- Device ON, Command OFF: Add to existing device (most common)
- Both ON: Replace existing command

### Send Mode 📤

**Purpose**: Transmit learned IR commands

**When to use**:
- Control your devices
- Test learned commands

**Toggle Behavior**: Auto-ON
- Both toggles automatically turn ON
- Select from existing devices/commands only

### Delete Command Mode 🗑️

**Purpose**: Remove specific command

**When to use**:
- Remove wrongly learned command
- Clean up unused commands

**Toggle Behavior**: Auto-ON
- Both toggles automatically turn ON
- Select command to delete

**⚠️ Warning**: Cannot be undone!

### Delete Device Mode 🗑️📦

**Purpose**: Remove entire device and all its commands

**When to use**:
- Remove device no longer owned
- Start fresh with device

**Toggle Behavior**: Auto-ON
- Device toggle automatically turns ON
- Select device to delete

**⚠️ Warning**: Deletes ALL commands for the device!

### List Device Commands Mode 📋

**Purpose**: View all commands for a device

**When to use**:
- Review learned commands
- Check command details

**Toggle Behavior**: Auto-ON
- Device toggle automatically turns ON
- Results shown in notification

---

## Common Workflows

### Workflow 1: Complete TV Setup

**Goal**: Control TV with multiple commands

```
1. Learn Mode
   - New Device: "Living Room TV"
   - New Command: "power"
   → Execute → Capture

2. Learn Mode (Device ON, Command OFF)
   - Existing Device: "Living Room TV"
   - New Command: "volume_up"
   → Execute → Capture

3. Repeat for:
   - volume_down
   - channel_up
   - channel_down
   - mute
   - input
   - menu

4. Test with Send Mode
```

### Workflow 2: Home Theater System

**Goal**: Control TV, Soundbar, and Cable Box

```
Device 1: TV
- power
- input
- menu

Device 2: Soundbar
- power
- volume_up
- volume_down
- input

Device 3: Cable Box
- power
- channel_up
- channel_down
- guide
```

### Workflow 3: Climate Control

**Goal**: Control air conditioner

```
Device: AC Living Room
- power
- temp_up
- temp_down
- mode (cool/heat/fan)
- fan_speed
- swing
```

---

## Tips & Tricks 💡

### Learning Tips

1. **Distance**: 
   - Optimal: 10-30 cm (4-12 inches)
   - Too close: May saturate sensor
   - Too far: May not capture

2. **Angle**:
   - Point directly at IR sensor
   - Avoid obstacles
   - Stay centered

3. **Press Duration**:
   - Short, firm press
   - Don't hold too long
   - Single press only

4. **Environment**:
   - Avoid direct sunlight on sensor
   - Turn off other IR sources
   - Reduce LED lights

### Naming Conventions

**Devices**: Descriptive and unique
- ✅ Good: "Samsung TV Living Room"
- ✅ Good: "Sony TV Bedroom"
- ❌ Bad: "TV" (too generic)
- ❌ Bad: "Device 1" (not descriptive)

**Commands**: Lowercase with underscores
- ✅ Good: "power", "volume_up", "channel_down"
- ✅ Good: "input_hdmi1", "mode_cool"
- ❌ Bad: "Power Button" (spaces)
- ❌ Bad: "VOL+" (special characters)

### Organization Tips

1. **Logical Grouping**:
   - Group by room: "Living Room TV", "Living Room Soundbar"
   - Or by device type: "Samsung TV 55", "Samsung TV 32"

2. **Consistent Naming**:
   - Use same command names across devices
   - Example: All devices use "power", not "on_off" or "toggle"

3. **Documentation**:
   - Use List Commands mode to review
   - Take notes on special commands
   - Document button combinations

---

## Troubleshooting Quick Fixes

### Learning Doesn't Capture

**Try**:
1. Check IR sensor is connected
2. Move closer (10-20 cm)
3. Press button firmly
4. Wait 2 seconds, try again
5. Check learning timeout (default 30s)

### Command Doesn't Work

**Try**:
1. Re-learn the command
2. Check device is in range
3. Verify command name is correct
4. Test with original remote first

### Toggles Not Switching

**Try**:
1. Refresh page (F5)
2. Change mode and change back
3. Check automation is enabled
4. Manually toggle if needed

### Lists Not Updating

**Try**:
1. Click "Refresh" button
2. Wait 2 seconds
3. Check database sensor values
4. Restart integration if needed

---

## Next Steps 🚀

Now that you're familiar with basics:

1. 📖 Read [Full Documentation](DOCUMENTATION_INDEX.md)
2. ❓ Check [FAQ](FAQ.md) for common questions
3. 🎯 Explore [Advanced Features](ADVANCED_FEATURES.md)
4. 🤖 Create [Automations](AUTOMATIONS.md)
5. 💬 Join [Community Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions)

---

## Need Help?

- 📖 [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- ❓ [FAQ](FAQ.md) - Frequently asked questions
- 🐛 [GitHub Issues](https://github.com/daangel27/haptique-extender-homeassistant/issues) - Report bugs
- 💬 [Discussions](https://github.com/daangel27/haptique-extender-homeassistant/discussions) - Ask questions

---

**Happy controlling! 🎮**
