# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

try:
    from .server.ECCameraServerSystem import ECCameraServerSystem
    from .data.cameraConfigs import ECCameraConfig
except:
    pass


serverSystem = None  # type: ECCameraServerSystem

def playCameraRoute(playerId, config, originPos, length, keyframes):
    # type: (str, ECCameraConfig, tuple[float, float, float], float, str | dict) -> None
    """
    播放摄像机动画
    :param config: 摄像机配置
    :param originPos: 起始位置
    :param length: 动画时长
    :param keyframes: 关键帧数据
    """
    if serverApi.GetLevelId() is None:
        raise RuntimeError("此API为服务端API，请在服务端使用！")
    if serverSystem is None:
        raise RuntimeError("ECCameraServerSystem 还未初始化！")
    
    serverSystem.playCameraRoute(playerId, config, originPos, length, keyframes)

def stopCameraRoute(playerId):
    # type: (str) -> None
    """
    停止摄像机动画
    :param playerId: 玩家ID
    """
    if serverApi.GetLevelId() is None:
        raise RuntimeError("此API为服务端API，请在服务端使用！")
    if serverSystem is None:
        raise RuntimeError("ECCameraServerSystem 还未初始化！")
    
    serverSystem.stopCameraRoute(playerId)
