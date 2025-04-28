# -*- coding: utf-8 -*-

try:
    from .ECCameraConfig import ECCameraConfig
except ImportError:
    pass


DEFAULT_CAMERA_CONFIG = {
    "hideHUD": True,
    "lockMovement": True,
    "depthOfField": {
        "enable": True,
        "blur": 0.1,
        "blurNear": 5.0,
        "blurFar": 10.0,
        "centerFocus": True
    },
    "vignette": {
        "enable": True,
        "center": [0.5, 0.5],
        "color": [0, 0, 0],
        "radius": 1.0,
        "smoothness": 1.0
    },
    "fov": 70.0
}  # type: ECCameraConfig