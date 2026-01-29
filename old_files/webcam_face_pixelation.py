"""
Real-time face pixelation using face-specific detectors.
Supports MediaPipe, YOLOv11-face, and OpenCV Haar Cascades.
Press 'q' to quit, '+/-' to adjust pixelation level, 'b' to toggle blur mode.
"""
import cv2
import time
from face_detectors import MediaPipeFaceDetector, YOLOFaceDetector, HaarCascadeFaceDetector
from utils import open_camera, pixelate_face, blur_face, display_fps


def main(detector_type='mediapipe'):
    """
    Run real-time face pixelation from webcam.

    Args:
        detector_type: 'mediapipe', 'yolo', or 'haar'
    """
    print("=" * 50)
    print("Real-Time Face Pixelation/Blur")
    print("=" * 50)

    # Load face detector based on type
    print(f"\nLoading {detector_type} detector...")
    if detector_type == 'mediapipe':
        detector = MediaPipeFaceDetector()
    elif detector_type == 'yolo':
        detector = YOLOFaceDetector()
    elif detector_type == 'haar':
        detector = HaarCascadeFaceDetector()
    else:
        print(f"✗ Unknown detector type: {detector_type}")
        print("  Available: 'mediapipe', 'yolo', 'haar'")
        return

    # Open webcam
    cap = open_camera(0)
    if cap is None:
        return

    print("\nControls:")
    print("  'q' - Quit")
    print("  '+' - Increase pixelation")
    print("  '-' - Decrease pixelation")
    print("  'b' - Toggle blur mode")
    print("  's' - Save screenshot")
    print("  'd' - Switch detector")
    print("\nStarting pixelation...\n")

    pixelation_level = 15
    blur_mode = False
    frame_count = 0
    start_time = time.time()
    current_detector_type = detector_type

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to read frame")
            break

        # Get face detections (only faces, not full bodies)
        detections = detector.detect(frame, conf_threshold=0.5)

        # Apply effect to each detected face
        for x1, y1, x2, y2, conf in detections:
            if blur_mode:
                frame = blur_face(frame, x1, y1, x2, y2, blur_strength=pixelation_level * 3)
            else:
                frame = pixelate_face(frame, x1, y1, x2, y2, pixelation=pixelation_level)

        # Calculate FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            frame_count = 0
            start_time = time.time()
        else:
            fps = 30.0

        # Display info
        display_fps(frame, fps)
        mode_text = f"Mode: {'Blur' if blur_mode else 'Pixelation'} | Level: {pixelation_level}"
        cv2.putText(frame, mode_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("YOLO26 - Face Privacy (Press 'q' to quit)", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n✓ Exiting...")
            break
        elif key == ord('+') or key == ord('='):
            pixelation_level = min(50, pixelation_level + 5)
            print(f"Pixelation level: {pixelation_level}")
        elif key == ord('-') or key == ord('_'):
            pixelation_level = max(5, pixelation_level - 5)
            print(f"Pixelation level: {pixelation_level}")
        elif key == ord('b'):
            blur_mode = not blur_mode
            print(f"Mode: {'Blur' if blur_mode else 'Pixelation'}")
        elif key == ord('s'):
            filename = f"output/pixelated_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Screenshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("✓ Done!")


if __name__ == "__main__":
    main()
