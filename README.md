# Cool Portfolio + Screen Clipper Project

This repository contains Bryce's portfolio website and a comprehensive plan + implementation for a 24/7 screen recording/clipping application.

## Contents

### 📁 Portfolio Website
- **Location:** Root directory (`index.html`, `css/`, `js/`)
- **Description:** Personal portfolio showcasing skills in Lua scripting, combat systems, and game development
- **View:** Open `index.html` in a browser

### 🎥 Screen Clipper Application
- **Location:** `screen-clipper/` directory
- **Description:** A 24/7 background screen recorder with circular buffer and hotkey clip saving
- **Documentation:** 
  - **Planning:** See `SCREEN_CLIPPER_PLAN.md` for comprehensive architecture and implementation guide
  - **Quick Start:** See `screen-clipper/QUICKSTART.md` to get started in 5 minutes
  - **Full Guide:** See `screen-clipper/README.md` for complete documentation

## Screen Clipper Overview

The Screen Clipper is a lightweight application that:

✅ Records your screen continuously in the background  
✅ Keeps a rolling buffer (5-10 minutes recommended, up to 24 hours)  
✅ Lets you save clips on-demand with a custom keybind (default: F9)  
✅ Runs 24/7 with optimized performance  
✅ Works cross-platform (Windows, macOS, Linux)  

### Quick Start

```bash
# Navigate to the screen-clipper directory
cd screen-clipper

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Press F9 to save the last 5 minutes
# Press ESC to exit
```

### Files

- **`SCREEN_CLIPPER_PLAN.md`** - Comprehensive planning document covering:
  - Technical architecture
  - Technology stack options (Python, Electron, C++, Go)
  - Implementation steps and timeline
  - Optimization strategies
  - Security and privacy considerations
  - Complete MVP code examples
  
- **`screen-clipper/`** - Working Python implementation:
  - `main.py` - Simple version (beginner-friendly)
  - `main_advanced.py` - Advanced version with config support
  - `config.toml` - Configuration file
  - `requirements.txt` - Python dependencies
  - `README.md` - Detailed usage guide
  - `QUICKSTART.md` - 5-minute quick start guide

## What's Included

### Planning Documentation
The `SCREEN_CLIPPER_PLAN.md` provides everything you need to build this software:
- Requirements analysis
- Architecture design
- Multiple technology stack options
- Step-by-step implementation guide
- Performance optimization tips
- Security best practices
- Testing checklist
- Full working code examples

### Working Implementation
Two versions of the application are provided:

1. **Simple Version** (`main.py`)
   - Single file, easy to understand
   - Perfect for learning or quick deployment
   - ~200 lines of well-commented code

2. **Advanced Version** (`main_advanced.py`)
   - Configuration file support (TOML)
   - Better error handling and logging
   - Clip management (auto-delete old clips)
   - More customization options

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** 500MB - 50GB (depends on buffer duration)
- **OS:** Windows 10+, macOS 10.14+, or Linux (X11/Wayland)
- **CPU:** Dual-core (quad-core recommended)

## Features

- ✅ Continuous background recording
- ✅ Circular buffer (no disk space waste)
- ✅ Custom keybind support (F9 by default)
- ✅ Configurable buffer duration (5 min - 24 hours)
- ✅ Adjustable FPS and resolution
- ✅ Low CPU/memory usage
- ✅ Multiple monitor support
- ✅ MP4 video output
- ✅ System tray integration (advanced version)
- ✅ Auto-cleanup of old clips

## Technology Stack

The implementation uses:
- **mss** - Fast screen capture
- **OpenCV** - Video encoding
- **pynput** - Global hotkey detection
- **numpy** - Efficient frame storage
- **Python 3.8+** - Core language

## Performance

Typical resource usage:
- **CPU:** 5-10% (dual-core @ 30 fps)
- **RAM:** 200MB - 1GB (5-10 min buffer at 1080p)
- **Disk:** Only when saving clips

## Usage Examples

### Basic Usage
```bash
python main.py
# Press F9 to save, ESC to exit
```

### Custom Configuration
```toml
# Edit config.toml
[recording]
fps = 30
buffer_duration_minutes = 10
resolution_scale = 0.75

[keybinds]
save_clip = "f9"
```

### Building Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Executable will be in dist/ folder
```

## Documentation Structure

```
.
├── SCREEN_CLIPPER_PLAN.md         # Complete planning & architecture
├── screen-clipper/
│   ├── README.md                  # Detailed usage guide
│   ├── QUICKSTART.md              # 5-minute quick start
│   ├── main.py                    # Simple implementation
│   ├── main_advanced.py           # Advanced implementation
│   ├── config.toml                # Configuration file
│   ├── requirements.txt           # Dependencies
│   └── .gitignore                 # Ignore clips/temp files
├── index.html                     # Portfolio website
└── README.md                      # This file
```

## Getting Started

1. **Read the plan:** Start with `SCREEN_CLIPPER_PLAN.md` to understand the full scope
2. **Try the MVP:** Follow `screen-clipper/QUICKSTART.md` to run the application
3. **Customize:** Edit `config.toml` to match your needs
4. **Extend:** Use the plan to add new features or optimize further

## License

MIT License - Feel free to use and modify for your projects

## Author

Bryce - Lua specialist with 9 years of coding experience

- Twitter/X: [@bryc_xe](https://x.com/bryc_xe)
- Discord: [Join Server](https://discord.gg/nZYdDUVFKy)

## Contributing

Suggestions and improvements welcome! This is a planning project and MVP implementation.

## Support

- For screen clipper questions, see the comprehensive documentation
- For portfolio inquiries, reach out via the contact methods above
- Report issues via GitHub issues

---

**Note:** This project provides both planning documentation and a working MVP. The planning document (`SCREEN_CLIPPER_PLAN.md`) contains everything you need to understand, build, and customize this software for your specific needs.
