#!/usr/bin/env python3
"""Try Zenodo for ds002315"""
import requests
import json

# ds002315 might be archived on Zenodo
print("Searching Zenodo for ds002315...")
resp = requests.get(
    "https://zenodo.org/api/records",
    params={"q": "ds002315", "sort": "bestmatch"},
    timeout=10
)

if resp.status_code == 200:
    data = resp.json()
    print(f"Found {data.get('hits', {}).get('total', 0)} results")
    for record in data.get('hits', {}).get('hits', [])[:3]:
        print(f"\n  Title: {record.get('metadata', {}).get('title')}")
        print(f"  ID: {record.get('id')}")
        for file in record.get('files', [])[:2]:
            print(f"    - {file.get('key')} ({file.get('size', 0)} bytes)")
else:
    print(f"Error: {resp.status_code}")

# Try direct HTTPS from OpenNeuro
print("\n\nTrying direct HTTPS snapshot download...")
urls_to_try = [
    "https://github.com/OpenNeuroDatasets/ds002315/archive/refs/heads/main.zip",
    "https://openneuro.org/datasets/ds002315/download",
]

for url in urls_to_try:
    print(f"Trying {url}...")
    try:
        resp = requests.head(url, timeout=5, allow_redirects=True)
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"  Content-Length: {resp.headers.get('content-length', 'unknown')} bytes")
    except Exception as e:
        print(f"  Error: {e}")

