# app/apis/abuseipdb.py

import requests
import os

def check_abuseipdb(ioc):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        return {"error": "AbuseIPDB API key not set"}

    url = "https://api.abuseipdb.com/api/v2/check"
    params = {
        "ipAddress": ioc,
        "maxAgeInDays": "90"
    }
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"AbuseIPDB Error {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "AbuseIPDB Exception", "message": str(e)}

