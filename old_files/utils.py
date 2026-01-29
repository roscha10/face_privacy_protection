"""
Utility functions for face detection project using YOLO26.
"""
import cv2
import numpy as np
from ultralytics import YOLO


def load_yolo_model(model_name="yolo26n.pt", task="detect"):
    """
    Load YOLO26 model.

    Args:
        model_name: Model variant (yolo26n.pt, yolo26s.pt, yolo26m.pt, yolo26l.pt, yolo26x.pt)
        task: Task type (detect, segment, pose, classify)

    Returns:
        YOLO model instance
    """
    try:
        model = YOLO(model_name)
        print(f"✓ YOLO26 model '{model_name}' loaded successfully")
        return model
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return None


def pixelate_face(img, x1, y1, x2, y2, pixelation=15):
    """
    Apply pixelation effect to face region.

    Args:
        img: Input image (numpy array)
        x1, y1: Top-left corner coordinates
        x2, y2: Bottom-right corner coordinates
        pixelation: Pixelation level (lower = more pixelated)

    Returns:
        Image with pixelated face region
    """
    h, w = img.shape[:2]
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(w - 1, int(x2))
    y2 = min(h - 1, int(y2))

    face_region = img[y1:y2, x1:x2]

    if face_region.size == 0:
        return img

    temp = cv2.resize(face_region, (pixelation, pixelation), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(temp, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)

    img[y1:y2, x1:x2] = pixelated
    return img


def blur_face(img, x1, y1, x2, y2, blur_strength=51):
    """
    Apply blur effect to face region.

    Args:
        img: Input image (numpy array)
        x1, y1: Top-left corner coordinates
        x2, y2: Bottom-right corner coordinates
        blur_strength: Kernel size for blur (must be odd)

    Returns:
        Image with blurred face region
    """
    h, w = img.shape[:2]
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(w - 1, int(x2))
    y2 = min(h - 1, int(y2))

    face_region = img[y1:y2, x1:x2]

    if face_region.size == 0:
        return img

    if blur_strength % 2 == 0:
        blur_strength += 1

    blurred = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 0)
    img[y1:y2, x1:x2] = blurred

    return img


def draw_face_box(img, x1, y1, x2, y2, label="", color=(0, 255, 0), thickness=2):
    """
    Draw bounding box around face with optional label.

    Args:
        img: Input image (numpy array)
        x1, y1: Top-left corner coordinates
        x2, y2: Bottom-right corner coordinates
        label: Text to display above box
        color: Box color in BGR format
        thickness: Line thickness

    Returns:
        Image with drawn box
    """
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

    if label:
        cv2.putText(
            img, label,
            (int(x1), max(int(y1) - 10, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8, color, thickness, cv2.LINE_AA
        )

    return img


def get_face_detections(model, frame, conf_threshold=0.25):
    """
    Get face/person detections from YOLO26 model.

    Args:
        model: YOLO model instance
        frame: Input frame
        conf_threshold: Confidence threshold for detections

    Returns:
        List of detection boxes [(x1, y1, x2, y2, conf), ...]
    """
    results = model.predict(frame, conf=conf_threshold, verbose=False)
    boxes = results[0].boxes

    detections = []
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0][:4].tolist()
        conf = box.conf[0].item()
        detections.append((x1, y1, x2, y2, conf))

    return detections


def open_camera(camera_id=0):
    """
    Open webcam with error handling.

    Args:
        camera_id: Camera device ID (0 for default)

    Returns:
        VideoCapture object or None if failed
    """
    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print(f"✗ Could not open camera {camera_id}")
        return None

    print(f"✓ Camera {camera_id} opened successfully")
    return cap


def display_fps(img, fps, position=(10, 30)):
    """
    Display FPS counter on image.

    Args:
        img: Input image
        fps: FPS value to display
        position: Text position (x, y)

    Returns:
        Image with FPS text
    """
    text = f"FPS: {fps:.1f}"
    cv2.putText(
        img, text, position,
        cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 0), 2, cv2.LINE_AA
    )
    return img
