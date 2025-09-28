#!/usr/bin/env python3
"""
Simple launcher script for Smart Auto Clicker
This script provides a convenient way to start the application
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from smart_auto_clicker import main
    
    if __name__ == "__main__":
        print("Smart Auto Clicker - Starting application...")
        main()
        
except ImportError as e:
    print(f"Error: Missing required dependencies. Please run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)