#!/usr/bin/env python3
"""
Quick Start Guide for Smart Auto Clicker
"""

print("Smart Auto Clicker - Quick Start Guide")
print("=" * 40)
print()

print("1. CLI Mode (Always Available)")
print("-" * 30)
print("   python3 cli_auto_clicker.py")
print("   Commands: add, list, run, save, load, clear, help, quit")
print()

print("2. GUI Mode (Requires Dependencies)")
print("-" * 30)
print("   pip install -r requirements.txt  # Install dependencies")
print("   python3 smart_auto_clicker.py    # Run GUI version")
print()

print("3. Demo Mode")
print("-" * 30)
print("   python3 demo.py                  # See working example")
print()

print("4. Run Tests")
print("-" * 30)
print("   python3 test_auto_clicker.py     # Verify functionality")
print()

print("Available Files:")
print("- smart_auto_clicker.py      : Full GUI application")
print("- cli_auto_clicker.py        : Command-line interface")
print("- demo.py                    : Working demonstration")
print("- test_auto_clicker.py       : Test suite")
print("- run.py                     : Simple launcher script")
print("- requirements.txt           : Full dependencies")
print("- requirements-minimal.txt   : Minimal dependencies")
print("- setup.py                   : Package installation")
print("- README.md                  : Complete documentation")
print()

print("Quick Example (CLI):")
print("$ python3 cli_auto_clicker.py")
print("> add 100 200 left 1.0 'First click'")
print("> add 300 400 right 1.5 'Menu click'") 
print("> list")
print("> run 3")
print("> save my_pattern.json")
print("> quit")
print()

print("For detailed usage, see README.md")

# Test basic functionality
print("\nTesting basic functionality...")
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from cli_auto_clicker import SimpleAutoClicker
    clicker = SimpleAutoClicker()
    clicker.add_click_point(100, 200)
    print("✅ CLI functionality working")
    
    try:
        from smart_auto_clicker import DEPENDENCIES_AVAILABLE
        missing = [dep for dep, avail in DEPENDENCIES_AVAILABLE.items() if not avail]
        if missing:
            print(f"⚠️  GUI has missing dependencies: {', '.join(missing)}")
        else:
            print("✅ GUI functionality available")
    except:
        print("⚠️  GUI functionality limited")
        
except Exception as e:
    print(f"❌ Error testing functionality: {e}")

print("\nReady to use!")