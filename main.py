#!/usr/bin/env python3
"""
OrcaSlicer Configuration Backup Tool
Entry point for the application with CLI argument handling
"""

import argparse
import sys
from cli import CLIInterface
from gui import GUIInterface

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="OrcaSlicer Configuration Backup and Restore Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Launch interactive CLI
  python main.py --gui        # Launch GUI interface
  python main.py --export backup.zip    # Export config to backup.zip
  python main.py --import backup.zip    # Import config from backup.zip
        """
    )
    
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Launch GUI interface instead of CLI"
    )
    
    parser.add_argument(
        "--export", 
        metavar="FILENAME",
        help="Export current configuration to specified zip file"
    )
    
    parser.add_argument(
        "--import", 
        dest="import_file",
        metavar="FILENAME",
        help="Import configuration from specified zip file"
    )
    
    args = parser.parse_args()
    
    try:
        if args.gui:
            # Launch GUI interface
            gui = GUIInterface()
            gui.run()
        elif args.export:
            # Direct export via CLI
            cli = CLIInterface()
            cli.export_config(args.export)
        elif args.import_file:
            # Direct import via CLI
            cli = CLIInterface()
            cli.import_config(args.import_file)
        else:
            # Interactive CLI mode
            cli = CLIInterface()
            cli.run_interactive()
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
