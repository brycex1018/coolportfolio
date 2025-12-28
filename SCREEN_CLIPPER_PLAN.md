# Screen Clipper Software - Implementation Plan

## Overview
A 24/7 background application that continuously records your desktop/screen activity in a rolling buffer and allows you to save the last X minutes (up to 24 hours) with a custom keybind.

## Requirements
- ✅ Continuous screen recording in background
- ✅ Rolling buffer (5-10 minutes recommended, up to 24 hours possible)
- ✅ Custom keybind to save/clip recent footage
- ✅ Optimized performance (low CPU/memory usage)
- ✅ 24/7 operation capability
- ✅ Cross-platform support (Windows, macOS, Linux)

---

## Technical Architecture

### Core Components

1. **Screen Capture Module**
   - Captures screen frames continuously
   - Efficient frame grabbing with minimal CPU overhead
   - Configurable FPS (15-30 fps recommended for balance)

2. **Circular Buffer Manager**
   - Stores frames in memory/disk in a circular buffer
   - Auto-overwrites oldest frames when buffer is full
   - Configurable buffer size (5 min - 24 hours)

3. **Keybind Handler**
   - Global hotkey registration
   - Detects custom keybind even when app is in background
   - Triggers clip save operation

4. **Video Encoder**
   - Encodes saved clips efficiently (H.264/H.265)
   - Applies compression to reduce file size
   - Outputs common formats (MP4, WebM)

5. **UI/System Tray Interface**
   - Minimal system tray icon
   - Configuration panel for settings
   - Status indicators (recording, buffer size, etc.)

---

## Technology Stack Options

### Option 1: Python-based Solution (Recommended for beginners)
**Pros:** Easy to develop, great libraries, cross-platform
**Cons:** Slightly higher resource usage than compiled languages

**Libraries:**
- **Screen capture:** `mss` (ultra-fast), `Pillow`, or `opencv-python`
- **Video encoding:** `opencv-python` (cv2.VideoWriter) or `imageio-ffmpeg`
- **Keybind detection:** `pynput` or `keyboard`
- **System tray:** `pystray` or `PyQt5`/`PyQt6`
- **Circular buffer:** Custom implementation with `collections.deque` or `numpy` arrays

**Sample structure:**
```
screen-clipper/
├── main.py              # Entry point
├── capture.py           # Screen capture logic
├── buffer.py            # Circular buffer management
├── hotkey.py            # Keybind handler
├── encoder.py           # Video encoding
├── tray.py              # System tray UI
├── config.py            # Configuration management
└── requirements.txt     # Dependencies
```

### Option 2: Electron + Node.js (For modern UI)
**Pros:** Great UI capabilities, web technologies
**Cons:** Higher memory usage, larger app size

**Libraries:**
- **Screen capture:** `robotjs`, `desktopCapturer` (Electron API)
- **Video encoding:** `fluent-ffmpeg`
- **Keybind:** `electron-globalshortcut` or `node-global-key-listener`
- **UI:** Electron's built-in UI framework

### Option 3: C++ with Qt (Best performance)
**Pros:** Maximum performance, minimal resource usage
**Cons:** Steeper learning curve, longer development time

**Libraries:**
- **Screen capture:** `Qt::QScreen::grabWindow()`
- **Video encoding:** FFmpeg C++ API
- **Keybind:** Platform-specific APIs (Windows: RegisterHotKey, Linux: XGrabKey)
- **UI:** Qt Widgets

### Option 4: Go (Good balance)
**Pros:** Good performance, compiled binary, easier than C++
**Cons:** Smaller ecosystem for screen recording

**Libraries:**
- **Screen capture:** `kbinani/screenshot`
- **Video encoding:** `go-ffmpeg` bindings
- **Keybind:** `robotgo` or platform-specific

---

## Implementation Steps

### Phase 1: MVP (Minimum Viable Product)
1. **Set up project structure**
   - Choose technology stack
   - Set up development environment
   - Install required dependencies

2. **Implement screen capture**
   ```python
   # Example with Python + mss
   from mss import mss
   
   def capture_screen():
       with mss() as sct:
           monitor = sct.monitors[1]  # Primary monitor
           screenshot = sct.grab(monitor)
           return screenshot
   ```

3. **Create circular buffer**
   ```python
   from collections import deque
   
   class CircularBuffer:
       def __init__(self, max_frames):
           self.buffer = deque(maxlen=max_frames)
       
       def add_frame(self, frame):
           self.buffer.append(frame)
       
       def get_frames(self, num_frames=None):
           if num_frames is None:
               return list(self.buffer)
           return list(self.buffer)[-num_frames:]
   ```

4. **Implement basic recording loop**
   ```python
   import time
   
   def recording_loop(buffer, fps=30):
       frame_interval = 1.0 / fps
       
       while True:
           start = time.time()
           frame = capture_screen()
           buffer.add_frame(frame)
           
           # Sleep to maintain target FPS
           elapsed = time.time() - start
           time.sleep(max(0, frame_interval - elapsed))
   ```

