# Screen Clipper - Feature Comparison & Use Cases

## Version Comparison

| Feature | Simple (`main.py`) | Advanced (`main_advanced.py`) |
|---------|-------------------|-------------------------------|
| Screen Recording | ✅ | ✅ |
| Circular Buffer | ✅ | ✅ |
| Hotkey Clip Save | ✅ (F9) | ✅ (Configurable) |
| Pause/Resume | ✅ (F8) | ✅ (Configurable) |
| Configuration File | ❌ | ✅ (TOML) |
| Logging | ❌ | ✅ (File + Console) |
| Auto-cleanup Old Clips | ❌ | ✅ |
| Resolution Scaling | ❌ | ✅ |
| Custom Output Directory | ❌ | ✅ |
| Monitor Selection | Primary only | ✅ Configurable |
| Debug Mode | ❌ | ✅ |
| Status Display | Basic | Enhanced |
| Code Size | ~200 lines | ~350 lines |
| Complexity | Beginner | Intermediate |

## Use Cases

### 🎮 Gaming Highlights
**Best for:** Saving epic gaming moments

**Configuration:**
```toml
[recording]
fps = 30
buffer_duration_minutes = 3
resolution_scale = 1.0
```

**Why:** High FPS and full resolution for quality. Short buffer for recent action.

### 💼 Work/Tutorial Recording
**Best for:** Documenting work processes, creating tutorials

**Configuration:**
```toml
[recording]
fps = 15
buffer_duration_minutes = 10
resolution_scale = 0.75
```

**Why:** Lower FPS saves resources. Longer buffer captures more context.

### 🔍 Bug Reproduction
**Best for:** Capturing bugs/issues for developers

**Configuration:**
```toml
[recording]
fps = 20
buffer_duration_minutes = 5
resolution_scale = 1.0
```

**Why:** Balanced quality and duration. Full resolution for clarity.

### 📊 Long-term Monitoring
**Best for:** Activity monitoring, time tracking

**Configuration:**
```toml
[recording]
fps = 5
buffer_duration_minutes = 30
resolution_scale = 0.5
```

**Why:** Very low FPS and resolution. Long buffer without high storage.

### 🎨 Creative Content
**Best for:** Content creators recording streams/videos

**Configuration:**
```toml
[recording]
fps = 30
buffer_duration_minutes = 5
resolution_scale = 1.0
codec = "H264"
```

**Why:** High quality capture with better codec. Medium buffer.

## Performance Comparison

### 1080p Recording (1920x1080)

| FPS | Scale | Buffer | RAM Usage | CPU Usage | Example Use |
|-----|-------|--------|-----------|-----------|-------------|
| 30 | 1.0 | 5 min | ~800 MB | 8-12% | Gaming |
| 30 | 0.75 | 10 min | ~600 MB | 6-10% | Streaming |
| 20 | 1.0 | 5 min | ~550 MB | 5-8% | Tutorials |
| 15 | 0.75 | 10 min | ~400 MB | 4-6% | Work |
| 10 | 0.5 | 30 min | ~300 MB | 3-5% | Monitoring |
| 5 | 0.5 | 60 min | ~200 MB | 2-3% | Long-term |

### 4K Recording (3840x2160)

| FPS | Scale | Buffer | RAM Usage | CPU Usage | Example Use |
|-----|-------|--------|-----------|-----------|-------------|
| 30 | 0.5 | 3 min | ~1.2 GB | 10-15% | Gaming (scaled to 1080p) |
| 20 | 0.5 | 5 min | ~800 MB | 8-12% | Content creation |
| 15 | 0.33 | 10 min | ~600 MB | 6-9% | Work (scaled to 1280x720) |

## Storage Estimates

### Clip File Sizes (MP4, medium quality)

| Resolution | Duration | Approx. Size |
|-----------|----------|--------------|
| 1920x1080 | 1 min | 15-20 MB |
| 1920x1080 | 5 min | 75-100 MB |
| 1920x1080 | 10 min | 150-200 MB |
| 1280x720 | 1 min | 8-12 MB |
| 1280x720 | 5 min | 40-60 MB |
| 1280x720 | 10 min | 80-120 MB |
| 3840x2160 | 1 min | 50-70 MB |
| 3840x2160 | 5 min | 250-350 MB |

### Disk Space Planning

For `max_clips = 100`:
- At 1080p, 5 min clips: ~10 GB
- At 720p, 5 min clips: ~5 GB
- At 1080p, 10 min clips: ~20 GB

