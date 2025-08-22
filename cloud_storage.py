"""
Cloud storage integration for OrcaSlicer Configuration Manager
Supports Google Drive and iCloud Drive for backup synchronization
"""

import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import tempfile
import shutil
import webbrowser
from datetime import datetime
import threading
import subprocess
import sys

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False

class CloudStorageManager:
    """Manages cloud storage authentication and operations"""
    
    def __init__(self, gui_parent=None):
        self.gui_parent = gui_parent
        self.credentials = {}
        self.services = {}
        self.app_folder = "OrcaSlicer Config Manager"
        self.credentials_file = Path.home() / ".orcaslicer_manager" / "credentials.json"
        self.credentials_file.parent.mkdir(exist_ok=True)
        self.load_credentials()
        
    def load_credentials(self):
        """Load stored credentials from file"""
        if self.credentials_file.exists():
            try:
                with open(self.credentials_file, 'r') as f:
                    data = json.load(f)
                    self.credentials = data.get('credentials', {})
            except Exception:
                pass
    
    def save_credentials(self):
        """Save credentials to file"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump({'credentials': self.credentials}, f)
        except Exception as e:
            if self.gui_parent:
                messagebox.showerror("Error", f"Failed to save credentials: {e}")

class GoogleDriveManager(CloudStorageManager):
    """Google Drive integration"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self, gui_parent=None):
        super().__init__(gui_parent)
        self.service = None
        self.folder_id = None
        
    def authenticate(self):
        """Authenticate with Google Drive"""
        if not GOOGLE_DRIVE_AVAILABLE:
            messagebox.showerror("Error", 
                               "Google Drive integration requires additional packages.\n"
                               "Please install: pip install google-api-python-client google-auth-oauthlib")
            return False
            
        try:
            creds = None
            token_file = self.credentials_file.parent / "google_token.json"
            
            # Load existing token
            if token_file.exists():
                creds = Credentials.from_authorized_user_file(str(token_file), self.SCOPES)
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Create OAuth flow
                    client_config = {
                        "web": {
                            "client_id": "your-client-id",
                            "client_secret": "your-client-secret",
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost:8080"]
                        }
                    }
                    
                    # For now, show instructions to user
                    messagebox.showinfo("Google Drive Authentication",
                                      "To enable Google Drive integration:\n\n"
                                      "1. Go to Google Cloud Console\n"
                                      "2. Create a new project or select existing\n"
                                      "3. Enable Google Drive API\n"
                                      "4. Create OAuth 2.0 credentials\n"
                                      "5. Download the credentials.json file\n\n"
                                      "This is a demo version - contact developer for full setup.")
                    return False
            
            # Save the credentials for next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            
            self.service = build('drive', 'v3', credentials=creds)
            self._ensure_app_folder()
            self.credentials['google_drive'] = True
            self.save_credentials()
            return True
            
        except Exception as e:
            messagebox.showerror("Authentication Error", f"Failed to authenticate with Google Drive: {e}")
            return False
    
    def _ensure_app_folder(self):
        """Ensure app folder exists in Google Drive"""
        try:
            # Search for existing folder
            results = self.service.files().list(
                q=f"name='{self.app_folder}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.folder_id = folders[0]['id']
            else:
                # Create folder
                folder_metadata = {
                    'name': self.app_folder,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata).execute()
                self.folder_id = folder['id']
                
        except Exception as e:
            raise Exception(f"Failed to create app folder: {e}")
    
    def upload_backup(self, local_file_path, callback=None):
        """Upload backup to Google Drive"""
        try:
            if not self.service:
                raise Exception("Not authenticated with Google Drive")
                
            filename = Path(local_file_path).name
            
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(local_file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            if callback:
                callback(f"Successfully uploaded {filename} to Google Drive")
            return True
            
        except Exception as e:
            if callback:
                callback(f"Upload failed: {e}")
            return False
    
    def download_backup(self, filename, local_path, callback=None):
        """Download backup from Google Drive"""
        try:
            if not self.service:
                raise Exception("Not authenticated with Google Drive")
                
            # Find file
            results = self.service.files().list(
                q=f"name='{filename}' and parents in '{self.folder_id}' and trashed=false"
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                raise Exception(f"File {filename} not found")
                
            file_id = files[0]['id']
            request = self.service.files().get_media(fileId=file_id)
            
            with open(local_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
            
            if callback:
                callback(f"Successfully downloaded {filename}")
            return True
            
        except Exception as e:
            if callback:
                callback(f"Download failed: {e}")
            return False
    
    def list_backups(self):
        """List available backups in Google Drive"""
        try:
            if not self.service:
                return []
                
            results = self.service.files().list(
                q=f"parents in '{self.folder_id}' and trashed=false and name contains '.zip'",
                fields="files(id,name,modifiedTime,size)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception:
            return []

class iCloudManager(CloudStorageManager):
    """iCloud Drive integration using local folder access"""
    
    def __init__(self, gui_parent=None):
        super().__init__(gui_parent)
        self.icloud_path = None
        self.app_folder_path = None
        
    def authenticate(self):
        """Set up iCloud Drive access"""
        try:
            # Find iCloud Drive path
            possible_paths = [
                Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs",
                Path.home() / "iCloud Drive (Archive)" / "iCloud Drive",
                Path.home() / "iCloud Drive"
            ]
            
            for path in possible_paths:
                if path.exists() and path.is_dir():
                    self.icloud_path = path
                    break
            
            if not self.icloud_path:
                messagebox.showerror("iCloud Not Found", 
                                   "iCloud Drive folder not found.\n"
                                   "Please ensure iCloud Drive is enabled in System Preferences.")
                return False
            
            # Create app folder
            self.app_folder_path = self.icloud_path / self.app_folder
            self.app_folder_path.mkdir(exist_ok=True)
            
            # Test write access
            test_file = self.app_folder_path / ".test"
            try:
                test_file.write_text("test")
                test_file.unlink()
            except Exception:
                messagebox.showerror("Permission Error", 
                                   "Cannot write to iCloud Drive folder.\n"
                                   "Please check permissions.")
                return False
            
            self.credentials['icloud'] = True
            self.save_credentials()
            return True
            
        except Exception as e:
            messagebox.showerror("iCloud Setup Error", f"Failed to set up iCloud integration: {e}")
            return False
    
    def upload_backup(self, local_file_path, callback=None):
        """Upload backup to iCloud Drive"""
        try:
            if not self.app_folder_path:
                raise Exception("iCloud Drive not set up")
                
            filename = Path(local_file_path).name
            dest_path = self.app_folder_path / filename
            
            shutil.copy2(local_file_path, dest_path)
            
            if callback:
                callback(f"Successfully copied {filename} to iCloud Drive")
            return True
            
        except Exception as e:
            if callback:
                callback(f"Upload failed: {e}")
            return False
    
    def download_backup(self, filename, local_path, callback=None):
        """Download backup from iCloud Drive"""
        try:
            if not self.app_folder_path:
                raise Exception("iCloud Drive not set up")
                
            source_path = self.app_folder_path / filename
            
            if not source_path.exists():
                raise Exception(f"File {filename} not found in iCloud Drive")
                
            shutil.copy2(source_path, local_path)
            
            if callback:
                callback(f"Successfully downloaded {filename}")
            return True
            
        except Exception as e:
            if callback:
                callback(f"Download failed: {e}")
            return False
    
    def list_backups(self):
        """List available backups in iCloud Drive"""
        try:
            if not self.app_folder_path or not self.app_folder_path.exists():
                return []
                
            backups = []
            for file_path in self.app_folder_path.glob("*.zip"):
                stat = file_path.stat()
                backups.append({
                    'name': file_path.name,
                    'modifiedTime': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'size': str(stat.st_size)
                })
                
            return sorted(backups, key=lambda x: x['modifiedTime'], reverse=True)
            
        except Exception:
            return []

class CloudStorageDialog:
    """Dialog for cloud storage operations"""
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.google_manager = GoogleDriveManager(parent)
        self.icloud_manager = iCloudManager(parent)
        
    def show_auth_dialog(self):
        """Show authentication dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Cloud Storage Authentication")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Choose Cloud Storage Service", 
                font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        tk.Label(frame, text="Select a service to authenticate and sync your backups:",
                wraplength=350).pack(pady=(0, 20))
        
        # Google Drive button
        google_btn = tk.Button(frame, text="🔗 Connect Google Drive",
                              command=lambda: self._authenticate('google'),
                              font=('Arial', 12),
                              bg='#4285F4', fg='white',
                              height=2, width=20)
        google_btn.pack(pady=5)
        
        # iCloud button
        icloud_btn = tk.Button(frame, text="🔗 Connect iCloud Drive",
                              command=lambda: self._authenticate('icloud'),
                              font=('Arial', 12),
                              bg='#007AFF', fg='white',
                              height=2, width=20)
        icloud_btn.pack(pady=5)
        
        # Status
        self.status_var = tk.StringVar()
        status_label = tk.Label(frame, textvariable=self.status_var,
                               wraplength=350, justify=tk.LEFT)
        status_label.pack(pady=(20, 0))
        
        # Update status
        self._update_status()
        
        # Close button
        tk.Button(frame, text="Close", 
                 command=dialog.destroy).pack(pady=(20, 0))
        
        self.dialog = dialog
        
    def _authenticate(self, service):
        """Authenticate with selected service"""
        self.status_var.set("Authenticating...")
        self.dialog.update()
        
        def auth_thread():
            if service == 'google':
                success = self.google_manager.authenticate()
            else:
                success = self.icloud_manager.authenticate()
                
            self.dialog.after(0, lambda: self._auth_complete(service, success))
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def _auth_complete(self, service, success):
        """Handle authentication completion"""
        if success:
            self.status_var.set(f"{service.title()} Drive connected successfully!")
        else:
            self.status_var.set(f"Failed to connect to {service.title()} Drive")
        
        self._update_status()
    
    def _update_status(self):
        """Update connection status display"""
        status = "Connection Status:\n"
        
        if self.google_manager.credentials.get('google_drive'):
            status += "✅ Google Drive: Connected\n"
        else:
            status += "❌ Google Drive: Not connected\n"
            
        if self.icloud_manager.credentials.get('icloud'):
            status += "✅ iCloud Drive: Connected"
        else:
            status += "❌ iCloud Drive: Not connected"
            
        self.status_var.set(status)
    
    def show_sync_dialog(self, operation='upload'):
        """Show upload/download dialog"""
        if not (self.google_manager.credentials.get('google_drive') or 
                self.icloud_manager.credentials.get('icloud')):
            messagebox.showwarning("Not Connected", 
                                 "Please authenticate with a cloud service first.")
            return
        
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Cloud Storage - {operation.title()}")
        dialog.geometry("500x400")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text=f"{operation.title()} Configuration Backup",
                font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Service selection
        service_frame = tk.Frame(frame)
        service_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(service_frame, text="Choose service:").pack(anchor=tk.W)
        
        self.service_var = tk.StringVar(value="icloud")
        
        if self.google_manager.credentials.get('google_drive'):
            tk.Radiobutton(service_frame, text="Google Drive", 
                          variable=self.service_var, value="google").pack(anchor=tk.W)
        
        if self.icloud_manager.credentials.get('icloud'):
            tk.Radiobutton(service_frame, text="iCloud Drive", 
                          variable=self.service_var, value="icloud").pack(anchor=tk.W)
        
        # Progress and status
        self.progress_var = tk.StringVar(value="Ready")
        tk.Label(frame, textvariable=self.progress_var).pack(anchor=tk.W)
        
        self.sync_progress = tk.Text(frame, height=10, width=60)
        self.sync_progress.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        if operation == 'upload':
            tk.Button(button_frame, text="Upload Current Config",
                     command=lambda: self._sync_operation('upload')).pack(side=tk.LEFT, padx=(0, 10))
        else:
            tk.Button(button_frame, text="Download Backup",
                     command=lambda: self._sync_operation('download')).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Close",
                 command=dialog.destroy).pack(side=tk.RIGHT)
        
        self.sync_dialog = dialog
    
    def _sync_operation(self, operation):
        """Perform upload or download operation"""
        service = self.service_var.get()
        manager = self.google_manager if service == 'google' else self.icloud_manager
        
        def log_message(message):
            self.sync_dialog.after(0, lambda: self._log_sync_message(message))
        
        def sync_thread():
            try:
                if operation == 'upload':
                    # Get current configuration backup
                    from orca_backup import OrcaBackup
                    backup_tool = OrcaBackup()
                    
                    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
                        filename = f"orcaslicer_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                        backup_file = Path(tmp.name).parent / filename
                        
                        log_message("Creating configuration backup...")
                        backup_tool.export_configuration(str(backup_file))
                        
                        log_message(f"Uploading to {service.title()} Drive...")
                        manager.upload_backup(str(backup_file), log_message)
                        
                        backup_file.unlink()  # Cleanup
                        
                else:
                    # Download operation
                    backups = manager.list_backups()
                    if not backups:
                        log_message("No backups found in cloud storage")
                        return
                    
                    # For simplicity, download the most recent backup
                    latest = backups[0]
                    filename = latest['name']
                    
                    # Ask user where to save
                    from tkinter import filedialog
                    save_path = filedialog.asksaveasfilename(
                        title="Save downloaded backup",
                        defaultextension=".zip",
                        filetypes=[("Zip files", "*.zip")]
                    )
                    
                    if save_path:
                        log_message(f"Downloading {filename}...")
                        manager.download_backup(filename, save_path, log_message)
                    
            except Exception as e:
                log_message(f"Operation failed: {e}")
        
        self.progress_var.set(f"{operation.title()}ing...")
        threading.Thread(target=sync_thread, daemon=True).start()
    
    def _log_sync_message(self, message):
        """Add message to sync progress log"""
        self.sync_progress.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.sync_progress.see(tk.END)