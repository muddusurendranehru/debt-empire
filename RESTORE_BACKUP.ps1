# DEBT EMPIRE - Restore from Backup
# Restores files from a backup if something breaks
# Double-click this file or run: .\RESTORE_BACKUP.ps1

Write-Host "`n=== DEBT EMPIRE - RESTORE FROM BACKUP ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
Set-Location $PSScriptRoot

# Check if backups exist
$backupsDir = "backups"
if (-not (Test-Path $backupsDir)) {
    Write-Host "[ERROR] No backups directory found!" -ForegroundColor Red
    Write-Host "No backups have been created yet." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# List available backups
Write-Host "Available backups:" -ForegroundColor Yellow
Write-Host ""
$backups = Get-ChildItem -Path $backupsDir -Directory | Sort-Object Name -Descending
$backupList = @()
$index = 1

foreach ($backup in $backups) {
    $manifestPath = Join-Path $backup.FullName "BACKUP_MANIFEST.json"
    $date = $backup.Name
    if (Test-Path $manifestPath) {
        try {
            $manifest = Get-Content $manifestPath | ConvertFrom-Json
            $date = $manifest.date
        } catch {
            # Use folder name if manifest can't be read
        }
    }
    
    Write-Host "  [$index] $($backup.Name) - $date" -ForegroundColor Cyan
    $backupList += $backup
    $index++
}

if ($backupList.Count -eq 0) {
    Write-Host "[ERROR] No backups found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host ""
Write-Host "Enter backup number to restore (or 'q' to quit): " -ForegroundColor Yellow -NoNewline
$selection = Read-Host

if ($selection -eq 'q' -or $selection -eq 'Q') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

try {
    $backupIndex = [int]$selection - 1
    if ($backupIndex -lt 0 -or $backupIndex -ge $backupList.Count) {
        Write-Host "[ERROR] Invalid selection!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit
    }
    
    $selectedBackup = $backupList[$backupIndex]
    Write-Host ""
    Write-Host "Selected backup: $($selectedBackup.Name)" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  WARNING: This will overwrite current files!" -ForegroundColor Red
    Write-Host "Continue? (y/N): " -ForegroundColor Yellow -NoNewline
    $confirm = Read-Host
    
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit
    }
    
    Write-Host ""
    Write-Host "Restoring files..." -ForegroundColor Yellow
    
    # Restore files
    $restored = 0
    Get-ChildItem -Path $selectedBackup.FullName -File | ForEach-Object {
        if ($_.Name -ne "BACKUP_MANIFEST.json") {
            Copy-Item -Path $_.FullName -Destination (Join-Path $PSScriptRoot $_.Name) -Force
            $restored++
        }
    }
    
    # Restore core/ directory
    $coreBackup = Join-Path $selectedBackup.FullName "core"
    if (Test-Path $coreBackup) {
        if (Test-Path "core") {
            Remove-Item -Path "core" -Recurse -Force
        }
        Copy-Item -Path $coreBackup -Destination "core" -Recurse -Force
        Write-Host "[OK] Restored core/ directory" -ForegroundColor Green
    }
    
    # Restore loans/ structure (JSON files)
    $loansBackup = Join-Path $selectedBackup.FullName "loans"
    if (Test-Path $loansBackup) {
        Get-ChildItem -Path $loansBackup -Recurse -Filter "*.json" | ForEach-Object {
            $relativePath = $_.FullName.Substring($loansBackup.Length + 1)
            $destPath = Join-Path "loans" $relativePath
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item -Path $_.FullName -Destination $destPath -Force
        }
        Write-Host "[OK] Restored loans/ structure" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "=== RESTORE COMPLETE ===" -ForegroundColor Green
    Write-Host "Restored $restored files from backup: $($selectedBackup.Name)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✅ Files restored! Test with: py empire.py" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "[ERROR] Restore failed: $_" -ForegroundColor Red
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