## Optimization Strategies

### Memory-Constrained Systems
```toml
[recording]
fps = 15
buffer_duration_minutes = 3
resolution_scale = 0.5

[performance]
memory_limit_mb = 512
```

### High-Performance Systems
```toml
[recording]
fps = 60
buffer_duration_minutes = 10
resolution_scale = 1.0

[performance]
use_gpu = true
quality = 9
```

### Battery-Powered Devices
```toml
[recording]
fps = 10
buffer_duration_minutes = 5
resolution_scale = 0.5

[advanced]
motion_detection = true
```

## Keyboard Shortcuts

### Default Shortcuts

| Key | Action | Customizable |
|-----|--------|--------------|
| F9 | Save clip | ✅ |
| F8 | Pause/Resume | ✅ |
| ESC | Exit | ✅ |

### Custom Shortcut Examples

```toml
[keybinds]
save_clip = "f10"
pause_recording = "ctrl+shift+p"
exit_app = "ctrl+shift+q"
```

## Command Line Options

### Simple Version
```bash
# Run with default settings
python main.py

# Run in foreground (see all output)
python main.py 2>&1 | tee recording.log
```

### Advanced Version
```bash
# Run with default config
python main_advanced.py

# Run with custom config
python main_advanced.py --config custom_config.toml

# Run with debug logging
python main_advanced.py --debug
```

## Integration Examples

### Run on Startup (Windows)

1. Create a batch file `start_clipper.bat`:
```batch
@echo off
cd C:\path\to\screen-clipper
python main.py
```

2. Place shortcut in: `shell:startup`

### Run on Startup (macOS)

Create `~/Library/LaunchAgents/com.screenclipper.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screenclipperpy</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/screen-clipper/main.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Run on Startup (Linux)

Create `~/.config/autostart/screen-clipper.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Screen Clipper
Exec=/usr/bin/python3 /path/to/screen-clipper/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## Troubleshooting Guide

### Issue: High CPU Usage

**Solutions:**
1. Reduce FPS: `fps = 15`
2. Lower resolution: `resolution_scale = 0.5`
3. Reduce buffer: `buffer_duration_minutes = 3`
4. Enable motion detection: `motion_detection = true`

### Issue: High Memory Usage

**Solutions:**
1. Reduce buffer duration
2. Lower resolution scale
3. Set memory limit: `memory_limit_mb = 512`

### Issue: Hotkey Not Working

**Solutions:**
1. Run as administrator (Windows)
2. Check if another app uses the same key
3. Try a different key combination
4. Check keyboard listener permissions

### Issue: Poor Video Quality

**Solutions:**
1. Increase FPS: `fps = 30`
2. Use full resolution: `resolution_scale = 1.0`
3. Better codec: `codec = "H264"`
4. Increase quality: `quality = 9`

### Issue: Clips Not Saving

**Solutions:**
1. Check output directory exists
2. Verify write permissions
3. Ensure enough disk space
4. Check codec support

## Advanced Features (Future)

### Planned Enhancements
- [ ] Audio capture support
- [ ] GPU-accelerated encoding
- [ ] Cloud upload integration
- [ ] Multiple monitor selection
- [ ] Region-specific recording
- [ ] Watermark support
- [ ] Variable FPS (based on activity)
- [ ] Preview window
- [ ] Clip trimming interface
- [ ] Automatic highlight detection

### Community Contributions Welcome!
Feel free to fork and extend with new features.

## FAQ

**Q: Can I record audio?**  
A: Not yet. This is planned for a future version.

**Q: Does it work on multiple monitors?**  
A: Yes, configure `monitor_index` in config.toml.

**Q: How much disk space do I need?**  
A: Depends on buffer + max clips. ~5-20 GB is typical.

**Q: Is it legal to record my screen?**  
A: Yes, for personal use. Follow local laws for recording others.

**Q: Can I upload clips automatically?**  
A: Not built-in. You can add a script to watch the clips folder.

**Q: Does it affect gaming performance?**  
A: Minimal impact at 15-30 FPS. Test and adjust as needed.

**Q: Can I run multiple instances?**  
A: Yes, but change output directories to avoid conflicts.

**Q: Is there a GUI?**  
A: Not yet. Command line only. GUI planned for future.

---

For more information, see:
- Full documentation: `README.md`
- Quick start: `QUICKSTART.md`
- Planning doc: `SCREEN_CLIPPER_PLAN.md`
