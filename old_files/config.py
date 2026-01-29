"""
Configuration file for YOLO26 Face Detection Project.
Centralized settings for models, paths, and parameters.
"""
import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
TEST_DIR = os.path.join(PROJECT_ROOT, "test")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# YOLO26 Model Configuration
YOLO_MODEL_VARIANTS = {
    "nano": "yolo26n.pt",      # Fastest, good accuracy
    "small": "yolo26s.pt",     # Balanced speed/accuracy
    "medium": "yolo26m.pt",    # Better accuracy
    "large": "yolo26l.pt",     # High accuracy
    "xlarge": "yolo26x.pt",    # Best accuracy
}

# Default model (change to 's', 'm', 'l', or 'x' for better accuracy)
DEFAULT_YOLO_MODEL = YOLO_MODEL_VARIANTS["nano"]

# Detection Parameters
DETECTION_CONF_THRESHOLD = 0.25  # Confidence threshold (0.0-1.0)
DETECTION_IOU_THRESHOLD = 0.45   # IoU threshold for NMS

# Age Prediction Model
AGE_MODEL_NAME = "nateraw/vit-age-classifier"

# Video Processing Settings
VIDEO_RESIZE_WIDTH = 480
VIDEO_RESIZE_HEIGHT = 480
VIDEO_CODEC = "mp4v"  # or 'XVID' for .avi

# Privacy Effect Settings
DEFAULT_PIXELATION_LEVEL = 15    # Lower = more pixelated
DEFAULT_BLUR_STRENGTH = 45       # Must be odd number
MIN_PIXELATION = 5
MAX_PIXELATION = 50

# Display Settings
SHOW_FPS = True
SHOW_CONFIDENCE = True
BOX_COLOR = (0, 255, 0)          # Green in BGR
BOX_THICKNESS = 2
FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_THICKNESS = 2

# Camera Settings
DEFAULT_CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Performance Settings
USE_GPU = True  # Set to False to force CPU
FPS_UPDATE_INTERVAL = 30  # Update FPS every N frames

# Output Settings
SCREENSHOT_PREFIX = "screenshot"
VIDEO_OUTPUT_PREFIX = "processed"
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Debug Settings
VERBOSE = False
SHOW_WARNINGS = True

# UI Text
APP_TITLE = "YOLO26 Face Detection Project"
APP_SUBTITLE = "Real-Time AI Face Detection & Processing"
VERSION = "1.0.0"

# Color Schemes (BGR format)
COLORS = {
    "green": (0, 255, 0),
    "red": (0, 0, 255),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}
