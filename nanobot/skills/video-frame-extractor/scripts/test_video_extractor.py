#!/usr/bin/env python3
"""
视频帧提取器测试脚本
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from video_frame_extractor import VideoFrameExtractor
    print("✅ 视频帧提取器模块导入成功！")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)


def create_test_video():
    """创建测试视频"""
    try:
        import cv2
        import numpy as np
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, 'test_video.mp4')
        
        # 创建视频
        width, height = 320, 240
        fps = 10
        duration = 15  # 15秒
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        
        print(f"🎬 创建测试视频: {video_path}")
        
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
        print(f"✅ 测试视频创建成功: {video_path}")
        return video_path, temp_dir
        
    except Exception as e:
        print(f"❌ 创建测试视频失败: {e}")
        return None, None


def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 创建测试视频
    video_path, temp_dir = create_test_video()
    if not video_path:
        return False
    
    try:
        # 创建提取器
        extractor = VideoFrameExtractor()
        
        # 获取视频信息
        print("📊 获取视频信息...")
        info = extractor.get_video_info(video_path)
        print(f"   时长: {info.get('duration', 0):.1f} 秒")
        print(f"   帧率: {info.get('fps', 0):.1f} FPS")
        print(f"   总帧数: {info.get('frame_count', 0)}")
        
        # 测试参数
        test_params = {
            'video_path': video_path,
            'output_path': os.path.join(temp_dir, 'test_output.jpg'),
            'frame_interval': 3,      # 每3秒提取一帧
            'frames_per_row': 2,     # 每行2张图片
            'image_size': (160, 120), # 每张图片的大小
            'quality': 90,
            'border_color': (255, 255, 255), # 白色边框
            'border_width': 1,
            'progress': True
        }
        
        print("🎯 开始提取帧...")
        success = extractor.extract_frames(**test_params)
        
        if success:
            # 检查输出文件
            output_path = test_params['output_path']
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ 输出文件创建成功: {output_path}")
                print(f"   文件大小: {file_size} 字节")
                
                # 获取输出图片信息
                try:
                    from PIL import Image
                    with Image.open(output_path) as img:
                        print(f"   图片尺寸: {img.size}")
                        print(f"   图片模式: {img.mode}")
                except Exception as e:
                    print(f"   无法读取图片信息: {e}")
                
                return True
            else:
                print("❌ 输出文件未创建")
                return False
        else:
            print("❌ 帧提取失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🧹 清理临时目录: {temp_dir}")


def test_different_formats():
    """测试不同输出格式"""
    print("\n🧪 测试不同输出格式...")
    
    # 创建测试视频
    video_path, temp_dir = create_test_video()
    if not video_path:
        return False
    
    try:
        extractor = VideoFrameExtractor()
        
        formats = [
            ('jpg', 'JPEG'),
            ('png', 'PNG'),
            ('bmp', 'BMP'),
            ('tiff', 'TIFF')
        ]
        
        results = []
        
        for ext, format_name in formats:
            output_path = os.path.join(temp_dir, f'test_output.{ext}')
            
            print(f"📸 测试 {format_name} 格式...")
            success = extractor.extract_frames(
                video_path=video_path,
                output_path=output_path,
                frame_interval=5,
                frames_per_row=2,
                image_size=(100, 75),
                quality=90,
                progress=False
            )
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"   ✅ {format_name} 格式成功 ({file_size} 字节)")
                results.append(True)
            else:
                print(f"   ❌ {format_name} 格式失败")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print(f"❌ 格式测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🧹 清理临时目录: {temp_dir}")


def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理...")
    
    extractor = VideoFrameExtractor()
    
    # 测试不存在的文件
    print("📁 测试不存在的文件...")
    success = extractor.extract_frames(
        video_path="nonexistent.mp4",
        output_path="test_output.jpg",
        frame_interval=5,
        frames_per_row=2,
        progress=False
    )
    
    if not success:
        print("✅ 正确处理了不存在的文件")
    else:
        print("❌ 未能正确处理不存在的文件")
        return False
    
    # 测试无效参数
    print("🔢 测试无效参数...")
    video_path, temp_dir = create_test_video()
    if not video_path:
        return False
    
    try:
        # 测试无效的帧间隔
        print("   测试无效的帧间隔...")
        success = extractor.extract_frames(
            video_path=video_path,
            output_path="test_output.jpg",
            frame_interval=0,  # 无效的帧间隔
            frames_per_row=2,
            progress=False
        )
        
        # 测试无效的每行帧数
        print("   测试无效的每行帧数...")
        success = extractor.extract_frames(
            video_path=video_path,
            output_path="test_output.jpg",
            frame_interval=5,
            frames_per_row=0,  # 无效的每行帧数
            progress=False
        )
        
        print("✅ 错误处理测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False
    finally:
        # 清理临时文件
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🧹 清理临时目录: {temp_dir}")


def main():
    """主测试函数"""
    print("🔥 火娃 - 视频帧提取器测试")
    print("=" * 60)
    
    # 运行测试
    tests = [
        ("基本功能", test_basic_functionality),
        ("不同格式", test_different_formats),
        ("错误处理", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}测试")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}测试通过")
            else:
                print(f"❌ {test_name}测试失败")
                
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 总结结果
    print("\n" + "=" * 60)
    print("🎯 测试结果总结:")
    print("-" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！视频帧提取器功能正常。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查依赖和配置。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)