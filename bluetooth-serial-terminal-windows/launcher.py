#!/usr/bin/env python3
import os
import sys
import platform

def main():
    print("=" * 60)
    print("Bluetooth Serial Terminal")
    print("=" * 60)
    print()
    
    if 'REPL_ID' in os.environ:
        print("⚠️  NOTE: This application is designed to run on Windows")
        print("   with Bluetooth hardware access.")
        print()
        print("   Since Replit is a cloud environment without Bluetooth")
        print("   hardware or GUI display, the application cannot run here.")
        print()
        print("📥 TO USE THIS APPLICATION:")
        print("   1. Download all project files to your Windows computer")
        print("   2. Install Python 3.11+ from python.org")
        print("   3. Run: python main.py")
        print("   OR")
        print("   4. Double-click run.bat on Windows")
        print()
        print("=" * 60)
        print("✅ Application files are ready for download!")
        print("=" * 60)
        
    else:
        print(f"Platform: {platform.system()}")
        print(f"Python: {sys.version}")
        print()
        
        if platform.system() != "Windows":
            print("⚠️  This application is optimized for Windows")
            print("   It may work on Linux/Mac with Bluetooth support")
            print()
        
        try:
            if os.environ.get('DISPLAY'):
                print("Starting GUI application...")
                import main
                main.main()
            else:
                print("❌ No display detected!")
                print("   GUI applications require a display.")
                print()
                print("   On Windows: Just run the application normally")
                print("   On Linux: Set DISPLAY environment variable")
        except Exception as e:
            print(f"❌ Error: {e}")
            print()
            print("Please ensure:")
            print("  - Python 3.11+ is installed")
            print("  - Dependencies are installed: pip install pyserial")
            print("  - Display is available for GUI")

if __name__ == "__main__":
    main()
