#!/usr/bin/env python3
"""
视频帧提取器
按指定间隔从视频中提取帧，并将多帧拼接成一张图片
"""

import cv2
import os
import numpy as np
from PIL import Image, ImageDraw
from typing import Tuple, Optional, List
import time
import math


class VideoFrameExtractor:
    """视频帧提取器类"""
    
    def __init__(self):
        """初始化提取器"""
        self.cap = None
        self.total_frames = 0
        self.fps = 0
        self.duration = 0
        
    def extract_frames(
        self,
        video_path: str,
        output_path: str,
        frame_interval: int = 5,
        frames_per_row: int = 3,
        image_size: Tuple[int, int] = (320, 240),
        quality: int = 90,
        border_color: Tuple[int, int, int] = (0, 0, 0),
        border_width: int = 1,
        progress: bool = True
    ) -> bool:
        """
        从视频中提取帧并拼接成一张图片
        
        Args:
            video_path: 视频文件路径
            output_path: 输出图片路径
            frame_interval: 帧提取间隔（秒）
            frames_per_row: 每行显示的帧数
            image_size: 每帧图片的大小 (width, height)
            quality: 图片质量（1-100）
            border_color: 边框颜色 (R, G, B)
            border_width: 边框宽度
            progress: 是否显示进度
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证输入文件
            if not os.path.exists(video_path):
                print(f"❌ 视频文件不存在: {video_path}")
                return False
            
            # 打开视频文件
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                print(f"❌ 无法打开视频文件: {video_path}")
                return False
            
            # 获取视频信息
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            print(f"🎬 视频信息:")
            print(f"   文件: {os.path.basename(video_path)}")
            print(f"   时长: {self.duration:.1f} 秒")
            print(f"   总帧数: {self.total_frames}")
            print(f"   帧率: {self.fps:.1f} FPS")
            
            # 计算需要提取的帧数
            frames_to_extract = max(1, int(self.duration // frame_interval))
            frames_to_extract = min(frames_to_extract, self.total_frames)
            
            print(f"📊 计划提取: {frames_to_extract} 帧 (每{frame_interval}秒一帧)")
            
            # 提取帧
            frames = []
            extracted_count = 0
            
            for i in range(frames_to_extract):
                # 计算当前帧的时间点
                target_time = i * frame_interval
                target_frame = int(target_time * self.fps)
                
                # 设置帧位置
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                
                # 读取帧
                ret, frame = self.cap.read()
                if ret:
                    # 调整大小
                    frame = cv2.resize(frame, image_size)
                    
                    # 添加边框
                    if border_width > 0:
                        frame = self._add_border(frame, border_color, border_width)
                    
                    # 转换为RGB格式
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
                    extracted_count += 1
                    
                    # 显示进度
                    if progress and (i + 1) % max(1, frames_to_extract // 10) == 0:
                        progress_percent = (i + 1) / frames_to_extract * 100
                        print(f"   进度: {progress_percent:.1f}%")
                else:
                    print(f"⚠️ 无法读取第 {i+1} 帧")
            
            # 释放视频
            self.cap.release()
            
            print(f"✅ 成功提取 {len(frames)} 帧")
            
            if len(frames) == 0:
                print("❌ 没有成功提取任何帧")
                return False
            
            # 拼接图片
            result_image = self._combine_frames(
                frames, frames_per_row, border_color, border_width
            )
            
            # 保存图片
            if self._save_image(result_image, output_path, quality):
                print(f"📸 图片已保存到: {output_path}")
                
                # 显示输出图片信息
                img_width, img_height = result_image.size
                print(f"📏 输出图片尺寸: {img_width} x {img_height}")
                
                return True
            else:
                print("❌ 图片保存失败")
                return False
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            return False
        finally:
            if self.cap is not None:
                self.cap.release()
    
    def _add_border(self, frame: np.ndarray, color: Tuple[int, int, int], width: int) -> np.ndarray:
        """给图片添加边框"""
        if width <= 0:
            return frame
        
        # 创建带边框的图片
        bordered_frame = cv2.copyMakeBorder(
            frame,
            width, width, width, width,
            cv2.BORDER_CONSTANT,
            value=color
        )
        
        return bordered_frame
    
    def _combine_frames(
        self,
        frames: List[np.ndarray],
        frames_per_row: int,
        border_color: Tuple[int, int, int],
        border_width: int
    ) -> Image.Image:
        """将多帧图片拼接成一张大图"""
        
        if len(frames) == 0:
            return Image.new('RGB', (100, 100), color=(0, 0, 0))
        
        # 计算网格布局
        frames_per_row = max(1, frames_per_row)
        rows = math.ceil(len(frames) / frames_per_row)
        
        # 获取单帧尺寸
        frame_height, frame_width = frames[0].shape[:2]
        
        # 计算输出图片尺寸
        output_width = frame_width * frames_per_row + border_width * 2 * (frames_per_row - 1)
        output_height = frame_height * rows + border_width * 2 * (rows - 1)
        
        # 创建输出图片
        output_image = Image.new('RGB', (output_width, output_height), color=border_color)
        
        # 粘贴每一帧
        for i, frame in enumerate(frames):
            row = i // frames_per_row
            col = i % frames_per_row
            
            # 转换为PIL图片
            frame_pil = Image.fromarray(frame)
            
            # 计算位置
            x = col * (frame_width + border_width * 2) + border_width
            y = row * (frame_height + border_width * 2) + border_width
            
            # 粘贴到输出图片
            output_image.paste(frame_pil, (x, y))
        
        return output_image
    
    def _save_image(
        self,
        image: Image.Image,
        output_path: str,
        quality: int
    ) -> bool:
        """保存图片到文件"""
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 根据文件扩展名选择保存格式
            ext = os.path.splitext(output_path)[1].lower()
            
            if ext in ['.jpg', '.jpeg']:
                # JPEG格式
                image.save(output_path, format='JPEG', quality=quality)
            elif ext == '.png':
                # PNG格式
                image.save(output_path, format='PNG', quality=quality)
            elif ext == '.bmp':
                # BMP格式
                image.save(output_path, format='BMP')
            elif ext == '.tiff':
                # TIFF格式
                image.save(output_path, format='TIFF')
            else:
                # 默认使用JPEG
                image.save(output_path, format='JPEG', quality=quality)
            
            return True
            
        except Exception as e:
            print(f"❌ 保存图片失败: {e}")
            return False
    
    def get_video_info(self, video_path: str) -> dict:
        """获取视频信息"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {}
            
            info = {
                'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'file_size': os.path.getsize(video_path)
            }
            
            cap.release()
            return info
            
        except Exception as e:
            print(f"❌ 获取视频信息失败: {e}")
            return {}


