#!/usr/bin/env python3
"""
Script to create a simple skull icon for the OrcaSlicer Config Manager
This creates both .ico (Windows) and .icns (Mac) formats
"""

import tkinter as tk
from tkinter import messagebox
import os

def create_skull_ascii_icon():
    """Create a text-based skull icon as a placeholder"""
    skull_art = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀
    ⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀
    ⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
    ⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀
    ⢸⣿⣿⣿⣿⣿⠟⠋⠉⠉⠉⠉⠉⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⡇⠀
    ⣿⣿⣿⣿⣿⠃⠀⢰⣶⣶⠀⠀⠀⠀⢰⣶⣶⠀⠀⠘⣿⣿⣿⣿⣿⣿⠀
    ⣿⣿⣿⣿⡟⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⢻⣿⣿⣿⣿⣿⠀
    ⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⢠⣤⣄⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⠀
    ⠸⣿⣿⣿⣿⣷⣦⣀⠀⠀⢀⣿⣿⣿⡀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⠇⠀
    ⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀
    ⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
    ⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠉⠛⠿⠋⠀⠀⠀⠀⠀⠀⠙⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
    """
    
    print("Skull Icon ASCII Art:")
    print(skull_art)
    
    return skull_art

def show_icon_instructions():
    """Show instructions for creating proper icon files"""
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    instructions = """
SKULL ICON SETUP INSTRUCTIONS

To add a skull icon to your OrcaSlicer Config Manager:

OPTION 1 - Download/Create Icons:
1. Find or create a skull icon image (PNG, JPG, etc.)
2. Convert to required formats:
   • Windows: Convert to 'skull_icon.ico' (256x256 or multiple sizes)
   • Mac: Convert to 'skull_icon.icns' (1024x1024 recommended)

OPTION 2 - Online Icon Generators:
1. Search for "skull icon" on sites like:
   • flaticon.com
   • iconmonstr.com
   • icons8.com
2. Download in ICO format for Windows
3. Convert to ICNS format for Mac using online converters

OPTION 3 - Use System Icons:
• The build scripts will work without icons
• Apps will use default system icons

PLACEMENT:
• Place 'skull_icon.ico' in the project folder for Windows
• Place 'skull_icon.icns' in the project folder for Mac
• Run the build scripts again

The build scripts will automatically detect and use the icons!
    """
    
    messagebox.showinfo("Skull Icon Setup", instructions)
    root.destroy()

def main():
    """Main function"""
    print("OrcaSlicer Config Manager - Skull Icon Creator")
    print("=" * 50)
    
    # Show ASCII skull
    create_skull_ascii_icon()
    
    # Show GUI instructions
    try:
        show_icon_instructions()
    except:
        # If GUI fails, show text instructions
        print("\nICON SETUP INSTRUCTIONS:")
        print("1. Create or download a skull icon image")
        print("2. Convert to skull_icon.ico (Windows) and skull_icon.icns (Mac)")
        print("3. Place files in project directory")
        print("4. Run build scripts")

if __name__ == "__main__":
    main()