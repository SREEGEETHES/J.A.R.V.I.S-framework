param (
    [switch]$Global,
    [string]$TargetDir = "."
)

if ($Global) {
    Write-Host "Installing JARVIS globally for Antigravity, OpenCode, and Claude Code..." -ForegroundColor Cyan
    
    $globalGemini = "$env:USERPROFILE\.gemini\config\skills"
    $globalOpenCode = "$env:USERPROFILE\.config\opencode\commands"
    $globalClaude = "$env:USERPROFILE\.claude\commands"

    New-Item -ItemType Directory -Force -Path $globalGemini | Out-Null
    New-Item -ItemType Directory -Force -Path $globalOpenCode | Out-Null
    New-Item -ItemType Directory -Force -Path $globalClaude | Out-Null

    Copy-Item -Recurse -Force -Path ".agents\skills\*" -Destination $globalGemini
    Copy-Item -Recurse -Force -Path ".opencode\commands\*" -Destination $globalOpenCode
    Copy-Item -Recurse -Force -Path ".claude\commands\*" -Destination $globalClaude

    Write-Host "JARVIS-FRAMEWORK installed globally! Available across all your projects." -ForegroundColor Green
    exit 0
}

Write-Host "Installing JARVIS-FRAMEWORK into: $TargetDir..." -ForegroundColor Cyan

$itemsToCopy = @(
    ".jarvis",
    ".agents",
    ".claude",
    ".clinerules",
    ".cursorrules",
    "CLAUDE.md",
    "GEMINI.md",
    ".windsurfrules"
)

foreach ($item in $itemsToCopy) {
    if (Test-Path $item) {
        Copy-Item -Recurse -Force -Path $item -Destination $TargetDir
    }
}

# Copy only OpenCode hooks (exclude node_modules, package.json, lockfiles)
if (Test-Path ".opencode/AGENTS.md") {
    $destOpenCode = Join-Path $TargetDir ".opencode/commands"
    New-Item -ItemType Directory -Force -Path $destOpenCode | Out-Null
    Copy-Item -Force -Path ".opencode/AGENTS.md" -Destination (Join-Path $TargetDir ".opencode/AGENTS.md")
    if (Test-Path ".opencode/commands") {
        Copy-Item -Recurse -Force -Path ".opencode/commands/*" -Destination $destOpenCode
    }
}

Write-Host "JARVIS-FRAMEWORK successfully installed in $TargetDir for all IDEs!" -ForegroundColor Green
