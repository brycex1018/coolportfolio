"""
Advanced Screen Clipper with Configuration Support

Enhanced version with TOML config loading, better performance, and more features.
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
import logging

# Try to import toml for config, fallback to defaults
try:
    import tomli as toml
except ImportError:
    try:
        import toml
    except ImportError:
        print("⚠️  TOML library not found. Install with: pip install tomli")
        toml = None


class Config:
    """Configuration manager with defaults."""
    
    # Defaults
    FPS = 30
    BUFFER_MINUTES = 5
    RESOLUTION_SCALE = 1.0
    CODEC = "mp4v"
    OUTPUT_DIR = "clips"
    FILENAME_FORMAT = "clip_%Y%m%d_%H%M%S.mp4"
    MAX_CLIPS = 100
    QUALITY = 7
    MONITOR_INDEX = 1
    CAPTURE_CURSOR = True
    MOTION_DETECTION = False
    DEBUG = False
    
    @classmethod
    def load(cls, config_path="config.toml"):
        """Load configuration from TOML file."""
        if not toml or not os.path.exists(config_path):
            print("⚠️  Using default configuration")
            return cls()
        
        try:
            with open(config_path, "rb") as f:
                data = toml.load(f)
            
            config = cls()
            
            # Recording settings
            rec = data.get("recording", {})
            config.FPS = rec.get("fps", cls.FPS)
            config.BUFFER_MINUTES = rec.get("buffer_duration_minutes", cls.BUFFER_MINUTES)
            config.RESOLUTION_SCALE = rec.get("resolution_scale", cls.RESOLUTION_SCALE)
            config.CODEC = rec.get("codec", cls.CODEC)
            
            # Storage settings
            storage = data.get("storage", {})
            config.OUTPUT_DIR = storage.get("output_directory", cls.OUTPUT_DIR)
            config.FILENAME_FORMAT = storage.get("filename_format", cls.FILENAME_FORMAT)
            config.MAX_CLIPS = storage.get("max_clips", cls.MAX_CLIPS)
            
            # Performance settings
            perf = data.get("performance", {})
            config.QUALITY = perf.get("quality", cls.QUALITY)
            
            # Monitor settings
            monitor = data.get("monitor", {})
            config.MONITOR_INDEX = monitor.get("monitor_index", cls.MONITOR_INDEX)
            
            # Advanced settings
            adv = data.get("advanced", {})
            config.CAPTURE_CURSOR = adv.get("capture_cursor", cls.CAPTURE_CURSOR)
            config.MOTION_DETECTION = adv.get("motion_detection", cls.MOTION_DETECTION)
            config.DEBUG = adv.get("debug_mode", cls.DEBUG)
            
            print("✅ Configuration loaded from config.toml")
            return config
            
        except Exception as e:
            print(f"⚠️  Error loading config: {e}. Using defaults.")
            return cls()


class ScreenClipper:
    """Main screen clipper application."""
    
    def __init__(self, config):
        self.config = config
        self.buffer_size = config.FPS * 60 * config.BUFFER_MINUTES
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.is_recording = True
        self.is_paused = False
        self.save_lock = threading.Lock()
        
        # Create output directory
        self.output_dir = Path(config.OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_level = logging.DEBUG if config.DEBUG else logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("screen_clipper.log")
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Stats
        self.frame_count = 0
        self.start_time = None
        self.clips_saved = 0
        
    def capture_frame(self, sct):
        """Capture a single frame from the screen."""
        try:
            # Validate monitor index
            if self.config.MONITOR_INDEX >= len(sct.monitors):
                self.logger.warning(f"Monitor index {self.config.MONITOR_INDEX} not available, using primary monitor")
                monitor_idx = 1 if len(sct.monitors) > 1 else 0
            else:
                monitor_idx = self.config.MONITOR_INDEX
            
            monitor = sct.monitors[monitor_idx]
            img = sct.grab(monitor)
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Apply resolution scaling if configured
            if self.config.RESOLUTION_SCALE != 1.0:
                width = int(frame.shape[1] * self.config.RESOLUTION_SCALE)
                height = int(frame.shape[0] * self.config.RESOLUTION_SCALE)
                frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            
            return frame
            
        except Exception as e:
            self.logger.error(f"Error capturing frame: {e}")
            return None
    
    def save_clip(self, frames):
        """Save frames to a video file."""
        if not frames:
            self.logger.warning("No frames to save!")
            return False
        
        with self.save_lock:
            try:
                # Generate timestamp-based filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.output_dir / f"clip_{timestamp}.mp4"
                
                height, width = frames[0].shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*self.config.CODEC)
                out = cv2.VideoWriter(str(filename), fourcc, self.config.FPS, (width, height))
                
                self.logger.info(f"Saving clip with {len(frames)} frames ({len(frames)//self.config.FPS} seconds)...")
                
                for frame in frames:
                    out.write(frame)
                
                out.release()
                
                file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
                self.logger.info(f"✅ Saved: {filename} ({file_size:.1f} MB)")
                
                self.clips_saved += 1
                self.cleanup_old_clips()
                
                return True
                
            except Exception as e:
                self.logger.error(f"Error saving clip: {e}")
                return False
    
    def cleanup_old_clips(self):
        """Remove old clips if max_clips limit is exceeded."""
        if self.config.MAX_CLIPS <= 0:
            return
        
        try:
            clips = sorted(self.output_dir.glob("clip_*.mp4"), key=os.path.getmtime)
            
            while len(clips) > self.config.MAX_CLIPS:
                oldest = clips.pop(0)
                oldest.unlink()
                self.logger.info(f"Deleted old clip: {oldest.name}")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up clips: {e}")
    
    def on_press(self, key):
        """Handle keyboard events."""
        try:
            if key == keyboard.Key.f9:
                self.logger.info(f"Hotkey pressed! Saving last {self.config.BUFFER_MINUTES} minutes...")
                frames_to_save = list(self.frame_buffer)
                threading.Thread(target=self.save_clip, args=(frames_to_save,), daemon=True).start()
                
            elif key == keyboard.Key.f8:
                self.is_paused = not self.is_paused
                status = "PAUSED" if self.is_paused else "RESUMED"
                self.logger.info(status)
                
            elif key == keyboard.Key.esc:
                self.logger.info("Stopping...")
                self.is_recording = False
                return False
                
        except AttributeError:
            pass
    
    def display_status(self):
        """Display recording status."""
        elapsed = time.time() - self.start_time
        buffer_seconds = min(elapsed, self.config.BUFFER_MINUTES * 60)
        buffer_usage = (self.frame_count % self.buffer_size) / self.buffer_size * 100
        
        print(f"\r⏺️  Recording... | "
              f"Buffer: {buffer_seconds:.0f}s / {self.config.BUFFER_MINUTES * 60}s | "
              f"Usage: {buffer_usage:.0f}% | "
              f"Frames: {self.frame_count:,} | "
              f"Clips: {self.clips_saved} | "
              f"Press F9 to save, F8 to pause, ESC to exit",
              end="", flush=True)
    
    def run(self):
        """Main application loop."""
        print("=" * 80)
        print("🎥 Screen Clipper - Advanced 24/7 Background Screen Recorder")
        print("=" * 80)
        print(f"\n⚙️  Configuration:")
        print(f"   • FPS: {self.config.FPS}")
        print(f"   • Buffer Duration: {self.config.BUFFER_MINUTES} minutes ({self.buffer_size:,} frames)")
        print(f"   • Resolution Scale: {self.config.RESOLUTION_SCALE}x")
        print(f"   • Codec: {self.config.CODEC}")
        print(f"   • Output Directory: {self.output_dir.absolute()}")
        print(f"   • Max Clips: {self.config.MAX_CLIPS}")
        print(f"\n🎮 Controls:")
        print(f"   • F9: Save last {self.config.BUFFER_MINUTES} minutes")
        print(f"   • F8: Pause/Resume recording")
        print(f"   • ESC: Exit application")
        print(f"\n📝 Starting recording...\n")
        
        # Start keyboard listener
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        
        self.start_time = time.time()
        
        try:
            with mss() as sct:
                while self.is_recording:
                    loop_start = time.time()
                    
                    if not self.is_paused:
                        frame = self.capture_frame(sct)
                        if frame is not None:
                            self.frame_buffer.append(frame)
                            self.frame_count += 1
                            
                            # Display status every 30 frames
                            if self.frame_count % 30 == 0:
                                self.display_status()
                    
                    # Maintain target FPS
                    elapsed = time.time() - loop_start
                    sleep_time = max(0, (1.0 / self.config.FPS) - elapsed)
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.print_summary()
    
    def print_summary(self):
        """Print session summary."""
        print("\n\n" + "=" * 80)
        print("📊 Session Summary:")
        print(f"   • Total frames captured: {self.frame_count:,}")
        print(f"   • Recording duration: {(time.time() - self.start_time) / 60:.1f} minutes")
        print(f"   • Clips saved: {self.clips_saved}")
        print(f"   • Clips location: {self.output_dir.absolute()}")
        print("=" * 80)
        print("\n👋 Screen Clipper stopped. Goodbye!\n")


def main():
    """Application entry point."""
    try:
        # Load configuration
        config = Config.load()
        
        # Create and run clipper
        clipper = ScreenClipper(config)
        clipper.run()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
