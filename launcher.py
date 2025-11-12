#!/usr/bin/env python3
"""
PyAI IDE Launcher
Entry point for the PyAI IDE application
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import and run main
if __name__ == "__main__":
    from main import main
    sys.exit(main())
