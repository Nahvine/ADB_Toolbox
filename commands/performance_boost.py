#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module tăng hiệu suất và dọn rác cho Android
"""

import os
import re
import time
import subprocess
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from utils import logger

console = Console()
log = logger.setup_logger()

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

def get_package_list():
    """
    Lấy danh sách các ứng dụng đã cài đặt
    
    Returns:
        list: Danh sách tên package của các ứng dụng
    """
    result = run_adb_command(["adb", "shell", "pm", "list", "packages", "-3"])
    
    if not result:
        return []
        
    packages = []
    for line in result.strip().split('\n'):
        if line.startswith("package:"):
            packages.append(line[8:])  # Bỏ "package:" ở đầu
            
    return packages

def clear_app_cache(package):
    """
    Xóa cache của ứng dụng
    
    Args:
        package (str): Tên package của ứng dụng
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    result = run_adb_command(["adb", "shell", "pm", "clear", package])
    return result is not None

def force_stop_app(package):
    """
    Dừng ứng dụng đang chạy
    
    Args:
        package (str): Tên package của ứng dụng
        
    Returns:
        bool: True nếu thành công, False nếu thất bại
    """
    result = run_adb_command(["adb", "shell", "am", "force-stop", package])
    return result is not None

def clear_all_cache():
    """Xóa cache của tất cả ứng dụng"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        packages = get_package_list()
        
        if not packages:
            console.print("[bold red]Không tìm thấy ứng dụng nào![/bold red]")
            return
            
        task = progress.add_task("[green]Đang xóa cache...", total=len(packages))
        
        count = 0
        for package in packages:
            progress.update(task, description=f"[green]Đang xóa cache: {package}")
            result = clear_app_cache(package)
            
            if result:
                count += 1
                
            progress.advance(task)
            
        console.print(f"[bold green]✓[/bold green] Đã xóa cache của {count}/{len(packages)} ứng dụng")
        log.info(f"Đã xóa cache của {count}/{len(packages)} ứng dụng")

def kill_background_apps():
    """Dừng các ứng dụng đang chạy nền"""
    result = run_adb_command(["adb", "shell", "ps"])
    
    if not result:
        console.print("[bold red]Không thể lấy danh sách tiến trình![/bold red]")
        return
        
    # Lọc các tiến trình Android app (thường có tên package là com.*)
    app_processes = []
    for line in result.strip().split('\n'):
        if "com." in line:
            parts = line.split()
            if len(parts) >= 9:  # Đảm bảo đủ cột
                pid = parts[1]
                package = parts[-1]
                if package.startswith("com."):
                    app_processes.append((pid, package))
    
    console.print(f"[yellow]Tìm thấy {len(app_processes)} ứng dụng đang chạy nền[/yellow]")
    
    count = 0
    for pid, package in app_processes:
        if force_stop_app(package):
            count += 1
            console.print(f"[green]Đã dừng: {package}[/green]")
            
    console.print(f"[bold green]✓[/bold green] Đã dừng {count}/{len(app_processes)} ứng dụng")
    log.info(f"Đã dừng {count}/{len(app_processes)} ứng dụng nền")

def increase_virtual_memory():
    """Tăng bộ nhớ ảo (swap) cho Android"""
    # Kiểm tra xem thiết bị có hỗ trợ thay đổi swap không
    result = run_adb_command(["adb", "shell", "su", "-c", "cat /proc/swaps"])
    
    if "Permission denied" in result or "not found" in result:
        console.print("[bold red]Thiết bị không được root hoặc không hỗ trợ swap![/bold red]")
        return False
        
    current_swap = "0MB"
    if result and "Filename" in result:
        lines = result.strip().split('\n')
        if len(lines) > 1:
            # Đã có swap
            parts = lines[1].split()
            if len(parts) >= 3:
                current_swap = f"{int(parts[2]) // 1024}MB"
    
    console.print(f"Swap hiện tại: [yellow]{current_swap}[/yellow]")
    
    choice = questionary.select(
        "Chọn kích thước swap mới:",
        choices=[
            "512MB",
            "1024MB (1GB)",
            "2048MB (2GB)",
            "Tắt swap",
            "↩️ Hủy"
        ]
    ).ask()
    
    if not choice or "Hủy" in choice:
        return False
        
    if "Tắt swap" in choice:
        result = run_adb_command(["adb", "shell", "su", "-c", "swapoff /data/swapfile"])
        if result is not None:
            console.print("[bold green]✓[/bold green] Đã tắt swap")
            log.info("Đã tắt swap")
        return True
        
    # Trích xuất kích thước (chỉ lấy số)
    swap_size = re.search(r"(\d+)", choice).group(1)
    
    # Tạo swap file mới
    commands = [
        f"dd if=/dev/zero of=/data/swapfile bs=1m count={swap_size}",
        "chmod 600 /data/swapfile",
        "mkswap /data/swapfile",
        "swapon /data/swapfile"
    ]
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("[green]Đang tạo swap...", total=len(commands))
        
        for cmd in commands:
            progress.update(task, description=f"[green]Đang chạy: {cmd}")
            run_adb_command(["adb", "shell", "su", "-c", cmd])
            progress.advance(task)
            
    console.print(f"[bold green]✓[/bold green] Đã tạo swap mới với kích thước {swap_size}MB")
    log.info(f"Đã tạo swap mới với kích thước {swap_size}MB")
    return True

def tweak_performance():
    """Tối ưu hiệu suất Android"""
    tweaks = [
        {"name": "Tắt hiệu ứng hình ảnh", "commands": [
            "adb shell settings put global window_animation_scale 0.0",
            "adb shell settings put global transition_animation_scale 0.0",
            "adb shell settings put global animator_duration_scale 0.0"
        ]},
        {"name": "Giảm thời gian chờ khi tắt ứng dụng", "commands": [
            "adb shell settings put global activity_manager_constants max_cached_processes=32"
        ]},
        {"name": "Tắt kiểm tra crash ứng dụng", "commands": [
            "adb shell settings put global anr_show_background false"
        ]},
        {"name": "Tối ưu RAM", "commands": [
            "adb shell settings put global sys.use_fifo_ui 1"
        ]}
    ]
    
    choice = questionary.select(
        "Chọn cách tối ưu:",
        choices=[
            "1️⃣ Áp dụng tất cả",
            "2️⃣ Chọn từng tùy chọn",
            "3️⃣ Khôi phục về mặc định",
            "↩️ Quay lại"
        ]
    ).ask()
    
    if not choice or "Quay lại" in choice:
        return
        
    if "Áp dụng tất cả" in choice:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("[green]Đang áp dụng tối ưu...", total=len(tweaks))
            
            for tweak in tweaks:
                progress.update(task, description=f"[green]Đang áp dụng: {tweak['name']}")
                
                for cmd in tweak["commands"]:
                    os.system(cmd)
                    time.sleep(0.2)
                    
                progress.advance(task)
                
        console.print("[bold green]✓[/bold green] Đã áp dụng tất cả các tối ưu")
        log.info("Đã áp dụng tất cả các tối ưu hiệu suất")
        
    elif "Chọn từng tùy chọn" in choice:
        for tweak in tweaks:
            apply = questionary.confirm(f"Áp dụng: {tweak['name']}?").ask()
            
            if apply:
                for cmd in tweak["commands"]:
                    os.system(cmd)
                    time.sleep(0.2)
                
                console.print(f"[green]Đã áp dụng: {tweak['name']}[/green]")
                log.info(f"Đã áp dụng tối ưu: {tweak['name']}")
                
    elif "Khôi phục về mặc định" in choice:
        reset_commands = [
            "adb shell settings put global window_animation_scale 1.0",
            "adb shell settings put global transition_animation_scale 1.0",
            "adb shell settings put global animator_duration_scale 1.0",
            "adb shell settings delete global activity_manager_constants",
            "adb shell settings put global anr_show_background true",
            "adb shell settings put global sys.use_fifo_ui 0"
        ]
        
        for cmd in reset_commands:
            os.system(cmd)
            time.sleep(0.2)
            
        console.print("[bold green]✓[/bold green] Đã khôi phục tất cả cài đặt về mặc định")
        log.info("Đã khôi phục cài đặt hiệu suất về mặc định")
    
    input("\nNhấn Enter để tiếp tục...")

def boost_menu():
    """Menu tăng hiệu suất và dọn rác"""
    while True:
        choice = questionary.select(
            "Chọn tính năng:",
            choices=[
                "1️⃣ Dọn rác - Xóa cache ứng dụng",
                "2️⃣ Dừng ứng dụng chạy nền",
                "3️⃣ Tăng bộ nhớ ảo (yêu cầu root)",
                "4️⃣ Tối ưu hiệu suất",
                "5️⃣ Chế độ tăng tốc nhanh (chạy tất cả)",
                "↩️ Quay lại"
            ]
        ).ask()
        
        if not choice or "Quay lại" in choice:
            break
            
        if "Dọn rác" in choice:
            clear_all_cache()
        elif "Dừng ứng dụng" in choice:
            kill_background_apps()
        elif "Tăng bộ nhớ ảo" in choice:
            increase_virtual_memory()
        elif "Tối ưu hiệu suất" in choice:
            tweak_performance()
        elif "Chế độ tăng tốc nhanh" in choice:
            console.print(Panel("[bold yellow]Bắt đầu quá trình tăng tốc toàn diện.[/bold yellow]"))
            
            console.print("[cyan]Bước 1: Dọn rác ứng dụng[/cyan]")
            clear_all_cache()
            
            console.print("[cyan]Bước 2: Dừng ứng dụng chạy nền[/cyan]")
            kill_background_apps()
            
            console.print("[cyan]Bước 3: Tối ưu hiệu suất[/cyan]")
            os.system("adb shell settings put global window_animation_scale 0.5")
            os.system("adb shell settings put global transition_animation_scale 0.5")
            os.system("adb shell settings put global animator_duration_scale 0.5")
            
            console.print("[bold green]✓[/bold green] Quá trình tăng tốc đã hoàn tất!")
            log.info("Đã thực hiện tăng tốc nhanh toàn diện")
            
            input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    boost_menu() 