# Video Frame Extractor

火娃的视频帧提取技能，可以按指定间隔从视频中提取帧，并将多帧拼接成一张图片保存到本地。

## 🎯 功能特性

- 🎬 **视频帧提取**: 按指定间隔从视频中提取帧
- 🖼️ **图像拼接**: 将多帧图片拼接成一张大图
- 💾 **本地保存**: 支持多种图片格式保存
- ⏱️ **时间控制**: 精确控制帧提取的时间间隔
- 📊 **进度显示**: 实时显示处理进度
- 🔄 **批量处理**: 支持多个视频文件批量处理

## 📦 安装

技能已自动安装到以下位置：
- `/Users/rama/.nanobot/workspace/skills/video-frame-extractor/`

## 🔧 依赖安装

确保安装了所有必需的库：

```bash
pip install opencv-python moviepy numpy Pillow
```

## 🚀 快速开始

### 基本用法

```python
from video_frame_extractor import VideoFrameExtractor

# 创建提取器
extractor = VideoFrameExtractor()

# 提取帧并拼接
extractor.extract_frames(
    video_path="input.mp4",
    output_path="output.jpg",
    frame_interval=5,      # 每5秒提取一帧
    frames_per_row=3,     # 每行3张图片
    image_size=(320, 240)  # 每张图片的大小
)
```

### 高级用法

```python
from video_frame_extractor import VideoFrameExtractor

# 创建提取器
extractor = VideoFrameExtractor()

# 自定义参数
extractor.extract_frames(
    video_path="input.mp4",
    output_path="output.png",
    frame_interval=10,     # 每10秒提取一帧
    frames_per_row=4,     # 每行4张图片
    image_size=(400, 300), # 每张图片的大小
    quality=95,           # 图片质量 (1-100)
    border_color=(0, 0, 0), # 边框颜色
    border_width=2,       # 边框宽度
    progress=True         # 显示进度
)
```

## 📋 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| video_path | str | 必填 | 视频文件路径 |
| output_path | str | 必填 | 输出图片路径 |
| frame_interval | int | 5 | 帧提取间隔（秒） |
| frames_per_row | int | 3 | 每行显示的帧数 |
| image_size | tuple | (320, 240) | 每帧图片的大小 |
| quality | int | 90 | 图片质量（1-100） |
| border_color | tuple | (0, 0, 0) | 边框颜色（RGB） |
| border_width | int | 1 | 边框宽度 |
| progress | bool | True | 是否显示进度 |

## 🎬 支持的格式

### 输入视频格式
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)
- FLV (.flv)

### 输出图片格式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

## 📖 使用示例

### 示例1: 创建视频预览图

```python
from video_frame_extractor import VideoFrameExtractor

extractor = VideoFrameExtractor()
extractor.extract_frames(
    video_path="movie.mp4",
    output_path="movie_preview.jpg",
    frame_interval=10,     # 每10秒一帧
    frames_per_row=4,     # 4x3网格
    image_size=(200, 150)
)
```

### 示例2: 提取关键帧

```python
from video_frame_extractor import VideoFrameExtractor

extractor = VideoFrameExtractor()
extractor.extract_frames(
    video_path="presentation.mp4",
    output_path="key_frames.jpg",
    frame_interval=30,     # 每30秒一帧
    frames_per_row=2,     # 2x2网格
    image_size=(400, 300)
)
```

### 示例3: 批量处理

```python
from video_frame_extractor import VideoFrameExtractor

extractor = VideoFrameExtractor()

# 批量处理多个视频
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]
for video_file in video_files:
    output_file = f"output_{video_file.split('.')[0]}.jpg"
    extractor.extract_frames(
        video_path=video_file,
        output_path=output_file,
        frame_interval=5,
        frames_per_row=3
    )
```

### 示例4: 获取视频信息

```python
from video_frame_extractor import VideoFrameExtractor

extractor = VideoFrameExtractor()

# 获取视频信息
info = extractor.get_video_info("video.mp4")
print(f"时长: {info['duration']:.1f} 秒")
print(f"帧率: {info['fps']:.1f} FPS")
print(f"总帧数: {info['frame_count']}")
print(f"分辨率: {info['width']}x{info['height']}")
```

## 🧪 测试

运行测试脚本验证功能：

```bash
cd /Users/rama/.nanobot/workspace/skills/video-frame-extractor/scripts
python3 test_video_extractor.py
```

运行演示脚本查看完整功能：

```bash
python3 demo.py
```

## 📊 性能优化

- 对于大视频文件，建议先截取片段
- 使用较小的图片尺寸以减少内存使用
- 调整帧间隔以平衡质量和性能
- 批量处理时建议逐个处理，避免内存不足

## ⚠️ 注意事项

- 视频处理需要较多内存，建议在处理大文件时关闭其他程序
- 处理时间取决于视频长度和参数设置
- 输出图片的大小取决于帧数和每行帧数
- 确保视频文件格式受支持且文件完整

## 🔧 故障排除

### 常见问题

1. **视频无法打开**
   - 检查视频文件路径是否正确
   - 确认视频格式是否支持
   - 检查文件权限

2. **内存不足**
   - 减少图片大小
   - 减少每行的帧数
   - 使用更小的视频文件

3. **图片质量差**
   - 增加图片质量参数
   - 增加图片尺寸
   - 减少压缩率

4. **依赖问题**
   - 确保安装了所有必需的库
   - 检查Python版本兼容性

### 依赖安装

如果遇到依赖问题，请确保安装了所有必需的库：

```bash
pip install opencv-python moviepy numpy Pillow
```

## 🎉 示例输出

处理完成后，您将得到一个包含多个视频帧的拼接图片，例如：

```
📸 图片已保存到: output.jpg
📏 输出图片尺寸: 980 x 480
```

这个图片将显示视频在不同时间点的关键帧，方便快速了解视频内容。

---

🔥 **火娃提示**: 这个技能非常适合创建视频预览图、提取关键帧、制作视频缩略图等场景。您可以根据需要调整参数来获得最佳效果！