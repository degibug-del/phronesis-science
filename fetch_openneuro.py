#!/usr/bin/env python3
"""Fetch OpenNeuro ds002315 using proper download method"""
import requests
import json
from pathlib import Path

# The download endpoint might require proper headers/session
print("Fetching OpenNeuro download link...")

session = requests.Session()

# Get the dataset page first
resp = session.get(
    "https://openneuro.org/datasets/ds002315/download",
    timeout=10,
    headers={"Accept": "application/json, text/plain, */*"}
)

print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")

if resp.status_code == 200:
    # Check if it's a redirect URL
    if resp.url != "https://openneuro.org/datasets/ds002315/download":
        print(f"Redirected to: {resp.url}")
    
    # Check for S3/AWS URLs in response
    if "s3" in resp.text.lower() or "amazonaws" in resp.text.lower():
        print("Found S3 URL reference in response")
        # Extract S3 URL
        import re
        s3_urls = re.findall(r'https://[^\s"<>]+s3[^\s"<>]+', resp.text)
        for url in s3_urls:
            print(f"  {url}")

# Try alternative: check if there's an API endpoint
print("\n\nTrying API endpoint...")
api_resp = requests.get(
    "https://openneuro.org/api/v1/datasets",
    params={"query": "ds002315"},
    timeout=10
)
print(f"API Status: {api_resp.status_code}")
if api_resp.status_code == 200:
    print(api_resp.json()[:500] if isinstance(api_resp.json(), dict) else str(api_resp.json())[:500])

