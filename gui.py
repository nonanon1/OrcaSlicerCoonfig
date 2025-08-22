"""
Graphical User Interface for OrcaSlicer Configuration Backup Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from orca_backup import OrcaBackup
from utils import format_file_size

class GUIInterface:
    """GUI interface using tkinter"""
    
    def __init__(self):
        self.backup_tool = OrcaBackup()
        self.root = None
        self.status_var = None
        self.progress_var = None
        
    def run(self):
        """Initialize and run the GUI"""
        self.root = tk.Tk()
        self.root.title("OrcaSlicer Configuration Backup Tool")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.create_widgets()
        self.update_status()
        
        # Center window
        self.center_window()
        
        self.root.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="OrcaSlicer Configuration Backup Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Current Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_var = tk.StringVar()
        status_text = tk.Text(status_frame, height=6, width=70, wrap=tk.WORD)
        status_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Scrollbar for status text
        status_scroll = ttk.Scrollbar(status_frame, orient="vertical", command=status_text.yview)
        status_scroll.grid(row=0, column=2, sticky=(tk.N, tk.S))
        status_text.configure(yscrollcommand=status_scroll.set)
        
        self.status_text = status_text
        
        # Refresh button
        refresh_btn = ttk.Button(status_frame, text="Refresh", command=self.update_status)
        refresh_btn.grid(row=1, column=0, pady=(10, 0), sticky=tk.W)
        
        # Export section
        export_frame = ttk.LabelFrame(main_frame, text="Export Configuration", padding="10")
        export_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        export_frame.columnconfigure(1, weight=1)
        
        ttk.Label(export_frame, text="Export current configuration to:").grid(row=0, column=0, sticky=tk.W)
        
        self.export_path_var = tk.StringVar()
        export_entry = ttk.Entry(export_frame, textvariable=self.export_path_var, width=50)
        export_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        export_browse_btn = ttk.Button(export_frame, text="Browse...", command=self.browse_export_file)
        export_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))
        
        export_btn = ttk.Button(export_frame, text="Export Configuration", 
                               command=self.export_config_threaded, style='Accent.TButton')
        export_btn.grid(row=2, column=0, pady=(10, 0), sticky=tk.W)
        
        # Import section
        import_frame = ttk.LabelFrame(main_frame, text="Import Configuration", padding="10")
        import_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        import_frame.columnconfigure(1, weight=1)
        
        ttk.Label(import_frame, text="Import configuration from:").grid(row=0, column=0, sticky=tk.W)
        
        self.import_path_var = tk.StringVar()
        import_entry = ttk.Entry(import_frame, textvariable=self.import_path_var, width=50)
        import_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        import_browse_btn = ttk.Button(import_frame, text="Browse...", command=self.browse_import_file)
        import_browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))
        
        # Backup checkbox
        self.create_backup_var = tk.BooleanVar(value=True)
        backup_check = ttk.Checkbutton(import_frame, text="Create backup of current configuration before import",
                                      variable=self.create_backup_var)
        backup_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        import_btn = ttk.Button(import_frame, text="Import Configuration", 
                               command=self.import_config_threaded, style='Accent.TButton')
        import_btn.grid(row=3, column=0, pady=(10, 0), sticky=tk.W)
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Set default export filename
        from datetime import datetime
        default_name = f"orca_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        self.export_path_var.set(default_name)
    
    def update_status(self):
        """Update the status display"""
        try:
            info = self.backup_tool.get_config_info()
            
            status_text = "OrcaSlicer Configuration Status\n"
            status_text += "=" * 40 + "\n\n"
            
            status_text += f"Installation found: {'Yes' if info['installation_found'] else 'No'}\n"
            if info['installation_path']:
                status_text += f"Installation path: {info['installation_path']}\n"
            
            status_text += f"Configuration found: {'Yes' if info['config_found'] else 'No'}\n"
            if info['config_path']:
                status_text += f"Configuration path: {info['config_path']}\n"
                if info['config_found']:
                    status_text += f"Configuration size: {format_file_size(info['config_size'])}\n"
                    status_text += f"Number of files: {info['file_count']}\n"
            
            if 'error' in info:
                status_text += f"\nError: {info['error']}\n"
            
            if not info['config_found']:
                status_text += "\nNote: OrcaSlicer configuration not found.\n"
                status_text += "Please ensure OrcaSlicer is installed and has been run at least once.\n"
            
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, status_text)
            
        except Exception as e:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Error updating status: {e}")
    
    def browse_export_file(self):
        """Browse for export file location"""
        filename = filedialog.asksaveasfilename(
            title="Save backup as...",
            defaultextension=".zip",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.export_path_var.set(filename)
    
    def browse_import_file(self):
        """Browse for import file location"""
        filename = filedialog.askopenfilename(
            title="Select backup file to import",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.import_path_var.set(filename)
    
    def export_config_threaded(self):
        """Export configuration in a separate thread"""
        export_path = self.export_path_var.get().strip()
        if not export_path:
            messagebox.showerror("Error", "Please specify an export filename")
            return
        
        # Check if file exists
        if Path(export_path).exists():
            if not messagebox.askyesno("File Exists", 
                                     f"File '{export_path}' already exists.\nDo you want to overwrite it?"):
                return
        
        # Start progress
        self.progress_var.set("Exporting configuration...")
        self.progress_bar.start()
        
        def export_thread():
            try:
                success = self.backup_tool.export_configuration(export_path)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.export_completed(success, export_path, None))
                
            except Exception as e:
                self.root.after(0, lambda: self.export_completed(False, export_path, str(e)))
        
        threading.Thread(target=export_thread, daemon=True).start()
    
    def export_completed(self, success, filename, error):
        """Handle export completion"""
        self.progress_bar.stop()
        
        if success:
            file_size = format_file_size(Path(filename).stat().st_size)
            self.progress_var.set("Export completed successfully")
            messagebox.showinfo("Export Successful", 
                              f"Configuration exported successfully!\n\nFile: {filename}\nSize: {file_size}")
        else:
            self.progress_var.set("Export failed")
            error_msg = f"Export failed"
            if error:
                error_msg += f": {error}"
            messagebox.showerror("Export Failed", error_msg)
    
    def import_config_threaded(self):
        """Import configuration in a separate thread"""
        import_path = self.import_path_var.get().strip()
        if not import_path:
            messagebox.showerror("Error", "Please specify an import filename")
            return
        
        if not Path(import_path).exists():
            messagebox.showerror("Error", f"File '{import_path}' not found")
            return
        
        # Show backup info
        backup_info = self.backup_tool.validator.get_backup_info(import_path)
        if backup_info and 'error' not in backup_info:
            info_text = "Backup Information:\n\n"
            for key, value in backup_info.items():
                info_text += f"{key}: {value}\n"
            info_text += f"\nThis will replace your current OrcaSlicer configuration.\n"
            info_text += f"Do you want to continue?"
        else:
            info_text = f"Import configuration from:\n{import_path}\n\n"
            info_text += f"This will replace your current OrcaSlicer configuration.\n"
            info_text += f"Do you want to continue?"
        
        if not messagebox.askyesno("Confirm Import", info_text):
            return
        
        create_backup = self.create_backup_var.get()
        
        # Start progress
        self.progress_var.set("Importing configuration...")
        self.progress_bar.start()
        
        def import_thread():
            try:
                success = self.backup_tool.import_configuration(import_path, create_backup)
                
                # Update UI in main thread
                self.root.after(0, lambda: self.import_completed(success, import_path, None))
                
            except Exception as e:
                self.root.after(0, lambda: self.import_completed(False, import_path, str(e)))
        
        threading.Thread(target=import_thread, daemon=True).start()
    
    def import_completed(self, success, filename, error):
        """Handle import completion"""
        self.progress_bar.stop()
        
        if success:
            self.progress_var.set("Import completed successfully")
            messagebox.showinfo("Import Successful", 
                              f"Configuration imported successfully!\n\n"
                              f"Please restart OrcaSlicer to see the changes.")
            # Update status display
            self.update_status()
        else:
            self.progress_var.set("Import failed")
            error_msg = f"Import failed"
            if error:
                error_msg += f": {error}"
            messagebox.showerror("Import Failed", error_msg)

def main():
    """Main entry point for GUI"""
    gui = GUIInterface()
    gui.run()

if __name__ == "__main__":
    main()
