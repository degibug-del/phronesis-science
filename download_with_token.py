#!/usr/bin/env python3
import requests
import tarfile
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
headers = {"Authorization": f"Bearer {TOKEN}"}

print("Downloading ds002315 with authenticated token...")

# Try download with auth header
url = "https://openneuro.org/datasets/ds002315/download"

resp = requests.get(
    url,
    headers=headers,
    timeout=30,
    stream=True,
    allow_redirects=True
)

print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")
print(f"Content-Length: {resp.headers.get('content-length')}")

if resp.status_code == 200:
    # Check if it's actually tar/gzip
    chunk = resp.raw.read(100)
    if chunk.startswith(b'\x1f\x8b'):  # gzip magic
        print("✓ Got gzipped data")
    elif chunk.startswith(b'PK'):  # zip
        print("✓ Got zip data")
    elif chunk.startswith(b'ustar'):  # tar
        print("✓ Got tar data")
    else:
        print(f"Unknown format, first bytes: {chunk[:50]}")
    
    # Download to file
    output_path = Path.home() / "data" / "ds002315.tar.gz"
    print(f"\nDownloading to {output_path}...")
    
    total_size = int(resp.headers.get('content-length', 0))
    downloaded = 0
    
    with open(output_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = (downloaded / total_size) * 100
                    print(f"\r  {pct:.1f}% ({downloaded / 1e9:.2f} GB / {total_size / 1e9:.2f} GB)", end='', flush=True)
    
    print(f"\n✓ Downloaded {downloaded / 1e9:.2f} GB")
    
    # Extract
    print("\nExtracting...")
    with tarfile.open(output_path, 'r:gz') as tar:
        tar.extractall(Path.home() / "data")
    print("✓ Extracted")

else:
    print(f"Error: {resp.status_code}")
    print(resp.text[:500])

