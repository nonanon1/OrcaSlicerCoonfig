"""
Simple GUI for OrcaSlicer Configuration Backup Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import tempfile
import zipfile
from pathlib import Path
from datetime import datetime
from orca_backup import OrcaBackup
from utils import format_file_size

class ConfigDiff:
    """Compare two OrcaSlicer configurations"""
    
    def __init__(self, backup_tool):
        self.backup_tool = backup_tool
    
    def compare_with_backup(self, backup_file):
        """
        Compare current configuration with a backup file
        
        Args:
            backup_file (str): Path to backup zip file
            
        Returns:
            dict: Comparison results
        """
        current_info = self.backup_tool.get_config_info()
        
        if not current_info['config_found']:
            return {'error': 'No current configuration found'}
        
        # Extract backup to temp directory for comparison
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                config_backup = temp_path / "config"
                if not config_backup.exists():
                    return {'error': 'Invalid backup file'}
                
                current_config = Path(current_info['config_path'])
                
                # Compare directory structures
                comparison = {
                    'current_files': set(),
                    'backup_files': set(),
                    'common_files': set(),
                    'different_files': [],
                    'only_in_current': set(),
                    'only_in_backup': set()
                }
                
                # Get all files in current config
                if current_config.exists():
                    for file_path in current_config.rglob('*'):
                        if file_path.is_file():
                            rel_path = file_path.relative_to(current_config)
                            comparison['current_files'].add(str(rel_path))
                
                # Get all files in backup config
                for file_path in config_backup.rglob('*'):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(config_backup)
                        comparison['backup_files'].add(str(rel_path))
                
                # Find common files and differences
                comparison['common_files'] = comparison['current_files'] & comparison['backup_files']
                comparison['only_in_current'] = comparison['current_files'] - comparison['backup_files']
                comparison['only_in_backup'] = comparison['backup_files'] - comparison['current_files']
                
                # Check for file content differences
                for rel_path in comparison['common_files']:
                    current_file = current_config / rel_path
                    backup_file = config_backup / rel_path
                    
                    try:
                        current_size = current_file.stat().st_size
                        backup_size = backup_file.stat().st_size
                        
                        if current_size != backup_size:
                            comparison['different_files'].append({
                                'file': rel_path,
                                'current_size': current_size,
                                'backup_size': backup_size,
                                'reason': 'Different file sizes'
                            })
                        else:
                            # For small files, compare content
                            if current_size < 1024 * 1024:  # Less than 1MB
                                try:
                                    with open(current_file, 'rb') as f1, open(backup_file, 'rb') as f2:
                                        if f1.read() != f2.read():
                                            comparison['different_files'].append({
                                                'file': rel_path,
                                                'current_size': current_size,
                                                'backup_size': backup_size,
                                                'reason': 'Different content'
                                            })
                                except Exception:
                                    pass
                    except Exception:
                        pass
                
                return comparison
                
        except Exception as e:
            return {'error': f'Failed to compare configurations: {e}'}

class OrcaBackupGUI:
    """Simple GUI for OrcaSlicer backup operations"""
    
    def __init__(self):
        self.backup_tool = OrcaBackup()
        self.diff_tool = ConfigDiff(self.backup_tool)
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.update_status()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("OrcaSlicer Configuration Manager")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="OrcaSlicer Configuration Manager", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Configuration Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=5, width=80)
        self.status_text.pack(fill=tk.X)
        
        # Main action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Save Configuration button
        save_btn = ttk.Button(button_frame, text="Save Configuration", 
                             command=self.save_configuration, style='Accent.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load Configuration button  
        load_btn = ttk.Button(button_frame, text="Load Configuration", 
                             command=self.load_configuration, style='Accent.TButton')
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Compare button
        compare_btn = ttk.Button(button_frame, text="Compare with Backup", 
                                command=self.compare_configurations)
        compare_btn.pack(side=tk.LEFT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        progress_label.pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Results/Diff section
        results_frame = ttk.LabelFrame(main_frame, text="Comparison Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def update_status(self):
        """Update configuration status display"""
        try:
            info = self.backup_tool.get_config_info()
            
            status = "OrcaSlicer Configuration Status\n"
            status += "=" * 50 + "\n"
            status += f"Installation found: {'Yes' if info['installation_found'] else 'No'}\n"
            
            if info['installation_path']:
                status += f"Installation path: {info['installation_path']}\n"
            
            status += f"Configuration found: {'Yes' if info['config_found'] else 'No'}\n"
            
            if info['config_path']:
                status += f"Configuration path: {info['config_path']}\n"
                if info['config_found']:
                    status += f"Configuration size: {format_file_size(info['config_size'])}\n"
                    status += f"Number of files: {info['file_count']}\n"
            
            if not info['config_found']:
                status += "\nWARNING: OrcaSlicer configuration not found.\n"
                status += "Please ensure OrcaSlicer is installed and run at least once.\n"
            
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, status)
            
        except Exception as e:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Error updating status: {e}")
    
    def save_configuration(self):
        """Save current configuration to a zip file"""
        # Get save location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"orca_config_backup_{timestamp}.zip"
        
        filename = filedialog.asksaveasfilename(
            title="Save Configuration As...",
            defaultextension=".zip",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        # Start progress
        self.progress_var.set("Saving configuration...")
        self.progress_bar.start()
        
        def save_thread():
            try:
                success = self.backup_tool.export_configuration(filename)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.save_completed(success, filename, None))
                
            except Exception as e:
                self.root.after(0, lambda: self.save_completed(False, filename, str(e)))
        
        threading.Thread(target=save_thread, daemon=True).start()
    
    def save_completed(self, success, filename, error):
        """Handle save completion"""
        self.progress_bar.stop()
        
        if success:
            file_size = format_file_size(Path(filename).stat().st_size)
            self.progress_var.set("Configuration saved successfully")
            
            result = f"Configuration saved successfully!\n\n"
            result += f"File: {filename}\n"
            result += f"Size: {file_size}\n"
            result += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
        else:
            self.progress_var.set("Save failed")
            error_msg = f"ERROR: Failed to save configuration"
            if error:
                error_msg += f":\n{error}"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)
            
            messagebox.showerror("Error", error_msg)
    
    def load_configuration(self):
        """Load configuration from a zip file"""
        filename = filedialog.askopenfilename(
            title="Select Configuration Backup",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        # Show confirmation dialog
        if not messagebox.askyesno("Confirm Load", 
                                  f"This will replace your current OrcaSlicer configuration with:\n{filename}\n\nA backup of your current configuration will be created automatically.\n\nDo you want to continue?"):
            return
        
        # Start progress
        self.progress_var.set("Loading configuration...")
        self.progress_bar.start()
        
        def load_thread():
            try:
                success = self.backup_tool.import_configuration(filename, create_backup=True)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.load_completed(success, filename, None))
                
            except Exception as e:
                self.root.after(0, lambda: self.load_completed(False, filename, str(e)))
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def load_completed(self, success, filename, error):
        """Handle load completion"""
        self.progress_bar.stop()
        
        if success:
            self.progress_var.set("Configuration loaded successfully")
            
            result = f"Configuration loaded successfully!\n\n"
            result += f"From: {filename}\n"
            result += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            result += "Please restart OrcaSlicer to see the changes.\n"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result)
            
            # Update status
            self.update_status()
            
            messagebox.showinfo("Success", "Configuration loaded successfully!\n\nPlease restart OrcaSlicer to see the changes.")
        else:
            self.progress_var.set("Load failed")
            error_msg = f"ERROR: Failed to load configuration"
            if error:
                error_msg += f":\n{error}"
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)
            
            messagebox.showerror("Error", error_msg)
    
    def compare_configurations(self):
        """Compare current configuration with a backup"""
        filename = filedialog.askopenfilename(
            title="Select Backup to Compare With",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        # Start progress
        self.progress_var.set("Comparing configurations...")
        self.progress_bar.start()
        
        def compare_thread():
            try:
                comparison = self.diff_tool.compare_with_backup(filename)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.compare_completed(comparison, filename))
                
            except Exception as e:
                self.root.after(0, lambda: self.compare_failed(str(e)))
        
        threading.Thread(target=compare_thread, daemon=True).start()
    
    def compare_completed(self, comparison, filename):
        """Handle comparison completion"""
        self.progress_bar.stop()
        self.progress_var.set("Comparison completed")
        
        if 'error' in comparison:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"ERROR: Comparison failed: {comparison['error']}")
            return
        
        # Build detailed comparison report
        report = f"Configuration Comparison Results\n"
        report += "=" * 60 + "\n"
        report += f"Backup file: {filename}\n"
        report += f"Comparison date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        total_current = len(comparison['current_files'])
        total_backup = len(comparison['backup_files'])
        total_common = len(comparison['common_files'])
        total_different = len(comparison['different_files'])
        only_current = len(comparison['only_in_current'])
        only_backup = len(comparison['only_in_backup'])
        
        report += "Summary:\n"
        report += f"   Current configuration files: {total_current}\n"
        report += f"   Backup configuration files: {total_backup}\n"
        report += f"   Common files: {total_common}\n"
        report += f"   Files with differences: {total_different}\n"
        report += f"   Only in current: {only_current}\n"
        report += f"   Only in backup: {only_backup}\n\n"
        
        if total_different == 0 and only_current == 0 and only_backup == 0:
            report += "Configurations are identical!\n"
        else:
            report += "Configurations have differences:\n\n"
            
            if comparison['different_files']:
                report += "Files with differences:\n"
                for diff in comparison['different_files']:
                    report += f"   • {diff['file']} - {diff['reason']}\n"
                    report += f"     Current: {format_file_size(diff['current_size'])}, "
                    report += f"Backup: {format_file_size(diff['backup_size'])}\n"
                report += "\n"
            
            if comparison['only_in_current']:
                report += "Files only in current configuration:\n"
                for file in sorted(comparison['only_in_current']):
                    report += f"   • {file}\n"
                report += "\n"
            
            if comparison['only_in_backup']:
                report += "Files only in backup:\n"
                for file in sorted(comparison['only_in_backup']):
                    report += f"   • {file}\n"
                report += "\n"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, report)
    
    def compare_failed(self, error):
        """Handle comparison failure"""
        self.progress_bar.stop()
        self.progress_var.set("Comparison failed")
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"ERROR: Comparison failed: {error}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point for the GUI"""
    app = OrcaBackupGUI()
    app.run()

if __name__ == "__main__":
    main()