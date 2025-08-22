"""
Utility classes and functions for OrcaSlicer path detection and file validation
"""

import os
import sys
import time
import zipfile
from pathlib import Path

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

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

class OrcaSlicerProcessDetector:
    """Lightweight OrcaSlicer process detection"""
    
    def __init__(self):
        self.process_names = ['orcaslicer', 'orcaslicer.exe', 'OrcaSlicer', 'OrcaSlicer.exe']
    
    def is_orcaslicer_running(self):
        """
        Check if OrcaSlicer process is currently running
        
        Returns:
            bool: True if OrcaSlicer is running, False otherwise
        """
        if not PSUTIL_AVAILABLE:
            # Fallback to basic OS commands if psutil not available
            return self._fallback_process_check()
        
        try:
            import psutil as ps
            for process in ps.process_iter(['name', 'exe']):
                try:
                    process_info = process.info
                    process_name = process_info.get('name', '').lower()
                    process_exe = process_info.get('exe', '')
                    
                    # Check process name
                    if any(name.lower() in process_name for name in self.process_names):
                        return True
                    
                    # Check executable path
                    if process_exe and any(name.lower() in process_exe.lower() for name in self.process_names):
                        return True
                        
                except (Exception):
                    # Handle any psutil exceptions
                    continue
                    
        except Exception:
            # If psutil fails, fallback to OS commands
            return self._fallback_process_check()
        
        return False
    
    def _fallback_process_check(self):
        """Fallback process detection using OS commands"""
        import subprocess
        
        try:
            if sys.platform.startswith('win'):
                # Windows: use tasklist
                result = subprocess.run(
                    ['tasklist', '/fi', 'imagename eq OrcaSlicer.exe'],
                    capture_output=True, text=True, timeout=5
                )
                return 'OrcaSlicer.exe' in result.stdout
            
            elif sys.platform == 'darwin':
                # macOS: use pgrep
                result = subprocess.run(
                    ['pgrep', '-i', 'orcaslicer'],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
            
            else:
                # Linux: use pgrep
                result = subprocess.run(
                    ['pgrep', '-i', 'orcaslicer'],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
                
        except Exception:
            # If all else fails, assume not running
            return False
    
    def wait_for_shutdown(self, max_wait_seconds=20, check_interval=2):
        """
        Wait for OrcaSlicer to shut down with periodic checking
        
        Args:
            max_wait_seconds (int): Maximum time to wait in seconds
            check_interval (int): How often to check in seconds
            
        Returns:
            dict: Result with 'shutdown' (bool) and 'time_waited' (float)
        """
        start_time = time.time()
        checks_made = 0
        
        while time.time() - start_time < max_wait_seconds:
            if not self.is_orcaslicer_running():
                return {
                    'shutdown': True,
                    'time_waited': time.time() - start_time,
                    'checks_made': checks_made
                }
            
            checks_made += 1
            time.sleep(check_interval)
        
        return {
            'shutdown': False,
            'time_waited': time.time() - start_time,
            'checks_made': checks_made
        }
