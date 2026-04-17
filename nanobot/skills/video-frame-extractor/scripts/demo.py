#!/usr/bin/env python3
"""
视频帧提取器演示脚本
"""

import os
import sys
import time
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from video_frame_extractor import VideoFrameExtractor
    print("✅ 视频帧提取器模块导入成功！")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)


def create_demo_video():
    """创建演示视频"""
    try:
        import cv2
        import numpy as np
        
        # 创建演示视频
        width, height = 640, 480
        fps = 30
        duration = 20  # 20秒
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = 'demo_video.mp4'
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        print(f"🎬 创建演示视频: {video_path}")
        
        for i in range(fps * duration):
            # 创建动态背景
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # 渐变背景
            t = i / (fps * duration)
            frame[:, :, 0] = int(128 + 127 * np.sin(2 * np.pi * t))  # 蓝色
            frame[:, :, 1] = int(128 + 127 * np.sin(2 * np.pi * t + 2*np.pi/3))  # 绿色
            frame[:, :, 2] = int(128 + 127 * np.sin(2 * np.pi * t + 4*np.pi/3))  # 红色
            
            # 添加动态圆形
            center_x = int(width/2 + 200 * np.sin(2 * np.pi * t * 0.5))
            center_y = int(height/2 + 150 * np.cos(2 * np.pi * t * 0.3))
            radius = int(50 + 30 * np.sin(2 * np.pi * t * 2))
            
            cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), -1)
            
            # 添加文字
            cv2.putText(frame, f'Demo Frame {i}', (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Time: {i/fps:.1f}s', (10, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        print(f"✅ 演示视频创建成功: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"❌ 创建演示视频失败: {e}")
        return None


def demo_basic_usage():
    """演示基本用法"""
    print("\n🎯 演示基本用法")
    print("=" * 50)
    
    # 创建演示视频
    video_path = create_demo_video()
    if not video_path:
        return False
    
    try:
        # 创建提取器
        extractor = VideoFrameExtractor()
        
        # 基本参数
        params = {
            'video_path': video_path,
            'output_path': 'demo_basic_output.jpg',
            'frame_interval': 4,      # 每4秒提取一帧
            'frames_per_row': 3,     # 每行3张图片
            'image_size': (200, 150), # 每张图片的大小
            'quality': 90,
            'border_color': (255, 255, 255), # 白色边框
            'border_width': 2,
            'progress': True
        }
        
        print("📊 参数设置:")
        for key, value in params.items():
            if key not in ['video_path', 'output_path']:
                print(f"   {key}: {value}")
        
        print(f"\n🎬 处理视频: {os.path.basename(video_path)}")
        
        start_time = time.time()
        success = extractor.extract_frames(**params)
        end_time = time.time()
        
        if success:
            print(f"✅ 基本用法演示成功！")
            print(f"⏱️ 处理耗时: {end_time - start_time:.2f} 秒")
            print(f"📸 输出文件: {params['output_path']}")
            
            # 显示输出文件信息
            if os.path.exists(params['output_path']):
                file_size = os.path.getsize(params['output_path'])
                print(f"📏 文件大小: {file_size} 字节")
            
            return True
        else:
            print("❌ 基本用法演示失败")
            return False
            
    except Exception as e:
        print(f"❌ 基本用法演示异常: {e}")
        return False


def demo_advanced_usage():
    """演示高级用法"""
    print("\n🎯 演示高级用法")
    print("=" * 50)
    
    # 创建演示视频
    video_path = create_demo_video()
    if not video_path:
        return False
    
    try:
        # 创建提取器
        extractor = VideoFrameExtractor()
        
        # 高级参数
        params = {
            'video_path': video_path,
            'output_path': 'demo_advanced_output.png',
            'frame_interval': 2,      # 每2秒提取一帧
            'frames_per_row': 4,     # 每行4张图片
            'image_size': (250, 188), # 每张图片的大小
            'quality': 95,
            'border_color': (0, 0, 0), # 黑色边框
            'border_width': 3,
            'progress': True
        }
        
        print("📊 高级参数设置:")
        for key, value in params.items():
            if key not in ['video_path', 'output_path']:
                print(f"   {key}: {value}")
        
        print(f"\n🎬 处理视频: {os.path.basename(video_path)}")
        
        start_time = time.time()
        success = extractor.extract_frames(**params)
        end_time = time.time()
        
        if success:
            print(f"✅ 高级用法演示成功！")
            print(f"⏱️ 处理耗时: {end_time - start_time:.2f} 秒")
            print(f"📸 输出文件: {params['output_path']}")
            
            # 显示输出文件信息
            if os.path.exists(params['output_path']):
                file_size = os.path.getsize(params['output_path'])
                print(f"📏 文件大小: {file_size} 字节")
            
            return True
        else:
            print("❌ 高级用法演示失败")
            return False
            
    except Exception as e:
        print(f"❌ 高级用法演示异常: {e}")
        return False


def demo_multiple_formats():
    """演示多种输出格式"""
    print("\n🎯 演示多种输出格式")
    print("=" * 50)
    
    # 创建演示视频
    video_path = create_demo_video()
    if not video_path:
        return False
    
    try:
        # 创建提取器
        extractor = VideoFrameExtractor()
        
        # 不同格式参数
        formats = [
            ('jpg', 'JPEG格式', 90),
            ('png', 'PNG格式', 95),
            ('bmp', 'BMP格式', 100),
            ('tiff', 'TIFF格式', 90)
        ]
        
        results = []
        
        for ext, format_name, quality in formats:
            output_path = f'demo_{ext}_output.{ext}'
            
            print(f"\n📸 处理 {format_name}...")
            
            success = extractor.extract_frames(
                video_path=video_path,
                output_path=output_path,
                frame_interval=3,
                frames_per_row=2,
                image_size=(180, 135),
                quality=quality,
                border_color=(255, 255, 255),
                border_width=1,
                progress=False
            )
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"   ✅ {format_name} 成功 ({file_size} 字节)")
                results.append(True)
            else:
                print(f"   ❌ {format_name} 失败")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print(f"❌ 多格式演示异常: {e}")
        return False


def demo_batch_processing():
    """演示批量处理"""
    print("\n🎯 演示批量处理")
    print("=" * 50)
    
    # 创建多个演示视频
    video_files = []
    for i in range(3):
        video_path = f'demo_video_{i}.mp4'
        if create_demo_video_with_suffix(f'_{i}'):
            video_files.append(video_path)
    
    if not video_files:
        print("❌ 无法创建演示视频")
        return False
    
    try:
        # 创建提取器
        extractor = VideoFrameExtractor()
        
        print(f"📁 批量处理 {len(video_files)} 个视频文件:")
        for video_file in video_files:
            print(f"   {video_file}")
        
        # 批量处理
        results = []
        for i, video_file in enumerate(video_files):
            output_path = f'batch_output_{i}.jpg'
            
            print(f"\n🎬 处理 {video_file}...")
            
            success = extractor.extract_frames(
                video_path=video_file,
                output_path=output_path,
                frame_interval=5,
                frames_per_row=2,
                image_size=(160, 120),
                quality=85,
                border_color=(255, 255, 255),
                border_width=1,
                progress=False
            )
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"   ✅ 处理成功 ({file_size} 字节)")
                results.append(True)
            else:
                print(f"   ❌ 处理失败")
                results.append(False)
        
        print(f"\n📊 批量处理结果: {sum(results)}/{len(results)} 成功")
        return all(results)
        
    except Exception as e:
        print(f"❌ 批量处理演示异常: {e}")
        return False
    finally:
        # 清理临时文件
        for video_file in video_files:
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"🧹 清理临时文件: {video_file}")


