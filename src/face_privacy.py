"""
Face Privacy Protection - Main Application

Real-time face detection and privacy protection using YOLOv11-Face.
Supports webcam, video files, and image processing with multiple anonymization effects.

Usage:
    python src/face_privacy.py --source webcam --effect pixelate
    python src/face_privacy.py --source video --input myvideo.mp4 --output result.avi
    python src/face_privacy.py --demo --input test/video_003.mp4 --output demo.avi
"""

import cv2
import numpy as np
import argparse
import time
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.detectors import YOLOFaceDetector
from src.effects import apply_pixelation, apply_blur, apply_blackbox, apply_emoji


class FacePrivacyApp:
    """Main application class for face privacy protection."""

    def __init__(self, args):
        """Initialize the application with command-line arguments."""
        self.args = args
        self.detector = YOLOFaceDetector(conf_threshold=0.4)
        self.effect_map = {
            'pixelate': apply_pixelation,
            'blur': apply_blur,
            'blackbox': apply_blackbox,
            'emoji': apply_emoji
        }
        self.show_help = False
        self.split_view = False

    def run(self):
        """Run the application based on command-line arguments."""
        if self.args.demo:
            self.create_demo_video()
        elif self.args.source == 'webcam':
            self.process_webcam()
        elif self.args.source == 'video':
            self.process_video()
        elif self.args.source == 'image':
            self.process_image()
        else:
            print(f"Error: Unknown source '{self.args.source}'")
            sys.exit(1)

    def create_demo_video(self):
        """Create side-by-side comparison demo video (Original vs Protected)."""
        print("=" * 70)
        print("Creating Side-by-Side Demo Video")
        print("=" * 70)

        input_path = self.args.input
        output_path = self.args.output

        if not os.path.exists(input_path):
            print(f"Error: Input file not found: {input_path}")
            return

        # Open video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {input_path}")
            return

        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"\nInput Video: {input_path}")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps:.2f}")
        print(f"  Total frames: {total_frames}")

        # Set output dimensions
        panel_width = 640
        panel_height = 480
        output_width = panel_width * 2
        output_height = panel_height + 100  # Extra space for title bar

        # Create video writer
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

        print(f"\nOutput: {output_path}")
        print(f"Output resolution: {output_width}x{output_height}\n")
        print("Processing...")

        frame_num = 0
        start_time = time.time()
        total_faces = 0

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

            # Detect faces
            detections = self.detector.detect(frame)
            total_faces += len(detections)

            # Apply privacy effect to protected frame
            effect_func = self.effect_map.get(self.args.effect, apply_pixelation)
            for x1, y1, x2, y2, conf in detections:
                frame_protected = effect_func(frame_protected, x1, y1, x2, y2, self.args.intensity)

            # Add labels
            frame_original = self._add_label(frame_original, "ORIGINAL", (255, 255, 255))
            frame_protected = self._add_label(frame_protected, "PROTECTED", (0, 255, 255))

            # Add detection info
            info_text = f"YOLOv11-Face | Faces: {len(detections)}"
            cv2.putText(frame_protected, info_text, (20, panel_height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

            # Combine side by side
            combined = np.hstack((frame_original, frame_protected))

            # Create title bar
            title_bar = np.zeros((100, output_width, 3), dtype=np.uint8)
            title_bar[:] = (20, 20, 20)
            cv2.putText(title_bar, "Face Privacy Protection - YOLOv11", (30, 45),
                       cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 3, cv2.LINE_AA)
            cv2.putText(title_bar, "AI-Powered Real-Time Anonymization", (30, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2, cv2.LINE_AA)

            # Combine with title
            final_frame = np.vstack((title_bar, combined))

            # Write frame
            out.write(final_frame)

            # Progress update
            if frame_num % 30 == 0:
                progress = (frame_num / total_frames) * 100
                elapsed = time.time() - start_time
                fps_processing = frame_num / elapsed if elapsed > 0 else 0
                eta = (total_frames - frame_num) / fps_processing if fps_processing > 0 else 0

                print(f"  Frame {frame_num}/{total_frames} ({progress:.1f}%) - "
                      f"{fps_processing:.1f} FPS - ETA: {eta:.0f}s")

        # Cleanup
        cap.release()
        out.release()

        elapsed_total = time.time() - start_time
        avg_faces = total_faces / frame_num if frame_num > 0 else 0

        print("\n" + "=" * 70)
        print("Demo Video Created Successfully!")
        print("=" * 70)
        print(f"Output: {output_path}")
        print(f"Frames processed: {frame_num}")
        print(f"Total faces detected: {total_faces}")
        print(f"Average faces per frame: {avg_faces:.2f}")
        print(f"Processing time: {elapsed_total:.1f}s")
        print(f"Average FPS: {frame_num/elapsed_total:.1f}")
        print("\nVideo ready for sharing!")

    def process_webcam(self):
        """Process webcam feed with real-time face privacy protection."""
        print("=" * 70)
        print("Real-Time Face Privacy Protection")
        print("=" * 70)
        print("\nStarting webcam...")
        print("\nControls:")
        print("  q       - Quit")
        print("  s       - Save screenshot")
        print("  SPACE   - Toggle split view (before/after)")
        print("  +/-     - Increase/decrease effect intensity")
        print("  1-4     - Switch effect (1=pixelate, 2=blur, 3=blackbox, 4=emoji)")
        print("  h       - Show/hide this help\n")

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam")
            return

        # Set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        fps_start_time = time.time()
        fps_frame_count = 0
        fps_value = 0

        current_effect = self.args.effect
        intensity = self.args.intensity

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab frame")
                break

            frame_original = frame.copy()

            # Detect faces
            detections = self.detector.detect(frame)

            # Apply effect
            effect_func = self.effect_map.get(current_effect, apply_pixelation)
            for x1, y1, x2, y2, conf in detections:
                frame = effect_func(frame, x1, y1, x2, y2, intensity)

            # Calculate FPS
            fps_frame_count += 1
            if time.time() - fps_start_time >= 1.0:
                fps_value = fps_frame_count
                fps_frame_count = 0
                fps_start_time = time.time()

            # Display info
            if self.args.fps:
                self._draw_info_overlay(frame, len(detections), fps_value, current_effect, intensity)

            # Show help overlay
            if self.show_help:
                self._draw_help_overlay(frame)

            # Display frame (split view or single)
            if self.split_view:
                combined = np.hstack((cv2.resize(frame_original, (640, 480)),
                                     cv2.resize(frame, (640, 480))))
                cv2.imshow('Face Privacy Protection', combined)
            else:
                cv2.imshow('Face Privacy Protection', frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"output/screenshot_{timestamp}.jpg"
                os.makedirs('output', exist_ok=True)
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved: {filename}")
            elif key == ord(' '):
                self.split_view = not self.split_view
            elif key == ord('+') or key == ord('='):
                intensity = min(intensity + 2, 50)
                print(f"Intensity: {intensity}")
            elif key == ord('-') or key == ord('_'):
                intensity = max(intensity - 2, 5)
                print(f"Intensity: {intensity}")
            elif key == ord('1'):
                current_effect = 'pixelate'
                print(f"Effect: {current_effect}")
            elif key == ord('2'):
                current_effect = 'blur'
                print(f"Effect: {current_effect}")
            elif key == ord('3'):
                current_effect = 'blackbox'
                print(f"Effect: {current_effect}")
            elif key == ord('4'):
                current_effect = 'emoji'
                print(f"Effect: {current_effect}")
            elif key == ord('h'):
                self.show_help = not self.show_help

        cap.release()
        cv2.destroyAllWindows()
        print("\nWebcam session ended.")

    def process_video(self):
        """Process video file with face privacy protection."""
        print("=" * 70)
        print("Video File Processing")
        print("=" * 70)

        input_path = self.args.input
        output_path = self.args.output

        if not os.path.exists(input_path):
            print(f"Error: Input file not found: {input_path}")
            return

        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video: {input_path}")
            return

        # Get properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"\nInput: {input_path}")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps:.2f}")
        print(f"  Total frames: {total_frames}")

        # Create output
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        print(f"\nOutput: {output_path}")
        print("Processing...\n")

        frame_num = 0
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1

            # Detect and apply effect
            detections = self.detector.detect(frame)
            effect_func = self.effect_map.get(self.args.effect, apply_pixelation)

            for x1, y1, x2, y2, conf in detections:
                frame = effect_func(frame, x1, y1, x2, y2, self.args.intensity)

            # Write frame
            out.write(frame)

            # Show progress
            if frame_num % 30 == 0:
                progress = (frame_num / total_frames) * 100
                elapsed = time.time() - start_time
                fps_processing = frame_num / elapsed if elapsed > 0 else 0

                print(f"  Frame {frame_num}/{total_frames} ({progress:.1f}%) - {fps_processing:.1f} FPS")

        cap.release()
        out.release()

        elapsed = time.time() - start_time
        print("\n" + "=" * 70)
        print("Video Processing Complete!")
        print("=" * 70)
        print(f"Output: {output_path}")
        print(f"Frames: {frame_num}")
        print(f"Time: {elapsed:.1f}s")
        print(f"Average FPS: {frame_num/elapsed:.1f}")

    def process_image(self):
        """Process single image with face privacy protection."""
        print("=" * 70)
        print("Image Processing")
        print("=" * 70)

        input_path = self.args.input
        output_path = self.args.output

        if not os.path.exists(input_path):
            print(f"Error: Input file not found: {input_path}")
            return

        # Read image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Error: Could not read image: {input_path}")
            return

        print(f"\nInput: {input_path}")
        print(f"  Resolution: {image.shape[1]}x{image.shape[0]}")

        # Detect and apply effect
        detections = self.detector.detect(image)
        print(f"  Faces detected: {len(detections)}")

        effect_func = self.effect_map.get(self.args.effect, apply_pixelation)
        for x1, y1, x2, y2, conf in detections:
            image = effect_func(image, x1, y1, x2, y2, self.args.intensity)

        # Save output
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        cv2.imwrite(output_path, image)

        print(f"\nOutput: {output_path}")
        print("Image processing complete!")

        # Display if requested
        if not self.args.no_display:
            cv2.imshow('Face Privacy Protection', image)
            print("\nPress any key to close...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def _add_label(self, frame, text, color):
        """Add label with semi-transparent background to frame."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 60), (20, 20, 20), -1)
        frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)
        cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1.2, color, 2, cv2.LINE_AA)
        return frame

    def _draw_info_overlay(self, frame, face_count, fps, effect, intensity):
        """Draw information overlay on frame."""
        h, w = frame.shape[:2]

        # Semi-transparent panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Text
        y_pos = 35
        cv2.putText(frame, f"FPS: {fps}", (20, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        y_pos += 30
        cv2.putText(frame, f"Faces: {face_count}", (20, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_pos += 30
        cv2.putText(frame, f"Effect: {effect} ({intensity})", (20, y_pos),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def _draw_help_overlay(self, frame):
        """Draw help overlay on frame."""
        h, w = frame.shape[:2]

        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//2 - 250, h//2 - 150), (w//2 + 250, h//2 + 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)

        # Help text
        help_text = [
            "CONTROLS",
            "",
            "q - Quit",
            "s - Save screenshot",
            "SPACE - Toggle split view",
            "+/- - Adjust intensity",
            "1-4 - Switch effect",
            "h - Hide help"
        ]

        y_pos = h//2 - 120
        for line in help_text:
            cv2.putText(frame, line, (w//2 - 200, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y_pos += 35


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Face Privacy Protection - Real-time anonymization using YOLOv11-Face',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --source webcam --effect pixelate
  %(prog)s --source video --input myvideo.mp4 --output protected.avi
  %(prog)s --demo --input test/video_003.mp4 --output demo.avi
        """
    )

    parser.add_argument('--source', type=str, default='webcam',
                       choices=['webcam', 'video', 'image'],
                       help='Input source type (default: webcam)')

    parser.add_argument('--input', type=str, default='test/video_003.mp4',
                       help='Path to input video/image file')

    parser.add_argument('--output', type=str, default='output/result.avi',
                       help='Path to save output file')

    parser.add_argument('--effect', type=str, default='pixelate',
                       choices=['pixelate', 'blur', 'blackbox', 'emoji'],
                       help='Privacy effect to apply (default: pixelate)')

    parser.add_argument('--intensity', type=int, default=15,
                       help='Effect intensity (5-50, default: 15)')

    parser.add_argument('--demo', action='store_true',
                       help='Create side-by-side demo video')

    parser.add_argument('--no-display', action='store_true',
                       help='Run without GUI display (save only)')

    parser.add_argument('--fps', action='store_true', default=True,
                       help='Show FPS counter (default: True)')

    args = parser.parse_args()

    # Validate intensity
    args.intensity = max(5, min(50, args.intensity))

    # Run application
    app = FacePrivacyApp(args)
    app.run()


if __name__ == '__main__':
    main()
