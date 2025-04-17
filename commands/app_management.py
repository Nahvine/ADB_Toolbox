#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for managing Android applications (install, uninstall, backup and restore)
"""

import os
import re
import subprocess
import questionary
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

def get_installed_apps():
    """
    Get list of installed applications
    
    Returns:
        list: List of package names
    """
    result = run_adb_command(["adb", "shell", "pm", "list", "packages", "-3"])
    
    if not result:
        return []
        
    packages = []
    for line in result.strip().split('\n'):
        if line.startswith("package:"):
            packages.append(line[8:])  # Remove "package:" prefix
            
    return packages

def get_app_info(package):
    """
    Get detailed information about an application
    
    Args:
        package (str): Package name
        
    Returns:
        dict: Application information
    """
    info = {
        "name": "Unknown",
        "version": "Unknown",
        "size": "Unknown",
        "path": "Unknown"
    }
    
    # Get app name
    result = run_adb_command(["adb", "shell", "dumpsys", "package", package, "|", "grep", "versionName"])
    if result:
        match = re.search(r"versionName=([^\s]+)", result)
        if match:
            info["version"] = match.group(1)
    
    # Get APK path
    result = run_adb_command(["adb", "shell", "pm", "path", package])
    if result and result.startswith("package:"):
        info["path"] = result[8:].strip()
    
    # Get display name
    result = run_adb_command(["adb", "shell", "dumpsys", "package", package, "|", "grep", "applicationInfo"])
    if result:
        match = re.search(r"labelRes=\d+ label=([^\s]+)", result)
        if match:
            info["name"] = match.group(1)
    
    return info

def install_app(apk_path):
    """
    Install application from APK file
    
    Args:
        apk_path (str): Path to APK file
        
    Returns:
        bool: True if successful, False if failed
    """
    if not os.path.exists(apk_path):
        console.print(f"[bold red]File not found: {apk_path}[/bold red]")
        return False
        
    console.print(f"[yellow]Installing: {os.path.basename(apk_path)}[/yellow]")
    
    result = run_adb_command(["adb", "install", "-r", apk_path])
    
    if result and "Success" in result:
        console.print("[bold green]✓[/bold green] Installation successful!")
        log.info(f"Installed application: {apk_path}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Installation failed!")
        return False

def uninstall_app(package):
    """
    Uninstall application
    
    Args:
        package (str): Package name
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print(f"[yellow]Uninstalling: {package}[/yellow]")
    
    result = run_adb_command(["adb", "uninstall", package])
    
    if result and "Success" in result:
        console.print("[bold green]✓[/bold green] Uninstallation successful!")
        log.info(f"Uninstalled application: {package}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Uninstallation failed!")
        return False

def backup_app(package, backup_dir):
    """
    Backup application
    
    Args:
        package (str): Package name
        backup_dir (str): Backup directory
        
    Returns:
        bool: True if successful, False if failed
    """
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Get APK path
    result = run_adb_command(["adb", "shell", "pm", "path", package])
    if not result or not result.startswith("package:"):
        console.print("[bold red]Could not get APK path![/bold red]")
        return False
        
    apk_path = result[8:].strip()
    
    # Create backup filename
    backup_file = os.path.join(backup_dir, f"{package}.apk")
    
    # Backup APK
    console.print(f"[yellow]Backing up: {package}[/yellow]")
    result = run_adb_command(["adb", "pull", apk_path, backup_file])
    
    if result and "pulled" in result:
        console.print(f"[bold green]✓[/bold green] Backed up to: {backup_file}")
        log.info(f"Backed up application {package} to {backup_file}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Backup failed!")
        return False

def restore_app(apk_path):
    """
    Restore application from backed up APK file
    
    Args:
        apk_path (str): Path to backed up APK file
        
    Returns:
        bool: True if successful, False if failed
    """
    return install_app(apk_path)

def app_management_menu():
    """Application management menu"""
    while True:
        choice = questionary.select(
            "Application Management:",
            choices=[
                "1️⃣ Install Application",
                "2️⃣ Uninstall Application",
                "3️⃣ Backup Application",
                "4️⃣ Restore Application",
                "5️⃣ View Installed Apps",
                "↩️ Back"
            ]
        ).ask()
        
        if not choice or "Back" in choice:
            break
            
        if "Install Application" in choice:
            apk_path = questionary.path("Enter path to APK file:").ask()
            if apk_path:
                install_app(apk_path)
                
        elif "Uninstall Application" in choice:
            packages = get_installed_apps()
            if not packages:
                console.print("[bold red]No applications found![/bold red]")
                continue
                
            package = questionary.select(
                "Select application to uninstall:",
                choices=packages + ["↩️ Cancel"]
            ).ask()
            
            if package and "Cancel" not in package:
                uninstall_app(package)
                
        elif "Backup Application" in choice:
            packages = get_installed_apps()
            if not packages:
                console.print("[bold red]No applications found![/bold red]")
                continue
                
            package = questionary.select(
                "Select application to backup:",
                choices=packages + ["↩️ Cancel"]
            ).ask()
            
            if package and "Cancel" not in package:
                backup_dir = questionary.path("Enter backup directory:").ask()
                if backup_dir:
                    backup_app(package, backup_dir)
                    
        elif "Restore Application" in choice:
            apk_path = questionary.path("Enter path to backed up APK file:").ask()
            if apk_path:
                restore_app(apk_path)
                
        elif "View Installed Apps" in choice:
            packages = get_installed_apps()
            if not packages:
                console.print("[bold red]No applications found![/bold red]")
                continue
                
            table = ui_helper.display_table(
                "Installed Applications",
                ["No.", "Package Name", "Version", "Path"],
                [[i+1, pkg, get_app_info(pkg)["version"], get_app_info(pkg)["path"]] for i, pkg in enumerate(packages)]
            )
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app_management_menu() 