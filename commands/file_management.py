#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for managing files and screen (push/pull files, browse file system, mirror screen)
"""

import os
import subprocess
import questionary
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from utils import logger
from utils import ui_helper

console = Console()
log = logger.setup_logger()

def run_adb_command(command):
    """
    Run ADB command and return result
    
    Args:
        command (list): ADB command as list of parameters
        
    Returns:
        str: Command result
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
        console.print(f"[bold red]Error running command: {e}[/bold red]")
        return None

def list_directory(path="/sdcard"):
    """
    List directory contents on device
    
    Args:
        path (str): Directory path to list
        
    Returns:
        list: List of files and directories
    """
    result = run_adb_command(["adb", "shell", "ls", "-la", path])
    
    if not result:
        return []
        
    items = []
    for line in result.strip().split('\n'):
        if line.startswith("total") or not line.strip():
            continue
            
        parts = line.split()
        if len(parts) >= 8:
            permissions = parts[0]
            size = parts[4]
            name = " ".join(parts[7:])
            
            is_dir = permissions.startswith("d")
            
            items.append({
                "name": name,
                "size": size,
                "is_dir": is_dir,
                "permissions": permissions
            })
            
    return items

def push_file(local_path, remote_path):
    """
    Push file from computer to device
    
    Args:
        local_path (str): File path on computer
        remote_path (str): Destination path on device
        
    Returns:
        bool: True if successful, False if failed
    """
    if not os.path.exists(local_path):
        console.print(f"[bold red]File not found: {local_path}[/bold red]")
        return False
        
    console.print(f"[yellow]Pushing file: {os.path.basename(local_path)}[/yellow]")
    
    result = run_adb_command(["adb", "push", local_path, remote_path])
    
    if result and "pushed" in result:
        console.print(f"[bold green]✓[/bold green] File pushed successfully!")
        log.info(f"Pushed file {local_path} to {remote_path}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Push failed!")
        return False

def pull_file(remote_path, local_path):
    """
    Pull file from device to computer
    
    Args:
        remote_path (str): File path on device
        local_path (str): Destination path on computer
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print(f"[yellow]Pulling file: {os.path.basename(remote_path)}[/yellow]")
    
    result = run_adb_command(["adb", "pull", remote_path, local_path])
    
    if result and "pulled" in result:
        console.print(f"[bold green]✓[/bold green] File pulled successfully!")
        log.info(f"Pulled file {remote_path} to {local_path}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Pull failed!")
        return False

def delete_file(remote_path):
    """
    Delete file on device
    
    Args:
        remote_path (str): File path to delete
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print(f"[yellow]Deleting file: {remote_path}[/yellow]")
    
    result = run_adb_command(["adb", "shell", "rm", remote_path])
    
    if result is not None:
        console.print(f"[bold green]✓[/bold green] File deleted successfully!")
        log.info(f"Deleted file {remote_path}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Delete failed!")
        return False

