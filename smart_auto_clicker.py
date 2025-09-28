#!/usr/bin/env python3
"""
Smart Auto Clicker - An intelligent auto-clicking application
"""

import sys
import os
import threading
import time
import json
from typing import List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Check for required dependencies and provide fallbacks
DEPENDENCIES_AVAILABLE = {
    'tkinter': False,
    'pyautogui': False,
    'pynput': False,
    'keyboard': False,
    'pillow': False
}

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    DEPENDENCIES_AVAILABLE['tkinter'] = True
except ImportError:
    print("Warning: tkinter not available. GUI functionality disabled.")

try:
    import pyautogui
    DEPENDENCIES_AVAILABLE['pyautogui'] = True
except ImportError:
    print("Warning: pyautogui not available. Actual clicking disabled (simulation mode only).")

try:
    from pynput import mouse
    DEPENDENCIES_AVAILABLE['pynput'] = True
except ImportError:
    print("Warning: pynput not available. Mouse event recording disabled.")

try:
    import keyboard
    DEPENDENCIES_AVAILABLE['keyboard'] = True
except ImportError:
    print("Warning: keyboard not available. Global hotkeys disabled.")

try:
    from PIL import Image
    DEPENDENCIES_AVAILABLE['pillow'] = True
except ImportError:
    print("Warning: Pillow not available. Screenshot functionality may be limited.")

@dataclass
class ClickPoint:
    """Represents a click point with position and timing"""
    x: int
    y: int
    button: str = "left"
    delay: float = 1.0
    description: str = ""

