# Smart Auto Clicker

A sophisticated auto-clicking application with intelligent recording and playback capabilities. This application allows you to record mouse click sequences and replay them with customizable timing and repetition settings.

## Features

- **Intuitive GUI**: Easy-to-use interface built with tkinter
- **Click Recording**: Record mouse clicks with automatic position detection
- **Smart Playback**: Replay recorded clicks with configurable timing
- **Flexible Repeat Options**: Run sequences once, multiple times, or indefinitely
- **Pattern Management**: Save and load click patterns for reuse
- **Global Hotkeys**: Control the application using F9 (record) and F10 (start/stop)
- **Real-time Position Display**: See current mouse coordinates in real-time
- **Click Point Editing**: Modify recorded click points after recording
- **Multi-button Support**: Support for left, right, and middle mouse buttons

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/chuongduong2810/smart-auto-clicker.git
cd smart-auto-clicker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python smart_auto_clicker.py
```

### Install as Package

```bash
pip install -e .
smart-auto-clicker
```

## Usage

### Getting Started

1. **Launch the application**:
   ```bash
   python smart_auto_clicker.py
   ```

2. **Record clicks**:
   - Click "Start Recording (F9)" or press F9
   - Click wherever you want to record click points
   - Press F9 again to stop recording

3. **Configure playback**:
   - Set the number of repetitions or choose "Forever"
   - Adjust individual click delays if needed

4. **Start auto-clicking**:
   - Click "Start Clicking (F10)" or press F10
   - Press F10 again to stop

### Advanced Features

#### Editing Click Points
- Select a click point in the list
- Click "Edit Selected" to modify position, delay, or description
- Use "Delete Selected" to remove unwanted points

#### Saving and Loading Patterns
- Use "Save Pattern" to save your click sequences to a JSON file
- Use "Load Pattern" to restore previously saved sequences
- Patterns include all click positions, timing, and settings

#### Global Hotkeys
- **F9**: Toggle recording mode (works even when app is not focused)
- **F10**: Start/stop auto-clicking (works even when app is not focused)

## Configuration

### Click Timing
- **Delay**: Time to wait after each click (0.1 to 10.0 seconds)
- **Individual Point Delays**: Each click point can have its own delay

### Repeat Options
- **Times**: Repeat the sequence a specific number of times
- **Forever**: Continuous repetition until manually stopped

## Safety Features

- Global hotkeys allow emergency stopping even when the application loses focus
- Threading ensures the GUI remains responsive during operation
- Automatic error handling prevents crashes during click execution

## Technical Details

### Dependencies
- **pynput**: Mouse and keyboard event handling
- **pyautogui**: Cross-platform GUI automation
- **pillow**: Image processing support
- **keyboard**: Global hotkey management
- **tkinter**: GUI framework (included with Python)

### File Formats
Click patterns are saved as JSON files with the following structure:
```json
{
  "click_points": [
    {
      "x": 100,
      "y": 200,
      "button": "left",
      "delay": 1.0,
      "description": "Click at 100, 200"
    }
  ],
  "created_at": "2025-01-01T12:00:00",
  "version": "1.0"
}
```

## Troubleshooting

### Common Issues

1. **"No module named 'pynput'"**
   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **Hotkeys not working**
   - Solution: Run the application as administrator (Windows) or with appropriate permissions (Linux/Mac)

3. **Clicks not registering**
   - Solution: Ensure the target application accepts programmatic clicks
   - Some security-focused applications may block automated input

4. **GUI not responding**
   - Solution: The clicking operations run in a separate thread, but very fast sequences might cause delays
   - Try increasing click delays or reducing repetition count

### Platform-Specific Notes

#### Windows
- May require administrator privileges for global hotkeys
- Windows Defender might flag the application as suspicious (false positive)

#### Linux
- Requires X11 display server
- May need additional permissions for input simulation
- Install: `sudo apt-get install python3-tk python3-dev`

#### macOS
- Requires accessibility permissions in System Preferences
- May need to allow the terminal or Python in Privacy settings

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is intended for legitimate automation purposes. Users are responsible for ensuring their use complies with applicable terms of service and laws. The developers are not responsible for any misuse of this software.
