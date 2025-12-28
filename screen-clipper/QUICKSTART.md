# Quick Start Guide - Screen Clipper

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- 2GB RAM minimum
- Windows 10+, macOS 10.14+, or Linux

## Installation Steps

### 1. Download or Clone

```bash
# If you have this as part of a repository
cd screen-clipper

# Or download the files directly
```

### 2. Install Dependencies

```bash
# On Windows
python -m pip install -r requirements.txt

# On macOS/Linux
python3 -m pip install -r requirements.txt
```

### 3. Run the Application

**Simple version (beginner-friendly):**
```bash
python main.py
```

**Advanced version (with config support):**
```bash
python main_advanced.py
```

### 4. Use It!

1. The app starts recording automatically in the background
2. Press **F9** to save the last 5 minutes to a video file
3. Find your clips in the `clips/` folder
4. Press **ESC** to exit

## Common Issues & Solutions

### Issue: "Module not found" error

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Permission denied on Linux/macOS

**Solution:**
```bash
sudo python3 main.py
```

Or give your user permission to capture screen:
```bash
# macOS
# System Preferences > Security & Privacy > Screen Recording

# Linux (X11)
xhost +local:
```

### Issue: High CPU usage

**Solution:** Edit `config.toml`:
```toml
[recording]
fps = 15              # Reduce from 30 to 15
resolution_scale = 0.5  # Record at half resolution
```

### Issue: Videos won't play

**Solution:** Install codec pack or try VLC player
- Windows: K-Lite Codec Pack
- macOS/Linux: VLC Media Player

## Customization

### Change Buffer Duration

Edit `main.py` line 17:
```python
BUFFER_MINUTES = 10  # Change from 5 to 10 minutes
```

Or in `config.toml`:
```toml
[recording]
buffer_duration_minutes = 10
```

### Change Hotkey

Edit `main.py` line 18:
```python
SAVE_HOTKEY = keyboard.Key.f10  # Change from F9 to F10
```

Or in `config.toml`:
```toml
[keybinds]
save_clip = "f10"
```

### Change Output Location

Edit `config.toml`:
```toml
[storage]
output_directory = "C:/MyClips"  # Windows
# or
output_directory = "~/Videos/Clips"  # macOS/Linux
```

## Performance Optimization

### For Gaming (High Quality)
```toml
[recording]
fps = 30
resolution_scale = 1.0
buffer_duration_minutes = 3
```

### For General Use (Balanced)
```toml
[recording]
fps = 20
resolution_scale = 0.75
buffer_duration_minutes = 5
```

### For Long Recording (Efficiency)
```toml
[recording]
fps = 10
resolution_scale = 0.5
buffer_duration_minutes = 15
```

## Next Steps

1. **Test it:** Record for a few minutes, press F9, check the `clips/` folder
2. **Customize:** Edit `config.toml` to match your needs
3. **Auto-start:** See README.md for instructions to run on boot
4. **Build executable:** See README.md to create a standalone .exe file

## Getting Help

- Check the full documentation: `SCREEN_CLIPPER_PLAN.md`
- Read the detailed README: `README.md`
- Report issues on GitHub

## Tips for Best Results

1. **Close unnecessary apps** before recording to save resources
2. **Use an SSD** for better write performance
3. **Monitor your disk space** - a 5-min buffer at 1080p = ~200MB RAM
4. **Test different FPS settings** to find your sweet spot
5. **Record at lower resolution** if you don't need full quality

---

**Enjoy your Screen Clipper!** 🎥✨
