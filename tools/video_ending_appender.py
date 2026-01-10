"""视频片尾添加工具"""
import os
import glob
import warnings
import argparse
from typing import Optional, List, Dict, Any
from moviepy import VideoFileClip, concatenate_videoclips
from utils.file_utils import ensure_dir
from utils.logger import get_logger

# 抑制 moviepy 的 "Proc not detected" 警告
warnings.filterwarnings('ignore', message='.*Proc not detected.*', category=UserWarning)

logger = get_logger(__name__)

# 支持的视频格式
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v']


class VideoEndingAppender:
    """视频片尾添加器"""
    
    def __init__(
        self, 
        output_dir: str = "./output/videos",
        task_id: Optional[str] = None
    ):
        """
        初始化视频片尾添加器
        
        Args:
            output_dir: 输出目录，默认为 "./output/videos"
            task_id: 可选的任务ID，用于任务隔离
        """
        self.task_id = task_id
        self.output_dir = output_dir
        ensure_dir(output_dir)
    
    def _find_video_files(self, video_dir: str) -> List[str]:
        """
        查找目录中的所有视频文件
        
        Args:
            video_dir: 视频目录路径
        
        Returns:
            视频文件路径列表
        """
        video_files = []
        for ext in VIDEO_EXTENSIONS:
            pattern = os.path.join(video_dir, f"*{ext}")
            video_files.extend(glob.glob(pattern))
            # 也搜索大写扩展名
            pattern_upper = os.path.join(video_dir, f"*{ext.upper()}")
            video_files.extend(glob.glob(pattern_upper))
        
        # 去重并排序
        video_files = sorted(list(set(video_files)))
        logger.info(f"在目录 {video_dir} 中找到 {len(video_files)} 个视频文件")
        return video_files
    
    def _resize_ending_to_match(self, ending_clip: VideoFileClip, main_clip: VideoFileClip) -> VideoFileClip:
        """
        调整片尾视频尺寸以匹配主视频
        
        Args:
            ending_clip: 片尾视频片段
            main_clip: 主视频片段
        
        Returns:
            调整后的片尾视频片段
        """
        main_size = main_clip.size
        ending_size = ending_clip.size
        
        # 如果尺寸相同，直接返回
        if main_size == ending_size:
            return ending_clip
        
        logger.info(f"调整片尾尺寸: {ending_size} -> {main_size}")
        # 使用 resize 方法调整尺寸，保持宽高比
        resized_ending = ending_clip.resized(main_size)
        return resized_ending
    
    def add_ending_to_video(
        self,
        video_path: str,
        ending_path: str,
        output_path: Optional[str] = None,
        prefix: str = "final_"
    ) -> Dict[str, Any]:
        """
        为单个视频添加片尾
        
        Args:
            video_path: 主视频文件路径
            ending_path: 片尾视频文件路径
            output_path: 输出文件路径（可选，如果不提供则自动生成）
            prefix: 输出文件名前缀，默认为 "final_"
        
        Returns:
            包含处理结果的字典，包含 success, input_path, output_path, error 等字段
        """
        result = {
            "success": False,
            "input_path": video_path,
            "output_path": None,
            "error": None
        }
        
        try:
            # 检查文件是否存在
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"视频文件不存在: {video_path}")
            if not os.path.exists(ending_path):
                raise FileNotFoundError(f"片尾视频文件不存在: {ending_path}")
            
            # 生成输出路径
            if output_path is None:
                video_dir = os.path.dirname(video_path)
                video_filename = os.path.basename(video_path)
                output_filename = prefix + video_filename
                output_path = os.path.join(self.output_dir, output_filename)
            
            logger.info(f"处理视频: {video_path}")
            logger.info(f"添加片尾: {ending_path}")
            logger.info(f"输出路径: {output_path}")
            
            # 加载视频
            main_clip = VideoFileClip(video_path)
            ending_clip = VideoFileClip(ending_path)
            
            # 调整片尾尺寸以匹配主视频
            ending_clip = self._resize_ending_to_match(ending_clip, main_clip)
            
            # 拼接视频（片尾会覆盖主视频末尾的音频）
            final_video = concatenate_videoclips([main_clip, ending_clip], method="compose")
            
            # 写入文件
            logger.info(f"正在写入最终视频: {output_path}")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30,
                logger=None  # 禁用 moviepy 的日志输出
            )
            
            # 清理资源
            main_clip.close()
            ending_clip.close()
            final_video.close()
            
            result["success"] = True
            result["output_path"] = output_path
            logger.info(f"视频处理完成: {output_path}")
            
        except Exception as e:
            error_msg = str(e)
            result["error"] = error_msg
            logger.error(f"处理视频失败 {video_path}: {error_msg}")
        
        return result
    
    def add_ending_to_videos(
        self,
        video_dir: str,
        ending_path: str,
        output_dir: Optional[str] = None,
        prefix: str = "final_"
    ) -> List[Dict[str, Any]]:
        """
        为指定目录下的所有视频添加片尾
        
        Args:
            video_dir: 包含视频文件的目录路径
            ending_path: 片尾视频文件路径
            output_dir: 输出目录（可选，如果不提供则使用实例的 output_dir）
            prefix: 输出文件名前缀，默认为 "final_"
        
        Returns:
            处理结果列表，每个元素包含 success, input_path, output_path, error 等字段
        """
        if output_dir is not None:
            # 如果提供了输出目录，临时更新
            original_output_dir = self.output_dir
            self.output_dir = output_dir
            ensure_dir(output_dir)
        else:
            original_output_dir = None
        
        # 检查片尾文件是否存在
        if not os.path.exists(ending_path):
            raise FileNotFoundError(f"片尾视频文件不存在: {ending_path}")
        
        # 查找所有视频文件
        video_files = self._find_video_files(video_dir)
        
        if not video_files:
            logger.warning(f"在目录 {video_dir} 中未找到任何视频文件")
            if original_output_dir is not None:
                self.output_dir = original_output_dir
            return []
        
        # 处理每个视频文件
        results = []
        success_count = 0
        fail_count = 0
        
        logger.info(f"开始处理 {len(video_files)} 个视频文件...")
        
        for i, video_path in enumerate(video_files, 1):
            logger.info(f"[{i}/{len(video_files)}] 处理: {os.path.basename(video_path)}")
            result = self.add_ending_to_video(video_path, ending_path, prefix=prefix)
            results.append(result)
            
            if result["success"]:
                success_count += 1
            else:
                fail_count += 1
        
        # 恢复原始输出目录
        if original_output_dir is not None:
            self.output_dir = original_output_dir
        
        logger.info(f"处理完成: 成功 {success_count} 个，失败 {fail_count} 个")
        return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="为指定目录下的所有视频添加片尾",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 为 output/videos 目录下的所有视频添加片尾，输出到默认目录
  uv run python -m tools.video_ending_appender ./output/videos ./path/to/ending.mp4

  # 指定输出目录
  uv run python -m tools.video_ending_appender ./output/videos ./path/to/ending.mp4 -o ./output/final_videos

  # 自定义文件前缀
  uv run python -m tools.video_ending_appender ./output/videos ./path/to/ending.mp4 -p "with_ending_"
        """
    )
    
    parser.add_argument(
        "video_dir",
        type=str,
        help="包含视频文件的目录路径"
    )
    
    parser.add_argument(
        "ending_path",
        type=str,
        help="片尾视频文件路径"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        dest="output_dir",
        help="输出目录（可选，如果不指定则使用默认目录 ./output/videos）"
    )
    
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default="final_",
        help="输出文件名前缀，默认为 'final_'"
    )
    
    args = parser.parse_args()
    
    # 验证输入目录是否存在
    if not os.path.exists(args.video_dir):
        print(f"错误: 视频目录不存在: {args.video_dir}")
        return 1
    
    if not os.path.isdir(args.video_dir):
        print(f"错误: 不是有效的目录: {args.video_dir}")
        return 1
    
    # 验证片尾文件是否存在
    if not os.path.exists(args.ending_path):
        print(f"错误: 片尾视频文件不存在: {args.ending_path}")
        return 1
    
    if not os.path.isfile(args.ending_path):
        print(f"错误: 不是有效的文件: {args.ending_path}")
        return 1
    
    # 确定输出目录
    output_dir = args.output_dir if args.output_dir else "./output/videos"
    
    try:
        # 创建工具实例
        appender = VideoEndingAppender(output_dir=output_dir)
        
        # 处理视频
        print(f"\n开始处理目录: {args.video_dir}")
        print(f"片尾视频: {args.ending_path}")
        print(f"输出目录: {output_dir}")
        print(f"文件前缀: {args.prefix}")
        print("=" * 60)
        
        results = appender.add_ending_to_videos(
            video_dir=args.video_dir,
            ending_path=args.ending_path,
            output_dir=output_dir,
            prefix=args.prefix
        )
        
        # 输出结果
        print("\n" + "=" * 60)
        success_count = sum(1 for r in results if r["success"])
        fail_count = len(results) - success_count
        
        print(f"处理完成: 成功 {success_count}/{len(results)}, 失败 {fail_count}/{len(results)}")
        print("=" * 60)
        
        if success_count > 0:
            print("\n成功处理的视频:")
            for result in results:
                if result["success"]:
                    print(f"  ✓ {os.path.basename(result['input_path'])}")
                    print(f"    → {result['output_path']}")
        
        if fail_count > 0:
            print("\n处理失败的视频:")
            for result in results:
                if not result["success"]:
                    print(f"  ✗ {os.path.basename(result['input_path'])}")
                    print(f"    错误: {result['error']}")
        
        print("=" * 60)
        
        return 0 if fail_count == 0 else 1
        
    except Exception as e:
        logger.error(f"处理失败: {e}", exc_info=True)
        print(f"\n错误: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

