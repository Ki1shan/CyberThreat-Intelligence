# app/apis/virustotal.py

import requests
import os

def check_virustotal(ioc):
    api_key = os.getenv("VT_API_KEY")
    if not api_key:
        return {"error": "VirusTotal API key not set"}

    url = f"https://www.virustotal.com/api/v3/search?query={ioc}"
    headers = {
        "x-apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"VT Error {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "VT Exception", "message": str(e)}