def create_sample_video():
    """创建一个示例视频用于测试"""
    try:
        import numpy as np
        
        # 创建一个简单的测试视频
        width, height = 320, 240
        fps = 30
        duration = 10  # 10秒
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('sample_video.mp4', fourcc, fps, (width, height))
        
        for i in range(fps * duration):
            # 创建渐变背景
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :, 0] = (i * 255) // (fps * duration)  # 蓝色通道
            frame[:, :, 1] = 255 - (i * 255) // (fps * duration)  # 绿色通道
            
            # 添加文字
            cv2.putText(frame, f'Frame {i}', (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        print("✅ 示例视频已创建: sample_video.mp4")
        
    except Exception as e:
        print(f"❌ 创建示例视频失败: {e}")


if __name__ == "__main__":
    print("🔥 火娃 - 视频帧提取器")
    print("=" * 50)
    
    # 创建示例视频（如果不存在）
    if not os.path.exists('sample_video.mp4'):
        print("🎬 创建示例视频...")
        create_sample_video()
        print()
    
    # 创建提取器
    extractor = VideoFrameExtractor()
    
    # 获取视频信息
    video_path = 'sample_video.mp4'
    if os.path.exists(video_path):
        print("📊 视频信息:")
        info = extractor.get_video_info(video_path)
        for key, value in info.items():
            print(f"   {key}: {value}")
        print()
    
    # 提取帧
    print("🎯 开始提取帧...")
    success = extractor.extract_frames(
        video_path=video_path,
        output_path='output_frames.jpg',
        frame_interval=2,      # 每2秒提取一帧
        frames_per_row=3,     # 每行3张图片
        image_size=(200, 150), # 每张图片的大小
        quality=95,           # 图片质量
        border_color=(255, 255, 255), # 白色边框
        border_width=2,       # 边框宽度
        progress=True         # 显示进度
    )
    
    if success:
        print("\n🎉 处理完成！")
        print(f"📸 输出文件: output_frames.jpg")
    else:
        print("\n❌ 处理失败！")