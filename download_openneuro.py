#!/usr/bin/env python3
"""
Download OpenNeuro ds002315 EEG data via API
Uses token-based auth for authenticated download
"""

import os
import json
import requests
from pathlib import Path
import tarfile
import io

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
DATASET_ID = "ds002315"
DATA_DIR = Path.home() / "data" / "ds002315"

# Create directory
DATA_DIR.mkdir(parents=True, exist_ok=True)

# List available subjects
print("Fetching dataset info...")
headers = {"Authorization": f"Bearer {TOKEN}"}
api_url = f"https://openneuro.org/api/graphql"

query = """
query {
  dataset(id: "%s") {
    id
    label
    summary {
      subjectCount
    }
    files(first: 100) {
      edges {
        node {
          id
          name
          size
        }
      }
    }
  }
}
""" % DATASET_ID

response = requests.post(api_url, json={"query": query}, headers=headers, timeout=30)
print(f"API Response status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        dataset = data['data'].get('dataset', {})
        print(f"Dataset: {dataset.get('label', 'unknown')}")
        summary = dataset.get('summary', {})
        print(f"Subjects: {summary.get('subjectCount', 'unknown')}")
else:
    print(f"Error: {response.text}")

# Try direct download of sample subject via S3
print("\nAttempting direct S3 download of subject 01...")
s3_url = f"https://openneuro.org/ds{DATASET_ID}/download?dir=sub-01/eeg"
try:
    resp = requests.get(s3_url, headers=headers, timeout=60, allow_redirects=True)
    if resp.status_code == 200:
        print(f"✓ Downloaded {len(resp.content)} bytes")
        # Save tar if it's compressed
        if b'\x1f\x8b' in resp.content[:10]:  # gzip magic
            import gzip
            content = gzip.decompress(resp.content)
        else:
            content = resp.content
        print(f"Content size: {len(content)} bytes")
    else:
        print(f"Download failed: {resp.status_code}")
except Exception as e:
    print(f"Error: {e}")

print("\nFalling back to synthetic validation...")
