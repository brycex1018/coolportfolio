# Screen Clipper - Example Output

## Terminal Output Examples

### Starting the Application

```
$ python main.py

================================================================================
🎥 Screen Clipper - 24/7 Background Screen Recorder
================================================================================

⚙️  Configuration:
   • FPS: 30
   • Buffer Duration: 5 minutes (9,000 frames)
   • Output Directory: /home/user/coolportfolio/screen-clipper/clips

🎮 Controls:
   • F9: Save last 5 minutes
   • F8: Pause/Resume recording
   • ESC: Exit application

📝 Starting recording...

⏺️  Recording... | Buffer: 150s / 300s | Usage: 50% | Frames: 4,500 | Press F9 to save, F8 to pause, ESC to exit
```

### Saving a Clip

```
⏺️  Recording... | Buffer: 300s / 300s | Usage: 100% | Frames: 15,234 | Press F9 to save, F8 to pause, ESC to exit

🎬 Hotkey pressed! Saving last 5 minutes...
💾 Saving clip with 9000 frames (300 seconds)...
✅ Saved: clips/clip_20250128_142536.mp4 (156.8 MB)

⏺️  Recording... | Buffer: 15s / 300s | Usage: 5% | Frames: 15,684 | Press F9 to save, F8 to pause, ESC to exit
```

### Pausing Recording

```
⏺️  Recording... | Buffer: 120s / 300s | Usage: 40% | Frames: 3,600 | Press F9 to save, F8 to pause, ESC to exit

⏸️  PAUSED

[Recording paused - no new frames captured]

▶️  RESUMED

⏺️  Recording... | Buffer: 5s / 300s | Usage: 2% | Frames: 3,750 | Press F9 to save, F8 to pause, ESC to exit
```

### Stopping the Application

```
⏺️  Recording... | Buffer: 280s / 300s | Usage: 93% | Frames: 8,400 | Press F9 to save, F8 to pause, ESC to exit

🛑 Stopping...

================================================================================
📊 Session Summary:
   • Total frames captured: 8,400
   • Recording duration: 4.7 minutes
   • Clips saved to: /home/user/coolportfolio/screen-clipper/clips
================================================================================

👋 Screen Clipper stopped. Goodbye!
```

## Advanced Version Output

```
$ python main_advanced.py

================================================================================
🎥 Screen Clipper - Advanced 24/7 Background Screen Recorder
================================================================================

✅ Configuration loaded from config.toml

⚙️  Configuration:
   • FPS: 30
   • Buffer Duration: 10 minutes (18,000 frames)
   • Resolution Scale: 0.75x
   • Codec: mp4v
   • Output Directory: /home/user/clips
   • Max Clips: 100

🎮 Controls:
   • F9: Save last 10 minutes
   • F8: Pause/Resume recording
   • ESC: Exit application

📝 Starting recording...

⏺️  Recording... | Buffer: 600s / 600s | Usage: 100% | Frames: 18,000 | Clips: 3 | Press F9 to save, F8 to pause, ESC to exit

🎬 Hotkey pressed! Saving last 10 minutes...
2025-01-28 14:35:21 [INFO] Saving clip with 18000 frames (600 seconds)...
2025-01-28 14:35:35 [INFO] ✅ Saved: /home/user/clips/clip_20250128_143521.mp4 (285.3 MB)
2025-01-28 14:35:35 [INFO] Deleted old clip: clip_20250127_091234.mp4

⏺️  Recording... | Buffer: 45s / 600s | Usage: 8% | Frames: 19,350 | Clips: 4 | Press F9 to save, F8 to pause, ESC to exit
```

## Clip File Structure

After running for a while, your clips directory looks like:

```
clips/
├── clip_20250128_140015.mp4  (156.8 MB)  - 5 min @ 1080p, 30fps
├── clip_20250128_141230.mp4  (145.2 MB)  - 5 min @ 1080p, 30fps
├── clip_20250128_142536.mp4  (158.4 MB)  - 5 min @ 1080p, 30fps
├── clip_20250128_143821.mp4  (152.7 MB)  - 5 min @ 1080p, 30fps
└── clip_20250128_145105.mp4  (149.9 MB)  - 5 min @ 1080p, 30fps

Total: 763.0 MB (5 clips)
```

## Configuration File Example

Your `config.toml` after customization:

