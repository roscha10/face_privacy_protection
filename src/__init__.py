"""
Face Privacy Protection Package

Main modules:
- detectors: Face detection implementations (YOLOv11-Face)
- effects: Privacy protection effects (pixelation, blur, etc.)
- face_privacy: Main CLI application
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

from .detectors import YOLOFaceDetector, FaceDetector
from .effects import (
    apply_pixelation,
    apply_blur,
    apply_blackbox,
    apply_emoji,
    apply_witness_protection,
    apply_colorize,
    get_available_effects,
    apply_effect
)

__all__ = [
    'YOLOFaceDetector',
    'FaceDetector',
    'apply_pixelation',
    'apply_blur',
    'apply_blackbox',
    'apply_emoji',
    'apply_witness_protection',
    'apply_colorize',
    'get_available_effects',
    'apply_effect'
]
