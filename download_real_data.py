#!/usr/bin/env python3
"""Download OpenNeuro ds002315 directly"""
import requests
import json
import os
from pathlib import Path

# Read from the environment, not baked in. This was a plaintext literal in four scripts
# until 2026-08-07. It never entered git history — the files were gitignored before the
# repo was initialised — and it should still be rotated, because a credential that has sat
# in cleartext has to be assumed leaked.
#
#     export OPENNEURO_TOKEN=...
import os
TOKEN = os.environ.get("OPENNEURO_TOKEN", "")
if not TOKEN:
    raise SystemExit("set OPENNEURO_TOKEN in the environment first")

# Try REST API to get dataset download URL
headers = {"Authorization": f"Bearer {TOKEN}"}

# 1. Get dataset info
print("Fetching dataset info...")
resp = requests.get(
    "https://openneuro.org/api/v1/datasets/ds002315",
    headers=headers,
    timeout=10
)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(json.dumps(data, indent=2)[:1000])
else:
    print(f"Error: {resp.text[:500]}")

# 2. Try direct AWS Requester Pays bucket
print("\n\nTrying AWS Requester Pays bucket...")
import subprocess

# OpenNeuro's standard S3 bucket
bucket_urls = [
    "s3://fcp-indi/data/Projects/ds002315/",
    "s3://openneuro/ds002315/",
    "s3://openneuro.org/ds002315/",
]

for bucket in bucket_urls:
    print(f"Trying {bucket}...")
    result = subprocess.run(
        ["aws", "s3", "ls", bucket, "--request-payer", "requester", "--no-sign-request"],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"✓ Found! Listing contents:")
        print(result.stdout[:500])
        break
    else:
        print(f"  Not found")

