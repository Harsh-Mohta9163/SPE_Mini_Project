#!/usr/bin/env bash
# ==============================================================================
# Automated Deployment Verification & Smoke Test Script (Bash)
# Course: CSE 816 (Software Production Engineering), IIIT Bangalore
# ==============================================================================
set -e

BASE_URL="${1:-http://localhost}"
echo "======================================================="
echo "  Testing Calculator Deployment at: ${BASE_URL}"
echo "======================================================="

# Health probe check
echo -n "Checking /actuator/health... "
HEALTH=$(curl -s "${BASE_URL}/actuator/health")
if echo "$HEALTH" | grep -q '"status":"UP"'; then
  echo "✅ UP"
else
  echo "❌ FAILED: $HEALTH"
  exit 1
fi

# Add test
echo -n "Testing Add: /api/v1/add?a=10&b=25... "
ADD_RESP=$(curl -s "${BASE_URL}/api/v1/add?a=10&b=25")
if echo "$ADD_RESP" | grep -q '"result":35'; then
  echo "✅ OK ($ADD_RESP)"
else
  echo "❌ FAILED: $ADD_RESP"
  exit 1
fi

# Subtract test
echo -n "Testing Subtract: /api/v1/subtract?a=40&b=15... "
SUB_RESP=$(curl -s "${BASE_URL}/api/v1/subtract?a=40&b=15")
if echo "$SUB_RESP" | grep -q '"result":25'; then
  echo "✅ OK ($SUB_RESP)"
else
  echo "❌ FAILED: $SUB_RESP"
  exit 1
fi

# Multiply test
echo -n "Testing Multiply: /api/v1/multiply?a=6&b=9... "
MUL_RESP=$(curl -s "${BASE_URL}/api/v1/multiply?a=6&b=9")
if echo "$MUL_RESP" | grep -q '"result":54'; then
  echo "✅ OK ($MUL_RESP)"
else
  echo "❌ FAILED: $MUL_RESP"
  exit 1
fi

# Divide test
echo -n "Testing Divide: /api/v1/divide?a=72&b=8... "
DIV_RESP=$(curl -s "${BASE_URL}/api/v1/divide?a=72&b=8")
if echo "$DIV_RESP" | grep -q '"result":9'; then
  echo "✅ OK ($DIV_RESP)"
else
  echo "❌ FAILED: $DIV_RESP"
  exit 1
fi

# Divide by Zero (expect 400)
echo -n "Testing Divide by Zero (expect HTTP 400)... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/v1/divide?a=10&b=0")
if [ "$HTTP_CODE" = "400" ]; then
  echo "✅ OK (Received expected HTTP 400)"
else
  echo "❌ FAILED (Received HTTP $HTTP_CODE)"
  exit 1
fi

echo "======================================================="
echo "🎉 All endpoints verified successfully!"
echo "======================================================="
