# -*- coding: utf-8 -*-
import json

import mod.client.extraClientApi as clientApi
from ECCamera.client.CameraSession import CameraSession

from ..config import *

ClientSystem = clientApi.GetClientSystemCls()


class ECCameraClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        super(ECCameraClientSystem, self).__init__(namespace, systemName)
        self.cameraSession = None  # type: CameraSession
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
                            "UiInitFinished", self, self.onUiInitFinished)
        self.ListenForEvent(ModName, ServerSystemName,
                            "RequestStartRoute", self, self.requestStartRoute)
        self.ListenForEvent(ModName, ServerSystemName,
                            "RequestStopRoute", self, self.requestStopRoute)

    def onFrameTick(self):
        if self.cameraSession:
            print("[ECCamera] onFrameTick")
            self.cameraSession.onFrameTick()

    def onUiInitFinished(self, args):
        clientApi.RegisterUI(ModName, UIKey, UIClsPath, UIScreenDef)
        screen = clientApi.CreateUI(ModName, UIKey, {"isHud" : 1})
        screen.system = self

    def requestStartRoute(self, args):
        config = args['config']
        origionPos = tuple(args['originPos'])
        length = args['length']
        keyframes = json.loads(args['keyframes'])
        print("[ECCamera] Start route with config: {}, origionPos: {}, length: {}, keyframes: {}".format(config, origionPos, length, keyframes))
        self.cameraSession = CameraSession(config, origionPos, length, keyframes)
        self.cameraSession.start()

    def requestStopRoute(self, args):
        print("[ECCamera] Stop route")
        if self.cameraSession:
            self.cameraSession.stop()
            self.cameraSession = None
    