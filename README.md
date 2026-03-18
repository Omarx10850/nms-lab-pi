# nms-lab-pi
Hybrid Network Observability Lab — Raspberry Pi, Zabbix, Grafana, Docker, Python

# NMS Lab — Raspberry Pi Network Monitoring

## Overview
A professional-grade network monitoring server built on a Raspberry Pi, running a containerised Zabbix + Grafana stack via Docker. Monitors real Linux infrastructure via Zabbix agent with automated alerting and daily config backups.

## Architecture
- **Hardware**: Raspberry Pi (headless, SSH-administered)
- **Monitoring**: Zabbix 6.4 (SNMP + Agent polling)
- **Visualisation**: Grafana (Zabbix datasource, 3-panel dashboard)
- **Database**: PostgreSQL 15
- **Containerisation**: Docker + Docker Compose
- **Automation**: Python + Netmiko, cron-scheduled daily backups
- **Logging**: rsyslog centralised syslog on port 514

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
