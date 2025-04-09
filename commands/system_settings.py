#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module tùy chỉnh các cài đặt hệ thống Android
"""

import os
import subprocess
import questionary
from rich.console import Console
from rich.table import Table
from rich.text import Text
from utils import logger

console = Console()
log = logger.setup_logger()

# Các namespace settings
NAMESPACES = ["system", "secure", "global"]

# Các cài đặt phổ biến cho mỗi namespace
COMMON_SETTINGS = {
    "system": [
        {"name": "accelerometer_rotation", "description": "Tự động xoay màn hình", "values": ["0", "1"]},
        {"name": "screen_brightness", "description": "Độ sáng màn hình (0-255)", "values": []},
        {"name": "screen_off_timeout", "description": "Thời gian tắt màn hình (ms)", "values": []},
        {"name": "font_scale", "description": "Tỷ lệ phông chữ (0.85-1.3)", "values": []}
    ],
    "secure": [
        {"name": "screensaver_enabled", "description": "Bật/tắt screensaver", "values": ["0", "1"]},
        {"name": "volume_button_music_control", "description": "Điều khiển nhạc bằng nút volume", "values": ["0", "1"]},
        {"name": "accessibility_display_inversion_enabled", "description": "Đảo ngược màu màn hình", "values": ["0", "1"]}
    ],
    "global": [
        {"name": "airplane_mode_on", "description": "Chế độ máy bay", "values": ["0", "1"]},
        {"name": "auto_time", "description": "Tự động cập nhật giờ", "values": ["0", "1"]},
        {"name": "bluetooth_on", "description": "Bật/tắt Bluetooth", "values": ["0", "1"]},
        {"name": "wifi_on", "description": "Bật/tắt WiFi", "values": ["0", "1"]}
    ]
}

def run_adb_command(command):
    """
    Chạy lệnh ADB và trả về kết quả
    
    Args:
        command (list): Lệnh ADB dưới dạng list các tham số
        
    Returns:
        str: Kết quả của lệnh
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Lỗi khi chạy lệnh: {e}[/bold red]")
        return None

def get_current_setting(namespace, key):
    """
    Lấy giá trị hiện tại của cài đặt
    
    Args:
        namespace (str): Namespace của cài đặt (system, secure, global)
        key (str): Tên cài đặt
        
    Returns:
        str: Giá trị hiện tại
    """
    result = run_adb_command(["adb", "shell", "settings", "get", namespace, key])
    return result if result else "null"

def settings_menu():
    """Menu tùy chỉnh hệ thống"""
    while True:
        namespace = questionary.select(
            "Chọn loại cài đặt:",
            choices=[
                "1️⃣ Cài đặt hệ thống (system)",
                "2️⃣ Cài đặt bảo mật (secure)",
                "3️⃣ Cài đặt toàn cục (global)",
                "4️⃣ Tùy chỉnh tùy ý (custom)",
                "↩️ Quay lại"
            ]
        ).ask()
        
        if not namespace or "Quay lại" in namespace:
            break
            
        if "system" in namespace:
            show_settings_list("system")
        elif "secure" in namespace:
            show_settings_list("secure")
        elif "global" in namespace:
            show_settings_list("global")
        elif "custom" in namespace:
            custom_setting()

def show_settings_list(namespace):
    """
    Hiển thị danh sách cài đặt trong namespace
    
    Args:
        namespace (str): Namespace của cài đặt
    """
    settings = COMMON_SETTINGS[namespace]
    
    table = Table(title=f"Cài đặt {namespace}")
    table.add_column("Tên", style="cyan")
    table.add_column("Mô tả", style="green")
    table.add_column("Giá trị hiện tại", style="yellow")
    
    for setting in settings:
        current_value = get_current_setting(namespace, setting["name"])
        table.add_row(
            setting["name"],
            setting["description"],
            current_value
        )
    
    console.print(table)
    
    setting_name = questionary.select(
        "Chọn cài đặt để thay đổi:",
        choices=[s["name"] for s in settings] + ["↩️ Quay lại"]
    ).ask()
    
    if not setting_name or "Quay lại" in setting_name:
        return
        
    selected_setting = next((s for s in settings if s["name"] == setting_name), None)
    change_setting(namespace, selected_setting)

