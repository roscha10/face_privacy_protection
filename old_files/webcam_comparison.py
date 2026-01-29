"""
Real-time comparison of face detection methods.
Compare YOLOv11-face, MediaPipe, and OpenCV Haar Cascades side-by-side.
"""
import cv2
import numpy as np
import time
from face_detectors import YOLOFaceDetector, MediaPipeFaceDetector, HaarCascadeFaceDetector
from utils import open_camera, pixelate_face


def draw_detections(frame, detections, color, label_prefix=""):
    """Draw bounding boxes on frame."""
    for x1, y1, x2, y2, conf in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{label_prefix}{conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame


def add_info_overlay(frame, detector_name, fps, num_detections, color):
    """Add information overlay to frame."""
    h, w = frame.shape[:2]

    # Semi-transparent overlay at top
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    # Detector name
    cv2.putText(frame, detector_name, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Detection count
    cv2.putText(frame, f"Faces: {num_detections}", (w - 150, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    return frame


def main():
    """Run side-by-side comparison of face detectors."""
    print("=" * 60)
    print("Face Detection Methods Comparison")
    print("=" * 60)

    # Initialize detectors
    print("\nInitializing detectors...")
    yolo_detector = YOLOFaceDetector()
    mediapipe_detector = MediaPipeFaceDetector()
    haar_detector = HaarCascadeFaceDetector()

    # Open webcam
    cap = open_camera(0)
    if cap is None:
        return

    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot comparison")
    print("  'b' - Toggle benchmark stats")
    print("  'p' - Toggle pixelation mode")
    print("\nStarting comparison...\n")

    # Settings
    conf_threshold = 0.5
    show_benchmark = False
    pixelate_mode = False

    # Colors for each detector (BGR)
    colors = {
        'yolo': (0, 255, 0),      # Green
        'mediapipe': (255, 0, 0),  # Blue
        'haar': (0, 165, 255)      # Orange
    }

    # FPS tracking
    fps_counters = {'yolo': 30.0, 'mediapipe': 30.0, 'haar': 30.0}
    frame_times = {'yolo': [], 'mediapipe': [], 'haar': []}

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to read frame")
            break

        # Resize for faster processing
        display_height = 480
        aspect_ratio = frame.shape[1] / frame.shape[0]
        display_width = int(display_height * aspect_ratio)
        frame = cv2.resize(frame, (display_width, display_height))

        # Create 3 copies for each detector
        frame_yolo = frame.copy()
        frame_mediapipe = frame.copy()
        frame_haar = frame.copy()

        # YOLOv11-face detection
        start = time.time()
        yolo_detections = yolo_detector.detect(frame, conf_threshold)
        yolo_time = (time.time() - start) * 1000
        frame_times['yolo'].append(yolo_time)

        if pixelate_mode:
            for x1, y1, x2, y2, conf in yolo_detections:
                frame_yolo = pixelate_face(frame_yolo, x1, y1, x2, y2, pixelation=15)
        else:
            frame_yolo = draw_detections(frame_yolo, yolo_detections, colors['yolo'])

        # MediaPipe detection
        start = time.time()
        mediapipe_detections = mediapipe_detector.detect(frame, conf_threshold)
        mediapipe_time = (time.time() - start) * 1000
        frame_times['mediapipe'].append(mediapipe_time)

        if pixelate_mode:
            for x1, y1, x2, y2, conf in mediapipe_detections:
                frame_mediapipe = pixelate_face(frame_mediapipe, x1, y1, x2, y2, pixelation=15)
        else:
            frame_mediapipe = draw_detections(frame_mediapipe, mediapipe_detections, colors['mediapipe'])

        # Haar Cascade detection
        start = time.time()
        haar_detections = haar_detector.detect(frame, conf_threshold)
        haar_time = (time.time() - start) * 1000
        frame_times['haar'].append(haar_time)

        if pixelate_mode:
            for x1, y1, x2, y2, conf in haar_detections:
                frame_haar = pixelate_face(frame_haar, x1, y1, x2, y2, pixelation=15)
        else:
            frame_haar = draw_detections(frame_haar, haar_detections, colors['haar'])

        # Calculate FPS (update every 30 frames)
        if frame_count % 30 == 0 and len(frame_times['yolo']) > 0:
            fps_counters['yolo'] = 1000 / np.mean(frame_times['yolo'][-30:])
            fps_counters['mediapipe'] = 1000 / np.mean(frame_times['mediapipe'][-30:])
            fps_counters['haar'] = 1000 / np.mean(frame_times['haar'][-30:])

        # Add overlays
        frame_yolo = add_info_overlay(frame_yolo, "YOLOv11-Face",
                                      fps_counters['yolo'], len(yolo_detections), colors['yolo'])
        frame_mediapipe = add_info_overlay(frame_mediapipe, "MediaPipe",
                                           fps_counters['mediapipe'], len(mediapipe_detections), colors['mediapipe'])
        frame_haar = add_info_overlay(frame_haar, "OpenCV Haar",
                                       fps_counters['haar'], len(haar_detections), colors['haar'])

        # Combine frames horizontally
        top_row = np.hstack((frame_yolo, frame_mediapipe))
        bottom_row = np.hstack((frame_haar, frame.copy()))  # Original in bottom right

        # Add label to original
        cv2.putText(bottom_row, "Original", (display_width + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        combined = np.vstack((top_row, bottom_row))

        # Add benchmark stats if enabled
        if show_benchmark:
            stats_y = combined.shape[0] - 120
            cv2.rectangle(combined, (0, stats_y), (combined.shape[1], combined.shape[0]), (0, 0, 0), -1)

            stats_text = [
                f"YOLO: {fps_counters['yolo']:.1f} FPS ({np.mean(frame_times['yolo'][-30:]):.1f}ms)",
                f"MediaPipe: {fps_counters['mediapipe']:.1f} FPS ({np.mean(frame_times['mediapipe'][-30:]):.1f}ms)",
                f"Haar: {fps_counters['haar']:.1f} FPS ({np.mean(frame_times['haar'][-30:]):.1f}ms)"
            ]

            for i, text in enumerate(stats_text):
                cv2.putText(combined, text, (10, stats_y + 30 + i * 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show combined view
        cv2.imshow("Face Detection Comparison (Press 'q' to quit)", combined)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n✓ Exiting...")
            break
        elif key == ord('s'):
            filename = f"output/comparison_{int(time.time())}.jpg"
            cv2.imwrite(filename, combined)
            print(f"✓ Screenshot saved: {filename}")
        elif key == ord('b'):
            show_benchmark = not show_benchmark
            print(f"Benchmark stats: {'ON' if show_benchmark else 'OFF'}")
        elif key == ord('p'):
            pixelate_mode = not pixelate_mode
            print(f"Pixelation mode: {'ON' if pixelate_mode else 'OFF'}")

        frame_count += 1

    # Print final statistics
    print("\n" + "=" * 60)
    print("Final Statistics")
    print("=" * 60)

    for name, times in frame_times.items():
        if len(times) > 0:
            avg_time = np.mean(times)
            avg_fps = 1000 / avg_time if avg_time > 0 else 0
            print(f"\n{name.upper()}:")
            print(f"  Average Time: {avg_time:.2f} ms")
            print(f"  Average FPS: {avg_fps:.1f}")

    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
