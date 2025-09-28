#!/usr/bin/env python3
"""
Demo script for Smart Auto Clicker
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli_auto_clicker import SimpleAutoClicker

def main():
    print("Smart Auto Clicker - Demo")
    print("=" * 40)
    
    clicker = SimpleAutoClicker()
    
    # Add some sample click points
    print("\n1. Adding sample click points:")
    clicker.add_click_point(100, 200, "left", 1.0, "First click")
    clicker.add_click_point(300, 400, "right", 1.5, "Menu click")
    clicker.add_click_point(500, 300, "left", 0.5, "Quick click")
    
    # List the points
    print("\n2. Current click points:")
    clicker.list_points()
    
    # Save pattern
    print("\n3. Saving pattern to demo_pattern.json:")
    clicker.save_pattern("demo_pattern.json")
    
    # Simulate clicking
    print("\n4. Simulating clicks (2 cycles):")
    clicker.simulate_clicks(2)
    
    # Clear and reload
    print("\n5. Clearing points and reloading from file:")
    clicker.clear_points()
    clicker.load_pattern("demo_pattern.json")
    clicker.list_points()
    
    print("\nDemo completed successfully!")

if __name__ == "__main__":
    main()