# J.A.R.V.I.S. Live Fire Protocol — start OWASP ZAP in daemon mode (Docker).
# Usage: .\scripts\run_zap.ps1 [-Port 8080]
param([int]$Port = 8080)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Write-Error 'Docker is required to run OWASP ZAP. Install Docker Desktop, then re-run.'
}

$running = docker ps --format '{{.Names}}' | Select-String -Pattern '^zap-daemon$' -Quiet
if ($running) {
  Write-Output "zap-daemon is already running on port $Port."
  exit 0
}

$exists = docker ps -a --format '{{.Names}}' | Select-String -Pattern '^zap-daemon$' -Quiet
if ($exists) {
  docker start zap-daemon | Out-Null
  Write-Output 'Restarted existing zap-daemon container.'
} else {
  docker run -u zap -p "${Port}:8080" -d --name zap-daemon `
    owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 `
    -config api.disablekey=true `
    -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true | Out-Null
  Write-Output "Started zap-daemon on port $Port."
}

Write-Output 'Waiting for ZAP API...'
for ($i = 0; $i -lt 30; $i++) {
  try {
    Invoke-RestMethod -Uri "http://localhost:$Port/JSON/core/view/version/" -TimeoutSec 5 | Out-Null
    Write-Output "ZAP is ready at http://localhost:$Port"
    exit 0
  } catch {
    Start-Sleep -Seconds 2
  }
}
Write-Error 'ZAP did not answer within 60s. Check: docker logs zap-daemon'
