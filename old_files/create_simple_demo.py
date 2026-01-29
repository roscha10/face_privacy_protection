"""
Create simple LinkedIn demo video using YOLOv11-Face (the one that works best).
Shows side-by-side comparison: Original vs Pixelated
"""
import cv2
import numpy as np
import time
from face_detectors import YOLOFaceDetector
from utils import pixelate_face


def add_label(frame, text, position='top', color=(0, 255, 255)):
    """Add label to frame with semi-transparent background."""
    h, w = frame.shape[:2]

    # Semi-transparent background
    overlay = frame.copy()
    if position == 'top':
        cv2.rectangle(overlay, (0, 0), (w, 60), (20, 20, 20), -1)
    else:
        cv2.rectangle(overlay, (0, h-60), (w, h), (20, 20, 20), -1)

    frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

    # Text
    y_pos = 40 if position == 'top' else h - 20
    cv2.putText(frame, text, (20, y_pos),
                cv2.FONT_HERSHEY_DUPLEX, 1.2, color, 2, cv2.LINE_AA)

    return frame


def process_video_simple(input_video="test/video_003.mp4", output_video="output/linkedin_simple.avi"):
    """
    Create simple side-by-side comparison video.

    Layout:
    ┌─────────────────┬─────────────────┐
    │    ORIGINAL     │    PROTECTED    │
    │                 │  (YOLOv11-Face) │
    └─────────────────┴─────────────────┘
    """
    print("=" * 60)
    print("Creating Simple LinkedIn Demo Video")
    print("=" * 60)

    # Initialize YOLO detector
    print("\nLoading YOLOv11-Face detector...")
    yolo_detector = YOLOFaceDetector()

    if yolo_detector.model is None:
        print("✗ YOLOv11-face model not found!")
        print("  Please ensure models/yolov11s-face.pt exists")
        return

    # Open video
    print(f"\nOpening video: {input_video}")
    cap = cv2.VideoCapture(input_video)

    if not cap.isOpened():
        print(f"✗ Could not open video: {input_video}")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"✓ Video loaded:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps:.2f}")
    print(f"  Total frames: {total_frames}")

    # Set output resolution (each panel)
    panel_width = 640
    panel_height = 480

    # Setup video writer (side by side)
    output_width = panel_width * 2
    output_height = panel_height

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, fps, (output_width, output_height + 100))

    print(f"\nProcessing video...")
    print(f"Output: {output_video}")
    print(f"Output resolution: {output_width}x{output_height + 100}")
    print("\nProgress:")

    frame_num = 0
    start_time = time.time()
    pixelation_level = 12
    total_faces_detected = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1

        # Resize frame
        frame = cv2.resize(frame, (panel_width, panel_height))

        # Create copies
        frame_original = frame.copy()
        frame_protected = frame.copy()

        # Detect and pixelate with YOLO
        detections = yolo_detector.detect(frame, conf_threshold=0.4)
        total_faces_detected += len(detections)

        for x1, y1, x2, y2, conf in detections:
            frame_protected = pixelate_face(frame_protected, x1, y1, x2, y2, pixelation_level)

        # Add labels
        frame_original = add_label(frame_original, "ORIGINAL", color=(255, 255, 255))
        frame_protected = add_label(frame_protected, "FACE PRIVACY PROTECTION", color=(0, 255, 255))

        # Add detection info to protected frame
        info_text = f"YOLOv11-Face | Faces: {len(detections)}"
        cv2.putText(frame_protected, info_text, (20, panel_height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

        # Combine side by side
        combined = np.hstack((frame_original, frame_protected))

        # Add title bar
        title_bar = np.zeros((100, output_width, 3), dtype=np.uint8)
        title_bar[:] = (20, 20, 20)

        cv2.putText(title_bar, "Real-Time Face Privacy Protection", (30, 45),
                    cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(title_bar, "AI-Powered Anonymization with YOLOv11", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2, cv2.LINE_AA)

        # Combine with title
        final_frame = np.vstack((title_bar, combined))

        # Write frame
        out.write(final_frame)

        # Progress update
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            elapsed = time.time() - start_time
            fps_processing = frame_num / elapsed
            eta = (total_frames - frame_num) / fps_processing if fps_processing > 0 else 0

            print(f"  Frame {frame_num}/{total_frames} ({progress:.1f}%) - "
                  f"Processing: {fps_processing:.1f} FPS - ETA: {eta:.0f}s - "
                  f"Faces detected: {total_faces_detected}")

    # Cleanup
    cap.release()
    out.release()

    elapsed_total = time.time() - start_time
    avg_faces_per_frame = total_faces_detected / frame_num if frame_num > 0 else 0

    print("\n" + "=" * 60)
    print("✓ Video processing completed!")
    print("=" * 60)
    print(f"Output file: {output_video}")
    print(f"Frames processed: {frame_num}")
    print(f"Total faces detected: {total_faces_detected}")
    print(f"Average faces per frame: {avg_faces_per_frame:.2f}")
    print(f"Total time: {elapsed_total:.1f}s")
    print(f"Average FPS: {frame_num/elapsed_total:.1f}")
    print("\n🎬 Video ready for LinkedIn!")


def main():
    """Main function."""
    import os

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Process video
    process_video_simple(
        input_video="test/video_003.mp4",
        output_video="output/linkedin_demo_simple.avi"
    )

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Check the video: output/linkedin_demo_simple.avi")
    print("2. Upload to LinkedIn")
    print("3. Use post template from LINKEDIN_POST.md")
    print("\n💡 Tip: Mention in your post that YOLOv11-Face was chosen")
    print("   for its superior performance in detecting faces at")
    print("   multiple angles and lighting conditions!")
    print("\nReady to showcase your AI skills! 🚀")


if __name__ == "__main__":
    main()