class SmartAutoClicker:
    """Main application class for the Smart Auto Clicker"""
    
    def __init__(self):
        if not DEPENDENCIES_AVAILABLE['tkinter']:
            raise ImportError("tkinter is required for GUI mode. Use CLI mode instead: python3 cli_auto_clicker.py")
            
        self.root = tk.Tk()
        self.root.title("Smart Auto Clicker")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Application state
        self.is_recording = False
        self.is_clicking = False
        self.click_points: List[ClickPoint] = []
        self.current_position = (0, 0)
        self.click_thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Settings
        self.repeat_count = tk.IntVar(value=1)
        self.repeat_forever = tk.BooleanVar(value=False)
        self.click_delay = tk.DoubleVar(value=1.0)
        self.hotkey_record = tk.StringVar(value="F9")
        self.hotkey_start_stop = tk.StringVar(value="F10")
        
        self.setup_ui()
        self.setup_hotkeys()
        
        # Update mouse position display
        self.update_mouse_position()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Mouse position display
        ttk.Label(main_frame, text="Current Mouse Position:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.position_label = ttk.Label(main_frame, text="(0, 0)", font=("Courier", 12))
        self.position_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Recording section
        recording_frame = ttk.LabelFrame(main_frame, text="Recording", padding="10")
        recording_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        recording_frame.columnconfigure(1, weight=1)
        
        self.record_button = ttk.Button(recording_frame, text="Start Recording (F9)", 
                                       command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, pady=5)
        
        ttk.Label(recording_frame, text="Click delay (seconds):").grid(row=0, column=1, sticky=tk.E, padx=10)
        delay_spinbox = ttk.Spinbox(recording_frame, from_=0.1, to=10.0, increment=0.1, 
                                   width=10, textvariable=self.click_delay)
        delay_spinbox.grid(row=0, column=2, pady=5)
        
        # Click points list
        points_frame = ttk.LabelFrame(main_frame, text="Recorded Click Points", padding="10")
        points_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        points_frame.columnconfigure(0, weight=1)
        points_frame.rowconfigure(0, weight=1)
        
        # Treeview for click points
        self.points_tree = ttk.Treeview(points_frame, columns=("position", "button", "delay", "description"), 
                                       show="headings", height=8)
        self.points_tree.heading("position", text="Position")
        self.points_tree.heading("button", text="Button")
        self.points_tree.heading("delay", text="Delay (s)")
        self.points_tree.heading("description", text="Description")
        
        self.points_tree.column("position", width=100)
        self.points_tree.column("button", width=80)
        self.points_tree.column("delay", width=80)
        self.points_tree.column("description", width=200)
        
        self.points_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        points_scrollbar = ttk.Scrollbar(points_frame, orient=tk.VERTICAL, command=self.points_tree.yview)
        points_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.points_tree.configure(yscrollcommand=points_scrollbar.set)
        
        # Control buttons for points
        points_buttons_frame = ttk.Frame(points_frame)
        points_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(points_buttons_frame, text="Clear All", command=self.clear_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(points_buttons_frame, text="Delete Selected", command=self.delete_selected_point).pack(side=tk.LEFT, padx=5)
        ttk.Button(points_buttons_frame, text="Edit Selected", command=self.edit_selected_point).pack(side=tk.LEFT, padx=5)
        
        # Playback section
        playback_frame = ttk.LabelFrame(main_frame, text="Playback", padding="10")
        playback_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        playback_frame.columnconfigure(1, weight=1)
        
        # Repeat options
        ttk.Label(playback_frame, text="Repeat:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        repeat_frame = ttk.Frame(playback_frame)
        repeat_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Checkbutton(repeat_frame, text="Forever", variable=self.repeat_forever).pack(side=tk.LEFT)
        
        ttk.Label(repeat_frame, text="Times:").pack(side=tk.LEFT, padx=(20, 5))
        repeat_spinbox = ttk.Spinbox(repeat_frame, from_=1, to=1000, width=10, 
                                    textvariable=self.repeat_count)
        repeat_spinbox.pack(side=tk.LEFT)
        
        # Control buttons
        controls_frame = ttk.Frame(playback_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(controls_frame, text="Start Clicking (F10)", 
                                      command=self.toggle_clicking)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="Save Pattern", command=self.save_pattern).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Load Pattern", command=self.load_pattern).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def setup_hotkeys(self):
        """Set up global hotkeys"""
        if not DEPENDENCIES_AVAILABLE['keyboard']:
            self.status_label.config(text="Global hotkeys not available (keyboard package missing)")
            return
            
        def on_hotkey_record():
            self.root.after(0, self.toggle_recording)
            
        def on_hotkey_start_stop():
            self.root.after(0, self.toggle_clicking)
        
        try:
            # Set up keyboard listener for hotkeys
            self.keyboard_listener = keyboard.GlobalHotKeys({
                '<f9>': on_hotkey_record,
                '<f10>': on_hotkey_start_stop
            })
            self.keyboard_listener.start()
        except Exception as e:
            print(f"Warning: Could not set up global hotkeys: {e}")
        
    def update_mouse_position(self):
        """Update the current mouse position display"""
        if not DEPENDENCIES_AVAILABLE['pyautogui']:
            self.position_label.config(text="(pyautogui not available)")
            self.root.after(1000, self.update_mouse_position)  # Check less frequently
            return
            
        try:
            x, y = pyautogui.position()
            self.current_position = (x, y)
            self.position_label.config(text=f"({x}, {y})")
        except:
            self.position_label.config(text="(position unavailable)")
        
        # Schedule next update
        self.root.after(50, self.update_mouse_position)
        
    def toggle_recording(self):
        """Toggle click recording mode"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
            
    def start_recording(self):
        """Start recording mouse clicks"""
        if not DEPENDENCIES_AVAILABLE['pynput']:
            messagebox.showerror("Error", "Mouse recording requires pynput package. Please install: pip install pynput")
            return
            
        self.is_recording = True
        self.record_button.config(text="Stop Recording (F9)")
        self.status_label.config(text="Recording clicks... Press F9 to stop")
        
        def on_click(x, y, button, pressed):
            if pressed and self.is_recording:
                click_point = ClickPoint(
                    x=x, y=y,
                    button=button.name,
                    delay=self.click_delay.get(),
                    description=f"Click at {x}, {y}"
                )
                self.click_points.append(click_point)
                self.root.after(0, self.update_points_tree)
        
        try:
            self.mouse_listener = mouse.Listener(on_click=on_click)
            self.mouse_listener.start()
        except Exception as e:
            self.is_recording = False
            self.record_button.config(text="Start Recording (F9)")
            messagebox.showerror("Error", f"Failed to start recording: {e}")
        
    def stop_recording(self):
        """Stop recording mouse clicks"""
        self.is_recording = False
        self.record_button.config(text="Start Recording (F9)")
        self.status_label.config(text="Recording stopped")
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
    def update_points_tree(self):
        """Update the points tree view"""
        # Clear existing items
        for item in self.points_tree.get_children():
            self.points_tree.delete(item)
            
        # Add current points
        for i, point in enumerate(self.click_points):
            self.points_tree.insert("", "end", values=(
                f"({point.x}, {point.y})",
                point.button,
                f"{point.delay:.1f}",
                point.description
            ))
            
    def clear_points(self):
        """Clear all recorded points"""
        if messagebox.askyesno("Confirm", "Clear all recorded points?"):
            self.click_points.clear()
            self.update_points_tree()
            self.status_label.config(text="All points cleared")
            
    def delete_selected_point(self):
        """Delete the selected point"""
        selection = self.points_tree.selection()
        if selection:
            index = self.points_tree.index(selection[0])
            del self.click_points[index]
            self.update_points_tree()
            self.status_label.config(text="Point deleted")
        else:
            messagebox.showwarning("Warning", "No point selected")
            
    def edit_selected_point(self):
        """Edit the selected point"""
        selection = self.points_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "No point selected")
            return
            
        index = self.points_tree.index(selection[0])
        point = self.click_points[index]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Click Point")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="X Position:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        x_var = tk.IntVar(value=point.x)
        ttk.Entry(dialog, textvariable=x_var, width=10).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Y Position:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        y_var = tk.IntVar(value=point.y)
        ttk.Entry(dialog, textvariable=y_var, width=10).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Delay (s):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        delay_var = tk.DoubleVar(value=point.delay)
        ttk.Entry(dialog, textvariable=delay_var, width=10).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        desc_var = tk.StringVar(value=point.description)
        ttk.Entry(dialog, textvariable=desc_var, width=20).grid(row=3, column=1, padx=10, pady=5)
        
        def save_changes():
            self.click_points[index] = ClickPoint(
                x=x_var.get(),
                y=y_var.get(),
                button=point.button,
                delay=delay_var.get(),
                description=desc_var.get()
            )
            self.update_points_tree()
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_changes).grid(row=4, column=0, pady=20)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=4, column=1, pady=20)
        
    def toggle_clicking(self):
        """Toggle auto-clicking mode"""
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
            
    def start_clicking(self):
        """Start the auto-clicking process"""
        if not self.click_points:
            messagebox.showwarning("Warning", "No click points recorded")
            return
            
        self.is_clicking = True
        self.start_button.config(text="Stop Clicking (F10)")
        self.status_label.config(text="Auto-clicking in progress...")
        
        # Start clicking in a separate thread
        self.click_thread = threading.Thread(target=self._click_worker)
        self.click_thread.daemon = True
        self.click_thread.start()
        
    def stop_clicking(self):
        """Stop the auto-clicking process"""
        self.is_clicking = False
        self.start_button.config(text="Start Clicking (F10)")
        self.status_label.config(text="Auto-clicking stopped")
        
    def _click_worker(self):
        """Worker method for performing clicks"""
        try:
            repeat_count = float('inf') if self.repeat_forever.get() else self.repeat_count.get()
            current_repeat = 0
            
            while self.is_clicking and current_repeat < repeat_count:
                for point in self.click_points:
                    if not self.is_clicking:
                        break
                    
                    if DEPENDENCIES_AVAILABLE['pyautogui']:
                        # Perform the actual click
                        if point.button == "left":
                            pyautogui.click(point.x, point.y)
                        elif point.button == "right":
                            pyautogui.rightClick(point.x, point.y)
                        elif point.button == "middle":
                            pyautogui.middleClick(point.x, point.y)
                    else:
                        # Simulation mode
                        print(f"Simulating {point.button} click at ({point.x}, {point.y})")
                        
                    # Wait for the specified delay
                    if self.is_clicking:
                        time.sleep(point.delay)
                        
                current_repeat += 1
                
        except Exception as e:
            print(f"Error during clicking: {e}")
        finally:
            # Update UI in main thread
            self.root.after(0, self.stop_clicking)
            
    def save_pattern(self):
        """Save the current click pattern to a file"""
        if not self.click_points:
            messagebox.showwarning("Warning", "No click points to save")
            return
            
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = {
                    "click_points": [asdict(point) for point in self.click_points],
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                    
                self.status_label.config(text=f"Pattern saved to {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save pattern: {e}")
                
    def load_pattern(self):
        """Load a click pattern from a file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    
                if "click_points" in data:
                    self.click_points = [
                        ClickPoint(**point_data) for point_data in data["click_points"]
                    ]
                    self.update_points_tree()
                    self.status_label.config(text=f"Pattern loaded from {os.path.basename(filename)}")
                else:
                    messagebox.showerror("Error", "Invalid pattern file format")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load pattern: {e}")
                
    def on_closing(self):
        """Handle application closing"""
        if self.is_clicking:
            self.stop_clicking()
        if self.is_recording:
            self.stop_recording()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        # Check if we should fallback to CLI mode
        if not DEPENDENCIES_AVAILABLE['tkinter']:
            print("GUI not available. Please install tkinter or use CLI mode:")
            print("python3 cli_auto_clicker.py")
            return 1
            
        # Show warnings for missing optional dependencies
        missing_deps = [dep for dep, available in DEPENDENCIES_AVAILABLE.items() 
                       if not available and dep != 'tkinter']
        
        if missing_deps:
            print(f"Warning: Some features may be limited due to missing dependencies: {', '.join(missing_deps)}")
            print("For full functionality, install: pip install -r requirements.txt")
            print()
        
        app = SmartAutoClicker()
        app.run()
        return 0
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nTrying fallback to CLI mode...")
        try:
            # Import and run CLI version as fallback
            from cli_auto_clicker import main as cli_main
            return cli_main()
        except ImportError:
            print("CLI fallback not available")
            return 1

if __name__ == "__main__":
    sys.exit(main() or 0)