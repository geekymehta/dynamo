import json
from pathlib import Path


def test_total_requests():
    """1. `total_requests` — the total number of log lines (integer)."""
    report_path = Path("/app/report.json")
    assert report_path.exists(), "no report.json found"
    with open(report_path) as f:
        data = json.load(f)
    assert "total_requests" in data, "Missing 'total_requests' key"
    assert data["total_requests"] == 6, f"Expected 6 total requests, got {data['total_requests']}"


def test_unique_ips():
    """2. `unique_ips` — the count of distinct client IP addresses (integer)."""
    report_path = Path("/app/report.json")
    assert report_path.exists(), "no report.json found"
    with open(report_path) as f:
        data = json.load(f)
    assert "unique_ips" in data, "Missing 'unique_ips' key"
    assert data["unique_ips"] == 3, f"Expected 3 unique IPs, got {data['unique_ips']}"


def test_top_path():
    """3. `top_path` — the most frequently requested URL path (string)."""
    report_path = Path("/app/report.json")
    assert report_path.exists(), "no report.json found"
    with open(report_path) as f:
        data = json.load(f)
    assert "top_path" in data, "Missing 'top_path' key"
    assert data["top_path"] == "/index.html", f"Expected '/index.html' top path, got {data['top_path']}"
