#!/usr/bin/env bash
# J.A.R.V.I.S. Live Fire Protocol — start OWASP ZAP in daemon mode (Docker).
# Usage: ./scripts/run_zap.sh [port]
# Default API port: 8080 (matches --zap-url default in zap_orchestrator.py).
set -euo pipefail

PORT="${1:-8080}"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is required to run OWASP ZAP. Install Docker, then re-run." >&2
  exit 1
fi

if docker ps --format '{{.Names}}' | grep -qx 'zap-daemon'; then
  echo "zap-daemon is already running on port ${PORT}."
  exit 0
fi

if docker ps -a --format '{{.Names}}' | grep -qx 'zap-daemon'; then
  docker start zap-daemon >/dev/null
  echo "Restarted existing zap-daemon container."
else
  docker run -u zap -p "${PORT}:8080" -d --name zap-daemon \
    owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 \
    -config api.disablekey=true \
    -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true
  echo "Started zap-daemon on port ${PORT}."
fi

echo "Waiting for ZAP API..."
for _ in $(seq 1 30); do
  if curl -fsS "http://localhost:${PORT}/JSON/core/view/version/" >/dev/null 2>&1; then
    echo "ZAP is ready at http://localhost:${PORT}"
    exit 0
  fi
  sleep 2
done
echo "ERROR: ZAP did not answer within 60s. Check: docker logs zap-daemon" >&2
exit 1
