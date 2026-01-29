"""
Interactive Face Privacy Demo - Perfect for LinkedIn!
Multiple privacy effects with beautiful UI and smooth transitions.
"""
import cv2
import numpy as np
import time
from face_detectors import MediaPipeFaceDetector, HaarCascadeFaceDetector
from utils import open_camera, pixelate_face, blur_face


class PrivacyEffect:
    """Different privacy protection effects."""

    @staticmethod
    def pixelate(frame, x1, y1, x2, y2, level=15):
        """Pixelate face."""
        return pixelate_face(frame, x1, y1, x2, y2, pixelation=level)

    @staticmethod
    def blur(frame, x1, y1, x2, y2, strength=45):
        """Blur face."""
        return blur_face(frame, x1, y1, x2, y2, blur_strength=strength)

    @staticmethod
    def black_box(frame, x1, y1, x2, y2):
        """Black box over face."""
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)
        return frame

    @staticmethod
    def emoji(frame, x1, y1, x2, y2):
        """Emoji over face."""
        # Create a simple emoji effect (smiley)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        radius = min((x2 - x1), (y2 - y1)) // 2

        # Yellow circle
        cv2.circle(frame, (center_x, center_y), radius, (0, 200, 255), -1)
        # Eyes
        eye_radius = radius // 6
        cv2.circle(frame, (center_x - radius//3, center_y - radius//4),
                   eye_radius, (0, 0, 0), -1)
        cv2.circle(frame, (center_x + radius//3, center_y - radius//4),
                   eye_radius, (0, 0, 0), -1)
        # Smile
        cv2.ellipse(frame, (center_x, center_y + radius//6),
                   (radius//2, radius//3), 0, 0, 180, (0, 0, 0), 3)
        return frame

    @staticmethod
    def witness_protection(frame, x1, y1, x2, y2):
        """Black bar over eyes (witness protection style)."""
        bar_height = (y2 - y1) // 3
        bar_y1 = y1 + (y2 - y1) // 3
        bar_y2 = bar_y1 + bar_height
        cv2.rectangle(frame, (x1, bar_y1), (x2, bar_y2), (0, 0, 0), -1)
        return frame

    @staticmethod
    def colorize(frame, x1, y1, x2, y2):
        """Colorize effect (psychedelic)."""
        face_region = frame[y1:y2, x1:x2]
        if face_region.size > 0:
            hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
            hsv[:, :, 0] = (hsv[:, :, 0] + 90) % 180  # Shift hue
            frame[y1:y2, x1:x2] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return frame


def draw_ui(frame, effect_name, privacy_level, fps, num_faces, show_help=True):
    """Draw beautiful UI overlay."""
    h, w = frame.shape[:2]

    # Top bar with semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 120), (20, 20, 20), -1)
    frame = cv2.addWeighted(overlay, 0.7, frame, 0.3, 0)

    # Title
    cv2.putText(frame, "FACE PRIVACY PROTECTION", (20, 40),
                cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 3)

    # Effect name
    cv2.putText(frame, f"Effect: {effect_name}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Privacy level bar
    bar_x = 350
    bar_y = 60
    bar_width = 200
    bar_height = 25

    # Background bar
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                  (50, 50, 50), -1)

    # Privacy level fill
    fill_width = int((privacy_level / 50) * bar_width)
    color = (0, 255, 0) if privacy_level < 20 else (0, 200, 255) if privacy_level < 35 else (0, 100, 255)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height),
                  color, -1)

    cv2.putText(frame, f"Level: {privacy_level}", (bar_x + bar_width + 10, bar_y + 18),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Stats - Right side
    stats_x = w - 200
    cv2.putText(frame, f"FPS: {fps:.1f}", (stats_x, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Faces: {num_faces}", (stats_x, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Help overlay (bottom)
    if show_help:
        help_overlay = frame.copy()
        help_h = 140
        cv2.rectangle(help_overlay, (0, h - help_h), (w, h), (20, 20, 20), -1)
        frame = cv2.addWeighted(help_overlay, 0.8, frame, 0.2, 0)

        help_text = [
            "CONTROLS:",
            "1-6: Change Effect  |  +/-: Adjust Level  |  SPACE: Split View  |  H: Toggle Help  |  Q: Quit"
        ]

        y_offset = h - help_h + 30
        for i, text in enumerate(help_text):
            color = (0, 255, 255) if i == 0 else (255, 255, 255)
            size = 0.7 if i == 0 else 0.6
            cv2.putText(frame, text, (20, y_offset + i * 35),
                       cv2.FONT_HERSHEY_SIMPLEX, size, color, 2)

    return frame


def main():
    """Run interactive face privacy demo."""
    print("=" * 60)
    print("FACE PRIVACY PROTECTION - Interactive Demo")
    print("=" * 60)

    # Initialize detector (MediaPipe for best balance)
    print("\nLoading face detector...")
    detector = MediaPipeFaceDetector(min_detection_confidence=0.5)

    # Fallback to Haar if MediaPipe fails
    if detector.detector is None:
        print("Falling back to OpenCV Haar Cascades...")
        detector = HaarCascadeFaceDetector()

    # Open webcam
    cap = open_camera(0)
    if cap is None:
        return

    # Effects
    effects = {
        '1': ('Pixelation', PrivacyEffect.pixelate),
        '2': ('Blur', PrivacyEffect.blur),
        '3': ('Black Box', PrivacyEffect.black_box),
        '4': ('Emoji 😊', PrivacyEffect.emoji),
        '5': ('Witness Protection', PrivacyEffect.witness_protection),
        '6': ('Colorize', PrivacyEffect.colorize),
    }

    # Settings
    current_effect = '1'
    privacy_level = 15
    split_view = False
    show_help = True

    # FPS tracking
    fps = 30.0
    frame_count = 0
    start_time = time.time()

    print("\nDemo started! Press 'H' to toggle help, 'Q' to quit")
    print("Try different effects (1-6) and adjust levels (+/-)\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to read frame")
            break

        # Resize for consistent display
        frame = cv2.resize(frame, (1280, 720))
        original_frame = frame.copy()

        # Detect faces
        detections = detector.detect(frame, conf_threshold=0.5)

        # Apply privacy effect
        effect_name, effect_func = effects[current_effect]

        for x1, y1, x2, y2, conf in detections:
            if current_effect in ['1', '2']:
                # Pixelate and blur use level parameter
                frame = effect_func(frame, x1, y1, x2, y2, privacy_level)
            else:
                # Other effects don't need level
                frame = effect_func(frame, x1, y1, x2, y2)

        # Split view mode (before/after comparison)
        if split_view:
            mid = frame.shape[1] // 2

            # Create split frame
            combined = np.zeros_like(frame)
            combined[:, :mid] = original_frame[:, :mid]
            combined[:, mid:] = frame[:, mid:]

            # Draw divider line
            cv2.line(combined, (mid, 0), (mid, frame.shape[0]),
                    (0, 255, 255), 3)

            # Labels
            cv2.putText(combined, "ORIGINAL", (20, frame.shape[0] - 30),
                       cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            cv2.putText(combined, "PROTECTED", (mid + 20, frame.shape[0] - 30),
                       cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

            frame = combined

        # Calculate FPS
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            frame_count = 0
            start_time = time.time()

        # Draw UI
        frame = draw_ui(frame, effect_name, privacy_level, fps,
                       len(detections), show_help)

        # Display
        cv2.imshow("Face Privacy Protection Demo - LinkedIn Ready!", frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("\n✓ Exiting demo...")
            break

        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6')]:
            current_effect = chr(key)
            effect_name, _ = effects[current_effect]
            print(f"Effect: {effect_name}")

        elif key == ord('+') or key == ord('='):
            privacy_level = min(50, privacy_level + 5)
            print(f"Privacy level: {privacy_level}")

        elif key == ord('-') or key == ord('_'):
            privacy_level = max(5, privacy_level - 5)
            print(f"Privacy level: {privacy_level}")

        elif key == ord(' '):  # Space bar
            split_view = not split_view
            print(f"Split view: {'ON' if split_view else 'OFF'}")

        elif key == ord('h'):
            show_help = not show_help

        elif key == ord('s'):
            filename = f"output/privacy_demo_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Screenshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Demo completed!")


if __name__ == "__main__":
    main()
