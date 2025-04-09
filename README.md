# ADB Toolbox

[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Vietnamese](https://img.shields.io/badge/Language-Tiếng%20Việt-green.svg)](README_VI.md)

## 📱 Overview

ADB Toolbox is a command-line interface (CLI) tool that helps users control Android devices through ADB (Android Debug Bridge) without having to remember complex commands. The software provides a user-friendly interface with interactive menus.

## ✨ Key Features

- 🔍 **Check connected devices**: Display list of connected Android devices
- 🚀 **Quick ADB commands**: Quickly execute commands like reboot, recovery, logcat
- ⚙️ **Hidden system settings**: Adjust system, secure, global settings
- 🧹 **Cleanup & Performance Boost**: Clear app cache, close background apps, optimize performance
- 📊 **Change DPI & Scale**: Adjust screen density and font scale
- ⏱️ **Preset shortcuts**: Run command chains from JSON configuration file
- 📝 **Logging & history**: Save performed operations in log file

## 🔧 System Requirements

- Python 3.6 or higher
- ADB (Android Debug Bridge) installed
- Python libraries: rich, questionary

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
├── main.py                  # Điểm khởi chạy
├── commands/                # Các module lệnh
│   ├── device_check.py      # Kiểm tra thiết bị
│   ├── system_settings.py   # Cài đặt hệ thống
│   └── performance_boost.py # Tăng hiệu suất
├── utils/                   # Các tiện ích
│   ├── logger.py            # Module ghi log
│   └── ui_helper.py         # Hỗ trợ giao diện
├── config/                  # Cấu hình
│   └── presets.json         # Cấu hình có sẵn
└── logs/                    # Thư mục chứa file log
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

---

**Note**: This tool was created for educational purposes and user support. Please use responsibly. 
