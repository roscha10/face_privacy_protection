"""
Create LinkedIn demo video comparing 3 face detection methods.
Shows 4 panels: Original + 3 pixelated versions (MediaPipe, YOLO, Haar)
"""
import cv2
import numpy as np
import time
from face_detectors import MediaPipeFaceDetector, YOLOFaceDetector, HaarCascadeFaceDetector
from utils import pixelate_face


def add_label(frame, text, position='top'):
    """Add label to frame."""
    h, w = frame.shape[:2]

    # Semi-transparent background
    overlay = frame.copy()
    if position == 'top':
        cv2.rectangle(overlay, (0, 0), (w, 50), (0, 0, 0), -1)
    else:
        cv2.rectangle(overlay, (0, h-50), (w, h), (0, 0, 0), -1)

    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    # Text
    y_pos = 35 if position == 'top' else h - 15
    cv2.putText(frame, text, (10, y_pos),
                cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 255), 2)

    return frame


def process_video(input_video="test/video_003.mp4", output_video="output/linkedin_demo.avi"):
    """
    Process video with 4 panels showing face pixelation comparison.

    Layout:
    ┌─────────────┬─────────────┐
    │  Original   │  MediaPipe  │
    ├─────────────┼─────────────┤
    │ YOLOv11     │  OpenCV     │
    └─────────────┴─────────────┘
    """
    print("=" * 60)
    print("Creating LinkedIn Demo Video")
    print("=" * 60)

    # Initialize detectors
    print("\nLoading face detectors...")
    mediapipe_detector = MediaPipeFaceDetector()
    yolo_detector = YOLOFaceDetector()
    haar_detector = HaarCascadeFaceDetector()

    # Check if YOLO model exists
    if yolo_detector.model is None:
        print("\n⚠ YOLOv11-face model not found!")
        print("  Continuing with MediaPipe and Haar only...")
        use_yolo = False
    else:
        use_yolo = True

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

    # Setup video writer (2x2 grid)
    output_width = panel_width * 2
    output_height = panel_height * 2

    # Use AVI with XVID codec (more compatible with Windows)
    output_video = output_video.replace('.mp4', '.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, fps, (output_width, output_height + 80))

    print(f"\nProcessing video...")
    print(f"Output: {output_video}")
    print(f"Output resolution: {output_width}x{output_height}")
    print("\nProgress:")

    frame_num = 0
    start_time = time.time()
    pixelation_level = 12

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1

        # Resize frame
        frame = cv2.resize(frame, (panel_width, panel_height))

        # Create 4 copies
        frame_original = frame.copy()
        frame_mediapipe = frame.copy()
        frame_yolo = frame.copy() if use_yolo else frame.copy()
        frame_haar = frame.copy()

        # Detect and pixelate with MediaPipe
        detections_mp = mediapipe_detector.detect(frame, conf_threshold=0.5)
        for x1, y1, x2, y2, conf in detections_mp:
            frame_mediapipe = pixelate_face(frame_mediapipe, x1, y1, x2, y2, pixelation_level)

        # Detect and pixelate with YOLO (if available)
        if use_yolo:
            detections_yolo = yolo_detector.detect(frame, conf_threshold=0.5)
            for x1, y1, x2, y2, conf in detections_yolo:
                frame_yolo = pixelate_face(frame_yolo, x1, y1, x2, y2, pixelation_level)

        # Detect and pixelate with Haar
        detections_haar = haar_detector.detect(frame, conf_threshold=0.5)
        for x1, y1, x2, y2, conf in detections_haar:
            frame_haar = pixelate_face(frame_haar, x1, y1, x2, y2, pixelation_level)

        # Add labels
        frame_original = add_label(frame_original, "ORIGINAL")
        frame_mediapipe = add_label(frame_mediapipe, "MediaPipe Face Detection")
        frame_yolo = add_label(frame_yolo, "YOLOv11-Face" if use_yolo else "YOLO (Not Available)")
        frame_haar = add_label(frame_haar, "OpenCV Haar Cascades")

        # Create 2x2 grid
        top_row = np.hstack((frame_original, frame_mediapipe))
        bottom_row = np.hstack((frame_yolo, frame_haar))
        combined = np.vstack((top_row, bottom_row))

        # Add title bar
        title_bar = np.zeros((80, output_width, 3), dtype=np.uint8)
        title_bar[:] = (20, 20, 20)
        cv2.putText(title_bar, "Face Privacy Protection - Method Comparison", (30, 50),
                    cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 255), 2)

        # Combine with title
        final_frame = np.vstack((title_bar, combined))

        # Resize to match output dimensions (if needed)
        if final_frame.shape[:2] != (output_height, output_width):
            final_frame = cv2.resize(final_frame, (output_width, output_height + 80))

        # Write frame
        out.write(final_frame)

        # Progress update
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            elapsed = time.time() - start_time
            fps_processing = frame_num / elapsed
            eta = (total_frames - frame_num) / fps_processing if fps_processing > 0 else 0

            print(f"  Frame {frame_num}/{total_frames} ({progress:.1f}%) - "
                  f"Processing: {fps_processing:.1f} FPS - ETA: {eta:.0f}s")

    # Cleanup
    cap.release()
    out.release()

    elapsed_total = time.time() - start_time

    print("\n" + "=" * 60)
    print("✓ Video processing completed!")
    print("=" * 60)
    print(f"Output file: {output_video}")
    print(f"Frames processed: {frame_num}")
    print(f"Total time: {elapsed_total:.1f}s")
    print(f"Average FPS: {frame_num/elapsed_total:.1f}")
    print("\n🎬 Video ready for LinkedIn!")


def main():
    """Main function."""
    import os

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Process video
    process_video(
        input_video="test/video_003.mp4",
        output_video="output/linkedin_demo.avi"
    )

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Check the video: output/linkedin_demo.mp4")
    print("2. Upload to LinkedIn")
    print("3. Use the suggested post template")
    print("\nReady to make an impact! 🚀")


if __name__ == "__main__":
    main()
