"""
Core functionality for OrcaSlicer configuration backup and restore
"""

import os
import sys
import zipfile
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from utils import OrcaSlicerPaths, FileValidator

class OrcaBackup:
    """Main class handling OrcaSlicer configuration backup and restore operations"""
    
    def __init__(self):
        self.paths = OrcaSlicerPaths()
        self.validator = FileValidator()
        
    def detect_installation(self):
        """
        Detect OrcaSlicer installation and configuration directory
        
        Returns:
            tuple: (installation_path, config_path) or (None, None) if not found
        """
        install_path = self.paths.get_installation_path()
        config_path = self.paths.get_config_path()
        
        if config_path and config_path.exists():
            return install_path, config_path
        
        return None, None
    
    def export_configuration(self, output_file):
        """
        Export current OrcaSlicer configuration to a zip file
        
        Args:
            output_file (str): Path to output zip file
            
        Returns:
            bool: True if successful, False otherwise
        """
        install_path, config_path = self.detect_installation()
        
        if not config_path:
            raise RuntimeError("OrcaSlicer configuration directory not found. Please ensure OrcaSlicer is installed and has been run at least once.")
        
        # Validate config directory has content
        if not any(config_path.iterdir()):
            raise RuntimeError("OrcaSlicer configuration directory is empty. Please run OrcaSlicer at least once to create configuration files.")
        
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create zip file with configuration
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add metadata
                metadata = {
                    'export_date': datetime.now().isoformat(),
                    'platform': sys.platform,
                    'config_path': str(config_path),
                    'install_path': str(install_path) if install_path else 'unknown'
                }
                
                zipf.writestr('backup_metadata.txt', 
                             '\n'.join([f"{k}: {v}" for k, v in metadata.items()]))
                
                # Add all configuration files and directories
                for root, dirs, files in os.walk(config_path):
                    # Skip cache and temporary directories
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['cache', 'temp', 'logs']]
                    
                    for file in files:
                        if file.startswith('.'):
                            continue
                            
                        file_path = Path(root) / file
                        arc_path = file_path.relative_to(config_path)
                        
                        try:
                            zipf.write(file_path, f"config/{arc_path}")
                        except (OSError, IOError) as e:
                            print(f"Warning: Could not backup file {file_path}: {e}")
            
            # Verify the created zip file
            if not self.validator.validate_backup_zip(output_file):
                raise RuntimeError("Created backup file failed validation")
            
            return True
            
        except Exception as e:
            # Clean up partial file on error
            if Path(output_file).exists():
                try:
                    os.remove(output_file)
                except:
                    pass
            raise RuntimeError(f"Failed to create backup: {e}")
    
    def import_configuration(self, zip_file, create_backup=True):
        """
        Import OrcaSlicer configuration from a zip file
        
        Args:
            zip_file (str): Path to backup zip file
            create_backup (bool): Whether to create backup of current config
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate input file
        if not self.validator.validate_backup_zip(zip_file):
            raise RuntimeError("Invalid or corrupted backup file")
        
        install_path, config_path = self.detect_installation()
        
        if not config_path:
            raise RuntimeError("OrcaSlicer configuration directory not found. Please ensure OrcaSlicer is installed.")
        
        # Create backup of current configuration if requested
        backup_path = None
        if create_backup and config_path.exists() and any(config_path.iterdir()):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"orca_config_backup_{timestamp}.zip"
            backup_path = config_path.parent / backup_filename
            
            try:
                self.export_configuration(str(backup_path))
                print(f"Current configuration backed up to: {backup_path}")
            except Exception as e:
                print(f"Warning: Could not create backup of current configuration: {e}")
                response = input("Continue without backup? (y/N): ").lower().strip()
                if response != 'y':
                    raise RuntimeError("Import cancelled by user")
        
        try:
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract zip file
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                # Verify extraction
                config_source = temp_path / "config"
                if not config_source.exists():
                    raise RuntimeError("Invalid backup file: missing config directory")
                
                # Remove existing configuration (but keep the directory)
                if config_path.exists():
                    for item in config_path.iterdir():
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                else:
                    config_path.mkdir(parents=True, exist_ok=True)
                
                # Copy new configuration
                for item in config_source.iterdir():
                    if item.is_file():
                        shutil.copy2(item, config_path)
                    elif item.is_dir():
                        shutil.copytree(item, config_path / item.name)
            
            return True
            
        except Exception as e:
            # Try to restore backup if import failed
            if backup_path and backup_path.exists():
                try:
                    print("Import failed, attempting to restore backup...")
                    self.import_configuration(str(backup_path), create_backup=False)
                    print("Backup restored successfully")
                except:
                    print("Failed to restore backup. Manual intervention may be required.")
            
            raise RuntimeError(f"Failed to import configuration: {e}")
    
    def get_config_info(self):
        """
        Get information about current OrcaSlicer configuration
        
        Returns:
            dict: Configuration information
        """
        install_path, config_path = self.detect_installation()
        
        info = {
            'installation_found': install_path is not None,
            'installation_path': str(install_path) if install_path else None,
            'config_found': config_path is not None and config_path.exists(),
            'config_path': str(config_path) if config_path else None,
            'config_size': 0,
            'file_count': 0
        }
        
        if config_path and config_path.exists():
            try:
                total_size = 0
                file_count = 0
                
                for root, dirs, files in os.walk(config_path):
                    for file in files:
                        file_path = Path(root) / file
                        try:
                            total_size += file_path.stat().st_size
                            file_count += 1
                        except:
                            pass
                
                info['config_size'] = total_size
                info['file_count'] = file_count
            except Exception as e:
                info['error'] = str(e)
        
        return info
