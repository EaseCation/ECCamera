# -*- coding: utf-8 -*-
class AnimationInterpolator(object):
    """
    基于Blockbench动画插值算法的Python实现
    处理不同类型的插值：线性、阶梯、贝塞尔曲线和Catmull-Rom样条
    """
    def __init__(self, keyframes):
        """
        初始化插值器
        参数:
        keyframes -- 关键帧数据列表
        """
        self.keyframes = keyframes
        self.channels = self._get_available_channels()
        self._organize_keyframes_by_channel()

    def _get_available_channels(self):
        """获取所有可用的通道"""
        channels = set()
        for kf in self.keyframes:
            channels.add(kf.get("channel"))
        return list(channels)

    def _organize_keyframes_by_channel(self):
        """将关键帧按通道组织并排序"""
        self.keyframes_by_channel = {}
        for channel in self.channels:
            self.keyframes_by_channel[channel] = []
        for kf in self.keyframes:
            channel = kf.get("channel")
            self.keyframes_by_channel[channel].append(kf)
        # 对每个通道的关键帧按时间排序
        for channel in self.channels:
            self.keyframes_by_channel[channel].sort(key=lambda x: x.get("time", 0))

    def get_value_at_time(self, time, channel=None):
        """
        根据时间获取指定通道(或所有通道)的插值值
        参数:
        time -- 当前时间点(秒)
        channel -- 指定通道名称，为None时返回所有通道的值
        返回:
        字典形式的插值结果
        """
        if channel is not None:
            if channel not in self.channels:
                return None
            return self._calculate_channel_value(time, channel)
        # 计算所有通道的值
        result = {}
        for ch in self.channels:
            result[ch] = self._calculate_channel_value(time, ch)
        return result

    def _calculate_channel_value(self, time, channel):
        """为特定通道计算特定时间的值"""
        keyframes = self.keyframes_by_channel[channel]
        if not keyframes:
            return None
        # 找到当前时间之前和之后的关键帧
        before_kf = None
        after_kf = None
        epsilon = 1.0/1200  # 用于浮点数比较的小值
        # 检查是否有与当前时间完全匹配的帧
        for kf in keyframes:
            kf_time = kf.get("time", 0)
            if abs(kf_time - time) < epsilon:
                return self._get_keyframe_value(kf)
        # 查找before和after帧
        for kf in keyframes:
            kf_time = kf.get("time", 0)
            if kf_time < time:
                if before_kf is None or kf_time > before_kf.get("time", 0):
                    before_kf = kf
            elif kf_time > time:
                if after_kf is None or kf_time < after_kf.get("time", 0):
                    after_kf = kf
        # 处理边界情况
        if before_kf is None and after_kf is None:
            return None
        if before_kf is None:
            return self._get_keyframe_value(after_kf)
        if after_kf is None:
            return self._get_keyframe_value(before_kf)
        # 处理step插值(阶梯)
        interpolation = before_kf.get("interpolation", "linear")
        if interpolation == "step":
            return self._get_keyframe_value(before_kf)
        # 根据插值类型计算
        if interpolation == "linear":
            return self._linear_interpolation(before_kf, after_kf, time)
        elif interpolation == "bezier":
            return self._bezier_interpolation(before_kf, after_kf, time)
        elif interpolation == "catmullrom":
            return self._catmullrom_interpolation(keyframes, before_kf, after_kf, time)
        # 默认使用线性插值
        return self._linear_interpolation(before_kf, after_kf, time)

    def _parse_value(self, value_str):
        """尝试将字符串转换为浮点数"""
        try:
            return float(value_str)
        except (ValueError, TypeError):
            return value_str

    def _get_keyframe_value(self, keyframe):
        """从关键帧中获取数据点的值"""
        result = {}
        data_points = keyframe.get("data_points", [])
        if data_points:
            data_point = data_points[0]  # 使用第一个数据点
            for key in data_point:
                result[key] = self._parse_value(data_point[key])
        return result

    def _linear_interpolation(self, before_kf, after_kf, time):
        """线性插值计算"""
        before_time = before_kf.get("time", 0)
        after_time = after_kf.get("time", 0)
        # 计算插值因子
        alpha = (time - before_time) / float(after_time - before_time) if after_time != before_time else 0
        before_value = self._get_keyframe_value(before_kf)
        after_value = self._get_keyframe_value(after_kf)
        result = {}
        for key in before_value:
            if key in after_value:
                try:
                    v1 = float(before_value[key])
                    v2 = float(after_value[key])
                    result[key] = v1 + (v2 - v1) * alpha
                except (ValueError, TypeError):
                    result[key] = before_value[key]
            else:
                result[key] = before_value[key]
        # 确保包含after_value中存在但before_value中不存在的键
        for key in after_value:
            if key not in before_value:
                result[key] = after_value[key]
        return result

    def _bezier_interpolation(self, before_kf, after_kf, time):
        """贝塞尔曲线插值计算"""
        before_time = before_kf.get("time", 0)
        after_time = after_kf.get("time", 0)
        # 计算插值因子
        alpha = (time - before_time) / float(after_time - before_time) if after_time != before_time else 0
        before_value = self._get_keyframe_value(before_kf)
        after_value = self._get_keyframe_value(after_kf)
        bezier_right_time = before_kf.get("bezier_right_time", [0.1, 0.1, 0.1])
        bezier_right_value = before_kf.get("bezier_right_value", [0, 0, 0])
        bezier_left_time = after_kf.get("bezier_left_time", [-0.1, -0.1, -0.1])
        bezier_left_value = after_kf.get("bezier_left_value", [0, 0, 0])
        result = {}
        for key_index, key in enumerate(['x', 'y', 'z']):
            if key in before_value and key in after_value:
                try:
                    # 获取起点和终点值
                    p0 = float(before_value[key])
                    p3 = float(after_value[key])
                    # 获取控制点
                    axis_index = key_index
                    # 控制点1(在起点之后)
                    if axis_index < len(bezier_right_value):
                        p1 = p0 + bezier_right_value[axis_index]
                    else:
                        p1 = p0
                    # 控制点2(在终点之前)
                    if axis_index < len(bezier_left_value):
                        p2 = p3 + bezier_left_value[axis_index]
                    else:
                        p2 = p3
                    # 使用贝塞尔曲线公式计算
                    t = alpha  # 使用alpha作为参数t的近似
                    result[key] = (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
                except (ValueError, TypeError, IndexError):
                    # 出错时使用线性插值
                    result[key] = before_value[key] if key in before_value else after_value[key]
            else:
                # 处理键不存在的情况
                if key in before_value:
                    result[key] = before_value[key]
                elif key in after_value:
                    result[key] = after_value[key]
        return result

    def _catmullrom_interpolation(self, keyframes, before_kf, after_kf, time):
        """Catmull-Rom样条插值计算"""
        keyframes_sorted = sorted(keyframes, key=lambda x: x.get("time", 0))
        before_index = keyframes_sorted.index(before_kf)
        before_plus = None
        if before_index > 0:
            before_plus = keyframes_sorted[before_index - 1]
        after_plus = None
        if before_index + 2 < len(keyframes_sorted):
            after_plus = keyframes_sorted[before_index + 2]
        before_time = before_kf.get("time", 0)
        after_time = after_kf.get("time", 0)
        # 计算插值因子
        alpha = (time - before_time) / float(after_time - before_time) if after_time != before_time else 0
        before_value = self._get_keyframe_value(before_kf)
        after_value = self._get_keyframe_value(after_kf)
        before_plus_value = self._get_keyframe_value(before_plus) if before_plus else None
        after_plus_value = self._get_keyframe_value(after_plus) if after_plus else None
        result = {}
        for key in ['x', 'y', 'z']:
            if key in before_value and key in after_value:
                try:
                    p1 = float(before_value[key])
                    p2 = float(after_value[key])
                    p0 = float(before_plus_value[key]) if before_plus_value and key in before_plus_value else p1
                    p3 = float(after_plus_value[key]) if after_plus_value and key in after_plus_value else p2
                    # Catmull-Rom插值公式
                    t = alpha
                    result[key] = 0.5 * ((2 * p1) +
                                         (-p0 + p2) * t +
                                         (2*p0 - 5*p1 + 4*p2 - p3) * t**2 +
                                         (-p0 + 3*p1 - 3*p2 + p3) * t**3)
                except (ValueError, TypeError):
                    # 出错时使用线性插值
                    v1 = float(before_value[key]) if isinstance(before_value[key], (int, float, str)) else 0
                    v2 = float(after_value[key]) if isinstance(after_value[key], (int, float, str)) else 0
                    result[key] = v1 + (v2 - v1) * alpha
            else:
                if key in before_value:
                    result[key] = before_value[key]
                elif key in after_value:
                    result[key] = after_value[key]
        return result
