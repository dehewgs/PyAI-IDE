#!/usr/bin/env python3
"""
PyAI IDE Launcher
Cross-platform launcher for the PyAI IDE application
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main launcher entry point"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Add src directory to Python path
    src_dir = script_dir / 'src'
    sys.path.insert(0, str(src_dir))
    
    # Import and run the main application
    try:
        from main import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error: Failed to import application: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
