"""
Face detection implementations using different methods.
Comparison between YOLOv11-face, MediaPipe, and OpenCV Haar Cascades.
"""
import cv2
import numpy as np
import time
from pathlib import Path


class YOLOFaceDetector:
    """Face detection using YOLOv11 specialized face model."""

    def __init__(self, model_path="models/yolov11s-face.pt"):
        """Initialize YOLO face detector."""
        from ultralytics import YOLO

        self.name = "YOLOv11-Face"
        self.model_path = model_path

        if not Path(model_path).exists():
            print(f"⚠ Warning: {model_path} not found")
            print("   Download from: https://github.com/akanametov/yolo-face")
            self.model = None
        else:
            self.model = YOLO(model_path)
            print(f"✓ {self.name} loaded")

    def detect(self, frame, conf_threshold=0.5):
        """
        Detect faces in frame.

        Returns:
            list of tuples: [(x1, y1, x2, y2, confidence), ...]
        """
        if self.model is None:
            return []

        results = self.model.predict(frame, conf=conf_threshold, verbose=False)
        boxes = results[0].boxes

        detections = []
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0][:4].tolist()
            conf = box.conf[0].item()
            detections.append((int(x1), int(y1), int(x2), int(y2), conf))

        return detections


class MediaPipeFaceDetector:
    """Face detection using Google MediaPipe (New Tasks API)."""

    def __init__(self, min_detection_confidence=0.5):
        """Initialize MediaPipe face detector."""
        try:
            import mediapipe as mp
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            import urllib.request
            import os

            self.name = "MediaPipe"

            # Download model if not exists
            model_path = "models/blaze_face_short_range.tflite"
            os.makedirs("models", exist_ok=True)

            if not os.path.exists(model_path):
                print(f"  Downloading MediaPipe face detection model...")
                model_url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
                urllib.request.urlretrieve(model_url, model_path)
                print(f"  ✓ Model downloaded to {model_path}")

            # Create FaceDetector options
            base_options = python.BaseOptions(
                model_asset_path=model_path
            )
            options = vision.FaceDetectorOptions(
                base_options=base_options,
                min_detection_confidence=min_detection_confidence
            )

            # Create the detector
            self.detector = vision.FaceDetector.create_from_options(options)
            self.mp = mp
            print(f"✓ {self.name} loaded")

        except ImportError as e:
            print(f"✗ MediaPipe not installed or wrong version: {e}")
            print("  Run: pip install mediapipe")
            self.detector = None
        except Exception as e:
            print(f"✗ Error loading MediaPipe: {e}")
            self.detector = None

    def detect(self, frame, conf_threshold=0.5):
        """
        Detect faces in frame using new MediaPipe Tasks API.

        Returns:
            list of tuples: [(x1, y1, x2, y2, confidence), ...]
        """
        if self.detector is None:
            return []

        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create MediaPipe Image
            mp_image = self.mp.Image(
                image_format=self.mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            # Detect faces
            detection_result = self.detector.detect(mp_image)

            detections = []
            if detection_result.detections:
                h, w = frame.shape[:2]

                for detection in detection_result.detections:
                    bbox = detection.bounding_box

                    # Get coordinates (already in absolute pixels)
                    x1 = int(bbox.origin_x)
                    y1 = int(bbox.origin_y)
                    x2 = int(bbox.origin_x + bbox.width)
                    y2 = int(bbox.origin_y + bbox.height)

                    # Get confidence score
                    conf = detection.categories[0].score if detection.categories else 1.0

                    if conf >= conf_threshold:
                        detections.append((x1, y1, x2, y2, conf))

            return detections

        except Exception as e:
            print(f"Error in MediaPipe detection: {e}")
            return []


class HaarCascadeFaceDetector:
    """Face detection using OpenCV Haar Cascades (classic method)."""

    def __init__(self):
        """Initialize Haar Cascade face detector."""
        self.name = "OpenCV Haar"

        # Load pre-trained Haar Cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.cascade = cv2.CascadeClassifier(cascade_path)

        if self.cascade.empty():
            print(f"✗ Failed to load Haar Cascade from {cascade_path}")
        else:
            print(f"✓ {self.name} loaded")

    def detect(self, frame, conf_threshold=0.5):
        """
        Detect faces in frame.

        Returns:
            list of tuples: [(x1, y1, x2, y2, confidence), ...]
        """
        # Convert to grayscale (Haar works better on grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Haar doesn't provide confidence, so we use 1.0
        detections = []
        for (x, y, w, h) in faces:
            detections.append((x, y, x + w, y + h, 1.0))

        return detections


class FaceDetectorBenchmark:
    """Benchmark different face detection methods."""

    def __init__(self):
        """Initialize all detectors."""
        print("\nInitializing face detectors...")
        print("-" * 50)

        self.detectors = {
            'yolo': YOLOFaceDetector(),
            'mediapipe': MediaPipeFaceDetector(),
            'haar': HaarCascadeFaceDetector()
        }

        self.stats = {
            name: {'times': [], 'detections': []}
            for name in self.detectors.keys()
        }

    def benchmark_frame(self, frame, conf_threshold=0.5):
        """
        Run all detectors on a frame and collect stats.

        Returns:
            dict: {detector_name: (detections, time_ms)}
        """
        results = {}

        for name, detector in self.detectors.items():
            start = time.time()
            detections = detector.detect(frame, conf_threshold)
            elapsed = (time.time() - start) * 1000  # Convert to ms

            self.stats[name]['times'].append(elapsed)
            self.stats[name]['detections'].append(len(detections))

            results[name] = (detections, elapsed)

        return results

    def get_stats(self):
        """Get average statistics for all detectors."""
        stats = {}

        for name, data in self.stats.items():
            if len(data['times']) > 0:
                stats[name] = {
                    'avg_time_ms': np.mean(data['times']),
                    'avg_fps': 1000 / np.mean(data['times']) if np.mean(data['times']) > 0 else 0,
                    'avg_detections': np.mean(data['detections']),
                    'total_frames': len(data['times'])
                }

        return stats

    def print_stats(self):
        """Print benchmark statistics."""
        stats = self.get_stats()

        print("\n" + "=" * 60)
        print("Face Detection Benchmark Results")
        print("=" * 60)

        for name, data in stats.items():
            detector_name = self.detectors[name].name
            print(f"\n{detector_name}:")
            print(f"  Average Time: {data['avg_time_ms']:.2f} ms")
            print(f"  Average FPS: {data['avg_fps']:.1f}")
            print(f"  Average Detections: {data['avg_detections']:.1f}")
            print(f"  Total Frames: {data['total_frames']}")
