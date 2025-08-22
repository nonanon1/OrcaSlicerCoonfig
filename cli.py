"""
Command Line Interface for OrcaSlicer Configuration Backup Tool
"""

import os
import sys
from pathlib import Path
from orca_backup import OrcaBackup
from utils import format_file_size

class CLIInterface:
    """Command line interface for the backup tool"""
    
    def __init__(self):
        self.backup_tool = OrcaBackup()
        
    def run_interactive(self):
        """Run interactive CLI mode"""
        self.print_header()
        
        # Check installation status
        info = self.backup_tool.get_config_info()
        self.display_status(info)
        
        if not info['config_found']:
            print("\nOrcaSlicer configuration not found. Please ensure OrcaSlicer is installed and has been run at least once.")
            return
        
        while True:
            self.print_menu()
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                self.interactive_export()
            elif choice == '2':
                self.interactive_import()
            elif choice == '3':
                self.display_detailed_info()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def print_header(self):
        """Print application header"""
        print("=" * 60)
        print("     OrcaSlicer Configuration Backup & Restore Tool")
        print("=" * 60)
    
    def print_menu(self):
        """Print main menu"""
        print("\n" + "-" * 40)
        print("Main Menu:")
        print("1. Export configuration to zip file")
        print("2. Import configuration from zip file")
        print("3. Show configuration details")
        print("4. Exit")
        print("-" * 40)
    
    def display_status(self, info):
        """Display current OrcaSlicer status"""
        print("\nCurrent Status:")
        print(f"  Installation found: {'Yes' if info['installation_found'] else 'No'}")
        if info['installation_path']:
            print(f"  Installation path:  {info['installation_path']}")
        
        print(f"  Configuration found: {'Yes' if info['config_found'] else 'No'}")
        if info['config_path']:
            print(f"  Configuration path:  {info['config_path']}")
            if info['config_found']:
                print(f"  Configuration size:  {format_file_size(info['config_size'])}")
                print(f"  Number of files:     {info['file_count']}")
    
    def display_detailed_info(self):
        """Display detailed configuration information"""
        print("\n" + "=" * 50)
        print("Detailed Configuration Information")
        print("=" * 50)
        
        info = self.backup_tool.get_config_info()
        self.display_status(info)
        
        if info['config_found']:
            config_path = Path(info['config_path'])
            print(f"\nConfiguration directory contents:")
            
            try:
                for item in sorted(config_path.iterdir()):
                    if item.is_file():
                        size = format_file_size(item.stat().st_size)
                        print(f"  📄 {item.name} ({size})")
                    elif item.is_dir():
                        file_count = sum(1 for _ in item.rglob('*') if _.is_file())
                        print(f"  📁 {item.name}/ ({file_count} files)")
            except Exception as e:
                print(f"  Error reading directory: {e}")
    
    def interactive_export(self):
        """Interactive export process"""
        print("\n" + "=" * 40)
        print("Export Configuration")
        print("=" * 40)
        
        # Get output filename
        while True:
            default_name = f"orca_config_backup_{self.get_timestamp()}.zip"
            filename = input(f"Enter output filename [{default_name}]: ").strip()
            
            if not filename:
                filename = default_name
            
            if not filename.endswith('.zip'):
                filename += '.zip'
            
            # Check if file exists
            if Path(filename).exists():
                overwrite = input(f"File '{filename}' already exists. Overwrite? (y/N): ").lower().strip()
                if overwrite != 'y':
                    continue
            
            break
        
        self.export_config(filename)
    
    def interactive_import(self):
        """Interactive import process"""
        print("\n" + "=" * 40)
        print("Import Configuration")
        print("=" * 40)
        
        # Get input filename
        while True:
            filename = input("Enter backup zip file path: ").strip()
            
            if not filename:
                print("Please enter a filename.")
                continue
            
            if not Path(filename).exists():
                print(f"File '{filename}' not found.")
                continue
            
            break
        
        # Show backup info
        validator = self.backup_tool.validator
        backup_info = validator.get_backup_info(filename)
        
        if backup_info:
            print("\nBackup file information:")
            for key, value in backup_info.items():
                if key != 'error':
                    print(f"  {key}: {value}")
        
        # Confirm import
        print(f"\nThis will replace your current OrcaSlicer configuration with the backup from:")
        print(f"  {filename}")
        
        confirm = input("\nDo you want to continue? (y/N): ").lower().strip()
        if confirm != 'y':
            print("Import cancelled.")
            return
        
        # Ask about backup
        backup_current = input("Create backup of current configuration before import? (Y/n): ").lower().strip()
        create_backup = backup_current != 'n'
        
        self.import_config(filename, create_backup)
    
    def export_config(self, filename):
        """Export configuration to file"""
        try:
            print(f"\nExporting configuration to '{filename}'...")
            
            success = self.backup_tool.export_configuration(filename)
            
            if success:
                file_size = format_file_size(Path(filename).stat().st_size)
                print(f"✅ Export successful!")
                print(f"   File: {filename}")
                print(f"   Size: {file_size}")
            else:
                print("❌ Export failed.")
                
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def import_config(self, filename, create_backup=True):
        """Import configuration from file"""
        try:
            print(f"\nImporting configuration from '{filename}'...")
            
            success = self.backup_tool.import_configuration(filename, create_backup)
            
            if success:
                print("✅ Import successful!")
                print("   Your OrcaSlicer configuration has been restored.")
                print("   Please restart OrcaSlicer to see the changes.")
            else:
                print("❌ Import failed.")
                
        except Exception as e:
            print(f"❌ Import failed: {e}")
    
    def get_timestamp(self):
        """Get timestamp string for filenames"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    """Main entry point for CLI"""
    cli = CLIInterface()
    cli.run_interactive()

if __name__ == "__main__":
    main()
