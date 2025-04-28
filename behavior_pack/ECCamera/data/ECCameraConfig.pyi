from typing import Optional, TypedDict


class LensStain(TypedDict):
    enable: Optional[bool]
    intensity: Optional[float]
    color: Optional[list[int]]

class DepthOfField(TypedDict):
    enable: Optional[bool]
    focus: Optional[float]
    blur: Optional[float]
    blurNear: Optional[float]
    blurFar: Optional[float]
    centerFocus: Optional[bool]

class Vignette(TypedDict):
    enable: Optional[bool]
    center: Optional[list[float]]
    color: Optional[list[float]]
    radius: Optional[float]
    smoothness: Optional[float]

class ColorAdjustmentTinit(TypedDict):
    intensity: float
    color: list[float]

class ColorAdjustment(TypedDict):
    enable: Optional[bool]
    brightness: Optional[float]
    contrast: Optional[float]
    saturation: Optional[float]
    tint: Optional[ColorAdjustmentTinit]

class ECCameraConfig(TypedDict):
    lockMovement: bool
    lockRotation: bool
    blockInteraction: Optional[bool]
    hideHUD: Optional[bool]
    lensStain: Optional[LensStain]
    keepLock: Optional[bool]
    depthOfField: Optional[DepthOfField]
    vignette: Optional[Vignette]
    adjustment: Optional[ColorAdjustment]
    fov: Optional[float]
    loop: Optional[bool]