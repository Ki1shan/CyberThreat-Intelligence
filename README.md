# ⚔️ Cyber Threat Intelligence Dashboard

![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-2.3.2-green)
![MongoDB](https://img.shields.io/badge/mongodb-4.4-brightgreen)
![Docker](https://img.shields.io/badge/docker-compose-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![APIs](https://img.shields.io/badge/APIs-VirusTotal%20%7C%20AbuseIPDB-orange)

> A Dockerized Cyber Threat Intelligence platform — lookup IPs and domains against VirusTotal and AbuseIPDB simultaneously, store results in MongoDB, and visualize threat intelligence in a Bootstrap dark-theme dashboard.

---

## ⚠️ Disclaimer

This tool is intended **ONLY** for:

- Authorized threat intelligence and SOC operations
- Security research and IOC analysis
- Cybersecurity education and training

**Always ensure you have authorization before investigating any IP or domain. API usage is subject to VirusTotal and AbuseIPDB terms of service.**

---

## Overview

Cyber Threat Intelligence Dashboard is a full-stack CTI platform that lets analysts submit Indicators of Compromise (IOCs) — IP addresses or domains — and instantly cross-reference them against two industry-standard threat intelligence feeds:

- **VirusTotal** — 70+ AV engine scan results, malicious/suspicious/harmless breakdown
- **AbuseIPDB** — community abuse confidence score, last 90 days of abuse reports

Every lookup is persisted to **MongoDB** with a UTC timestamp, building a searchable historical IOC database. The entire stack runs in **Docker** with a single command.

---

## Screenshot

![CTI Dashboard](CTI.png)

*Live lookups — `45.83.64.1` flagged as malicious (13 VT detections), `8.8.8.8` clean (Google DNS). Docker containers visible in terminal.*

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│              CYBER THREAT INTELLIGENCE DASHBOARD                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │           FLASK WEB APP (app factory pattern)             │  │
│  │   GET  /        → render dashboard (all IOCs from DB)    │  │
│  │   POST /lookup  → query APIs → store → redirect          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              │                                   │
│            ┌─────────────────┴──────────────────┐               │
│            ▼                                    ▼               │
│  ┌──────────────────────┐         ┌───────────────────────────┐  │
│  │  VIRUSTOTAL API v3   │         │  ABUSEIPDB API v2         │  │
│  │  apis/virustotal.py  │         │  apis/abuseipdb.py        │  │
│  │                      │         │                           │  │
│  │  /api/v3/search      │         │  /api/v2/check            │  │
│  │  x-apikey header     │         │  maxAgeInDays: 90         │  │
│  │  Returns:            │         │  Returns:                 │  │
│  │  - malicious count   │         │  - abuseConfidenceScore   │  │
│  │  - suspicious count  │         │  - total reports          │  │
│  │  - harmless count    │         │  - last reported          │  │
│  └──────────────────────┘         └───────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              MONGODB (flask-pymongo)                      │  │
│  │   Database  : cti_dashboard                               │  │
│  │   Collection: iocs                                        │  │
│  │   Fields    : ioc, timestamp, virustotal{}, abuseipdb{}   │  │
│  │   Sorted    : timestamp DESC                              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │         BOOTSTRAP 5 DASHBOARD (dashboard.html)            │  │
│  │   Dark theme, IOC table, VT stats, AbuseIPDB score        │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              DOCKER COMPOSE                               │  │
│  │   cti_flask_app  → Flask on :5000                        │  │
│  │   cti_mongo      → MongoDB 4.4 on :27017                 │  │
│  │   mongo_data     → persistent named volume               │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Features

- **Dual API enrichment** — every IOC queried against VirusTotal AND AbuseIPDB simultaneously
- **MongoDB persistence** — full IOC history with UTC timestamps, sorted newest first
- **Docker Compose** — one command spins up Flask + MongoDB, no manual setup
- **Environment variable config** — API keys via `.env`, never hardcoded
- **Bootstrap 5 dark dashboard** — clean analyst-facing table view
- **App factory pattern** — Flask Blueprint architecture, modular and scalable
- **Graceful error handling** — missing API key detection, HTTP error responses captured

---

## Real-World Results

| IOC | VT Malicious | VT Suspicious | VT Harmless | Abuse Score | Verdict |
|-----|-------------|--------------|-------------|-------------|---------|
| 45.83.64.1 | 13 | 1 | 52 | 0 | ⚠️ Malicious |
| 8.8.8.8 | 0 | 0 | 61 | 0 | ✅ Clean |

---

## Project Structure

```
CyberThreat-Intelligence/
│
├── run.py                        # Entry point — listens on 0.0.0.0:5000
├── Dockerfile                    # Flask app container
├── docker-compose.yml            # Flask + MongoDB orchestration
├── requirements.txt              # Python dependencies
├── .env                          # API keys (not committed to Git)
│
├── app/
│   ├── __init__.py               # App factory, PyMongo init, Blueprint register
│   ├── routes.py                 # / (dashboard) and /lookup (IOC submission) routes
│   │
│   ├── apis/
│   │   ├── virustotal.py         # VirusTotal v3 API client
│   │   └── abuseipdb.py          # AbuseIPDB v2 API client
│   │
│   └── templates/
│       └── dashboard.html        # Bootstrap 5 dark theme dashboard
│
├── CTI.png                       # Dashboard screenshot
└── CTI_Report.docx               # Sample CTI analysis report
```

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Python, Flask | 2.3.2 |
| Database | MongoDB | 4.4 |
| ODM | flask-pymongo | 2.3.0 |
| HTTP Client | requests | 2.31.0 |
| Config | python-dotenv | 1.0.1 |
| Frontend | Bootstrap 5 dark theme | 5.3.0 |
| Containerization | Docker, Docker Compose | — |
| Threat Intel | VirusTotal API v3 | — |
| Threat Intel | AbuseIPDB API v2 | — |

---

## Prerequisites

- Docker + Docker Compose installed
- VirusTotal API key (free tier available)
- AbuseIPDB API key (free tier available)

---

## Installation

**Clone the repository:**
```bash
git clone https://github.com/Ki1shan/CyberThreat-Intelligence.git
cd CyberThreat-Intelligence
```

**Create your `.env` file:**
```bash
VT_API_KEY=your_virustotal_api_key_here
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
FLASK_SECRET_KEY=your_random_secret_key_here
```

**Start the full stack:**
```bash
docker compose up --build
```

**Open in browser:**
```
http://127.0.0.1:5000
```

---

## Usage

1. Open `http://127.0.0.1:5000`
2. Enter an IP address or domain in the **Lookup** field
3. Click **Lookup**
4. Results appear instantly in the dashboard table:
   - **IOC** — submitted indicator
   - **Timestamp** — UTC lookup time
   - **VirusTotal** — malicious / suspicious / undetected / harmless counts
   - **AbuseIPDB** — Abuse Confidence Score (0-100)
5. All lookups persist in MongoDB — full history visible on every page load

---

## API Reference

### VirusTotal (`apis/virustotal.py`)
```
GET https://www.virustotal.com/api/v3/search?query={ioc}
Header: x-apikey: {VT_API_KEY}
Returns: data[0].attributes.last_analysis_stats
         → malicious, suspicious, undetected, harmless, timeout counts
```

### AbuseIPDB (`apis/abuseipdb.py`)
```
GET https://api.abuseipdb.com/api/v2/check
Params: ipAddress={ioc}, maxAgeInDays=90
Header: Key: {ABUSEIPDB_API_KEY}, Accept: application/json
Returns: data.abuseConfidenceScore (0-100)
```

---

## Docker Services

| Service | Container | Port | Notes |
|---------|-----------|------|-------|
| Flask App | `cti_flask_app` | 5000 | Depends on MongoDB |
| MongoDB | `cti_mongo` | 27017 | Persistent named volume |

```bash
docker compose up -d       # Start detached
docker compose down        # Stop all services
docker compose logs -f     # Follow live logs
```

---

## Get Free API Keys

| Service | Free Tier | Link |
|---------|-----------|------|
| VirusTotal | ✅ 4 lookups/min | [virustotal.com/gui/join-us](https://www.virustotal.com/gui/join-us) |
| AbuseIPDB | ✅ 1000 checks/day | [abuseipdb.com/register](https://www.abuseipdb.com/register) |

---

## Author

**Kishan N**
Offensive Security Engineer | Threat Intelligence | SOC Engineering

Built this CTI platform to demonstrate practical threat intelligence enrichment — combining two industry-standard feeds into a persistent, queryable IOC database with a clean analyst-facing dashboard.

---

## License

MIT License — see `LICENSE` file for details.

---

*Know your adversary before they know you.*
