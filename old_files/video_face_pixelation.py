"""
Process video files to pixelate faces using YOLO26.
Creates side-by-side comparison of original and pixelated video.
"""
import cv2
import numpy as np
import os
from utils import load_yolo_model, pixelate_face, get_face_detections


def process_video(input_video="test/video_005.mp4", output_video="output/pixelated_output.mp4",
                  display_width=480, display_height=480, pixelation_level=15):
    """
    Process video file and pixelate detected faces.

    Args:
        input_video: Path to input video file
        output_video: Path to save output video
        display_width: Width for display/output
        display_height: Height for display/output
        pixelation_level: Level of pixelation to apply
    """
    print("=" * 50)
    print("YOLO26 Video Face Pixelation")
    print("=" * 50)

    # Load YOLO26 model
    model = load_yolo_model("yolo26n.pt")
    if model is None:
        return

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Open video file
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"✗ Could not open video: {input_video}")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"\n✓ Video loaded: {input_video}")
    print(f"  Total frames: {total_frames}")
    print(f"  FPS: {fps:.2f}")

    # Setup video writer (side-by-side comparison)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (display_width * 2, display_height))

    print(f"\nProcessing video...")
    print("Press 'q' to stop processing\n")

    frame_num = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1

        # Resize frame
        original_frame = cv2.resize(frame, (display_width, display_height))
        pixelated_frame = original_frame.copy()

        # Detect faces
        detections = get_face_detections(model, pixelated_frame, conf_threshold=0.25)

        # Apply pixelation to detected faces
        for x1, y1, x2, y2, conf in detections:
            pixelated_frame = pixelate_face(pixelated_frame, x1, y1, x2, y2,
                                           pixelation=pixelation_level)

        # Combine frames side-by-side
        combined_frame = np.hstack((original_frame, pixelated_frame))

        # Add labels
        cv2.putText(combined_frame, "Original", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(combined_frame, "Pixelated", (display_width + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Write to output
        out.write(combined_frame)

        # Display progress
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"Progress: {progress:.1f}% ({frame_num}/{total_frames} frames)")

        # Show preview
        cv2.imshow("Processing Video (Press 'q' to stop)", combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n✗ Processing stopped by user")
            break

    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    if frame_num == total_frames:
        print(f"\n✓ Video processed successfully!")
        print(f"✓ Output saved to: {output_video}")
    else:
        print(f"\n⚠ Partial processing completed ({frame_num}/{total_frames} frames)")


def main():
    """Main function with example usage."""
    # Example: Process default video
    process_video(
        input_video="test/video_005.mp4",
        output_video="output/pixelated_output.mp4",
        pixelation_level=15
    )


if __name__ == "__main__":
    main()
