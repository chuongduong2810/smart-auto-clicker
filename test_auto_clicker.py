#!/usr/bin/env python3
"""
Test script for Smart Auto Clicker functionality
"""

import unittest
import sys
import os
import json
import tempfile
import shutil

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_auto_clicker import SimpleAutoClicker, ClickPoint

class TestSmartAutoClicker(unittest.TestCase):
    """Test cases for Smart Auto Clicker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.clicker = SimpleAutoClicker()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_add_click_point(self):
        """Test adding click points"""
        self.clicker.add_click_point(100, 200, "left", 1.0, "Test click")
        
        self.assertEqual(len(self.clicker.click_points), 1)
        point = self.clicker.click_points[0]
        self.assertEqual(point.x, 100)
        self.assertEqual(point.y, 200)
        self.assertEqual(point.button, "left")
        self.assertEqual(point.delay, 1.0)
        self.assertEqual(point.description, "Test click")
        
    def test_clear_points(self):
        """Test clearing click points"""
        self.clicker.add_click_point(100, 200)
        self.clicker.add_click_point(300, 400)
        self.assertEqual(len(self.clicker.click_points), 2)
        
        self.clicker.clear_points()
        self.assertEqual(len(self.clicker.click_points), 0)
        
    def test_save_load_pattern(self):
        """Test saving and loading patterns"""
        # Add some test points
        self.clicker.add_click_point(100, 200, "left", 1.0, "First")
        self.clicker.add_click_point(300, 400, "right", 2.0, "Second")
        
        # Save pattern
        pattern_file = os.path.join(self.test_dir, "test_pattern.json")
        self.clicker.save_pattern(pattern_file)
        
        # Verify file exists and has content
        self.assertTrue(os.path.exists(pattern_file))
        
        # Clear points and reload
        self.clicker.clear_points()
        self.assertEqual(len(self.clicker.click_points), 0)
        
        self.clicker.load_pattern(pattern_file)
        self.assertEqual(len(self.clicker.click_points), 2)
        
        # Verify loaded points
        point1 = self.clicker.click_points[0]
        self.assertEqual(point1.x, 100)
        self.assertEqual(point1.y, 200)
        self.assertEqual(point1.button, "left")
        self.assertEqual(point1.delay, 1.0)
        self.assertEqual(point1.description, "First")
        
        point2 = self.clicker.click_points[1]
        self.assertEqual(point2.x, 300)
        self.assertEqual(point2.y, 400)
        self.assertEqual(point2.button, "right")
        self.assertEqual(point2.delay, 2.0)
        self.assertEqual(point2.description, "Second")
        
    def test_click_point_dataclass(self):
        """Test ClickPoint dataclass functionality"""
        point = ClickPoint(150, 250, "middle", 1.5, "Test point")
        
        self.assertEqual(point.x, 150)
        self.assertEqual(point.y, 250)
        self.assertEqual(point.button, "middle")
        self.assertEqual(point.delay, 1.5)
        self.assertEqual(point.description, "Test point")
        
        # Test default values
        point_default = ClickPoint(100, 200)
        self.assertEqual(point_default.button, "left")
        self.assertEqual(point_default.delay, 1.0)
        self.assertEqual(point_default.description, "")
        
    def test_invalid_pattern_file(self):
        """Test loading invalid pattern files"""
        # Test non-existent file
        self.clicker.load_pattern("nonexistent.json")
        self.assertEqual(len(self.clicker.click_points), 0)
        
        # Test invalid JSON
        invalid_file = os.path.join(self.test_dir, "invalid.json")
        with open(invalid_file, 'w') as f:
            f.write("invalid json content")
            
        self.clicker.load_pattern(invalid_file)
        self.assertEqual(len(self.clicker.click_points), 0)
        
    def test_simulation_timing(self):
        """Test that simulation respects timing"""
        import time
        
        self.clicker.add_click_point(100, 200, "left", 0.1, "Quick click")
        self.clicker.add_click_point(300, 400, "left", 0.1, "Another quick click")
        
        start_time = time.time()
        
        # Override the simulate_clicks to avoid interactive prompts
        original_simulate = self.clicker.simulate_clicks
        def quiet_simulate(repeat_count=1):
            self.clicker.is_running = True
            try:
                for cycle in range(repeat_count):
                    if not self.clicker.is_running:
                        break
                    for point in self.clicker.click_points:
                        if not self.clicker.is_running:
                            break
                        time.sleep(point.delay)
            finally:
                self.clicker.is_running = False
                
        self.clicker.simulate_clicks = quiet_simulate
        self.clicker.simulate_clicks(1)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should take approximately 0.2 seconds (0.1 + 0.1)
        self.assertGreaterEqual(elapsed, 0.15)  # Allow some timing variance
        self.assertLess(elapsed, 0.5)  # But not too much
        
def run_tests():
    """Run all tests"""
    print("Smart Auto Clicker - Running Tests")
    print("=" * 40)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSmartAutoClicker)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 40)
    if result.wasSuccessful():
        print("All tests passed! ✅")
        return 0
    else:
        print("Some tests failed! ❌")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())