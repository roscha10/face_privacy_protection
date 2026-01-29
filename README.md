# Face Privacy Protection with YOLOv11-Face

Real-time face detection and privacy protection using AI-powered anonymization techniques.

![Demo](assets/demo.gif)
> *Real-time face pixelation demonstration (Original vs Protected)*

## Overview

This project implements automatic face detection and anonymization for privacy protection in images and videos. It uses the YOLOv11-Face model for robust face detection across various angles and lighting conditions, combined with multiple privacy protection effects.

**Key Applications:**
- GDPR/CCPA compliance for video content
- Automated dataset anonymization
- Privacy-first surveillance systems
- Social media content protection
- Medical imaging privacy

## Model Information

| Property | Details |
|----------|---------|
| Model Architecture | YOLOv11s-Face |
| Framework | Ultralytics YOLO (PyTorch) |
| Input Resolution | 640x480 (configurable) |
| Performance | ~45 FPS (real-time on CPU) |
| Model Source | [Ultralytics](https://github.com/ultralytics/ultralytics) |
| Precision | FP32 |

## Features

- **Real-time Processing**: Webcam and video file support with live FPS monitoring
- **Multiple Privacy Effects**:
  - Pixelation (adjustable intensity)
  - Gaussian blur
  - Black box anonymization
  - Emoji overlay
  - Witness protection mode
  - Colorize effect
- **Flexible I/O**: Camera input, video files, or image processing
- **Side-by-Side Comparison**: Before/after view for quality assessment
- **Export Functionality**: Save processed videos and screenshots

## Requirements

- Python 3.8 or higher
- Webcam (for real-time demos)
- 4GB RAM minimum (8GB recommended)

### Dependencies

```
opencv-python>=4.8.0
ultralytics>=8.4.0
torch>=2.0.0
numpy>=1.24.0
Pillow>=10.0.0
```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/roscha10/face_privacy_protection.git
cd face_privacy_protection
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The YOLOv11s-Face model will be automatically downloaded on first run.

## Usage

### Quick Start - Real-Time Webcam

```bash
python src/face_privacy.py --source webcam --effect pixelate
```

### Process Video File

```bash
python src/face_privacy.py --source video --input test/video_003.mp4 --output output/result.avi
```

### Create Demo Video (Side-by-Side Comparison)

```bash
python src/face_privacy.py --demo --input test/video_003.mp4 --output output/demo.avi
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--source` | Input source: `webcam`, `video`, `image` | `webcam` |
| `--input` | Path to input video/image file | `test/video_003.mp4` |
| `--output` | Path to save output file | `output/result.avi` |
| `--effect` | Privacy effect: `pixelate`, `blur`, `blackbox`, `emoji` | `pixelate` |
| `--intensity` | Effect intensity (5-50 for pixelation) | `15` |
| `--demo` | Create side-by-side comparison video | `False` |
| `--no-display` | Run without GUI display (save only) | `False` |
| `--fps` | Show FPS counter | `True` |

### Interactive Controls (Real-Time Mode)

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `s` | Save screenshot |
| `SPACE` | Toggle split view (before/after) |
| `+` / `-` | Increase/decrease effect intensity |
| `1-6` | Switch between effects |
| `h` | Show/hide help overlay |

## Examples

### Example 1: Privacy Protection for Social Media

```bash
# Process video with pixelation and save
python src/face_privacy.py --source video --input myvideo.mp4 --effect pixelate --intensity 15 --output protected_video.avi
```

### Example 2: Real-Time Demonstration

```bash
# Interactive webcam demo with blur effect
python src/face_privacy.py --source webcam --effect blur --intensity 20
```

### Example 3: Batch Image Processing

```bash
# Process single image
python src/face_privacy.py --source image --input photo.jpg --output protected_photo.jpg --effect blackbox
```

## Project Structure

```
face_privacy_protection/
├── assets/                    # Demo GIFs and screenshots
├── src/
│   ├── face_privacy.py       # Main CLI application
│   ├── detectors.py          # YOLOv11-Face detector implementation
│   └── effects.py            # Privacy effect implementations
├── models/                    # Auto-downloaded YOLO models
├── test/                      # Sample videos and images
├── output/                    # Generated output files
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Performance Benchmarks

Tested on consumer hardware (Intel i5-1135G7, 16GB RAM):

| Operation | FPS | Latency |
|-----------|-----|---------|
| Face Detection (YOLOv11s) | ~45 | ~22ms |
| Detection + Pixelation | ~40 | ~25ms |
| Detection + Blur | ~35 | ~28ms |
| Video Processing (offline) | ~30 | ~33ms |

## Technical Details

### Face Detection

The project uses **YOLOv11s-Face**, a specialized variant of YOLO optimized for face detection. Key advantages:

- High accuracy across multiple face angles (profile, 3/4, frontal)
- Robust performance in varying lighting conditions
- Real-time inference on CPU
- Superior detection of partially occluded faces

### Privacy Effects

**Pixelation**: Block-based downsampling preserving face area shape while preventing recognition.

**Blur**: Gaussian blur with configurable kernel size for softer anonymization.

**Black Box**: Complete face region masking for maximum privacy.

**Emoji Overlay**: Playful anonymization using emoji graphics.

## Use Cases

### GDPR Compliance
Automatically anonymize faces in surveillance footage or user-generated content before storage or processing.

### Dataset Creation
Generate anonymized datasets for machine learning research while preserving scene context and body poses.

### Content Moderation
Real-time privacy protection for live streaming platforms or video conferencing applications.

### Medical Privacy
Protect patient identities in medical imaging or clinical documentation.

## Troubleshooting

### Model Not Found
If you see "YOLOv11-face model not found", ensure the `models/` directory exists. The model downloads automatically on first run.

### Camera Access Error
- Close other applications using the webcam
- Check camera permissions in your OS settings
- Try specifying camera index: modify `cv2.VideoCapture(0)` to use a different camera

### Video Codec Issues
The default output format is AVI (XVID codec) for Windows compatibility. To use MP4:
- Install ffmpeg
- Change codec in `config.py` to `mp4v`

### Low FPS Performance
- Reduce input resolution in `config.py`
- Lower confidence threshold to reduce processing
- Use `--no-display` flag for headless processing

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Ultralytics** - YOLOv11 model and framework
- **OpenCV** - Computer vision library
- **PyTorch** - Deep learning framework

## Citation

If you use this project in your research or application, please cite:

```bibtex
@software{face_privacy_protection,
  title = {Face Privacy Protection with YOLOv11-Face},
  author = {Rodrigo Schaab},
  year = {2026},
  url = {https://github.com/roscha10/face_privacy_protection}
}
```

## Contact

For questions, issues, or collaboration opportunities:

- **GitHub Issues**: [Report a bug](https://github.com/roscha10/face_privacy_protection/issues)
- **LinkedIn**: [Rodrigo Schaab](https://linkedin.com/in/rodrigo-schaab)

---

**⭐ Star this repository if you find it useful!**
