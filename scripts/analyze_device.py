#!/usr/bin/env python3
"""Analyze GeekMagic device API by crawling its web interface.

Usage:
    python scripts/analyze_device.py <device_ip>

Example:
    python scripts/analyze_device.py 192.168.1.100

This script fetches all known pages from the device and analyzes them
to discover API endpoints, parameters, and data structures.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import urllib.request
from urllib.error import URLError

# Known pages on GeekMagic devices
PAGES = [
    "/",
    "/index.html",
    "/network.html",
    "/weather.html",
    "/time.html",
    "/image.html",
    "/settings.html",
    "/js/settings.js",
]

# Known JSON endpoints
JSON_ENDPOINTS = [
    "/v.json",
    "/app.json",
    "/brt.json",
    "/space.json",
    "/delay.json",
    "/album.json",
    "/city.json",
    "/dst.json",
    "/day.json",
    "/font.json",
    "/colon.json",
    "/config.json",
    "/timebrt.json",
]


def fetch(url: str) -> str | None:
    """Fetch URL content, handling compression."""
    # Validate URL scheme (only http for local devices)
    if not url.startswith("http://"):
        return None
    try:
        req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip, deflate"})  # noqa: S310
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            data = resp.read()
            # Handle gzip
            if data[:2] == b"\x1f\x8b":
                data = gzip.decompress(data)
            return data.decode("utf-8", errors="ignore")
    except (URLError, TimeoutError):
        return None


def extract_json_endpoints(content: str) -> set[str]:
    """Extract JSON endpoint references from HTML/JS."""
    patterns = [
        r"getData\(['\"]/?([^'\"]+\.json)['\"]",
        r"getJSON\(['\"]/?([^'\"]+\.json)['\"]",
        r"\.get\(['\"]/?([^'\"]+\.json)['\"]",
        r"\.open\(['\"][A-Z]+['\"],\s*['\"]/?([^'\"]+\.json)['\"]",
    ]
    endpoints = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            endpoints.add("/" + match.group(1).lstrip("/"))
    return endpoints


def extract_set_params(content: str) -> set[str]:
    """Extract /set?param=value API parameters."""
    pattern = r"/set\?([^\"'&\s]+)"
    params = set()
    for match in re.finditer(pattern, content):
        query = match.group(1)
        for part in query.split("&"):
            if "=" in part:
                params.add(part.split("=")[0])
            else:
                params.add(part.split("+")[0])
    return params


def extract_api_paths(content: str) -> set[str]:
    """Extract API paths like /doUpload, /delete, /wifisave, etc."""
    patterns = [
        r'action=["\']([^"\']+)["\']',
        r"url\s*[:=]\s*['\"]([^'\"]+)['\"]",
    ]
    paths = set()
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            path = match.group(1)
            if path.startswith("/") and not any(
                path.endswith(ext) for ext in [".html", ".js", ".css", ".json"]
            ):
                paths.add(path.split("?")[0])
    return paths


def analyze_json(content: str) -> dict | None:
    """Parse JSON and return field types."""
    if not content or content.strip() == "404":
        return None
    try:
        data = json.loads(content.strip())
        if isinstance(data, dict):
            return {k: type(v).__name__ for k, v in data.items()}
    except json.JSONDecodeError:
        pass
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    device_ip = sys.argv[1]
    base_url = f"http://{device_ip}"

    print("=" * 60)
    print(f"GeekMagic Device Analysis: {device_ip}")
    print("=" * 60)

    # Fetch pages
    print("\nFetching pages...")
    all_content = ""
    for page in PAGES:
        url = base_url + page
        content = fetch(url)
        if content:
            all_content += content
            print(f"  {page} - OK")
        else:
            print(f"  {page} - N/A")

    # Extract endpoints from HTML/JS
    discovered_json = extract_json_endpoints(all_content)
    set_params = extract_set_params(all_content)
    api_paths = extract_api_paths(all_content)

    # Fetch JSON endpoints
    print("\nFetching JSON endpoints...")
    json_structures: dict[str, dict] = {}
    all_json = set(JSON_ENDPOINTS) | discovered_json

    for endpoint in sorted(all_json):
        url = base_url + endpoint
        content = fetch(url)
        if content and (structure := analyze_json(content)):
            json_structures[endpoint] = structure
            print(f"  {endpoint} - OK")
        else:
            print(f"  {endpoint} - N/A")

    # Output analysis
    print("\n" + "=" * 60)
    print("API Analysis Results")
    print("=" * 60)

    print("\n## JSON Endpoints")
    for ep in sorted(all_json):
        marker = "[OK]" if ep in json_structures else "[N/A]"
        print(f"  GET {ep} {marker}")

    print("\n## /set API Parameters")
    for param in sorted(set_params):
        print(f"  /set?{param}=<value>")

    print("\n## Other API Endpoints")
    for path in sorted(api_paths):
        print(f"  {path}")

    if json_structures:
        print("\n## JSON Response Structures")
        for endpoint, fields in sorted(json_structures.items()):
            print(f"\n  {endpoint}:")
            for key, typ in fields.items():
                print(f"    {key}: {typ}")

    print("\n" + "=" * 60)
    print("Share this output when reporting device compatibility issues")
    print("=" * 60)


if __name__ == "__main__":
    main()
