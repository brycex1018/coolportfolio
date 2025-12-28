# Screen Clipper - Installation & Usage Guide

A lightweight 24/7 screen recording tool that keeps a rolling buffer of your screen activity and lets you save clips on demand with a hotkey.

## Quick Start

### Installation

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Basic Usage

1. **Start Recording**: Run `python main.py` - it will start recording in the background
2. **Save Clip**: Press `F9` to save the last 5 minutes (configurable)
3. **Stop Recording**: Press `ESC` or close the system tray icon
4. **Find Clips**: Check the `clips/` folder in the application directory

## Configuration

Edit `config.toml` to customize settings:

```toml
[recording]
fps = 30                    # Frame rate (15-60)
buffer_duration_minutes = 5 # How much to keep in buffer (1-1440)
resolution_scale = 1.0      # 1.0 = full res, 0.5 = half

[keybinds]
save_clip = "f9"           # Key to save clip
pause_recording = "f8"      # Key to pause/resume
```

## System Requirements

- **RAM**: 1GB minimum, 2GB recommended
- **Storage**: 100MB - 10GB depending on buffer size
- **CPU**: Dual-core processor recommended
- **OS**: Windows 10+, macOS 10.14+, Linux (X11)

## Features

- ✅ Continuous background recording
- ✅ Circular buffer (no disk space waste)
- ✅ Custom keybind support
- ✅ Low CPU/memory usage
- ✅ System tray integration
- ✅ Auto-start on boot (optional)
- ✅ Multiple monitor support

## Troubleshooting

### "Permission Denied" on Linux/macOS
```bash
sudo python main.py
```

### High CPU Usage
- Reduce FPS in config (e.g., 15 fps)
- Lower resolution_scale (e.g., 0.5)
- Reduce buffer duration

### Keybind Not Working
- Make sure app is running as administrator (Windows)
- Check if another app is using the same keybind
- Try a different key in config.toml

## Advanced Usage

### Auto-start on Boot

**Windows:**
1. Press `Win + R`, type `shell:startup`
2. Create a shortcut to `main.py` in the startup folder

**macOS:**
```bash
# Create launch agent
cp screen-clipper.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/screen-clipper.plist
```

**Linux:**
```bash
# Create systemd service
sudo cp screen-clipper.service /etc/systemd/system/
sudo systemctl enable screen-clipper
sudo systemctl start screen-clipper
```

### Record Specific Region

Edit `main.py` and modify the monitor selection:
```python
# Record specific region
monitor = {
    "top": 100,
    "left": 100, 
    "width": 1920,
    "height": 1080
}
```

### Change Output Format

In `encoder.py`, change the codec:
```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4
# or
fourcc = cv2.VideoWriter_fourcc(*'H264')  # H.264 (better quality)
```

## Performance Tips

1. **Optimize for your use case:**
   - Gaming/action: 30 fps, full resolution
   - General use: 15 fps, 0.75 scale
   - Monitoring only: 5 fps, 0.5 scale

2. **Buffer management:**
   - Short term (< 5 min): Store in RAM
   - Long term (> 5 min): Consider disk buffer

3. **Use SSD for better performance**

## Privacy & Security

- All recordings are stored locally
- No data is sent to external servers
- Clear buffer with `Ctrl+Shift+F9`
- Configure auto-pause for sensitive apps in config

## Building Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico main.py

# Find executable in dist/ folder
```

## License

MIT License - See LICENSE file

## Contributing

Pull requests welcome! Please read CONTRIBUTING.md first.

## Support

- Report issues: [GitHub Issues](https://github.com/brycex1018/coolportfolio/issues)
- Documentation: See SCREEN_CLIPPER_PLAN.md
- Contact: Check portfolio for contact info