5. **Add keybind handler**
   ```python
   from pynput import keyboard
   
   def on_press(key, buffer, output_path):
       try:
           if key == keyboard.Key.f9:  # Example: F9 key
               save_clip(buffer, output_path)
       except AttributeError:
           pass
   
   def listen_for_hotkey(buffer, output_path):
       with keyboard.Listener(on_press=lambda k: on_press(k, buffer, output_path)) as listener:
           listener.join()
   ```

6. **Implement video encoding**
   ```python
   import cv2
   
   def save_clip(buffer, output_path, fps=30):
       frames = buffer.get_frames()
       if not frames:
           return
       
       # Get frame dimensions
       height, width = frames[0].shape[:2]
       
       # Initialize video writer
       fourcc = cv2.VideoWriter_fourcc(*'mp4v')
       out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
       
       # Write frames
       for frame in frames:
           out.write(frame)
       
       out.release()
   ```

### Phase 2: Optimization
1. **Memory management**
   - Store frames in compressed format
   - Implement memory-mapped files for large buffers
   - Add disk-based buffer for longer durations

2. **Performance tuning**
   - Use multi-threading for capture and encoding
   - Implement frame dropping during high load
   - Add GPU acceleration if available

3. **Quality vs size trade-off**
   - Configurable resolution scaling
   - Adjustable compression settings
   - Smart FPS adjustment based on activity

### Phase 3: User Experience
1. **Configuration UI**
   - Buffer duration slider (5 min - 24 hours)
   - Custom keybind selector
   - FPS and quality settings
   - Output directory selection

2. **System tray integration**
   - Start/stop recording
   - Status indicators
   - Quick access to recent clips

3. **Auto-start on boot**
   - Windows: Add to Startup folder
   - macOS: Launch Agent
   - Linux: systemd service or autostart

### Phase 4: Advanced Features
1. **Smart features**
   - Motion detection to reduce buffer size
   - Audio capture support
   - Multiple monitor support
   - Region selection (partial screen)

2. **Clip management**
   - Auto-naming with timestamps
   - Clip library viewer
   - Quick sharing options
   - Cloud sync (optional)

---

## Dependencies & Requirements

### For Python Implementation

**Essential libraries:**
```txt
mss>=9.0.0           # Screen capture
opencv-python>=4.8.0  # Video processing
numpy>=1.24.0         # Array operations
pynput>=1.7.6         # Keyboard/mouse monitoring
pystray>=0.19.4       # System tray icon
Pillow>=10.0.0        # Image processing
```

**Optional libraries:**
```txt
pyinstaller>=6.0.0    # Create standalone executable
psutil>=5.9.0         # System monitoring
toml>=0.10.2          # Configuration files
```

### System Requirements
- **CPU:** Dual-core processor (Quad-core recommended)
- **RAM:** 2GB minimum (4GB recommended for longer buffers)
- **Storage:** 500MB - 50GB (depends on buffer duration)
- **OS:** Windows 10+, macOS 10.14+, Linux (X11 or Wayland)

---

## Optimization Strategies

### 1. Resolution Scaling
Record at lower resolution than screen (e.g., 720p instead of 4K)
```python
def resize_frame(frame, scale=0.5):
    height, width = frame.shape[:2]
    return cv2.resize(frame, (int(width * scale), int(height * scale)))
```

### 2. Variable FPS
- Lower FPS when idle (10 fps)
- Higher FPS during activity (30 fps)
- Detect activity via frame difference

### 3. Compression
- Use H.264 or H.265 codec
- Balance quality vs file size
- Hardware encoding if available (NVENC, QuickSync)

### 4. Disk vs Memory Buffer
- **Short buffer (< 5 min):** Keep in RAM
- **Long buffer (> 5 min):** Use disk with memory cache
- Implement hybrid approach

### 5. Multi-threading
```python
import threading
from queue import Queue

capture_queue = Queue(maxsize=300)  # ~10 seconds at 30fps

def capture_thread():
    while True:
        frame = capture_screen()
        capture_queue.put(frame)

def save_thread(buffer):
    while True:
        frame = capture_queue.get()
        buffer.add_frame(frame)
```

---

## Security & Privacy Considerations

### Privacy Features
1. **Clear buffer on demand**
   - Manual buffer clear button
   - Auto-clear on user request

2. **Pause recording**
   - Temporary pause hotkey
   - Auto-pause on specific apps (configurable)

3. **Visual indicator**
   - Show recording status
   - Optional on-screen overlay

4. **Data protection**
   - Local storage only (no cloud by default)
   - Encrypted buffer option
   - Secure file permissions

### Best Practices
- Don't capture sensitive information unintentionally
- Inform users that recording is active
- Provide easy access to delete recordings
- Follow local recording laws and regulations

---

## Configuration File Example

```toml
# config.toml

[recording]
fps = 30
resolution_scale = 1.0  # 1.0 = full resolution, 0.5 = half
buffer_duration_minutes = 10
codec = "h264"

[keybinds]
save_clip = "f9"
pause_recording = "f8"
clear_buffer = "ctrl+shift+f9"

[storage]
output_directory = "~/ScreenClips"
filename_format = "clip_%Y%m%d_%H%M%S.mp4"
max_clips = 100  # Auto-delete oldest

[performance]
use_gpu = true
thread_count = 2
memory_limit_mb = 1024

[privacy]
show_recording_indicator = true
auto_pause_apps = ["banking-app", "password-manager"]
```

