#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for executing custom commands and backing up settings
"""

import os
import json
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

def execute_custom_command(command):
    """
    Execute custom ADB command
    
    Args:
        command (str): ADB command to execute
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print(f"[yellow]Executing command: {command}[/yellow]")
    
    # Check if command starts with "adb"
    if not command.startswith("adb "):
        command = "adb " + command
        
    result = run_adb_command(command.split())
    
    if result is not None:
        console.print("[bold green]✓[/bold green] Command executed successfully!")
        console.print(f"[cyan]Result:[/cyan]\n{result}")
        log.info(f"Executed command: {command}")
        return True
    else:
        console.print("[bold red]✗[/bold red] Command execution failed!")
        return False

def save_command_preset(name, commands):
    """
    Save command preset to configuration file
    
    Args:
        name (str): Preset name
        commands (list): List of commands
        
    Returns:
        bool: True if successful, False if failed
    """
    preset_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/presets.json")
    
    # Read current configuration
    presets = {}
    if os.path.exists(preset_file):
        try:
            with open(preset_file, "r", encoding="utf-8") as f:
                presets = json.load(f)
        except Exception as e:
            console.print(f"[bold red]Error reading configuration file: {e}[/bold red]")
            return False
    
    # Add new preset
    presets[name] = commands
    
    # Save configuration file
    try:
        with open(preset_file, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=4, ensure_ascii=False)
            
        console.print(f"[bold green]✓[/bold green] Preset '{name}' saved successfully!")
        log.info(f"Saved command preset: {name}")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving configuration file: {e}[/bold red]")
        return False

def backup_settings(backup_file):
    """
    Backup system settings
    
    Args:
        backup_file (str): Backup file path
        
    Returns:
        bool: True if successful, False if failed
    """
    console.print("[yellow]Backing up system settings...[/yellow]")
    
    # Get list of namespaces
    namespaces = ["system", "secure", "global"]
    
    # Create object to store settings
    settings = {}
    
    # Get settings from each namespace
    for namespace in namespaces:
        result = run_adb_command(["adb", "shell", "settings", "list", namespace])
        
        if not result:
            continue
            
        settings[namespace] = {}
        
        for line in result.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                settings[namespace][key.strip()] = value.strip()
    
    # Save to file
    try:
        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
            
        console.print(f"[bold green]✓[/bold green] Settings backed up to: {backup_file}")
        log.info(f"Backed up system settings to {backup_file}")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving backup file: {e}[/bold red]")
        return False

def restore_settings(backup_file):
    """
    Restore system settings from backup file
    
    Args:
        backup_file (str): Backup file path
        
    Returns:
        bool: True if successful, False if failed
    """
    if not os.path.exists(backup_file):
        console.print(f"[bold red]Backup file not found: {backup_file}[/bold red]")
        return False
        
    console.print("[yellow]Restoring system settings...[/yellow]")
    
    try:
        with open(backup_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
            
        # Restore each namespace
        for namespace, values in settings.items():
            console.print(f"[cyan]Restoring {namespace} settings...[/cyan]")
            
            for key, value in values.items():
                result = run_adb_command(["adb", "shell", "settings", "put", namespace, key, value])
                
                if result is None:
                    console.print(f"[bold red]Error restoring {namespace}.{key}[/bold red]")
                    
        console.print("[bold green]✓[/bold green] Settings restored successfully!")
        log.info(f"Restored system settings from {backup_file}")
        return True
    except Exception as e:
        console.print(f"[bold red]Error reading backup file: {e}[/bold red]")
        return False

def custom_command_menu():
    """Custom command execution menu"""
    while True:
        choice = questionary.select(
            "Custom Command Execution:",
            choices=[
                "1️⃣ Execute ADB Command",
                "2️⃣ Create New Preset",
                "3️⃣ Backup System Settings",
                "4️⃣ Restore System Settings",
                "↩️ Back"
            ]
        ).ask()
        
        if not choice or "Back" in choice:
            break
            
        if "Execute ADB Command" in choice:
            command = questionary.text("Enter ADB command:").ask()
            if command:
                execute_custom_command(command)
                
        elif "Create New Preset" in choice:
            name = questionary.text("Enter preset name:").ask()
            if name:
                commands = []
                while True:
                    command = questionary.text("Enter ADB command (leave empty to finish):").ask()
                    if not command:
                        break
                    commands.append(command)
                    
                if commands:
                    save_command_preset(name, commands)
                    
        elif "Backup System Settings" in choice:
            backup_file = questionary.path("Enter backup file path:").ask()
            if backup_file:
                backup_settings(backup_file)
                
        elif "Restore System Settings" in choice:
            backup_file = questionary.path("Enter backup file path:").ask()
            if backup_file:
                if ui_helper.confirm_action("Are you sure you want to restore system settings? This may cause data loss."):
                    restore_settings(backup_file)

if __name__ == "__main__":
    custom_command_menu() 