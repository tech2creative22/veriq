"""Dependency-free HTTP smoke test for a running Veriq deployment."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


FRONTEND_URL = os.getenv("VERIQ_FRONTEND_URL", "http://127.0.0.1:3000").rstrip("/")
BACKEND_URL = os.getenv("VERIQ_BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def check(url: str, expected_text: str | None = None) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": "veriq-smoke-test/1.0"})
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        if expected_text and expected_text not in body:
            raise RuntimeError(f"{url} did not contain expected text: {expected_text}")
        return {"url": url, "status": response.status, "bytes": len(body)}


def main() -> int:
    checks = [
        check(f"{BACKEND_URL}/health", '"healthy"'),
        check(f"{BACKEND_URL}/api/v1/intelligence/latest-evidence", '"success":true'),
    ]
    for route in ("/", "/early-intervention", "/beacon", "/decision-brief", "/settings", "/upload"):
        checks.append(check(f"{FRONTEND_URL}{route}"))
    print(json.dumps({"success": True, "checks": checks}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, urllib.error.URLError) as error:
        print(json.dumps({"success": False, "error": str(error)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
