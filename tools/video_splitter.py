"""视频切割工具（根据时间标记）"""
import os
import asyncio
import warnings
import numpy as np
from typing import Optional
from moviepy import VideoFileClip, ImageClip
from models.script_model import Script
from config import TEMP_BASE_DIR
from utils.file_utils import ensure_dir, cleanup_segment_files, get_task_subdir
from utils.logger import get_logger

# 抑制 moviepy 的 "Proc not detected" 警告
warnings.filterwarnings('ignore', message='.*Proc not detected.*', category=UserWarning)

logger = get_logger(__name__)


class VideoSplitter:
    """视频切割器"""
    
    def __init__(
        self, 
        output_dir: str = "./output/video_segments",
        task_id: Optional[str] = None
    ):
        self.task_id = task_id
        # 如果有 task_id，使用任务专属目录；否则使用默认目录（向后兼容）
        if task_id:
            self.output_dir = get_task_subdir(task_id, "video_segments", TEMP_BASE_DIR)
        else:
            self.output_dir = output_dir
            ensure_dir(output_dir)
    
    async def split_by_segments(
        self, 
        video_path: str, 
        script: Script
    ) -> list[tuple[int, str, float]]:
        """
        根据 script 中的音频时长信息精确切割视频
        
        严格按照每个片段的 audio_duration 进行切割，确保音画同步。
        如果视频片段时长不足，会在合并时用冻结帧填充（由 video_merger 处理）。
        
        返回 [(segment_id, video_path, duration), ...]
        """
        # 清理旧的视频片段文件，防止复用旧文件（仅在任务专属目录中清理）
        if self.task_id:
            # 任务专属目录，清理该任务的文件
            cleanup_segment_files(self.output_dir, "segment_*.mp4")
        else:
            # 向后兼容：清理全局目录的文件
            cleanup_segment_files(self.output_dir, "segment_*.mp4")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        # 使用异步线程执行视频处理操作
        return await asyncio.to_thread(self._split_by_segments_sync, video_path, script)
    
    def _split_by_segments_sync(
        self, 
        video_path: str, 
        script: Script
    ) -> list[tuple[int, str, float]]:
        """同步的视频切割实现（在后台线程中执行）"""
        video = VideoFileClip(video_path)
        segments = []
        
        # 提前提取最后一帧，用于生成冻结帧
        last_frame = None
        try:
            if video.duration > 0:
                # 获取最后一帧（稍微提前一点，避免边界问题）
                last_frame_time = max(0, video.duration - 0.01)
                last_frame = video.get_frame(last_frame_time)
        except Exception as e:
            logger.warning(f"无法提取视频最后一帧: {e}，将使用黑色画面作为冻结帧")
            # 如果无法提取，创建一个黑色画面
            if video.size:
                last_frame = np.zeros((int(video.h), int(video.w), 3), dtype=np.uint8)
        
        current_time = 0.0
        remaining_segments = []  # 记录需要生成冻结帧的片段
        
        for segment in script.segments:
            if segment.audio_duration:
                # 严格按照音频时长切割视频，确保音画同步
                end_time = current_time + segment.audio_duration
                
                # 如果当前片段已经超出视频时长，需要生成冻结帧
                if current_time >= video.duration:
                    logger.warning(f"片段 {segment.segment_id} 超出视频时长，将使用冻结帧")
                    remaining_segments.append(segment)
                    continue
                
                # 确保不超过视频总时长
                if end_time > video.duration:
                    end_time = video.duration
                
                # 切割视频片段（严格按照音频时长，如果视频不够长会在合并时用冻结帧填充）
                clip = video.subclipped(current_time, end_time)
                output_path = os.path.join(
                    self.output_dir, 
                    f"segment_{segment.segment_id}.mp4"
                )
                
                logger.info(f"切割片段 {segment.segment_id}: {current_time:.2f}s - {end_time:.2f}s (音频时长: {segment.audio_duration:.2f}s)")
                # 在关闭前保存 duration
                clip_duration = clip.duration
                clip.write_videofile(
                    output_path, 
                    codec='libx264', 
                    audio_codec='aac',
                    logger=None  # 禁用 moviepy 的日志输出
                )
                clip.close()
                
                segments.append((segment.segment_id, output_path, clip_duration))
                current_time = end_time
        
        # 为超出视频时长的片段生成冻结帧
        if remaining_segments:
            logger.info(f"为 {len(remaining_segments)} 个片段生成冻结帧视频")
            
            # 如果无法提取最后一帧，创建一个黑色画面
            if last_frame is None:
                if video.size:
                    last_frame = np.zeros((int(video.h), int(video.w), 3), dtype=np.uint8)
                else:
                    # 如果视频没有尺寸信息，创建一个默认尺寸的画面
                    last_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            
            for segment in remaining_segments:
                if segment.audio_duration:
                    output_path = os.path.join(
                        self.output_dir, 
                        f"segment_{segment.segment_id}.mp4"
                    )
                    
                    # 创建冻结帧视频
                    freeze_clip = ImageClip(last_frame, duration=segment.audio_duration)
                    
                    logger.info(f"生成冻结帧片段 {segment.segment_id}: 时长 {segment.audio_duration:.2f}s")
                    freeze_clip.write_videofile(
                        output_path,
                        codec='libx264',
                        fps=30,  # 设置帧率
                        logger=None  # 禁用 moviepy 的日志输出
                    )
                    freeze_clip.close()
                    
                    segments.append((segment.segment_id, output_path, segment.audio_duration))
        
        video.close()
        logger.info(f"视频切割完成，共 {len(segments)} 个片段（其中 {len(remaining_segments)} 个为冻结帧）")
        return segments
