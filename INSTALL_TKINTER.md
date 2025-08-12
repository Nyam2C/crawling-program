# 🛠️ tkinter Installation Guide

The GUI version of this application requires `tkinter`, which is not always included with Python installations. Here's how to install it on different operating systems:

## 🐧 Linux

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### CentOS/RHEL/Fedora:
```bash
# For newer versions (Fedora/RHEL 8+):
sudo dnf install python3-tkinter

# For older versions:
sudo yum install tkinter
```

### Arch Linux:
```bash
sudo pacman -S tk
```

### openSUSE:
```bash
sudo zypper install python3-tk
```

## 🍎 macOS

tkinter should be included with Python installations. If not:

```bash
# Using Homebrew:
brew install python-tk

# Or reinstall Python with tkinter:
brew reinstall python
```

## 🪟 Windows

tkinter should be included with Python from python.org. If not:

1. **Reinstall Python** from [python.org](https://python.org)
2. Make sure to check **"Add Python to PATH"** during installation
3. Make sure **"tcl/tk and IDLE"** option is selected

## 🧪 Verify Installation

Test if tkinter is working:

```python
python3 -c "import tkinter; print('tkinter is available!')"
```

## 🔄 Alternative Solutions

If you can't install tkinter:

### Option 1: Use CLI Version
```bash
python main.py
```

### Option 2: Use Web Interface (if available)
Check if there's a web version available in the repository.

### Option 3: Use Docker
```bash
# Build and run with GUI support (Linux with X11)
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix your-app
```

## 📋 Troubleshooting

### Error: "No module named '_tkinter'"
This means tkinter wasn't compiled with your Python installation. Try:
- Reinstalling Python with tkinter support
- Using a different Python distribution (like Anaconda)

### Error: "couldn't connect to display"
On Linux, you may need to:
```bash
export DISPLAY=:0
xhost +local:
```

### WSL (Windows Subsystem for Linux)
For GUI apps in WSL, you'll need an X server like VcXsrv or WSL2 with GUI support.

## 💡 Quick Test

Run this to test your tkinter installation:

```python
#!/usr/bin/env python3
import tkinter as tk

root = tk.Tk()
root.title("tkinter Test")
label = tk.Label(root, text="✅ tkinter is working!")
label.pack(pady=20, padx=20)
button = tk.Button(root, text="Close", command=root.quit)
button.pack(pady=10)
root.mainloop()
```

If you see a window with the text "tkinter is working!", you're all set! 🎉