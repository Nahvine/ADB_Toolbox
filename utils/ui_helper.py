#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module hỗ trợ giao diện người dùng cho ADB Toolbox
"""

import os
import subprocess
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.rule import Rule
from rich.prompt import Prompt
from . import logger

console = Console()
log = logger.setup_logger()

ASCII_LOGO = r"""
    _    ____  ____    _____           _ _               
   / \  |  _ \| __ )  |_   _|__   ___ | | |__   _____  __
  / _ \ | | | |  _ \    | |/ _ \ / _ \| | '_ \ / _ \ \/ /
 / ___ \| |_| | |_) |   | | (_) | (_) | | |_) | (_) >  < 
/_/   \_\____/|____/    |_|\___/ \___/|_|_.__/ \___/_/\_\
"""

def show_logo():
    """Hiển thị logo ASCII"""
    console.print(Text(ASCII_LOGO, style="bold yellow"))
    console.print(Rule("[bold blue]Android Debug Bridge Toolbox[/bold blue]"))
    console.print("")

def run_command_and_display(command, title=None):
    """
    Chạy lệnh và hiển thị kết quả
    
    Args:
        command (str): Lệnh cần chạy
        title (str, optional): Tiêu đề cho kết quả
    """
    if title:
        console.print(f"[bold cyan]{title}:[/bold cyan]")
        
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task("[green]Đang chạy lệnh...", total=1)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            progress.update(task, completed=1)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    console.print(Panel(output, title=command, border_style="green"))
                else:
                    console.print("[yellow]Lệnh đã thực thi nhưng không có kết quả trả về.[/yellow]")
            else:
                console.print(f"[bold red]Lỗi khi chạy lệnh: {result.stderr}[/bold red]")
                
            # Ghi log
            log.info(f"Đã chạy lệnh: {command}")
                
        except Exception as e:
            progress.update(task, completed=1)
            console.print(f"[bold red]Lỗi: {e}[/bold red]")
            log.error(f"Lỗi khi chạy lệnh {command}: {e}")
    
    return

def display_table(title, headers, rows):
    """
    Hiển thị dữ liệu dạng bảng
    
    Args:
        title (str): Tiêu đề của bảng
        headers (list): Danh sách tiêu đề cột
        rows (list): Danh sách các hàng dữ liệu
    """
    table = Table(title=title)
    
    # Thêm các cột
    for idx, header in enumerate(headers):
        style = "cyan" if idx % 2 == 0 else "green"
        table.add_column(header, style=style)
    
    # Thêm các hàng
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)

def progress_operation(description, operations, on_complete=None):
    """
    Hiển thị tiến trình cho một chuỗi thao tác
    
    Args:
        description (str): Mô tả thao tác
        operations (list): Danh sách các thao tác cần thực hiện
        on_complete (callable, optional): Hàm callback khi hoàn thành
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task(description, total=len(operations))
        
        results = []
        for idx, operation in enumerate(operations, 1):
            operation_desc = operation.get("description", f"Thao tác {idx}")
            progress.update(task, description=f"[green]{operation_desc}")
            
            try:
                if "command" in operation:
                    result = subprocess.run(
                        operation["command"],
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    results.append({
                        "success": result.returncode == 0,
                        "output": result.stdout if result.returncode == 0 else result.stderr,
                        "operation": operation
                    })
                elif "function" in operation and callable(operation["function"]):
                    result = operation["function"](*operation.get("args", []), **operation.get("kwargs", {}))
                    results.append({
                        "success": True,
                        "output": result,
                        "operation": operation
                    })
            except Exception as e:
                results.append({
                    "success": False,
                    "output": str(e),
                    "operation": operation
                })
                
            progress.advance(task)
            time.sleep(0.2)  # Giảm thiểu hiệu ứng nhấp nháy
        
        if on_complete and callable(on_complete):
            on_complete(results)
            
        return results

def confirm_action(message, default=False):
    """
    Xác nhận hành động từ người dùng
    
    Args:
        message (str): Thông báo xác nhận
        default (bool, optional): Giá trị mặc định
        
    Returns:
        bool: True nếu người dùng xác nhận, False nếu không
    """
    yes_no = "(Y/n)" if default else "(y/N)"
    response = Prompt.ask(f"{message} {yes_no}", default="y" if default else "n")
    return response.lower() in ("y", "yes", "có", "co", "c")

def show_animation(message, duration=2):
    """
    Hiển thị animation quay với thông báo
    
    Args:
        message (str): Thông báo hiển thị
        duration (int, optional): Thời gian hiển thị (giây)
    """
    spinners = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    
    end_time = time.time() + duration
    i = 0
    
    try:
        while time.time() < end_time:
            console.print(f"\r{spinners[i % len(spinners)]} {message}", end="")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            
        console.print("\r" + " " * (len(message) + 2) + "\r", end="")
    except KeyboardInterrupt:
        console.print("\r" + " " * (len(message) + 2) + "\r", end="")
        raise

def error_message(message):
    """
    Hiển thị thông báo lỗi
    
    Args:
        message (str): Thông báo lỗi
    """
    console.print(f"[bold red]❌ Lỗi: {message}[/bold red]")

def success_message(message):
    """
    Hiển thị thông báo thành công
    
    Args:
        message (str): Thông báo thành công
    """
    console.print(f"[bold green]✓ {message}[/bold green]")

def warning_message(message):
    """
    Hiển thị cảnh báo
    
    Args:
        message (str): Thông báo cảnh báo
    """
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")

def clear_screen():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Test UI elements
    clear_screen()
    show_logo()
    
    success_message("Đây là thông báo thành công")
    warning_message("Đây là thông báo cảnh báo")
    error_message("Đây là thông báo lỗi")
    
    display_table(
        "Bảng dữ liệu mẫu", 
        ["STT", "Tên", "Giá trị"], 
        [
            [1, "Item 1", 100],
            [2, "Item 2", 200],
            [3, "Item 3", 300]
        ]
    )
    
    run_command_and_display("echo Hello ADB Toolbox", "Lệnh mẫu")
    
    operations = [
        {"description": "Thao tác 1", "command": "echo 'Test 1'"},
        {"description": "Thao tác 2", "command": "echo 'Test 2'"},
        {"description": "Thao tác 3", "command": "echo 'Test 3'"}
    ]
    
    def on_complete(results):
        success_message("Đã hoàn thành tất cả thao tác!")
        
    progress_operation("Đang thực hiện thao tác mẫu", operations, on_complete)
    
    input("Nhấn Enter để kết thúc...") 