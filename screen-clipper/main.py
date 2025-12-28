"""
Screen Clipper - Main Application Entry Point

A 24/7 background screen recorder with circular buffer and hotkey clip saving.
"""

import time
import cv2
import numpy as np
from mss import mss
from pynput import keyboard
from collections import deque
from datetime import datetime
import os
import sys
import threading
from pathlib import Path

# Configuration
FPS = 30  # Frames per second
BUFFER_MINUTES = 5  # How many minutes to keep in buffer
SAVE_HOTKEY = keyboard.Key.f9  # Hotkey to save clip
PAUSE_HOTKEY = keyboard.Key.f8  # Hotkey to pause/resume
EXIT_HOTKEY = keyboard.Key.esc  # Hotkey to exit

# Calculate buffer size
BUFFER_SIZE = FPS * 60 * BUFFER_MINUTES

# Create output directory
OUTPUT_DIR = Path("clips")
OUTPUT_DIR.mkdir(exist_ok=True)

# Global state
frame_buffer = deque(maxlen=BUFFER_SIZE)
is_recording = True
is_paused = False
save_lock = threading.Lock()


def capture_frame(sct):
    """
    Capture a single frame from the screen.
    
    Args:
        sct: MSS screen capture instance
        
    Returns:
        numpy.ndarray: Captured frame in BGR format
    """
    # Ensure monitor exists, fall back to first available
    if len(sct.monitors) < 2:
        monitor = sct.monitors[0]  # Use all monitors
    else:
        monitor = sct.monitors[1]  # Primary monitor
    
    img = sct.grab(monitor)
    frame = np.array(img)
    return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)


def save_clip(frames):
    """
    Save frames to a video file.
    
    Args:
        frames: List of frames to save
    """
    if not frames:
        print("⚠️  No frames to save!")
        return
    
    with save_lock:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"clip_{timestamp}.mp4"
        
        try:
            height, width = frames[0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(filename), fourcc, FPS, (width, height))
            
            print(f"💾 Saving clip with {len(frames)} frames ({len(frames)//FPS} seconds)...")
            
            for frame in frames:
                out.write(frame)
            
            out.release()
            
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            print(f"✅ Saved: {filename} ({file_size:.1f} MB)")
            
        except Exception as e:
            print(f"❌ Error saving clip: {e}")


def on_press(key):
    """
    Handle keyboard events.
    
    Args:
        key: Pressed key
        
    Returns:
        False to stop listener, None to continue
    """
    global is_recording, is_paused
    
    try:
        if key == SAVE_HOTKEY:
            print(f"\n🎬 Hotkey pressed! Saving last {BUFFER_MINUTES} minutes...")
            # Save in background thread to not block recording
            frames_to_save = list(frame_buffer)
            threading.Thread(target=save_clip, args=(frames_to_save,), daemon=True).start()
            
        elif key == PAUSE_HOTKEY:
            is_paused = not is_paused
            status = "⏸️  PAUSED" if is_paused else "▶️  RESUMED"
            print(f"\n{status}")
            
        elif key == EXIT_HOTKEY:
            print("\n🛑 Stopping...")
            is_recording = False
            return False
            
    except AttributeError:
        pass


def display_status(frame_count, start_time):
    """
    Display recording status.
    
    Args:
        frame_count: Current frame count
        start_time: Recording start time
    """
    elapsed = time.time() - start_time
    buffer_seconds = min(elapsed, BUFFER_MINUTES * 60)
    buffer_usage = (frame_count % BUFFER_SIZE) / BUFFER_SIZE * 100
    
    print(f"\r⏺️  Recording... | "
          f"Buffer: {buffer_seconds:.0f}s / {BUFFER_MINUTES * 60}s | "
          f"Usage: {buffer_usage:.0f}% | "
          f"Frames: {frame_count:,} | "
          f"Press F9 to save, F8 to pause, ESC to exit",
          end="", flush=True)


def main():
    """Main application loop."""
    global is_recording
    
    print("=" * 80)
    print("🎥 Screen Clipper - 24/7 Background Screen Recorder")
    print("=" * 80)
    print(f"\n⚙️  Configuration:")
    print(f"   • FPS: {FPS}")
    print(f"   • Buffer Duration: {BUFFER_MINUTES} minutes ({BUFFER_SIZE:,} frames)")
    print(f"   • Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"\n🎮 Controls:")
    print(f"   • F9: Save last {BUFFER_MINUTES} minutes")
    print(f"   • F8: Pause/Resume recording")
    print(f"   • ESC: Exit application")
    print(f"\n📝 Starting recording...\n")
    
    # Start keyboard listener in background
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Main recording loop
    frame_count = 0
    start_time = time.time()
    
    try:
        with mss() as sct:
            while is_recording:
                loop_start = time.time()
                
                if not is_paused:
                    # Capture and store frame
                    frame = capture_frame(sct)
                    frame_buffer.append(frame)
                    frame_count += 1
                    
                    # Display status every 30 frames
                    if frame_count % 30 == 0:
                        display_status(frame_count, start_time)
                
                # Maintain target FPS
                elapsed = time.time() - loop_start
                sleep_time = max(0, (1.0 / FPS) - elapsed)
                time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
    finally:
        print("\n\n" + "=" * 80)
        print("📊 Session Summary:")
        print(f"   • Total frames captured: {frame_count:,}")
        print(f"   • Recording duration: {(time.time() - start_time) / 60:.1f} minutes")
        print(f"   • Clips saved to: {OUTPUT_DIR.absolute()}")
        print("=" * 80)
        print("\n👋 Screen Clipper stopped. Goodbye!\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
