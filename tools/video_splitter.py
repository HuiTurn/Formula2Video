"""视频切割工具（根据时间标记）"""
import os
import numpy as np
from moviepy import VideoFileClip, ImageClip
from models.script_model import Script
from utils.file_utils import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)


class VideoSplitter:
    """视频切割器"""
    
    def __init__(self, output_dir: str = "./output/video_segments"):
        self.output_dir = output_dir
        ensure_dir(output_dir)
    
    def split_by_segments(
        self, 
        video_path: str, 
        script: Script
    ) -> list[tuple[int, str, float]]:
        """
        根据 script 中的时间信息切割视频
        返回 [(segment_id, video_path, duration), ...]
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
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
                # 计算结束时间（包含 0.5 秒缓冲）
                end_time = current_time + segment.audio_duration + 0.5
                
                # 如果当前片段已经超出视频时长，需要生成冻结帧
                if current_time >= video.duration:
                    logger.warning(f"片段 {segment.segment_id} 超出视频时长，将使用冻结帧")
                    remaining_segments.append(segment)
                    continue
                
                # 确保不超过视频总时长
                if end_time > video.duration:
                    end_time = video.duration
                
                # 切割视频片段
                clip = video.subclipped(current_time, end_time)
                output_path = os.path.join(
                    self.output_dir, 
                    f"segment_{segment.segment_id}.mp4"
                )
                
                logger.info(f"切割片段 {segment.segment_id}: {current_time:.2f}s - {end_time:.2f}s")
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
