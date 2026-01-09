"""视频音频合并工具（冻结帧、平滑过渡）"""
import os
import warnings
from typing import Optional
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
from models.script_model import Script
from utils.file_utils import ensure_dir, sanitize_filename
from utils.logger import get_logger

# 抑制 moviepy 的 "Proc not detected" 警告
warnings.filterwarnings('ignore', message='.*Proc not detected.*', category=UserWarning)

logger = get_logger(__name__)


class VideoMerger:
    """视频合并器"""
    
    def __init__(
        self, 
        output_dir: str = "./output/videos",
        task_id: Optional[str] = None
    ):
        self.task_id = task_id
        # 最终输出始终保存到 output/videos 目录（不变）
        self.output_dir = output_dir
        ensure_dir(output_dir)
    
    def merge_with_freeze_frame(
        self,
        video_segments: list[tuple[int, str, float]],
        audio_segments: list[tuple[int, str, float]],
        script: Script,
        output_filename: str = None
    ) -> str:
        """合并视频和音频，使用冻结帧填充"""
        if output_filename is None:
            output_filename = sanitize_filename(script.title) + ".mp4"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # 1. 按 segment_id 排序
        video_segments = sorted(video_segments, key=lambda x: x[0])
        audio_segments = sorted(audio_segments, key=lambda x: x[0])
        
        if len(video_segments) != len(audio_segments):
            raise ValueError(f"视频片段数 ({len(video_segments)}) 与音频片段数 ({len(audio_segments)}) 不匹配")
        
        # 2. 处理每个片段
        final_clips = []
        for (vid_id, vid_path, vid_duration), (aud_id, aud_path, aud_duration) in zip(
            video_segments, audio_segments
        ):
            if vid_id != aud_id:
                raise ValueError(f"片段 ID 不匹配: 视频 {vid_id} vs 音频 {aud_id}")
            
            if not os.path.exists(vid_path):
                raise FileNotFoundError(f"视频文件不存在: {vid_path}")
            if not os.path.exists(aud_path):
                raise FileNotFoundError(f"音频文件不存在: {aud_path}")
            
            video_clip = VideoFileClip(vid_path)
            audio_clip = AudioFileClip(aud_path)
            
            logger.info(f"处理片段 {vid_id}: 视频 {vid_duration:.2f}s, 音频 {aud_duration:.2f}s")
            
            # 3. 时长匹配（视频应该已经对齐，这里做验证和调整）
            duration_diff = abs(vid_duration - aud_duration)
            if duration_diff > 0.1:
                # 如果视频比音频长，截取视频
                if vid_duration > aud_duration:
                    logger.warning(f"片段 {vid_id}: 视频比音频长 {duration_diff:.2f}s，截取视频")
                    # MoviePy 2.1.2+ 使用 subclipped() 或切片语法
                    video_clip = video_clip.subclipped(0, aud_duration)
                # 如果视频比音频短，使用最后一帧填充
                else:
                    logger.warning(f"片段 {vid_id}: 视频比音频短 {duration_diff:.2f}s，使用冻结帧填充")
                    # MoviePy 2.1.2+ 兼容：使用 get_frame 获取最后一帧，然后创建 ImageClip
                    try:
                        # 尝试使用 to_ImageClip 方法（如果可用）
                        last_frame = video_clip.to_ImageClip(t=video_clip.duration)
                    except AttributeError:
                        # 如果 to_ImageClip 不存在，使用 get_frame + ImageClip
                        last_frame_img = video_clip.get_frame(video_clip.duration)
                        last_frame = ImageClip(last_frame_img)
                    freeze_duration = aud_duration - vid_duration
                    freeze_clip = last_frame.with_duration(freeze_duration)
                    video_clip = concatenate_videoclips([video_clip, freeze_clip])
            
            # 4. 合并音频
            # MoviePy 2.1.2+ 使用 with_audio() 替代 set_audio()
            final_clip = video_clip.with_audio(audio_clip)
            final_clips.append(final_clip)
        
        # 5. 拼接所有片段
        logger.info(f"开始合并 {len(final_clips)} 个片段...")
        final_video = concatenate_videoclips(final_clips, method="compose")
        
        logger.info(f"正在写入最终视频: {output_path}")
        final_video.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac',
            fps=30,
            logger=None  # 禁用 moviepy 的日志输出
        )
        
        # 清理资源
        for clip in final_clips:
            clip.close()
        final_video.close()
        
        logger.info(f"视频合并完成: {output_path}")
        return output_path
