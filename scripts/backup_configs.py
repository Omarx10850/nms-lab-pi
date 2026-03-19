#!/usr/bin/env python3
"""
backup_configs.py — Automated System Snapshot Backup Script
NMS Lab | Raspberry Pi Network Monitoring Project

Description:
    Connects to network devices or Linux hosts via SSH using Netmiko,
    collects system information, and saves timestamped backup files.
    Designed to run daily via cron for automated infrastructure documentation.

Usage:
    python3 backup_configs.py

Cron schedule (daily at midnight):
    0 0 * * * python3 /home/pi/backup_configs.py

Author: Omar Al-Zoubi
"""

from netmiko import ConnectHandler
from datetime import datetime
import os

# ─── Device Configuration ─────────────────────────────────────────────────────
# Add additional devices to this list as your infrastructure grows
# Replace YOUR_PI_PASSWORD with your actual password before running
devices = [
    {
        'device_type': 'linux',
        'host': '192.168.0.50',       # nms-pi static IP
        'username': 'pi',              # Linux username
        'password': 'YOUR_PI_PASSWORD', # Set before running
    }
]

# ─── Backup Directory ─────────────────────────────────────────────────────────
BACKUP_DIR = '/home/pi/backups'
os.makedirs(BACKUP_DIR, exist_ok=True)

# ─── Commands to collect system information ───────────────────────────────────
COMMANDS = [
    'uname -a',        # Kernel and OS info
    'uptime',          # System uptime and load
    'df -h',           # Disk usage
    'free -h',         # Memory usage
    'ip addr show',    # Network interfaces
    'docker ps',       # Running containers
]

# ─── Main Backup Loop ─────────────────────────────────────────────────────────
def backup_device(device):
    """Connect to a device and collect system information."""
    host = device['host']
    print(f"[+] Connecting to {host}...")

    try:
        connection = ConnectHandler(**device)
        output = f"Backup Report — {host}\n"
        output += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += "=" * 60 + "\n\n"

        for cmd in COMMANDS:
            output += f"--- {cmd} ---\n"
            output += connection.send_command(cmd)
            output += "\n\n"

        connection.disconnect()

        # Save to timestamped file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{BACKUP_DIR}/{host}_{timestamp}.txt"
        with open(filename, 'w') as f:
            f.write(output)

        print(f"[+] Backup saved: {filename}")

    except Exception as e:
        print(f"[-] Failed to backup {host}: {e}")


if __name__ == '__main__':
    print(f"Starting backup run — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for device in devices:
        backup_device(device)
    print("Backup run complete.")
