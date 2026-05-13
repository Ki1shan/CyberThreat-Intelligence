
# Cyber Threat Intelligence Dashboard

## Overview

A centralized platform for investigating Indicators of Compromise (IOCs) using real-time threat intelligence APIs. Built using:

- Flask (Python backend)
- MongoDB (Historical tracking)
- Bootstrap 5 (Dark themed UI)
- VirusTotal API v3
- AbuseIPDB API v2
- Dockerized architecture

---

## Features

### IOC Lookup
- IP/domain search
- Parallel API queries (VT & AbuseIPDB)
- Normalized results with threat scores

### Historical Tracking
- MongoDB stores all lookups
- View previous investigations with timestamps

### Dashboard Interface
- Clean table view of IOC results
- Dark mode with threat indicators

---

## Setup Instructions

Prerequisites

- Docker and docker-compose
- API Keys for:
  - VirusTotal (`VT_API_KEY`)
  - AbuseIPDB (`ABUSEIPDB_API_KEY`)

 How to Use
    Enter IP/domain and click "Lookup"
   View:
    VirusTotal stats
    AbuseIPDB score
    Results saved to MongoDB

 Security Practices
    API keys stored in environment variables
    HTTPS API queries
    Isolated MongoDB container

### Run Instructions

```bash
docker-compose up -d

Dashboard: http://localhost:5000
