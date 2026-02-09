"""
Routes module
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from routes.auth import router as auth_router

__all__ = ['auth_router']
