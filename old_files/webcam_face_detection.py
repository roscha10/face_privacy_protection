"""
Real-time face/person detection using YOLO26 from webcam.
Press 'q' to quit, 's' to save screenshot.
"""
import cv2
import time
from utils import load_yolo_model, open_camera, get_face_detections, draw_face_box, display_fps


def main():
    """Run real-time detection from webcam."""
    print("=" * 50)
    print("YOLO26 Real-Time Detection")
    print("=" * 50)

    # Load YOLO26 model (nano version for speed)
    model = load_yolo_model("yolo26n.pt")
    if model is None:
        return

    # Open webcam
    cap = open_camera(0)
    if cap is None:
        return

    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot")
    print("\nStarting detection...\n")

    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to read frame")
            break

        # Get detections
        detections = get_face_detections(model, frame, conf_threshold=0.25)

        # Draw boxes
        for x1, y1, x2, y2, conf in detections:
            label = f"Person {conf:.2f}"
            draw_face_box(frame, x1, y1, x2, y2, label=label)

        # Calculate and display FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            frame_count = 0
            start_time = time.time()
        else:
            fps = 30.0

        display_fps(frame, fps)

        # Show frame
        cv2.imshow("YOLO26 - Real-Time Detection (Press 'q' to quit)", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n✓ Exiting...")
            break
        elif key == ord('s'):
            filename = f"output/screenshot_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Screenshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("✓ Done!")


if __name__ == "__main__":
    main()
