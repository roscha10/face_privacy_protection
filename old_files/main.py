"""
YOLO26 Face Detection Project
Main menu for accessing different demos and features.
"""
import os
import sys


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header."""
    print("=" * 60)
    print(" " * 15 + "YOLO26 Face Detection Project")
    print(" " * 10 + "Real-Time AI Face Detection & Processing")
    print("=" * 60)
    print()


def print_menu():
    """Print main menu options."""
    print("Available Demos:")
    print()
    print("  [1] Real-Time Face Detection")
    print("      → Detect faces/people from webcam with YOLO26")
    print()
    print("  [2] Face Pixelation/Blur")
    print("      → Privacy mode with adjustable pixelation or blur")
    print()
    print("  [3] Age Prediction")
    print("      → Estimate age using YOLO26 + ViT AI model")
    print()
    print("  [4] Video Processing")
    print("      → Process video files and pixelate faces")
    print()
    print("  [5] Face Privacy Demo 🎯 LINKEDIN READY!")
    print("      → 6 Interactive effects: Pixelate, Blur, Emoji, and more!")
    print()
    print("  [6] Face Detection Comparison")
    print("      → Compare YOLOv11-face vs MediaPipe vs OpenCV")
    print()
    print("  [7] System Information")
    print("      → View installed packages and model info")
    print()
    print("  [0] Exit")
    print()
    print("-" * 60)


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import cv2
        import torch
        from ultralytics import YOLO
        from transformers import AutoModelForImageClassification
        return True
    except ImportError as e:
        print(f"\n✗ Missing dependency: {e}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt")
        return False


def show_system_info():
    """Display system and package information."""
    print("\n" + "=" * 60)
    print("System Information")
    print("=" * 60)

    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except:
        print("OpenCV: Not installed")

    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
    except:
        print("PyTorch: Not installed")

    try:
        import ultralytics
        print(f"Ultralytics version: {ultralytics.__version__}")
    except:
        print("Ultralytics: Not installed")

    try:
        import transformers
        print(f"Transformers version: {transformers.__version__}")
    except:
        print("Transformers: Not installed")

    print("\nPress Enter to continue...")
    input()


def run_demo(choice):
    """
    Run selected demo.

    Args:
        choice: Menu selection number
    """
    if choice == '1':
        print("\nLaunching Real-Time Face Detection...")
        print("Press 'q' to quit, 's' to save screenshot\n")
        import webcam_face_detection
        webcam_face_detection.main()

    elif choice == '2':
        print("\nLaunching Face Pixelation/Blur...")
        print("Press 'q' to quit, '+/-' to adjust level, 'b' to toggle blur\n")
        import webcam_face_pixelation
        webcam_face_pixelation.main()

    elif choice == '3':
        print("\nLaunching Age Prediction...")
        print("Loading models (this may take a moment)...\n")
        import webcam_age_prediction
        webcam_age_prediction.main()

    elif choice == '4':
        print("\nVideo Processing")
        print("-" * 60)
        print("\nAvailable test videos:")

        # List test videos
        test_dir = "test"
        if os.path.exists(test_dir):
            videos = [f for f in os.listdir(test_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
            for i, video in enumerate(videos, 1):
                print(f"  [{i}] {video}")

        print("\nEnter video filename (or press Enter for default):")
        video_input = input("> ").strip()

        if not video_input:
            video_input = "test/video_005.mp4"
        elif not video_input.startswith("test/"):
            video_input = f"test/{video_input}"

        print(f"\nProcessing: {video_input}")
        import video_face_pixelation
        video_face_pixelation.process_video(input_video=video_input)

    elif choice == '5':
        print("\n🎯 Face Privacy Protection Demo - LinkedIn Ready!")
        print("-" * 60)
        print("Interactive demo with 6 privacy effects:")
        print("  1️⃣  Pixelation - Classic privacy effect")
        print("  2️⃣  Blur - Smooth Gaussian blur")
        print("  3️⃣  Black Box - Complete anonymization")
        print("  4️⃣  Emoji - Fun smiley face overlay")
        print("  5️⃣  Witness Protection - Black bar over eyes")
        print("  6️⃣  Colorize - Psychedelic effect")
        print("\nControls:")
        print("  • 1-6: Switch effects")
        print("  • +/-: Adjust privacy level")
        print("  • SPACE: Split view (before/after)")
        print("  • H: Toggle help")
        print("  • S: Save screenshot")
        print("\nStarting demo...\n")
        import face_privacy_demo
        face_privacy_demo.main()

    elif choice == '6':
        print("\nFace Detection Comparison")
        print("-" * 60)
        print("Compare 3 detection methods side-by-side:")
        print("  • YOLOv11-face (specialized YOLO model)")
        print("  • MediaPipe (Google's face detection)")
        print("  • OpenCV Haar Cascades (classic method)")
        print("\nPress 'q' to quit, 's' to save, 'b' for benchmark, 'p' for pixelation\n")
        import webcam_comparison
        webcam_comparison.main()

    elif choice == '7':
        show_system_info()


def main():
    """Main application loop."""
    if not check_dependencies():
        return

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("Select option [0-7]: ").strip()

        if choice == '0':
            print("\nExiting... Thanks for using Face Detection Project!")
            sys.exit(0)

        elif choice in ['1', '2', '3', '4', '5', '6', '7']:
            clear_screen()
            try:
                run_demo(choice)
            except KeyboardInterrupt:
                print("\n\nDemo interrupted by user")
            except Exception as e:
                print(f"\n✗ Error running demo: {e}")
                import traceback
                traceback.print_exc()

            print("\nPress Enter to return to menu...")
            input()

        else:
            print("\n✗ Invalid option. Please select 0-7.")
            print("Press Enter to continue...")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
