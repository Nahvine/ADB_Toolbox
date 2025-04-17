![image](https://github.com/user-attachments/assets/954addd0-74b2-42a8-9e01-3ad73de330c4)

# ADB Toolbox

[![Version](https://img.shields.io/badge/version-1.1-blue.svg)](https://github.com/Nahvine/ADB_Toolbox)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Vietnamese](https://img.shields.io/badge/Language-Tiếng%20Việt-green.svg)](README.vi.md)

A command-line interface tool for managing Android devices via ADB without needing to remember complex commands.

## Features

- 🔍 Check connected devices
- ⚡ Quick ADB commands
- 🔧 Hidden system settings
- 🚀 Clean & optimize
- 📱 Change DPI & scale
- 📦 App management (install, uninstall, backup, restore)
- 📂 File & screen management (push/pull files, browse file system, mirror screen)
- 💾 Custom commands & backup (execute custom commands, create presets, backup/restore settings)
- ⚡ Preset shortcuts
- 📝 Operation history
- 🔄 Device refresh
- ❓ Help & troubleshooting

## Installation

1. Make sure you have Python 3.6+ installed
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Make sure ADB is installed and added to system PATH
4. Run the program:
```bash
python main.py
```

## Usage

1. Connect your Android device via USB
2. Enable USB debugging on your device
3. Select features from the main menu to perform operations

## Requirements

- Python 3.6+
- ADB (Android Debug Bridge)
- USB debugging enabled on Android device
- Required Python packages (see requirements.txt)

## Note

- Some features require root access on the device
- Be careful when modifying system settings
- All operations are logged for later review

## Support

For support, please contact: example@email.com

## 📋 Installation

1. Clone this repository:
   ```
   git clone https://github.com/Nahvine/ADB_Toolbox.git
   cd ADB_Toolbox
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Make sure ADB is installed and in your system PATH.

## 🚀 Usage

1. Connect your Android device via USB and enable USB Debugging.

2. Run the application:
   ```
   python adb_toolbox/main.py
   ```
   
   On Windows, you can use the batch file:
   ```
   start_adb_toolbox.bat
   ```

3. Use arrow keys to navigate and Enter to select options from the menu.

## 📊 Project Structure

```
adb_toolbox/
│
├── main.py                  
├── commands/                
│   ├── device_check.py      
│   ├── system_settings.py   
│   ├── performance_boost.py
│   ├── app_management.py
│   ├── file_management.py
│   └── custom_commands.py
├── utils/                   
│   ├── logger.py            
│   └── ui_helper.py         
├── config/                  
│   └── presets.json         
└── logs/                    
```

## 🔒 Permissions

Some features of ADB Toolbox require special access on Android devices:

- **Rooted devices**: Some features like increasing virtual memory (swap) require root access.
- **ADB over network**: Wireless connection feature requires debugging over network to be enabled.
- **USB Debugging permission**: Always needs USB debugging mode enabled and ADB connection confirmed.

## 📝 Notes

- Be careful when changing system settings. Some changes may affect device operation.
- Always backup important data before making major changes.
- This tool is not responsible for any damage that may occur to your device.

## 🔄 Updates

Check the repository regularly for new features and bug fixes.

## 📜 License

This project is distributed under the MIT license. See the LICENSE file for more details.

## 👥 Contributions

All contributions are welcome! Create a pull request or report issues if you encounter problems.

**Note**: This tool was created for educational purposes and user support. Please use responsibly. 
>>>>>>> c1b47df47117e069380ba3a26024af98f20a7b07
