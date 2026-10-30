#!/usr/bin/env python3
"""
Automated Deployment Verification & Smoke Test Script
=====================================================
Course: CSE 816 (Software Production Engineering)
Project: End-to-End CI/CD Pipeline for Calculator REST API
Faculty: Prof. B. Thangaraju

This script verifies end-to-end functionality of the deployed Calculator
REST API running behind the Nginx reverse proxy (or direct container).
"""

import sys
import json
import urllib.request
import urllib.error
import time

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost"
print(f"\n=======================================================")
print(f"  Calculator REST API - Deployment Verification Suite  ")
print(f"  Target URL: {BASE_URL}")
print(f"=======================================================\n")

TEST_CASES = [
    {
        "name": "Spring Actuator Health Probe",
        "url": f"{BASE_URL}/actuator/health",
        "expected_status": 200,
        "validator": lambda data: data.get("status") == "UP"
    },
    {
        "name": "Addition: /api/v1/add?a=15&b=25",
        "url": f"{BASE_URL}/api/v1/add?a=15&b=25",
        "expected_status": 200,
        "validator": lambda data: data.get("operation") == "add" and data.get("result") == 40.0
    },
    {
        "name": "Subtraction: /api/v1/subtract?a=100&b=35",
        "url": f"{BASE_URL}/api/v1/subtract?a=100&b=35",
        "expected_status": 200,
        "validator": lambda data: data.get("operation") == "subtract" and data.get("result") == 65.0
    },
    {
        "name": "Multiplication: /api/v1/multiply?a=7&b=8",
        "url": f"{BASE_URL}/api/v1/multiply?a=7&b=8",
        "expected_status": 200,
        "validator": lambda data: data.get("operation") == "multiply" and data.get("result") == 56.0
    },
    {
        "name": "Division: /api/v1/divide?a=84&b=4",
        "url": f"{BASE_URL}/api/v1/divide?a=84&b=4",
        "expected_status": 200,
        "validator": lambda data: data.get("operation") == "divide" and data.get("result") == 21.0
    },
    {
        "name": "Divide by Zero Validation (HTTP 400 Expected)",
        "url": f"{BASE_URL}/api/v1/divide?a=50&b=0",
        "expected_status": 400,
        "validator": lambda data: "error" in data and "Division by zero" in data.get("error", "")
    },
    {
        "name": "Missing Parameter Validation (HTTP 400 Expected)",
        "url": f"{BASE_URL}/api/v1/add?a=10",
        "expected_status": 400,
        "validator": lambda data: "error" in data
    }
]

passed_count = 0
failed_count = 0

for i, test in enumerate(TEST_CASES, 1):
    print(f"[{i}/{len(TEST_CASES)}] Testing: {test['name']}...")
    try:
        req = urllib.request.Request(test["url"], headers={"User-Agent": "SmokeTest/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = response.read().decode("utf-8")
            data = json.loads(body)
    except urllib.error.HTTPError as e:
        status_code = e.code
        body = e.read().decode("utf-8")
        try:
            data = json.loads(body)
        except Exception:
            data = {"raw_body": body}
    except Exception as e:
        print(f"  ❌ FAILED: Network / Connection error: {e}")
        failed_count += 1
        continue

    # Validation
    status_match = status_code == test["expected_status"]
    data_valid = False
    try:
        data_valid = test["validator"](data)
    except Exception as val_err:
        data_valid = False

    if status_match and data_valid:
        print(f"  ✅ PASSED (HTTP {status_code}): {json.dumps(data)}")
        passed_count += 1
    else:
        print(f"  ❌ FAILED:")
        print(f"     Expected Status: {test['expected_status']}, Got: {status_code}")
        print(f"     Payload: {json.dumps(data)}")
        failed_count += 1

print("\n" + "=" * 55)
print(f"  Summary: {passed_count} Passed, {failed_count} Failed out of {len(TEST_CASES)} tests.")
print("=" * 55 + "\n")

if failed_count > 0:
    sys.exit(1)
else:
    print("✨ All smoke tests passed successfully! Deployment is fully verified.\n")
    sys.exit(0)