def create_directory(remote_path):
    """
    Create directory on device
    
    Args:
        remote_path (str): Directory path to create
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print(f"[yellow]Creating directory: {remote_path}[/yellow]")
    
    result = run_adb_command(["adb", "shell", "mkdir", "-p", remote_path])
    
    if result is not None:
        console.print(f"[bold green]✓[/bold green] Directory created successfully!")
        log.info(f"Created directory {remote_path}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Create failed!")
        return False

def start_screen_mirroring():
    """
    Start screen mirroring
    
    Returns:
        bool: True if successful, False if failed
    """
    console.print("[yellow]Starting screen mirroring...[/yellow]")
    console.print("[yellow]Note: You need to install scrcpy before using this feature.[/yellow]")
    
    try:
        # Check if scrcpy is installed
        result = subprocess.run(
            ["scrcpy", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            console.print("[bold red]scrcpy not found! Please install scrcpy first.[/bold red]")
            console.print("[yellow]Installation guide: https://github.com/Genymobile/scrcpy[/yellow]")
            return False
            
        # Start scrcpy
        subprocess.Popen(["scrcpy"])
        console.print("[bold green]✓[/bold green] Screen mirroring started!")
        log.info("Started screen mirroring")
        return True
        
    except Exception as e:
        console.print(f"[bold red]Error starting screen mirroring: {e}[/bold red]")
        return False

def file_browser(current_path="/sdcard"):
    """
    File browser on device
    
    Args:
        current_path (str): Current path
    """
    while True:
        console.print(f"[bold cyan]Current path: {current_path}[/bold cyan]")
        
        items = list_directory(current_path)
        
        if not items:
            console.print("[bold red]Could not read directory![/bold red]")
            break
            
        # Create choice list
        choices = []
        
        # Add option to go back to parent directory
        if current_path != "/":
            choices.append("📁 .. (Back)")
            
        # Add files and directories
        for item in items:
            if item["is_dir"]:
                choices.append(f"📁 {item['name']}/")
            else:
                size = item["size"]
                choices.append(f"📄 {item['name']} ({size} bytes)")
                
        # Add other options
        choices.extend([
            "📤 Push file to device",
            "📥 Pull file from device",
            "🗑️ Delete file/directory",
            "📁 Create new directory",
            "↩️ Back"
        ])
        
        choice = questionary.select(
            "Select action:",
            choices=choices
        ).ask()
        
        if not choice or "Back" in choice:
            break
            
        if ".. (Back)" in choice:
            # Go back to parent directory
            parent_path = os.path.dirname(current_path)
            if parent_path:
                current_path = parent_path
            else:
                current_path = "/"
                
        elif choice.startswith("📁 ") and not ".." in choice:
            # Enter subdirectory
            dir_name = choice[3:].rstrip("/")
            current_path = os.path.join(current_path, dir_name)
            
        elif "Push file to device" in choice:
            local_path = questionary.path("Enter file path on computer:").ask()
            if local_path:
                remote_path = questionary.text(
                    "Enter destination path on device:",
                    default=os.path.join(current_path, os.path.basename(local_path))
                ).ask()
                
                if remote_path:
                    push_file(local_path, remote_path)
                    
        elif "Pull file from device" in choice:
            file_name = questionary.select(
                "Select file to pull:",
                choices=[item["name"] for item in items if not item["is_dir"]] + ["↩️ Cancel"]
            ).ask()
            
            if file_name and "Cancel" not in file_name:
                local_path = questionary.path("Enter save path:").ask()
                if local_path:
                    remote_path = os.path.join(current_path, file_name)
                    pull_file(remote_path, local_path)
                    
        elif "Delete file/directory" in choice:
            item_name = questionary.select(
                "Select file/directory to delete:",
                choices=[item["name"] for item in items] + ["↩️ Cancel"]
            ).ask()
            
            if item_name and "Cancel" not in item_name:
                if ui_helper.confirm_action(f"Are you sure you want to delete {item_name}?"):
                    remote_path = os.path.join(current_path, item_name)
                    delete_file(remote_path)
                    
        elif "Create new directory" in choice:
            dir_name = questionary.text("Enter new directory name:").ask()
            if dir_name:
                new_dir_path = os.path.join(current_path, dir_name)
                create_directory(new_dir_path)
                
        input("\nPress Enter to continue...")

def file_management_menu():
    """File and screen management menu"""
    while True:
        choice = questionary.select(
            "File and Screen Management:",
            choices=[
                "1️⃣ File Browser",
                "2️⃣ Push File to Device",
                "3️⃣ Pull File from Device",
                "4️⃣ Screen Mirroring",
                "↩️ Back"
            ]
        ).ask()
        
        if not choice or "Back" in choice:
            break
            
        if "File Browser" in choice:
            file_browser()
            
        elif "Push File to Device" in choice:
            local_path = questionary.path("Enter file path on computer:").ask()
            if local_path:
                remote_path = questionary.text(
                    "Enter destination path on device:",
                    default="/sdcard/" + os.path.basename(local_path)
                ).ask()
                
                if remote_path:
                    push_file(local_path, remote_path)
                    
        elif "Pull File from Device" in choice:
            remote_path = questionary.text("Enter file path on device:").ask()
            if remote_path:
                local_path = questionary.path("Enter save path:").ask()
                if local_path:
                    pull_file(remote_path, local_path)
                    
        elif "Screen Mirroring" in choice:
            start_screen_mirroring()

if __name__ == "__main__":
    file_management_menu() 