---

## Project Timeline Estimate

### Simple version (Python MVP):
- **Week 1:** Core recording + circular buffer
- **Week 2:** Keybind handler + video encoding
- **Week 3:** System tray UI + configuration
- **Week 4:** Testing + optimization

### Full-featured version:
- **Month 1:** MVP + basic features
- **Month 2:** UI polish + optimization
- **Month 3:** Advanced features + testing
- **Month 4:** Documentation + deployment

---

## Testing Checklist

- [ ] Screen capture works on all monitors
- [ ] Buffer correctly wraps (circular behavior)
- [ ] Keybind triggers on all applications
- [ ] Video encoding produces valid files
- [ ] No memory leaks during 24h+ operation
- [ ] CPU usage stays below 10%
- [ ] Application survives system sleep/wake
- [ ] Configuration persists across restarts
- [ ] System tray icon displays correctly
- [ ] Auto-start on boot works
- [ ] Clips are saved with correct timestamp
- [ ] Large buffers (>1 hour) work without crashes

---

## Alternative Approaches

### 1. Use Existing Tools as Base
- **OBS Studio:** Open-source, can be automated
- **ShareX:** Has replay buffer feature
- **Windows Game Bar:** Built-in Windows feature (limited)

### 2. Cloud-Based Solution
- Stream to cloud service with DVR-like functionality
- Higher latency but less local storage

### 3. Browser Extension
- Record active tab only
- Limited to browser content
- Easier to deploy

---

## Next Steps

1. **Choose your technology stack** based on:
   - Your programming experience
   - Performance requirements
   - Desired features

2. **Set up development environment:**
   ```bash
   # For Python
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install mss opencv-python pynput pystray pillow numpy
   ```

3. **Start with MVP:** Get basic recording working first

4. **Iterate:** Add features incrementally

5. **Test thoroughly:** Run for extended periods to catch issues

---

## Recommended Starting Point: Python MVP

Create a simple prototype to validate the concept:

```python
# simple_clipper.py
import time
import cv2
import numpy as np
from mss import mss
from pynput import keyboard
from collections import deque
from datetime import datetime

# Configuration
FPS = 30
BUFFER_MINUTES = 5
HOTKEY = keyboard.Key.f9

# Calculate buffer size
BUFFER_SIZE = FPS * 60 * BUFFER_MINUTES

# Initialize
frame_buffer = deque(maxlen=BUFFER_SIZE)
is_recording = True

def capture_frame(sct):
    """Capture a single frame."""
    monitor = sct.monitors[1]
    img = sct.grab(monitor)
    frame = np.array(img)
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

def save_clip(frames):
    """Save frames to video file."""
    if not frames:
        print("No frames to save!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"clip_{timestamp}.mp4"
    
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, FPS, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    print(f"Saved clip: {filename}")

def on_press(key):
    """Handle key press."""
    global is_recording
    
    if key == HOTKEY:
        print(f"Saving last {BUFFER_MINUTES} minutes...")
        save_clip(list(frame_buffer))
    elif key == keyboard.Key.esc:
        is_recording = False
        return False

# Start keyboard listener in background
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Main recording loop
print(f"Recording started. Press F9 to save last {BUFFER_MINUTES} minutes. Press ESC to exit.")

with mss() as sct:
    while is_recording:
        start_time = time.time()
        
        # Capture and store frame
        frame = capture_frame(sct)
        frame_buffer.append(frame)
        
        # Maintain target FPS
        elapsed = time.time() - start_time
        sleep_time = max(0, (1.0 / FPS) - elapsed)
        time.sleep(sleep_time)

print("Recording stopped.")
```

Run with:
```bash
python simple_clipper.py
```

This gives you a working prototype to build upon!

---

## Resources & References

### Documentation
- **FFmpeg:** https://ffmpeg.org/documentation.html
- **OpenCV:** https://docs.opencv.org/
- **mss:** https://python-mss.readthedocs.io/

### Similar Projects
- **OBS Studio:** https://github.com/obsproject/obs-studio
- **ShareX:** https://github.com/ShareX/ShareX
- **SimpleScreenRecorder:** https://github.com/MaartenBaert/ssr

### Tutorials
- Screen recording basics
- Circular buffer implementation
- Global hotkey registration per OS
- Video encoding optimization

---

## Conclusion

This plan provides a comprehensive roadmap to build a screen clipper application. Start with the Python MVP to validate the concept, then expand based on your needs. The key challenges are:

1. **Performance optimization** - Keep CPU/memory usage low
2. **Cross-platform compatibility** - Different APIs per OS
3. **User experience** - Make it seamless and non-intrusive
4. **Storage management** - Handle large video buffers efficiently

Good luck with your project! Start small, test often, and iterate based on real usage.
