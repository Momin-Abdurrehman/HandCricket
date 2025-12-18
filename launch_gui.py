#!/usr/bin/env python3
"""
Standalone GUI launcher for Hand Cricket AI
Run this directly to launch the GUI interface
"""

if __name__ == "__main__":
    try:
        import tkinter as tk
        print("✓ Tkinter is available")
        
        # Import and run the GUI
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from src.ui import run
        print("✓ Starting Hand Cricket AI GUI...")
        run()
        
    except ImportError as e:
        if 'tkinter' in str(e).lower() or '_tkinter' in str(e).lower():
            print("=" * 60)
            print("❌ Tkinter is NOT available")
            print("=" * 60)
            print("\nTkinter is required for the GUI but is not installed.")
            print("\nTo install Tkinter:")
            print("  • macOS: brew install python-tk@3.10")
            print("  • Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  • Windows: Tkinter comes with Python")
            print("\nAlternatively, use the CLI mode:")
            print("  python main.py play")
        else:
            print(f"Error importing modules: {e}")
            raise
