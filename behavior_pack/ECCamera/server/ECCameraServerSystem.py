# -*- coding: utf-8 -*-
import json
import mod.server.extraServerApi as serverApi
from ..config import *
from ..data.cameraConfigs import DEFAULT_CAMERA_CONFIG
from ..data.demos import demoKeyframesJson

try:
    from ..data.ECCameraConfig import ECCameraConfig
except:
    pass

from .. import ecCameraApi

ServerSystem = serverApi.GetServerSystemCls()


class ECCameraServerSystem(ServerSystem):

    def __init__(self, namespace, systemName):
        super(ECCameraServerSystem, self).__init__(namespace, systemName)
        ecCameraApi.serverSystem = self
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                            "CustomCommandTriggerServerEvent", self, self.onCustomCommandTrigger)

    def onCustomCommandTrigger(self, args):
        if args['command'] == 'eccamera':
            origin = args['origin']
            entityId = origin['entityId']
            compComp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            # 目前只是测试
            ecCameraApi.playCameraRoute(
                entityId, 
                DEFAULT_CAMERA_CONFIG, 
                compComp.GetFootPos(), 
                6.0, 
                demoKeyframesJson
            )

    def playCameraRoute(self, playerId, config, originPos, length, keyframes):
        # type: (str, ECCameraConfig, tuple[float, float, float], float, str | dict) -> None
        """
        播放摄像机动画
        :param config: 摄像机配置
        :param originPos: 起始位置
        :param length: 动画时长
        :param keyframes: 关键帧数据
        """
        if not isinstance(keyframes, str):
            keyframes = json.dumps(keyframes)
        
        self.NotifyToClient(playerId, "RequestStartRoute", {
            'config': config,
            'originPos': originPos,
            'length': length,
            'keyframes': keyframes
        })

    def stopCameraRoute(self, playerId):
        # type: (str) -> None
        """
        停止摄像机动画
        :param playerId: 玩家ID
        """
        self.NotifyToClient(playerId, "RequestStopRoute", {})