def change_setting(namespace, setting):
    """
    Thay đổi giá trị của cài đặt
    
    Args:
        namespace (str): Namespace của cài đặt
        setting (dict): Thông tin cài đặt
    """
    current_value = get_current_setting(namespace, setting["name"])
    console.print(f"Giá trị hiện tại: [yellow]{current_value}[/yellow]")
    
    if setting["values"]:
        # Nếu có danh sách giá trị cố định
        value = questionary.select(
            "Chọn giá trị mới:",
            choices=setting["values"] + ["↩️ Hủy"]
        ).ask()
        
        if not value or "Hủy" in value:
            return
    else:
        # Nếu là giá trị tùy chỉnh
        value = questionary.text(
            "Nhập giá trị mới:",
            default=current_value
        ).ask()
        
        if not value:
            return
    
    # Thực hiện thay đổi
    result = run_adb_command(["adb", "shell", "settings", "put", namespace, setting["name"], value])
    
    if result is not None or result == "":  # ADB put thường không trả về output khi thành công
        console.print(f"[bold green]✓[/bold green] Đã thay đổi [cyan]{setting['name']}[/cyan] thành [yellow]{value}[/yellow]")
        log.info(f"Đã thay đổi {namespace}.{setting['name']} từ {current_value} thành {value}")
    else:
        console.print("[bold red]✗[/bold red] Không thể thay đổi cài đặt")

def custom_setting():
    """Tùy chỉnh cài đặt tùy ý"""
    namespace = questionary.select(
        "Chọn namespace:",
        choices=NAMESPACES
    ).ask()
    
    if not namespace:
        return
        
    key = questionary.text("Nhập tên cài đặt:").ask()
    
    if not key:
        return
        
    current_value = get_current_setting(namespace, key)
    console.print(f"Giá trị hiện tại: [yellow]{current_value}[/yellow]")
    
    value = questionary.text(
        "Nhập giá trị mới:",
        default=current_value
    ).ask()
    
    if not value:
        return
        
    # Thực hiện thay đổi
    result = run_adb_command(["adb", "shell", "settings", "put", namespace, key, value])
    
    if result is not None or result == "":
        console.print(f"[bold green]✓[/bold green] Đã thay đổi [cyan]{key}[/cyan] thành [yellow]{value}[/yellow]")
        log.info(f"Đã thay đổi {namespace}.{key} từ {current_value} thành {value}")
    else:
        console.print("[bold red]✗[/bold red] Không thể thay đổi cài đặt")

def dpi_menu():
    """Menu thay đổi DPI và scale màn hình"""
    current_dpi = run_adb_command(["adb", "shell", "wm", "density"])
    current_scale = get_current_setting("system", "font_scale")
    
    if current_dpi:
        # Trích xuất số DPI từ output "Physical density: 420"
        current_dpi = current_dpi.split(":")[-1].strip() if ":" in current_dpi else current_dpi
    
    console.print(f"DPI hiện tại: [yellow]{current_dpi}[/yellow]")
    console.print(f"Tỷ lệ phông chữ hiện tại: [yellow]{current_scale}[/yellow]")
    
    choice = questionary.select(
        "Chọn tùy chọn:",
        choices=[
            "1️⃣ Thay đổi DPI",
            "2️⃣ Thay đổi tỷ lệ phông chữ",
            "3️⃣ Khôi phục về mặc định",
            "↩️ Quay lại"
        ]
    ).ask()
    
    if not choice or "Quay lại" in choice:
        return
        
    if "Thay đổi DPI" in choice:
        new_dpi = questionary.text(
            "Nhập giá trị DPI mới (thông thường từ 160 đến 600):",
            default=current_dpi
        ).ask()
        
        if new_dpi:
            result = run_adb_command(["adb", "shell", "wm", "density", new_dpi])
            console.print(f"[bold green]✓[/bold green] Đã thay đổi DPI thành [yellow]{new_dpi}[/yellow]")
            console.print("[yellow]Lưu ý: Một số thay đổi có thể yêu cầu khởi động lại thiết bị.[/yellow]")
            log.info(f"Đã thay đổi DPI từ {current_dpi} thành {new_dpi}")
            
    elif "Thay đổi tỷ lệ phông chữ" in choice:
        new_scale = questionary.text(
            "Nhập tỷ lệ phông chữ mới (0.85 đến 1.3):",
            default=current_scale
        ).ask()
        
        if new_scale:
            result = run_adb_command(["adb", "shell", "settings", "put", "system", "font_scale", new_scale])
            console.print(f"[bold green]✓[/bold green] Đã thay đổi tỷ lệ phông chữ thành [yellow]{new_scale}[/yellow]")
            log.info(f"Đã thay đổi tỷ lệ phông chữ từ {current_scale} thành {new_scale}")
            
    elif "Khôi phục về mặc định" in choice:
        run_adb_command(["adb", "shell", "wm", "density", "reset"])
        run_adb_command(["adb", "shell", "settings", "put", "system", "font_scale", "1.0"])
        console.print("[bold green]✓[/bold green] Đã khôi phục DPI và tỷ lệ phông chữ về mặc định")
        log.info("Đã khôi phục DPI và tỷ lệ phông chữ về mặc định")
    
    input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    settings_menu() 