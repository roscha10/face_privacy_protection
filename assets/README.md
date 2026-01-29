# Assets Directory

This directory contains demo media files for the Face Privacy Protection project.

## Demo GIF

The main README.md references `demo.gif` which should be placed here. You can create a demo GIF by:

1. Running the demo video generator:
   ```bash
   python src/face_privacy.py --demo --input test/video_003.mp4 --output output/demo.avi
   ```

2. Converting the output AVI to GIF using ffmpeg or online tools:
   ```bash
   ffmpeg -i output/demo.avi -vf "fps=10,scale=800:-1:flags=lanczos" assets/demo.gif
   ```

## Screenshots

Place project screenshots here for documentation purposes:
- Before/after comparisons
- Different privacy effects
- Real-time processing examples

## Recommended Tools

- **GIF Creation**: ffmpeg, ezgif.com, giphy.com
- **Screenshot Capture**: Use the `s` key during real-time processing
- **Video Editing**: Any video editor or ffmpeg for trimming/optimization
