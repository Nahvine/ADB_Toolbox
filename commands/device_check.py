#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module kiểm tra kết nối thiết bị Android
"""

import os
import re
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()

def get_connected_devices():
    """
    Lấy danh sách thiết bị Android đang kết nối
    
    Returns:
        list: Danh sách các thiết bị (serial numbers)
    """
    try:
        result = subprocess.run(
            ["adb", "devices"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Bỏ qua dòng tiêu đề
        
        for line in lines:
            if not line.strip():
                continue
                
            parts = line.split('\t')
            if len(parts) >= 2 and "device" in parts[1]:
                devices.append(parts[0].strip())
                
        return devices
    except Exception as e:
        console.print(f"[bold red]Lỗi khi kiểm tra thiết bị: {e}[/bold red]")
        return []

def get_device_info(device_id):
    """
    Lấy thông tin chi tiết về thiết bị
    
    Args:
        device_id (str): Serial number của thiết bị
        
    Returns:
        dict: Thông tin thiết bị
    """
    info = {
        "model": "Không xác định",
        "android_version": "Không xác định",
        "brand": "Không xác định",
        "battery": "Không xác định"
    }
    
    try:
        # Lấy model
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
            capture_output=True, 
            text=True
        )
        info["model"] = result.stdout.strip()
        
        # Lấy phiên bản Android
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.build.version.release"],
            capture_output=True, 
            text=True
        )
        info["android_version"] = result.stdout.strip()
        
        # Lấy thương hiệu
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "getprop", "ro.product.brand"],
            capture_output=True, 
            text=True
        )
        info["brand"] = result.stdout.strip()
        
        # Lấy thông tin pin
        result = subprocess.run(
            ["adb", "-s", device_id, "shell", "dumpsys", "battery"],
            capture_output=True, 
            text=True
        )
        
        match = re.search(r"level: (\d+)", result.stdout)
        if match:
            info["battery"] = f"{match.group(1)}%"
            
        return info
    except Exception as e:
        console.print(f"[bold red]Lỗi khi lấy thông tin thiết bị: {e}[/bold red]")
        return info

def check_devices_menu():
    """Hiển thị menu kiểm tra thiết bị"""
    devices = get_connected_devices()
    
    if not devices:
        console.print("[bold red]Không tìm thấy thiết bị nào![/bold red]")
        console.print("[yellow]Hãy kết nối thiết bị và bật USB Debugging.[/yellow]")
        input("\nNhấn Enter để quay lại...")
        return
        
    console.print(f"[bold green]Đã tìm thấy {len(devices)} thiết bị:[/bold green]")
    
    table = Table(title="Danh sách thiết bị Android")
    table.add_column("STT", style="cyan")
    table.add_column("Serial", style="green")
    table.add_column("Model", style="magenta")
    table.add_column("Thương hiệu", style="yellow")
    table.add_column("Android", style="blue")
    table.add_column("Pin", style="red")
    
    for idx, device_id in enumerate(devices, 1):
        info = get_device_info(device_id)
        table.add_row(
            str(idx),
            device_id,
            info["model"],
            info["brand"],
            info["android_version"],
            info["battery"]
        )
    
    console.print(table)
    input("\nNhấn Enter để quay lại...")
    
if __name__ == "__main__":
    check_devices_menu() 