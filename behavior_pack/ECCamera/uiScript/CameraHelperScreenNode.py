# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

if False:
	from ..client.ECCameraClientSystem import ECCameraClientSystem


class CameraHelperScreenNode(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)
		self.system = None  # type: ECCameraClientSystem

	def Create(self):
		"""
		@description UI创建成功时调用
		"""
		pass

	@ViewBinder.binding(ViewBinder.BF_BindString, '#tick_refresh_auxiliary')
	def tick_refresh_auxiliary(self):
		self.system.onFrameTick()