def create_demo_video_with_suffix(suffix=''):
    """创建带后缀的演示视频"""
    try:
        import cv2
        import numpy as np
        
        width, height = 320, 240
        fps = 15
        duration = 10
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = f'demo_video{suffix}.mp4'
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        for i in range(fps * duration):
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :, 0] = (i * 255) // (fps * duration)
            frame[:, :, 1] = 255 - (i * 255) // (fps * duration)
            
            cv2.putText(frame, f'Demo{suffix} Frame {i}', (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            out.write(frame)
        
        out.release()
        return True
        
    except Exception as e:
        print(f"❌ 创建演示视频失败: {e}")
        return False


def main():
    """主演示函数"""
    print("🔥 火娃 - 视频帧提取器演示")
    print("=" * 60)
    
    # 演示项目
    demos = [
        ("基本用法", demo_basic_usage),
        ("高级用法", demo_advanced_usage),
        ("多种格式", demo_multiple_formats),
        ("批量处理", demo_batch_processing)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n🎬 {demo_name}演示")
        print("-" * 40)
        
        try:
            result = demo_func()
            results.append((demo_name, result))
            
            if result:
                print(f"✅ {demo_name}演示成功")
            else:
                print(f"❌ {demo_name}演示失败")
                
        except Exception as e:
            print(f"❌ {demo_name}演示异常: {e}")
            results.append((demo_name, False))
    
    # 总结结果
    print("\n" + "=" * 60)
    print("🎯 演示结果总结:")
    print("-" * 40)
    
    passed = 0
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{demo_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 总体结果: {passed}/{total} 演示成功")
    
    if passed == total:
        print("🎉 所有演示成功！视频帧提取器功能正常。")
        print("\n💡 使用提示:")
        print("   - 基本用法适合快速创建视频预览")
        print("   - 高级用法适合精细控制输出效果")
        print("   - 多种格式支持不同需求")
        print("   - 批量处理适合处理多个视频文件")
    else:
        print("⚠️ 部分演示失败，请检查依赖和配置。")
    
    # 清理演示文件
    print("\n🧹 清理演示文件...")
    demo_files = ['demo_video.mp4', 'demo_basic_output.jpg', 'demo_advanced_output.png']
    for file in demo_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"   删除: {file}")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)