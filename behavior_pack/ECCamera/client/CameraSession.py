# -*- coding: utf-8 -*-
import time
import mod.client.extraClientApi as clientApi

from .AnimationInterpolator import AnimationInterpolator
from .CameraConfigOperator import CameraConfigOperator

comp = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId())


class CameraSession(object):

    def __init__(self, config, originPos, length, keyframes):
        self.configOperator = CameraConfigOperator(config)  # type: CameraConfigOperator
        self.originPos = originPos  # type: tuple[float, float, float]
        self.playing = False
        self.length = length
        self.timeStart = 0
        self.interpolator = AnimationInterpolator(keyframes)
        self.originFov = comp.GetFov()

    def start(self):
        self.playing = True
        self.timeStart = time.time()
        self.configOperator.apply()

    def stop(self):
        self.playing = False
        self.timeStart = 0
        comp.SetFov(self.originFov)
        comp.UnLockCamera()
        comp.UnDepartCamera()
        comp.ResetCameraBindActorId()
        self.configOperator.restore()

    def onFrameTick(self):
        if self.playing:
            timePassed = time.time() - self.timeStart
            if timePassed > self.length:
                self.stop()
                return
            interpolationData = self.interpolator.get_value_at_time(timePassed)
            positionData = interpolationData['position'] if 'position' in interpolationData else {'x': 0, 'y': 0, 'z': 0}
            rotationData = interpolationData['rotation'] if 'rotation' in interpolationData else {'x': 0, 'y': 0, 'z': 0}
            fovData = interpolationData['fov'] if 'fov' in interpolationData else None
            position = self.transformPosition(positionData)
            rotation = self.transformRotation(rotationData)
            fov = fovData['x'] if fovData else None
            self.applyCamera(position, rotation, fov)

    def transformPosition(self, position):
        return (-position['x'] / 16.0, position['y'] / 16.0, position['z'] / 16.0)
    
    def transformRotation(self, rotation):
        return (-rotation['y'], -(rotation['x'] - 180), rotation['z'])

    def applyCamera(self, position, rotation, fov):
        comp.LockCamera(
            (self.originPos[0] + position[0], self.originPos[1] + position[1], self.originPos[2] + position[2]),
            (rotation[0], rotation[1])
        )
        # comp.DepartCamera()
        # comp.SetCameraPos(position)
        # comp.SetCameraRotation(rotation)
        if fov:
            comp.SetFov(fov)