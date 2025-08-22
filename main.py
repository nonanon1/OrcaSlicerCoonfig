#!/usr/bin/env python3
"""
OrcaSlicer Configuration Backup Tool
GUI-only application for backing up and restoring OrcaSlicer configurations
"""

import sys
from gui import OrcaBackupGUI

def main():
    """Main entry point for the GUI application"""
    try:
        app = OrcaBackupGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()