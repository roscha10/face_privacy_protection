"""
Real-time age prediction using YOLO26 for detection and ViT for age estimation.
Press 'q' to quit, 's' to save screenshot.
"""
import cv2
import torch
import time
from transformers import AutoModelForImageClassification, AutoProcessor
from PIL import Image
from utils import load_yolo_model, open_camera, get_face_detections, draw_face_box, display_fps


def load_age_model():
    """Load age prediction model from Hugging Face."""
    print("Loading age prediction model...")
    model_name = "nateraw/vit-age-classifier"

    model = AutoModelForImageClassification.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)
    model.eval()

    print("✓ Age prediction model loaded")
    return model, processor


def predict_age(face_crop, age_model, processor):
    """
    Predict age from face crop.

    Args:
        face_crop: Face region in BGR format
        age_model: Age prediction model
        processor: Model processor

    Returns:
        Estimated age (int)
    """
    if face_crop.size == 0:
        return None

    # Convert to PIL image
    face_pil = Image.fromarray(cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB))
    inputs = processor(images=face_pil, return_tensors="pt")

    # Predict
    with torch.no_grad():
        outputs = age_model(**inputs)
    estimated_age = outputs.logits.argmax().item()

    return estimated_age


def main():
    """Run real-time age prediction from webcam."""
    print("=" * 50)
    print("YOLO26 + ViT Age Prediction")
    print("=" * 50)

    # Load models
    face_detector = load_yolo_model("yolo26n.pt")
    if face_detector is None:
        return

    age_model, processor = load_age_model()

    # Open webcam
    cap = open_camera(0)
    if cap is None:
        return

    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save screenshot")
    print("\nStarting age prediction...\n")

    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("✗ Failed to read frame")
            break

        # Detect faces
        detections = get_face_detections(face_detector, frame, conf_threshold=0.3)

        for x1, y1, x2, y2, conf in detections:
            # Extract face region
            face_crop = frame[int(y1):int(y2), int(x1):int(x2)]

            # Predict age
            estimated_age = predict_age(face_crop, age_model, processor)

            if estimated_age is not None:
                label = f"Age: {estimated_age} | Conf: {conf:.2f}"
                draw_face_box(frame, x1, y1, x2, y2, label=label)

        # Calculate FPS
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
        cv2.imshow("YOLO26 + Age Prediction (Press 'q' to quit)", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n✓ Exiting...")
            break
        elif key == ord('s'):
            filename = f"output/age_prediction_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"✓ Screenshot saved: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("✓ Done!")


if __name__ == "__main__":
    main()
