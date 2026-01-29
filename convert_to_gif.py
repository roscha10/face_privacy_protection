"""
Quick script to convert demo.avi to optimized GIF for GitHub README
"""
import cv2
from PIL import Image
import os

def video_to_gif(input_path, output_path, fps=10, scale_width=800, max_frames=100):
    """Convert video to optimized GIF."""

    print(f"Converting {input_path} to GIF...")

    # Open video
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"Error: Could not open {input_path}")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Original: {total_frames} frames at {original_fps:.2f} FPS")
    print(f"Target: {min(total_frames, max_frames)} frames at {fps} FPS")

    # Calculate frame skip
    frame_skip = int(original_fps / fps)

    frames = []
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret or saved_count >= max_frames:
            break

        # Only keep every Nth frame
        if frame_count % frame_skip == 0:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize
            h, w = rgb_frame.shape[:2]
            new_width = scale_width
            new_height = int(h * (new_width / w))

            # Convert to PIL Image and resize
            pil_img = Image.fromarray(rgb_frame)
            pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            frames.append(pil_img)
            saved_count += 1

            if saved_count % 10 == 0:
                print(f"  Processed {saved_count} frames...")

        frame_count += 1

    cap.release()

    if not frames:
        print("Error: No frames extracted")
        return

    print(f"\nSaving GIF with {len(frames)} frames...")

    # Save as GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000//fps,  # Duration in milliseconds
        loop=0,  # Loop forever
        optimize=True
    )

    # Check file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✓ GIF created: {output_path}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Frames: {len(frames)}")
    print(f"  FPS: {fps}")

    if size_mb > 10:
        print(f"\n⚠ Warning: GIF is large ({size_mb:.2f} MB)")
        print("  GitHub recommends < 10 MB for best performance")
        print("  Consider reducing max_frames or scale_width")

if __name__ == "__main__":
    video_to_gif(
        input_path="assets/demo.avi",
        output_path="assets/demo.gif",
        fps=10,
        scale_width=800,
        max_frames=100  # Limit to 100 frames (~10 seconds at 10 FPS)
    )

    print("\n✓ Done! You can now commit and push to GitHub.")
