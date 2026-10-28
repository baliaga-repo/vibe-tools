# ==============================================================================
# Vibe Tools Universal Updater Bootstrap (PowerShell One-Liner)
# Digunakan untuk menarik updater pada proyek lama yang belum memiliki vibe_tools/
# ==============================================================================

[CmdletBinding()]
param (
    [string]$TargetDir = (Get-Location).Path,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

Write-Host "`n🚀 [VIBE TOOLS BOOTSTRAP] Mengunduh pembaruan ekosistem..." -ForegroundColor Cyan

$VibeToolsDir = Join-Path $TargetDir "vibe_tools"
if (-not (Test-Path $VibeToolsDir)) {
    New-Item -ItemType Directory -Path $VibeToolsDir -Force | Out-Null
}

$UpdaterScript = Join-Path $VibeToolsDir "update_ecosystem.py"
$RemoteUrl = "https://raw.githubusercontent.com/baliaga-repo/vibe-tools/main/vibe_tools/update_ecosystem.py"

try {
    Invoke-WebRequest -Uri $RemoteUrl -OutFile $UpdaterScript -UseBasicParsing
    Write-Host "✅ update_ecosystem.py berhasil diunduh." -ForegroundColor Green
} catch {
    Write-Warning "Gagal mengunduh dari GitHub ($($_.Exception.Message)). Mencoba eksekusi Python lokal..."
}

if (Test-Path $UpdaterScript) {
    $ArgsList = @($UpdaterScript, "--target", $TargetDir)
    if ($CheckOnly) {
        $ArgsList += "--check"
    }
    python @ArgsList
} else {
    Write-Error "Berkas update_ecosystem.py tidak ditemukan."
}

