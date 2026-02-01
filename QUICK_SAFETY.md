# 🛡️ Quick Safety Reference

## Before Making ANY Changes

### 1. **ALWAYS Backup First**
```powershell
# Double-click: BACKUP.ps1
# Or run: .\BACKUP.ps1
```
Creates timestamped backup in `backups/YYYY-MM-DD_HH-MM-SS/`

---

## Safe Editing Rules

### ✅ **SAFE (Won't Break Anything)**
- ✅ Add new files: `new_feature.py`, `new_dashboard.html`
- ✅ Add new folders: `features/new_feature/`
- ✅ Add new functions (don't delete old ones)
- ✅ Add new fields to JSON (don't remove existing)

### ⚠️ **CAREFUL (Backup First)**
- ⚠️ Modify existing Python files
- ⚠️ Change HTML generators
- ⚠️ Update configuration files

### ❌ **NEVER (Will Break System)**
- ❌ Delete existing functions
- ❌ Rename core files (empire.py, verifier.py)
- ❌ Remove fields from masters.json
- ❌ Modify verifier.html directly (use generator)

---

## If Something Breaks

### Restore from Backup
```powershell
# Double-click: RESTORE_BACKUP.ps1
# Or run: .\RESTORE_BACKUP.ps1
```
Select backup number → Restore → Test

---

## Quick Commands

| Action | Command |
|--------|---------|
| **Backup** | `.\BACKUP.ps1` |
| **Restore** | `.\RESTORE_BACKUP.ps1` |
| **Test Empire** | `py empire.py` |
| **Regenerate Dashboard** | `py generate_verifier_html.py` |
| **Open Safety Guide** | `Start-Process SAFE_EDITING_GUIDE.html` |

---

## Full Guide

Open `SAFE_EDITING_GUIDE.html` in browser for complete instructions with examples.
