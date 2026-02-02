#!/usr/bin/env python3
"""
Refresh Debt Empire dashboard and verifier from current masters.json.
Run after replacing masters.json (e.g. from Editable Master Dashboard Save).
"""
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

MASTERS_FILE = SCRIPT_DIR / "masters.json"


def main():
    if not MASTERS_FILE.exists():
        print(f"[!] masters.json not found in {SCRIPT_DIR}")
        print("    Sync from Senior Arbitrage Manager first, or save from Editable Master Dashboard.")
        sys.exit(1)

    sys.path.insert(0, str(SCRIPT_DIR))

    # Regenerate dashboard.html via empire
    try:
        import empire
        analyzer = empire.DebtEmpireAnalyzer()
        if analyzer.load_masters_json():
            analyzer.generate_dashboard()
            print("[OK] dashboard.html regenerated")
        else:
            print("[!] Could not load masters.json")
            sys.exit(1)
    except Exception as e:
        print(f"[!] Dashboard generation: {e}")
        sys.exit(1)

    # Regenerate verifier.html
    try:
        import subprocess
        r = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "generate_verifier_html.py")],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r.returncode == 0:
            print("[OK] verifier.html regenerated")
        else:
            print("[!] Verifier generation had warnings (verifier.html may still be updated)")
    except Exception as e:
        print("[!] Verifier generation failed. Run: python generate_verifier_html.py")

    print("\nDone. Open dashboard.html or verifier.html")


if __name__ == "__main__":
    main()
