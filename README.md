# ECCamera

一个用于Minecraft（我的世界）游戏的相机控制模组，提供强大的相机动画和特效功能。

## 简介

ECCamera是一个为《我的世界》中国版 设计的高级相机控制模组，允许开发者和内容创作者创建电影级的相机动画和特效。（就像是EC的圣符传说那样）

该模组支持直接导入在 Blockbench 中通过插件 `Cameras`，在动画模式中，创建的可视化创建电影级运镜。

完整支持Blockbench的多种插值方式（贝塞尔曲线、线性、阶梯和Catmull-Rom样条），以及丰富的后期处理效果，如景深、晕影和颜色调整等。

![preview](preview.gif)

## 主要功能

- **相机动画路径**：支持在Blockbench通过Cameras插件，基于关键帧创建复杂的相机移动路径
- **多种插值方式**：支持贝塞尔曲线、线性、阶梯和Catmull-Rom样条插值
- **高级相机配置**：
  - 景深效果（深度模糊）
  - 晕影效果
  - 颜色调整（亮度、对比度、饱和度、色调）
  - 镜头染色
  - FOV（视场角）控制
- **游戏界面控制**：隐藏HUD、锁定移动和旋转等

## 安装要求

- Minecraft（我的世界）网易版客户端
- MCStudio开发环境
- Python 2.7

## 安装方法

### 推荐方式

#### 通过我们的 `mcpywrap` 包管理程序，作为依赖安装

1. 安装 mcpywrap 命令行工具：

    ``` bash
    pip install mcpywrap
    ```

2. clone 此项目到本机的某位置（不要在自己的Mod中）

    ``` bash
    git clone https://github.com/EaseCation/ECCamera.git
    ```

3. 在此项目目录打开命令行工具

4. 在命令行中输入以下命令安装为系统依赖

    ``` bash
    mcpy
    ```

5. 执行以下命令可运行此Mod的demo测试

    ``` bash
    mcpy run
    ```

#### 将此项目用作自己的Mod的依赖时

1. 只需要在 **自己的Mod目录** 下，执行 `mcpy` 向导式初始化项目。

    ``` bash
    mcpy
    ```

2. 执行 `mcpy add ECCamera` 添加此项目作为依赖。

    
    ``` bash
    mcpy add ECCamera
    ```

3. 接着，IDE会自动识别Mod依赖，并正确处理代码提示。

4. 执行 `mcpy run` 运行自己的Mod游戏测试。依赖的模组会自动加载。

    ``` bash
    mcpy run
    ```

5. 最终，需要发布Mod时，执行 `mcpy build` 进行构建与打包，打包产物将默认在 `build` 目录下。

    ``` bash
    mcpy build
    ```


### 原始方式（不推荐）

1. 在MCStudio中导入此项目
2. 导入本模组代码到MCStudio项目中
3. 在MCStudio中点击"开发测试"按钮，可以单独运行此Mod进行demo测试
4. 通过将此插件的对应内容复制到自己插件中，进行使用（真的不推荐啊！）

## API 调用方法

### API 概述

ECCamera提供了简单易用的API，可以在服务端脚本中轻松控制相机：

```python
import Mod.server.extraServerApi as serverApi
from ECCamera import ecCameraApi
from ECCamera.data.cameraConfigs import DEFAULT_CAMERA_CONFIG

# 播放相机动画
ecCameraApi.playCameraRoute(
    playerId,               # 玩家ID
    DEFAULT_CAMERA_CONFIG,  # 相机配置（可自定义，详见下方说明）
    (0, 0, 0),              # 动画相对偏移位置（一般为世界坐标）
    6.0,                    # 动画时长（秒）
    keyframes_json          # 关键帧数据
)

# 停止相机动画
ecCameraApi.stopCameraRoute(playerId)
```

其中，**关键帧数据** 是一个JSON格式的字符串，直接用 json 模式打开 bbmodel 文件，找到其中camera的动画即可。

### 相机配置

可以自定义相机配置，包括景深、晕影和颜色调整等效果：

```python
camera_config = {
    "hideHUD": True,          # 隐藏游戏界面
    "lockMovement": True,     # 锁定玩家移动
    "depthOfField": {         # 景深效果
        "enable": True,
        "blur": 0.1,
        "blurNear": 5.0,
        "blurFar": 10.0,
        "centerFocus": True
    },
    "vignette": {             # 晕影效果
        "enable": True,
        "center": [0.5, 0.5],
        "color": [0, 0, 0],
        "radius": 1.0,
        "smoothness": 1.0
    },
    "fov": 70.0               # 视场角
}
```

### 测试DEMO

使用命令`/eccamera`，可在游戏中测试相机功能。

## 关键帧格式

ECCamera使用JSON格式的关键帧数据来定义相机动画。每个关键帧包含以下信息：

- `channel`: 动画通道（position或rotation）
- `data_points`: 数据点，包含xyz坐标或旋转角度
- `time`: 关键帧时间点（秒）
- `interpolation`: 插值类型（bezier、linear、step或catmullrom）
- 贝塞尔曲线控制点（当使用bezier插值时）

示例关键帧数据可参考`behavior_pack/ECCamera/data/demos.py`文件。

## 开发计划

- 应该直接支持导入整个 bbmodel 文件
- 直接在游戏中可视化配置相机动画，并支持一键导出为bbmodel文件，方便在Blockbench中进行进一步细节调整。
- 关于更多演员实体的支持

## 许可证

MIT License

## 作者

boybook