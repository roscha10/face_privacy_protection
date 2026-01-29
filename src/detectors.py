"""
Face Detection Module

Implements face detection using YOLOv11-Face model from Ultralytics.
The model is optimized for detecting faces at various angles and lighting conditions.
"""

import os
import cv2
import numpy as np
from pathlib import Path


class YOLOFaceDetector:
    """
    YOLOv11-Face detector for robust face detection.

    This detector uses the YOLOv11s-face model which provides:
    - High accuracy across multiple face angles (frontal, profile, 3/4)
    - Real-time performance on CPU (~45 FPS)
    - Robust detection in varying lighting conditions
    - Superior handling of partially occluded faces
    """

    def __init__(self, model_path="models/yolov11s-face.pt", conf_threshold=0.5):
        """
        Initialize YOLO face detector.

        Args:
            model_path (str): Path to YOLOv11s-face model file
            conf_threshold (float): Confidence threshold for detections (0-1)
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None

        self._load_model()

    def _load_model(self):
        """Load the YOLO model. Downloads if not present."""
        try:
            from ultralytics import YOLO

            # Check if model exists
            if os.path.exists(self.model_path):
                print(f"Loading YOLOv11-Face model from {self.model_path}")
                self.model = YOLO(self.model_path)
                print("Model loaded successfully!")
            else:
                print(f"Model not found at {self.model_path}")
                print("Please ensure the YOLOv11s-face.pt model is in the models/ directory")
                print("\nYou can download specialized face detection models from:")
                print("  https://github.com/akanametov/yolo-face")
                print("  https://github.com/derronqi/yolov8-face")
                self.model = None

        except ImportError:
            print("Error: ultralytics package not installed")
            print("Install with: pip install ultralytics")
            self.model = None
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            self.model = None

    def detect(self, frame, conf_threshold=None):
        """
        Detect faces in a frame.

        Args:
            frame (numpy.ndarray): Input image/frame (BGR format)
            conf_threshold (float, optional): Override default confidence threshold

        Returns:
            list: List of detections [(x1, y1, x2, y2, confidence), ...]
                  Returns empty list if no faces detected or model not loaded
        """
        if self.model is None:
            return []

        threshold = conf_threshold if conf_threshold is not None else self.conf_threshold

        try:
            # Run inference
            results = self.model(frame, conf=threshold, verbose=False)

            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())

                    # Convert to integers
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    # Ensure coordinates are within frame boundaries
                    h, w = frame.shape[:2]
                    x1 = max(0, min(x1, w))
                    y1 = max(0, min(y1, h))
                    x2 = max(0, min(x2, w))
                    y2 = max(0, min(y2, h))

                    detections.append((x1, y1, x2, y2, confidence))

            return detections

        except Exception as e:
            print(f"Error during detection: {e}")
            return []

    def get_model_info(self):
        """
        Get information about the loaded model.

        Returns:
            dict: Model information including path, type, and status
        """
        return {
            'model_path': self.model_path,
            'model_type': 'YOLOv11s-Face',
            'loaded': self.model is not None,
            'conf_threshold': self.conf_threshold,
            'framework': 'Ultralytics YOLO (PyTorch)'
        }


class FaceDetector:
    """
    Generic face detector interface.
    Currently wraps YOLOFaceDetector but can be extended for other detectors.
    """

    def __init__(self, detector_type='yolo', **kwargs):
        """
        Initialize face detector.

        Args:
            detector_type (str): Type of detector ('yolo')
            **kwargs: Additional arguments passed to specific detector
        """
        if detector_type == 'yolo':
            self.detector = YOLOFaceDetector(**kwargs)
        else:
            raise ValueError(f"Unknown detector type: {detector_type}")

    def detect(self, frame, **kwargs):
        """Detect faces in frame."""
        return self.detector.detect(frame, **kwargs)

    def get_info(self):
        """Get detector information."""
        return self.detector.get_model_info()
