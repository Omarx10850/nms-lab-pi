# nms-lab-pi
Hybrid Network Observability Lab — Raspberry Pi, Zabbix, Grafana, Docker, Python

# NMS Lab — Raspberry Pi Network Monitoring

## Overview
A professional-grade network monitoring server built on a Raspberry Pi, running a containerised Zabbix + Grafana stack via Docker. Monitors real Linux infrastructure via Zabbix agent with automated alerting and daily config backups.

## Architecture

### Physical Infrastructure
- **Hardware**: Raspberry Pi (headless, SSH-administered, static IP 192.168.0.50)
- **Monitoring**: Zabbix 6.4 (Agent polling, 43 metrics collected)
- **Visualisation**: Grafana (Zabbix datasource, 3-panel dashboard)
- **Database**: PostgreSQL 15
- **Containerisation**: Docker + Docker Compose (5 containers)
- **Automation**: Python + Netmiko, cron-scheduled daily backups
- **Logging**: rsyslog centralised syslog on port 514

### Virtual Network Lab (Cisco Packet Tracer)
- **Topology**: R1 — R2 routers, S1 — S2 switches, PC1 — PC2 endpoints
- **Routing**: OSPF configured across all routers for dynamic route advertisement
- **Monitoring config**: SNMPv2c and Syslog configured on all Cisco devices
- **Purpose**: Demonstrates Cisco IOS configuration knowledge alongside the live monitoring stack

### Stack Diagram
┌─────────────────────────────────────────────┐
│              Raspberry Pi (nms-pi)           │
│                192.168.0.50                  │
│                                              │
│  ┌─────────────┐    ┌──────────────────┐    │
│  │   Zabbix    │───►│     Grafana      │    │
│  │   Server    │    │      :3000       │    │
│  │   :10051    │    └──────────────────┘    │
│  └──────┬──────┘                            │
│         │                                   │
│  ┌──────▼──────┐    ┌──────────────────┐    │
│  │  PostgreSQL │    │   Zabbix Web     │    │
│  │   :5432     │    │      :80         │    │
│  └─────────────┘    └──────────────────┘    │
│                                              │
│  ┌─────────────┐                            │
│  │   Zabbix    │                            │
│  │   Agent     │                            │
│  │   :10050    │                            │
│  └─────────────┘                            │
└─────────────────────────────────────────────┘

## Tools & Technologies
Raspberry Pi | Zabbix | Grafana | Docker | PostgreSQL | Python | Netmiko | rsyslog | SNMP | Linux | SSH | Git

## Monitored Metrics
- CPU utilisation (real-time time series)
- Available memory %
- Disk usage %

## Alerting
Zabbix trigger actions configured to send Gmail alerts on Warning+ severity events.

## Project Structure
- `scripts/` — Python automation scripts
- `config/` — Sample Cisco SNMP/Syslog config snippets
- `screenshots/` — Grafana dashboard and Zabbix monitoring views
- `topology/` — Network topology diagram


## How to Deploy

### Prerequisites
- Raspberry Pi running Raspberry Pi OS Lite (64-bit)
- Docker and Docker Compose installed
- Static IP configured on the Pi

### Steps
1. Clone this repository onto your Pi:
```
   git clone https://github.com/Omarx10850/nms-lab-pi.git
```
2. Start the monitoring stack:
```
   cd nms-lab-pi
   docker compose up -d
```
3. Access Zabbix at `http://<pi-ip>` — default credentials: Admin/zabbix
4. Access Grafana at `http://<pi-ip>:3000` — default credentials: admin/admin123
5. Add your host in Zabbix under Data collection → Hosts
6. Run the backup script manually to verify:
```
   python3 scripts/backup_configs.py
```

## Key Challenges & Solutions

**Zabbix 7.4 / Grafana plugin incompatibility**
The Grafana Zabbix plugin (v6.3.0) was incompatible with Zabbix 7.4's API. Resolved by downgrading the Zabbix stack to 6.4 which is fully supported by the plugin.

**Docker network connectivity**
The Zabbix server could not reach the Zabbix agent using the Pi's WiFi IP. Resolved by identifying the agent's internal Docker IP using `docker network inspect` and updating the host interface in Zabbix accordingly.

**Static IP configuration**
Newer Raspberry Pi OS uses NetworkManager instead of dhcpcd. Resolved using `nmcli` to set a permanent static IP via the NetworkManager connection profile.

**Zabbix agent version mismatch**
Default `zabbix/zabbix-agent:alpine-latest` pulled version 7.4 which was incompatible with the 6.4 server. Resolved by explicitly pinning the agent image to `zabbix/zabbix-agent:alpine-6.4-latest`.

## Results & Outcomes

- Monitoring stack fully operational — 5 Docker containers running continuously on Raspberry Pi hardware
- Zabbix agent collecting 43 metrics from live Linux infrastructure, updating every 15-30 seconds
- Grafana dashboard rendering real-time CPU, memory, and disk data with growing history
- Automated daily backup script generating timestamped system snapshots, scheduled via cron
- Gmail alerting pipeline confirmed operational on Warning+ severity triggers
- Full infrastructure-as-code — entire stack reproducible from a single `docker compose up -d`
