# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

try:
    from ..data.ECCameraConfig import ECCameraConfig
except:
    pass

compPostProcess = clientApi.GetEngineCompFactory().CreatePostProcess(clientApi.GetLevelId())
compOperation = clientApi.GetEngineCompFactory().CreateOperation(clientApi.GetLevelId())
compCamera = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId())
compGame = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
compPlayerView = clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId())


class CameraConfigOperator(object):

    def __init__(self, config):
        self.config = config  # type: ECCameraConfig
        
        # 保存原始设置以便恢复
        self._originalFov = compCamera.GetFov()
        self._originalPerspective = compPlayerView.GetPerspective()

    def apply(self):
        """应用相机配置"""
        try:
            # 保存原始设置
            self._originalFov = compCamera.GetFov()
            self._originalPerspective = compPlayerView.GetPerspective()

            # 设置第三人称
            compPlayerView.SetPerspective(1)

            # 锁定移动和旋转
            if self.config.get("lockMovemest", False):
                compOperation.SetMoveLock(True)
            if self.config.get("lockRotation", False):
                compOperation.SetCanDrag(False)
            
            # 隐藏HUD
            if self.config.get("hideHUD", False):
                clientApi.HideHudGUI(True)
            
            # 阻止方块交互
            if self.config.get("blockInteraction", False):
                pass  # 暂不支持
            
            # 应用FOV
            if "fov" in self.config and self.config["fov"] is not None:
                compCamera.SetFov(float(self.config["fov"]))
            
            # 应用深度场景效果
            if "depthOfField" in self.config and self.config["depthOfField"]:
                dof = self.config["depthOfField"]
                self._set_depth_of_field(dof)
            
            # 应用晕影效果
            if "vignette" in self.config and self.config["vignette"]:
                vignette = self.config["vignette"]
                self._set_vignette(vignette)
            
            # 应用颜色调整
            if "adjustment" in self.config and self.config["adjustment"]:
                adjustment = self.config["adjustment"]
                self._set_color_adjustment(adjustment)
            
            # 应用镜头染色
            if "lensStain" in self.config and self.config["lensStain"]:
                lens = self.config["lensStain"]
                self._set_lens_stain(lens)
                
            return True
        except Exception as e:
            print("相机配置应用失败: {}".format(e))
            return False

    def restore(self):
        """取消应用相机配置，恢复默认设置"""
        try:
            # 设置人称
            compPlayerView.SetPerspective(self._originalPerspective)

            # 只有在配置中设置了锁定移动才解锁
            if self.config.get("lockMovement", False):
                compOperation.SetMoveLock(False)
                
            # 只有在配置中设置了锁定旋转才解锁
            if self.config.get("lockRotation", False):
                compOperation.SetCanDrag(True)
                
            # 只有在配置中设置了阻止交互才解锁
            if self.config.get("blockInteraction", False):
                pass
            
            # 只有在配置中设置了隐藏HUD才恢复
            if self.config.get("hideHUD", False):
                clientApi.HideHudGUI(False)
            
            # 只有在配置中设置了FOV才恢复
            if "fov" in self.config and self.config["fov"] is not None:
                compCamera.SetFov(self._originalFov)
            
            # 只有在配置中启用了深度场景效果才禁用
            if "depthOfField" in self.config and self.config["depthOfField"]:
                if self.config["depthOfField"].get("enable", False):
                    compPostProcess.SetEnableDepthOfField(False)
            
            # 只有在配置中启用了晕影效果才禁用
            if "vignette" in self.config and self.config["vignette"]:
                if self.config["vignette"].get("enable", False):
                    compPostProcess.SetEnableVignette(False)
            
            # 只有在配置中启用了颜色调整才重置
            if "adjustment" in self.config and self.config["adjustment"]:
                if self.config["adjustment"].get("enable", False):
                    self._reset_color_adjustment()
            
            # 只有在配置中启用了镜头染色才禁用
            if "lensStain" in self.config and self.config["lensStain"]:
                if self.config["lensStain"].get("enable", False):
                    compPostProcess.SetEnableLensStain(False)
            
            return True
        except Exception as e:
            print("相机配置取消应用失败: {}".format(e))
            return False
    
    def _set_depth_of_field(self, dof):
        """设置景深效果"""
        if "enable" in dof:
            compPostProcess.SetEnableDepthOfField(dof["enable"])
        
        if not dof.get("enable", False):
            return
            
        if "focus" in dof:
            compPostProcess.SetDepthOfFieldFocusDistance(float(dof["focus"]))
        if "blur" in dof:
            compPostProcess.SetDepthOfFieldBlurRadius(float(dof["blur"]))
        if "blurNear" in dof:
            compPostProcess.SetDepthOfFieldNearBlurScale(float(dof["blurNear"]))
        if "blurFar" in dof:
            compPostProcess.SetDepthOfFieldFarBlurScale(float(dof["blurFar"]))
        if "centerFocus" in dof:
            compPostProcess.SetDepthOfFieldUseCenterFocus(bool(dof["centerFocus"]))
    
    def _set_vignette(self, vignette):
        """设置晕影效果"""
        if "enable" in vignette:
            compPostProcess.SetEnableVignette(vignette["enable"])
        
        if not vignette.get("enable", False):
            return
            
        if "center" in vignette:
            compPostProcess.SetVignetteCenter(vignette["center"])
        if "color" in vignette:
            compPostProcess.SetVignetteRGB(vignette["color"])
        if "radius" in vignette:
            compPostProcess.SetVignetteRadius(float(vignette["radius"]))
        if "smoothness" in vignette:
            compPostProcess.SetVignetteSmoothness(float(vignette["smoothness"]))
    
    def _set_color_adjustment(self, adjustment):
        """设置颜色调整"""
        if "enable" in adjustment:
            compPostProcess.SetEnableColorAdjustment(adjustment["enable"])
        
        if not adjustment.get("enable", False):
            return
            
        if "brightness" in adjustment:
            compPostProcess.SetColorAdjustmentBrightness(float(adjustment["brightness"]))
        if "contrast" in adjustment:
            compPostProcess.SetColorAdjustmentContrast(float(adjustment["contrast"]))
        if "saturation" in adjustment:
            compPostProcess.SetColorAdjustmentSaturation(float(adjustment["saturation"]))
        if "tint" in adjustment:
            tint = adjustment["tint"]
            if "intensity" in tint and "color" in tint:
                compPostProcess.SetColorAdjustmentTint(float(tint["intensity"]), tint["color"])
    
    def _set_lens_stain(self, lens):
        """设置镜头染色"""
        if "enable" in lens:
            compPostProcess.SetEnableLensStain(lens["enable"])
        
        if not lens.get("enable", False):
            return
            
        if "intensity" in lens:
            compPostProcess.SetLensStainIntensity(float(lens["intensity"]))
        if "color" in lens:
            compPostProcess.SetLensStainColor(lens["color"])
    
    def _reset_color_adjustment(self):
        """重置颜色调整"""
        compPostProcess.SetEnableColorAdjustment(False)
        compPostProcess.SetColorAdjustmentBrightness(0.0)
        compPostProcess.SetColorAdjustmentContrast(1.0)
        compPostProcess.SetColorAdjustmentSaturation(1.0)
        compPostProcess.SetColorAdjustmentTint(0.0, [1.0, 1.0, 1.0])