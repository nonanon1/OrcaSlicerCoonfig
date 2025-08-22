"""
Utility classes and functions for OrcaSlicer path detection and file validation
"""

import os
import sys
import zipfile
from pathlib import Path

class OrcaSlicerPaths:
    """Handle OrcaSlicer path detection across different platforms"""
    
    def __init__(self):
        self.platform = sys.platform
        
    def get_installation_path(self):
        """
        Get OrcaSlicer installation path based on platform
        
        Returns:
            Path: Installation path if found, None otherwise
        """
        if self.platform.startswith('win'):
            return self._get_windows_installation_path()
        elif self.platform == 'darwin':
            return self._get_macos_installation_path()
        else:
            return self._get_linux_installation_path()
    
    def get_config_path(self):
        """
        Get OrcaSlicer configuration directory path
        
        Returns:
            Path: Configuration path if found, None otherwise
        """
        if self.platform.startswith('win'):
            return self._get_windows_config_path()
        elif self.platform == 'darwin':
            return self._get_macos_config_path()
        else:
            return self._get_linux_config_path()
    
    def _get_windows_installation_path(self):
        """Get Windows installation path"""
        possible_paths = [
            Path(os.environ.get('PROGRAMFILES', 'C:\\Program Files')) / 'OrcaSlicer',
            Path(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)')) / 'OrcaSlicer',
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs' / 'OrcaSlicer',
        ]
        
        for path in possible_paths:
            if path.exists() and (path / 'OrcaSlicer.exe').exists():
                return path
        return None
    
    def _get_macos_installation_path(self):
        """Get macOS installation path"""
        possible_paths = [
            Path('/Applications/OrcaSlicer.app'),
            Path(os.path.expanduser('~/Applications/OrcaSlicer.app')),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def _get_linux_installation_path(self):
        """Get Linux installation path"""
        possible_paths = [
            Path('/usr/bin/orcaslicer'),
            Path('/usr/local/bin/orcaslicer'),
            Path(os.path.expanduser('~/Applications/OrcaSlicer')),
            Path('/opt/OrcaSlicer'),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def _get_windows_config_path(self):
        """Get Windows configuration path"""
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            config_path = Path(appdata) / 'OrcaSlicer'
            if config_path.exists():
                return config_path
        
        # Also check local appdata
        localappdata = os.environ.get('LOCALAPPDATA', '')
        if localappdata:
            config_path = Path(localappdata) / 'OrcaSlicer'
            if config_path.exists():
                return config_path
        
        return None
    
    def _get_macos_config_path(self):
        """Get macOS configuration path"""
        home = os.path.expanduser('~')
        possible_paths = [
            Path(home) / 'Library' / 'Application Support' / 'OrcaSlicer',
            Path(home) / '.config' / 'OrcaSlicer',
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def _get_linux_config_path(self):
        """Get Linux configuration path"""
        home = os.path.expanduser('~')
        possible_paths = [
            Path(home) / '.config' / 'OrcaSlicer',
            Path(home) / '.local' / 'share' / 'OrcaSlicer',
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None

class FileValidator:
    """Validate backup files and configurations"""
    
    def validate_backup_zip(self, zip_path):
        """
        Validate that a zip file is a valid OrcaSlicer backup
        
        Args:
            zip_path (str): Path to zip file
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not Path(zip_path).exists():
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Check for required metadata
                if 'backup_metadata.txt' not in zipf.namelist():
                    return False
                
                # Check for config directory
                has_config = any(name.startswith('config/') for name in zipf.namelist())
                if not has_config:
                    return False
                
                # Test zip integrity
                zipf.testzip()
                
                return True
                
        except (zipfile.BadZipFile, zipfile.LargeZipFile):
            return False
        except Exception:
            return False
    
    def get_backup_info(self, zip_path):
        """
        Get information from backup metadata
        
        Args:
            zip_path (str): Path to backup zip file
            
        Returns:
            dict: Backup information
        """
        info = {}
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                if 'backup_metadata.txt' in zipf.namelist():
                    metadata = zipf.read('backup_metadata.txt').decode('utf-8')
                    for line in metadata.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            info[key.strip()] = value.strip()
                
                # Count files in backup
                config_files = [name for name in zipf.namelist() if name.startswith('config/')]
                info['file_count'] = len(config_files)
                
        except Exception as e:
            info['error'] = str(e)
        
        return info

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
