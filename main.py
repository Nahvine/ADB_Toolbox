#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ADB Toolbox - Công cụ điều khiển thiết bị Android qua giao diện dòng lệnh
"""

import os
import sys
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import questionary

# Import các module từ thư mục commands
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from commands import device_check
from commands import system_settings
from commands import performance_boost
from utils import logger
from utils import ui_helper

# Khởi tạo console
console = Console()
log = logger.setup_logger()

def show_header():
    """Hiển thị header của ứng dụng"""
    console.print(Panel(
        Text("ADB TOOLBOX", style="bold yellow"), 
        subtitle="v1.0", 
        style="bold blue"
    ))
    
    console.print("[bold green]Chào mừng đến với ADB Toolbox![/bold green]")
    console.print("Công cụ điều khiển thiết bị Android không cần nhớ lệnh ADB.\n")

def main_menu():
    """Hiển thị menu chính của ứng dụng"""
    while True:
        show_header()
        
        # Kiểm tra thiết bị đang kết nối
        devices = device_check.get_connected_devices()
        if devices:
            console.print(f"[bold green]✓[/bold green] {len(devices)} thiết bị đang kết nối.")
        else:
            console.print("[bold red]✗[/bold red] Không có thiết bị Android nào đang kết nối!")
            console.print("[yellow]Hãy kết nối thiết bị của bạn và bật chế độ gỡ lỗi (USB Debugging).[/yellow]\n")
        
        choice = questionary.select(
            "Chọn tính năng:",
            choices=[
                "1️⃣ Kiểm tra thiết bị kết nối",
                "2️⃣ Các lệnh ADB nhanh",
                "3️⃣ Tuỳ chỉnh hệ thống ẩn",
                "4️⃣ Dọn rác & Tăng tốc",
                "5️⃣ Thay đổi DPI & Scale",
                "6️⃣ Shortcut cấu hình sẵn",
                "7️⃣ Xem lịch sử thao tác",
                "🔄 Làm mới thiết bị",
                "❓ Trợ giúp",
                "❌ Thoát"
            ]
        ).ask()
        
        if not choice:
            continue
        
        if "Kiểm tra thiết bị kết nối" in choice:
            device_check.check_devices_menu()
        elif "Các lệnh ADB nhanh" in choice:
            quick_commands_menu()
        elif "Tuỳ chỉnh hệ thống ẩn" in choice:
            system_settings.settings_menu()
        elif "Dọn rác & Tăng tốc" in choice:
            performance_boost.boost_menu()
        elif "Thay đổi DPI & Scale" in choice:
            system_settings.dpi_menu()
        elif "Shortcut cấu hình sẵn" in choice:
            load_presets()
        elif "Xem lịch sử thao tác" in choice:
            view_logs()
        elif "Làm mới thiết bị" in choice:
            refresh_devices()
        elif "Trợ giúp" in choice:
            show_help()
        elif "Thoát" in choice:
            console.print("[yellow]Cảm ơn bạn đã sử dụng ADB Toolbox! Tạm biệt.[/yellow]")
            sys.exit(0)

def quick_commands_menu():
    """Menu các lệnh ADB nhanh"""
    choices = [
        "↩️ Quay lại",
        "🔄 Khởi động lại thiết bị",
        "🔄 Khởi động lại vào Recovery",
        "🔄 Khởi động lại vào Bootloader",
        "📱 Thông tin thiết bị",
        "📊 Hiển thị logcat",
        "🔌 Sideload (cài đặt ROM/ZIP)"
    ]
    
    choice = questionary.select("Chọn lệnh nhanh:", choices=choices).ask()
    
    if not choice or "Quay lại" in choice:
        return
    
    if "Khởi động lại thiết bị" in choice:
        os.system("adb reboot")
        log.info("Đã khởi động lại thiết bị")
    elif "Khởi động lại vào Recovery" in choice:
        os.system("adb reboot recovery")
        log.info("Đã khởi động lại vào Recovery")
    elif "Khởi động lại vào Bootloader" in choice:
        os.system("adb reboot bootloader")
        log.info("Đã khởi động lại vào Bootloader")
    elif "Thông tin thiết bị" in choice:
        ui_helper.run_command_and_display("adb shell getprop | grep model")
    elif "Hiển thị logcat" in choice:
        console.print("[yellow]Đang hiển thị logcat. Nhấn Ctrl+C để dừng...[/yellow]")
        os.system("adb logcat")
    elif "Sideload" in choice:
        console.print("[yellow]Vui lòng chọn file ZIP để sideload...[/yellow]")
        # Thêm code chọn file ở đây
        
def refresh_devices():
    """Làm mới danh sách thiết bị"""
    console.print("[yellow]Đang làm mới danh sách thiết bị...[/yellow]")
    os.system("adb kill-server")
    time.sleep(1)
    os.system("adb start-server")
    time.sleep(1)
    device_check.check_devices_menu()

def view_logs():
    """Xem lịch sử thao tác"""
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/adb_toolbox.log"), "r") as f:
            logs = f.readlines()
            
        table = Table(title="Lịch sử thao tác")
        table.add_column("Thời gian", style="cyan")
        table.add_column("Thao tác", style="green")
        
        for log_line in logs[-20:]:  # Chỉ hiển thị 20 dòng gần nhất
            parts = log_line.strip().split(" - ", 1)
            if len(parts) >= 2:
                timestamp, action = parts
                table.add_row(timestamp, action)
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Lỗi khi đọc file log: {e}[/bold red]")
    
    input("\nNhấn Enter để tiếp tục...")

def load_presets():
    """Tải các cấu hình đã lưu"""
    preset_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/presets.json")
    
    if not os.path.exists(preset_file):
        console.print("[yellow]Chưa có cấu hình nào được lưu.[/yellow]")
        return
    
    try:
        with open(preset_file, "r") as f:
            presets = json.load(f)
        
        choices = ["↩️ Quay lại"] + list(presets.keys())
        choice = questionary.select("Chọn cấu hình:", choices=choices).ask()
        
        if not choice or "Quay lại" in choice:
            return
        
        commands = presets[choice]
        console.print(f"[green]Đang chạy cấu hình: {choice}[/green]")
        
        for cmd in commands:
            console.print(f"[yellow]Đang chạy: {cmd}[/yellow]")
            os.system(cmd)
            time.sleep(0.5)
            
        console.print("[bold green]Hoàn tất![/bold green]")
        input("Nhấn Enter để tiếp tục...")
            
    except Exception as e:
        console.print(f"[bold red]Lỗi khi tải cấu hình: {e}[/bold red]")

def show_help():
    """Hiển thị thông tin trợ giúp"""
    help_text = """
    [bold green]HƯỚNG DẪN SỬ DỤNG[/bold green]
    
    [cyan]1. Đảm bảo thiết bị Android của bạn được kết nối và đã bật USB Debugging.[/cyan]
    [cyan]2. Chọn các tính năng từ menu chính để thực hiện.[/cyan]
    [cyan]3. Với các tùy chỉnh hệ thống, hãy cẩn thận vì một số thay đổi có thể ảnh hưởng đến thiết bị.[/cyan]
    
    [bold yellow]Lưu ý:[/bold yellow] Các thao tác đều được ghi vào log để bạn có thể kiểm tra lại sau.
    
    [bold red]Khắc phục sự cố:[/bold red]
    - Nếu thiết bị không được phát hiện, hãy kiểm tra:
      + Cáp USB có được kết nối không
      + USB Debugging đã được bật chưa
      + Driver USB đã được cài đặt
    - Khởi động lại công cụ ADB Toolbox nếu gặp vấn đề
    
    [bold green]Liên hệ hỗ trợ:[/bold green] example@email.com
    """
    
    console.print(Panel(help_text, title="Trợ giúp", border_style="green"))
    input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    try:
        # Đảm bảo thư mục logs tồn tại
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Đã dừng chương trình.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Lỗi không mong muốn: {e}[/bold red]")
        log.error(f"Lỗi không mong muốn: {e}")
        sys.exit(1) 