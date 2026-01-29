"""
Privacy Effects Module

Implements various anonymization effects for face privacy protection.
Each effect provides a different level and style of privacy protection.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw


def apply_pixelation(frame, x1, y1, x2, y2, level=12):
    """
    Apply pixelation effect to face region.

    Pixelation provides strong anonymization while maintaining the general
    shape and position of the face. Higher levels provide stronger privacy
    protection but may be more visually obvious.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int): Pixelation level (5-50, higher = more pixelated)

    Returns:
        numpy.ndarray: Frame with pixelated face region
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Extract face region
    face_region = frame[y1:y2, x1:x2]

    if face_region.size == 0:
        return frame

    # Calculate pixelation size
    face_h, face_w = face_region.shape[:2]
    pixel_size = max(1, min(level, min(face_h, face_w) // 2))

    # Downsample
    small = cv2.resize(face_region,
                      (max(1, face_w // pixel_size), max(1, face_h // pixel_size)),
                      interpolation=cv2.INTER_LINEAR)

    # Upsample back to original size
    pixelated = cv2.resize(small, (face_w, face_h), interpolation=cv2.INTER_NEAREST)

    # Replace region in frame
    frame[y1:y2, x1:x2] = pixelated

    return frame


def apply_blur(frame, x1, y1, x2, y2, level=20):
    """
    Apply Gaussian blur effect to face region.

    Blur provides softer anonymization compared to pixelation. Good for
    situations where you want to obscure details while maintaining a more
    natural appearance.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int): Blur intensity (5-50, higher = more blurred)

    Returns:
        numpy.ndarray: Frame with blurred face region
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Extract face region
    face_region = frame[y1:y2, x1:x2]

    if face_region.size == 0:
        return frame

    # Calculate kernel size (must be odd)
    kernel_size = level * 2 + 1

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(face_region, (kernel_size, kernel_size), 0)

    # Replace region in frame
    frame[y1:y2, x1:x2] = blurred

    return frame


def apply_blackbox(frame, x1, y1, x2, y2, level=None):
    """
    Apply black box effect to face region.

    Complete anonymization by replacing the face with a solid black rectangle.
    Provides maximum privacy protection but is the most obvious visually.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int, optional): Not used, included for interface consistency

    Returns:
        numpy.ndarray: Frame with black box over face
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Draw black rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)

    # Add border for better visibility
    cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 50), 2)

    return frame


def apply_emoji(frame, x1, y1, x2, y2, level=None):
    """
    Apply emoji overlay effect to face region.

    Playful anonymization using a smiley face emoji. Good for casual
    applications or when you want a friendlier appearance.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int, optional): Not used, included for interface consistency

    Returns:
        numpy.ndarray: Frame with emoji over face
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Calculate face dimensions
    face_w = x2 - x1
    face_h = y2 - y1

    if face_w <= 0 or face_h <= 0:
        return frame

    # Create emoji using PIL for better quality
    emoji_size = min(face_w, face_h)
    emoji = Image.new('RGBA', (emoji_size, emoji_size), (255, 255, 0, 255))
    draw = ImageDraw.Draw(emoji)

    # Draw smiley face
    # Eyes
    eye_y = emoji_size // 3
    left_eye_x = emoji_size // 3
    right_eye_x = emoji_size * 2 // 3
    eye_radius = emoji_size // 12

    draw.ellipse([left_eye_x - eye_radius, eye_y - eye_radius,
                  left_eye_x + eye_radius, eye_y + eye_radius],
                 fill=(0, 0, 0, 255))
    draw.ellipse([right_eye_x - eye_radius, eye_y - eye_radius,
                  right_eye_x + eye_radius, eye_y + eye_radius],
                 fill=(0, 0, 0, 255))

    # Smile
    mouth_y = emoji_size * 2 // 3
    mouth_width = emoji_size // 2
    draw.arc([emoji_size // 2 - mouth_width // 2, mouth_y - mouth_width // 2,
              emoji_size // 2 + mouth_width // 2, mouth_y + mouth_width // 2],
             0, 180, fill=(0, 0, 0, 255), width=emoji_size // 25)

    # Convert to OpenCV format
    emoji_cv = cv2.cvtColor(np.array(emoji), cv2.COLOR_RGBA2BGR)

    # Resize emoji to fit face
    emoji_resized = cv2.resize(emoji_cv, (face_w, face_h))

    # Calculate position to center emoji
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    emoji_x1 = max(0, center_x - face_w // 2)
    emoji_y1 = max(0, center_y - face_h // 2)
    emoji_x2 = min(w, emoji_x1 + face_w)
    emoji_y2 = min(h, emoji_y1 + face_h)

    # Adjust emoji size if it extends beyond frame
    actual_w = emoji_x2 - emoji_x1
    actual_h = emoji_y2 - emoji_y1

    if actual_w != face_w or actual_h != face_h:
        emoji_resized = emoji_resized[:actual_h, :actual_w]

    # Overlay emoji
    frame[emoji_y1:emoji_y2, emoji_x1:emoji_x2] = emoji_resized

    return frame


def apply_witness_protection(frame, x1, y1, x2, y2, level=None):
    """
    Apply witness protection style black bar effect.

    Classic anonymization style with a horizontal black bar across the eyes.
    Inspired by traditional witness protection in media.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int, optional): Not used, included for interface consistency

    Returns:
        numpy.ndarray: Frame with black bar across eyes
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Calculate bar position (across eyes, roughly 1/3 from top)
    face_h = y2 - y1
    bar_height = face_h // 4
    bar_y1 = y1 + face_h // 3
    bar_y2 = bar_y1 + bar_height

    # Draw black bar
    cv2.rectangle(frame, (x1, bar_y1), (x2, bar_y2), (0, 0, 0), -1)

    return frame


def apply_colorize(frame, x1, y1, x2, y2, level=None):
    """
    Apply color mask effect to face region.

    Replaces face with a solid color overlay. Provides good anonymization
    while being less harsh than pure black.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        level (int, optional): Not used, included for interface consistency

    Returns:
        numpy.ndarray: Frame with colored face region
    """
    # Validate coordinates
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return frame

    # Create colored overlay (teal color)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (128, 128, 0), -1)

    # Blend with original
    alpha = 0.8
    frame[y1:y2, x1:x2] = cv2.addWeighted(overlay[y1:y2, x1:x2], alpha,
                                          frame[y1:y2, x1:x2], 1 - alpha, 0)

    # Add border
    cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 100, 0), 2)

    return frame


# Effect registry for easy access
EFFECTS = {
    'pixelate': apply_pixelation,
    'blur': apply_blur,
    'blackbox': apply_blackbox,
    'emoji': apply_emoji,
    'witness': apply_witness_protection,
    'colorize': apply_colorize
}


def get_available_effects():
    """
    Get list of available privacy effects.

    Returns:
        list: List of effect names
    """
    return list(EFFECTS.keys())


def apply_effect(frame, x1, y1, x2, y2, effect_name='pixelate', level=12):
    """
    Apply specified privacy effect to face region.

    Args:
        frame (numpy.ndarray): Input frame (BGR)
        x1, y1, x2, y2 (int): Face bounding box coordinates
        effect_name (str): Name of effect to apply
        level (int): Effect intensity parameter

    Returns:
        numpy.ndarray: Frame with effect applied
    """
    effect_func = EFFECTS.get(effect_name, apply_pixelation)
    return effect_func(frame, x1, y1, x2, y2, level)
