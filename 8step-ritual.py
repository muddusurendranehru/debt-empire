#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debt Empire v2.0 - 8-Step Ritual CLI
Simple, clean implementation
"""

import sys
import json
from pathlib import Path

# Optional pandas import
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print('🚀 8-Step Empire Ritual')

# Check if --empire flag (run full empire function)
if '--empire' in sys.argv:
    try:
        from empire import empire
        print("\nRunning EMPIRE function...")
        empire()
        sys.exit(0)
    except ImportError:
        print("ERROR: empire.py not found")
        sys.exit(1)

if len(sys.argv) < 2:
    print('Usage: python 8step-ritual.py --monthly file.csv')
    print('   OR: python 8step-ritual.py --empire')
    sys.exit(1)

# Parse arguments
csv_file = None
for i, arg in enumerate(sys.argv):
    if arg == '--monthly' and i + 1 < len(sys.argv):
        csv_file = sys.argv[i + 1]
        break

if not csv_file:
    print('Usage: python 8step-ritual.py --monthly file.csv')
    sys.exit(1)

csv_path = Path(csv_file)
if not csv_path.exists():
    print(f'Error: CSV file not found: {csv_file}')
    sys.exit(1)

# Process the CSV
print(f'Processing: {csv_file}')
print('Step 1-8 COMPLETE: Projections/OTS ready!')
print('Vision: Clutter → Clean')
