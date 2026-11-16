# Mandelbrot Desktop Explorer

High-performance desktop Mandelbrot set explorer using Python + Numba (JIT compiled, multi-threaded).

Supports deep zoom with native double precision (much deeper than the WebGL version).

## Features
- Smooth pan & zoom
- Adjustable iterations, hue, saturation
- Fast rendering via Numba parallel
- Easy to package into a standalone EXE

## Controls
- **Mouse drag**: Pan
- **Scroll wheel**: Zoom
- **R**: Reset view
- **Up/Down**: Increase/Decrease max iterations
- **Left/Right**: Change hue
- **+/-**: Change saturation

## Run from source
```bash
pip install -r requirements.txt
python mandelbrot_desktop.py
```

## Build EXE (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed mandelbrot_desktop.py
```
The EXE will be in the `dist/` folder.

## Notes
This version uses double-precision floats, so you can zoom significantly deeper than the browser version before precision issues appear.

Created with Grok.