```toml
[recording]
fps = 25                    # Reduced from 30 for efficiency
buffer_duration_minutes = 8 # Extended from 5 for more context
resolution_scale = 0.8      # Slight reduction for better performance
codec = "H264"              # Better quality codec

[keybinds]
save_clip = "f10"          # Changed from F9
pause_recording = "f9"      # Swapped with save
exit_app = "ctrl+shift+q"   # More intentional exit

[storage]
output_directory = "D:/MyClips"  # Custom location
filename_format = "recording_%Y%m%d_%H%M%S.mp4"
max_clips = 50              # Keep last 50 clips only

[performance]
quality = 8                 # Higher quality
memory_limit_mb = 2048      # 2GB limit

[monitor]
monitor_index = 2           # Secondary monitor

[advanced]
capture_cursor = true
motion_detection = false
debug_mode = true
```

## Log File Output (Advanced Version)

Content of `screen_clipper.log`:

```
2025-01-28 14:25:10 [INFO] Starting Screen Clipper v1.0
2025-01-28 14:25:10 [INFO] Configuration loaded successfully
2025-01-28 14:25:10 [INFO] Recording started - Buffer: 10 minutes (18000 frames)
2025-01-28 14:25:10 [INFO] Keyboard listener started
2025-01-28 14:30:15 [INFO] Hotkey pressed! Saving last 10 minutes...
2025-01-28 14:30:15 [INFO] Saving clip with 18000 frames (600 seconds)...
2025-01-28 14:30:28 [INFO] ✅ Saved: /home/user/clips/clip_20250128_143015.mp4 (285.3 MB)
2025-01-28 14:35:21 [INFO] Hotkey pressed! Saving last 10 minutes...
2025-01-28 14:35:21 [INFO] Saving clip with 18000 frames (600 seconds)...
2025-01-28 14:35:35 [INFO] ✅ Saved: /home/user/clips/clip_20250128_143521.mp4 (285.3 MB)
2025-01-28 14:35:35 [INFO] Deleted old clip: clip_20250127_091234.mp4
2025-01-28 14:40:12 [INFO] Pause requested
2025-01-28 14:40:12 [INFO] Recording paused
2025-01-28 14:42:05 [INFO] Resume requested
2025-01-28 14:42:05 [INFO] Recording resumed
2025-01-28 14:50:00 [INFO] Exit requested
2025-01-28 14:50:00 [INFO] Stopping Screen Clipper...
2025-01-28 14:50:00 [INFO] Session statistics:
2025-01-28 14:50:00 [INFO]   - Total frames: 45,000
2025-01-28 14:50:00 [INFO]   - Duration: 25.0 minutes
2025-01-28 14:50:00 [INFO]   - Clips saved: 3
2025-01-28 14:50:00 [INFO] Screen Clipper stopped successfully
```

## System Resource Monitor

### During Recording (Task Manager / Activity Monitor)

```
Process: python main.py
CPU: 7.2%
Memory: 642 MB
Disk: Write ~15 MB/s (when saving)
Network: 0 KB/s
```

### Breakdown by Component

| Component | CPU % | Memory |
|-----------|-------|--------|
| Screen Capture | 3-4% | 100 MB |
| Buffer Storage | 1-2% | 500 MB |
| Video Encoding | 2-3% | 30 MB |
| Hotkey Listener | <1% | 10 MB |
| **Total** | **7-10%** | **640 MB** |

## Clip Playback

Playing a saved clip in VLC Media Player:

```
File: clip_20250128_142536.mp4
Resolution: 1920x1080
FPS: 30
Duration: 5:00
Bitrate: ~4200 kbps
Codec: MPEG-4 (mp4v)
Size: 156.8 MB
```

## Error Examples

### Missing Dependencies

```
$ python main.py

Traceback (most recent call last):
  File "main.py", line 8, in <module>
    from mss import mss
ModuleNotFoundError: No module named 'mss'

Solution:
$ pip install -r requirements.txt
```

### Permission Denied (Linux)

```
$ python main.py

❌ Error: Permission denied to capture screen

Solution:
$ sudo python main.py
# or configure screen capture permissions
```

### Disk Full

```
⏺️  Recording... | Buffer: 300s / 300s | Usage: 100% | Frames: 9,000

🎬 Hotkey pressed! Saving last 5 minutes...
💾 Saving clip with 9000 frames (300 seconds)...
❌ Error saving clip: [Errno 28] No space left on device

Solution: Free up disk space or reduce buffer/max_clips
```

## Success Stories

### Gaming Highlight Capture
```
🎮 Saved epic Valorant ace!
File: clip_20250128_203015.mp4
Size: 82.4 MB (90 seconds at 1080p/30fps)
```

### Bug Reproduction
```
🐛 Captured software bug for dev team
File: clip_20250128_151234.mp4
Size: 156.8 MB (5 minutes showing full bug scenario)
```

### Tutorial Recording
```
📚 Recorded coding tutorial
File: clip_20250128_103045.mp4
Size: 312.5 MB (10 minutes at 1080p/25fps)
```

---

**These examples show realistic usage patterns and outputs from the Screen Clipper application.**
