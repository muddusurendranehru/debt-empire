#!/usr/bin/env python3
"""
Sync to Debt Empire Master Board
Reads masters_debt_empire.json (exported from Senior Arbitrage Manager),
updates masters.json, and regenerates dashboard.html.
Does NOT destroy success - additive sync only.
"""
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)  # Ensure empire.py reads from correct folder
INPUT_FILE = SCRIPT_DIR / "masters_debt_empire.json"
MASTERS_FILE = SCRIPT_DIR / "masters.json"


def main():
    do_refresh = "--refresh" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--refresh"]

    if do_refresh:
        if not MASTERS_FILE.exists():
            print(f"[!] masters.json not found. Sync from Senior Arbitrage Manager first.")
            sys.exit(1)
        print("[OK] Refreshing from current masters.json")
    else:
        if len(args) > 0:
            src = Path(args[0])
        else:
            src = INPUT_FILE

        if not src.exists():
            print(f"[!] File not found: {src}")
            print("    1. In Senior Arbitrage Manager: DEBT MANAGER tab → Sync to Master Board")
            print("    2. Save downloaded masters_debt_empire.json to debt-empire folder")
            print("    3. Run: python sync_to_master_board.py")
            print("    Or: python sync_to_master_board.py path/to/masters_debt_empire.json")
            print("    Or: python sync_to_master_board.py --refresh  (regenerate from existing masters.json)")
            sys.exit(1)

        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "loans" not in data:
            print("[!] Invalid format: missing 'loans' array")
            sys.exit(1)

        with open(MASTERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] masters.json updated from {src.name} ({len(data['loans'])} loans)")

    # Regenerate dashboard via empire.py
    try:
        sys.path.insert(0, str(SCRIPT_DIR))
        import empire
        analyzer = empire.DebtEmpireAnalyzer()
        if analyzer.load_masters_json():
            analyzer.generate_dashboard()
            print("[OK] dashboard.html regenerated")
        else:
            print("[!] Could not load masters.json for dashboard generation")
    except Exception as e:
        print(f"[!] Dashboard generation: {e}")
        print("    You can run: python empire.py")

    print("\n→ Open dashboard.html or verifier.html")
    print("→ Add new loan / Add documents: Senior Arbitrage Manager")


if __name__ == "__main__":
    main()
