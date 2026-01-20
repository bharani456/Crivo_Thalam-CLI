#!/usr/bin/env python3
"""
Crivo Thalam CLI - Device Authentication and Management
"""

import click
import requests
import json
import platform
import socket
import uuid
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

# Configuration
API_URL = os.getenv("CRIVO_API_URL", "http://localhost:8000")
CONFIG_DIR = Path.home() / ".crivo_thalam"
CONFIG_FILE = CONFIG_DIR / "device.json"


def get_device_info():
    """Collect device information"""
    return {
        "device_name": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "device_id": str(uuid.getnode())  # MAC address as unique ID
    }


def save_device_config(data):
    """Save device configuration locally"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    console.print(f"[green]✓[/green] Configuration saved to {CONFIG_FILE}")


def load_device_config():
    """Load device configuration"""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


@click.group()
def cli():
    """Crivo Thalam CLI - Device Management"""
    pass


@cli.command()
def setup():
    """Setup and register this device"""
    console.print(Panel.fit(
        "[bold cyan]Crivo Thalam Device Setup[/bold cyan]\n"
        "This will register your device and generate an authorization link.",
        border_style="cyan"
    ))
    
    # Check if already configured
    existing_config = load_device_config()
    if existing_config:
        console.print("\n[yellow]⚠[/yellow]  Device already configured!")
        console.print(f"Device ID: [cyan]{existing_config.get('device_id')}[/cyan]")
        
        if not click.confirm("Do you want to reconfigure?", default=False):
            return
    
    # Get device information
    console.print("\n[bold]Collecting device information...[/bold]")
    device_info = get_device_info()
    
    # Display device info
    table = Table(title="Device Information", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in device_info.items():
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(table)
    
    # Request device registration
    console.print("\n[bold]Registering device with Crivo Thalam...[/bold]")
    
    try:
        response = requests.post(
            f"{API_URL}/api/devices/register",
            json=device_info,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            
            # Save configuration
            save_device_config({
                "device_id": data["device_id"],
                "device_name": device_info["device_name"],
                "auth_link": data["auth_link"],
                "is_authorized": False
            })
            
            # Display success message with auth link
            console.print("\n[green]✓[/green] Device registered successfully!\n")
            
            console.print(Panel.fit(
                f"[bold yellow]Authorization Required[/bold yellow]\n\n"
                f"Please visit this link to authorize your device:\n\n"
                f"[bold cyan]{data['auth_link']}[/bold cyan]\n\n"
                f"Device ID: [dim]{data['device_id']}[/dim]",
                border_style="yellow"
            ))
            
            console.print("\n[dim]After authorizing, run: [bold]crivo-thalam status[/bold] to check status[/dim]")
            
        else:
            console.print(f"[red]✗[/red] Registration failed: {response.json().get('detail', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        console.print(f"[red]✗[/red] Could not connect to Crivo Thalam API at {API_URL}")
        console.print("[dim]Make sure the backend server is running[/dim]")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.command()
def status():
    """Check device authorization status"""
    config = load_device_config()
    
    if not config:
        console.print("[red]✗[/red] Device not configured. Run [bold]crivo-thalam setup[/bold] first.")
        return
    
    console.print(Panel.fit(
        "[bold cyan]Device Status[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        response = requests.get(
            f"{API_URL}/api/devices/{config['device_id']}/status",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Update local config
            config['is_authorized'] = data['is_authorized']
            if data.get('authorized_by'):
                config['authorized_by'] = data['authorized_by']
            save_device_config(config)
            
            # Display status
            table = Table(show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value")
            
            table.add_row("Device ID", config['device_id'])
            table.add_row("Device Name", config['device_name'])
            table.add_row("Status", 
                         "[green]✓ Authorized[/green]" if data['is_authorized'] 
                         else "[yellow]⚠ Pending Authorization[/yellow]")
            
            if data.get('authorized_by'):
                table.add_row("Authorized By", data['authorized_by'])
            if data.get('authorized_at'):
                table.add_row("Authorized At", data['authorized_at'])
            
            console.print(table)
            
            if not data['is_authorized']:
                console.print(f"\n[yellow]Authorization Link:[/yellow]\n{config['auth_link']}")
                
        else:
            console.print(f"[red]✗[/red] Could not fetch status: {response.json().get('detail', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        console.print(f"[red]✗[/red] Could not connect to Crivo Thalam API at {API_URL}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {str(e)}")


@cli.command()
def info():
    """Show device configuration"""
    config = load_device_config()
    
    if not config:
        console.print("[red]✗[/red] Device not configured. Run [bold]crivo-thalam setup[/bold] first.")
        return
    
    console.print(Panel.fit(
        "[bold cyan]Device Configuration[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print(json.dumps(config, indent=2))


@cli.command()
def reset():
    """Reset device configuration"""
    if CONFIG_FILE.exists():
        if click.confirm("Are you sure you want to reset device configuration?", default=False):
            CONFIG_FILE.unlink()
            console.print("[green]✓[/green] Device configuration reset successfully")
    else:
        console.print("[yellow]⚠[/yellow]  No configuration found")


if __name__ == "__main__":
    cli()
