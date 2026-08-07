#!/usr/bin/env python3
import requests
import json

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

# Try simplified GraphQL query
print("Querying for file download URLs...")

query = """
{
  dataset(id: "ds002315") {
    name
    id
  }
}
"""

resp = requests.post(
    "https://openneuro.org/api/graphql",
    json={"query": query},
    headers=headers,
    timeout=10
)

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(json.dumps(data, indent=2))
else:
    print(resp.text[:500])

