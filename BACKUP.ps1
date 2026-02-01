# DEBT EMPIRE - Safe Backup Script
# Creates timestamped backup before making changes
# Double-click this file or run: .\BACKUP.ps1

Write-Host "`n=== DEBT EMPIRE BACKUP ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Create backups directory
$backupsDir = "backups"
if (-not (Test-Path $backupsDir)) {
    New-Item -ItemType Directory -Path $backupsDir | Out-Null
    Write-Host "[OK] Created backups/ directory" -ForegroundColor Green
}

# Create timestamped backup folder
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupPath = Join-Path $backupsDir $timestamp
New-Item -ItemType Directory -Path $backupPath | Out-Null

Write-Host "Creating backup: $backupPath" -ForegroundColor Yellow
Write-Host ""

# Files to backup (exclude large/unnecessary files)
$filesToBackup = @(
    "*.py",
    "*.json",
    "*.html",
    "*.md",
    "*.txt",
    "*.ps1",
    "*.bat",
    "*.sh",
    "core\*",
    "loans\*",
    "ots-pdfs\*"
)

$backedUp = 0
$skipped = 0

# Backup Python files
Get-ChildItem -Path . -Filter "*.py" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $backupPath $_.Name) -ErrorAction SilentlyContinue
    if ($?) { $backedUp++ } else { $skipped++ }
}

# Backup JSON files
Get-ChildItem -Path . -Filter "*.json" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $backupPath $_.Name) -ErrorAction SilentlyContinue
    if ($?) { $backedUp++ } else { $skipped++ }
}

# Backup HTML files
Get-ChildItem -Path . -Filter "*.html" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $backupPath $_.Name) -ErrorAction SilentlyContinue
    if ($?) { $backedUp++ } else { $skipped++ }
}

# Backup documentation
Get-ChildItem -Path . -Filter "*.md" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $backupPath $_.Name) -ErrorAction SilentlyContinue
    if ($?) { $backedUp++ } else { $skipped++ }
}

# Backup PowerShell scripts
Get-ChildItem -Path . -Filter "*.ps1" -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $backupPath $_.Name) -ErrorAction SilentlyContinue
    if ($?) { $backedUp++ } else { $skipped++ }
}

# Backup core/ directory
if (Test-Path "core") {
    $coreBackup = Join-Path $backupPath "core"
    Copy-Item -Path "core" -Destination $coreBackup -Recurse -ErrorAction SilentlyContinue
    if ($?) {
        Write-Host "[OK] Backed up core/ directory" -ForegroundColor Green
    }
}

# Backup loans/ directory (structure only, not large files)
if (Test-Path "loans") {
    $loansBackup = Join-Path $backupPath "loans"
    # Only backup meta.json and loan.json files, not large PDFs
    Get-ChildItem -Path "loans" -Recurse -Filter "*.json" | ForEach-Object {
        $relativePath = $_.FullName.Substring((Resolve-Path "loans").Path.Length + 1)
        $destPath = Join-Path $loansBackup $relativePath
        $destDir = Split-Path $destPath -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        Copy-Item -Path $_.FullName -Destination $destPath -ErrorAction SilentlyContinue
    }
    Write-Host "[OK] Backed up loans/ structure (JSON files only)" -ForegroundColor Green
}

# Create backup manifest
$manifest = @{
    timestamp = $timestamp
    date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    files_backed_up = $backedUp
    location = $backupPath
    note = "Backup created before making changes"
} | ConvertTo-Json -Depth 3

$manifest | Out-File -FilePath (Join-Path $backupPath "BACKUP_MANIFEST.json") -Encoding UTF8

Write-Host ""
Write-Host "=== BACKUP COMPLETE ===" -ForegroundColor Green
Write-Host "Backup location: $backupPath" -ForegroundColor Cyan
Write-Host "Files backed up: $backedUp" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Safe to make changes now!" -ForegroundColor Green
Write-Host "   If something breaks, restore from: $backupPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
