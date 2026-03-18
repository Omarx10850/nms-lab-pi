from netmiko import ConnectHandler
from datetime import datetime
import os

# Device list
devices = [
    {
        'device_type': 'linux',
        'host': '192.168.0.50',
        'username': 'pi',
        'password': 'THE_PI_PASSWORD',
    }
]

# Create backup directory
os.makedirs('/home/pi/backups', exist_ok=True)

# Loop through devices and backup
for device in devices:
    try:
        print(f"Connecting to {device['host']}...")
        connection = ConnectHandler(**device)
        output = connection.send_command('uname -a && uptime && df -h && free -h')
        connection.disconnect()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"/home/pi/backups/{device['host']}_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(output)

        print(f"Backup saved: {filename}")

    except Exception as e:
        print(f"Failed to backup {device['host']}: {e}")
