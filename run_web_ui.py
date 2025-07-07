#!/usr/bin/env python3
"""
Facebook Rental Agent Web UI Launcher
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['streamlit', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing packages."""
    print(f"Installing missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print(f"pip install {' '.join(packages)}")
        return False

def main():
    print("🏠 Facebook Rental Agent Web UI")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        install_choice = input("Install missing dependencies? (y/n): ").lower()
        if install_choice == 'y':
            if not install_dependencies(missing):
                return
        else:
            print("Please install dependencies manually and try again.")
            return
    
    # Check if web_ui.py exists
    if not os.path.exists('web_ui.py'):
        print("❌ web_ui.py not found!")
        return
    
    # Launch Streamlit
    print("🚀 Starting web UI...")
    print("📱 The web interface will open in your browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'web_ui.py', '--server.port=8501'])
    except KeyboardInterrupt:
        print("\n👋 Web UI stopped.")

if __name__ == "__main__":
    main() 