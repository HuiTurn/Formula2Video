"""edge-tts 语音生成工具（返回精确时长）"""
import edge_tts
import asyncio
import os
from typing import Optional
from mutagen.mp3 import MP3
from models.script_model import Script, Segment
from config import TTS_OUTPUT_DIR, TTS_VOICE, TEMP_BASE_DIR
from utils.file_utils import ensure_dir, cleanup_segment_files, get_task_subdir


class TTSGenerator:
    """TTS 生成器"""
    
    def __init__(
        self, 
        voice: str = TTS_VOICE, 
        output_dir: str = TTS_OUTPUT_DIR,
        task_id: Optional[str] = None
    ):
        self.voice = voice
        self.task_id = task_id
        # 如果有 task_id，使用任务专属目录；否则使用默认目录（向后兼容）
        if task_id:
            self.output_dir = get_task_subdir(task_id, "audio_segments", TEMP_BASE_DIR)
        else:
            self.output_dir = output_dir
            ensure_dir(output_dir)
    
    async def generate_segment_audio(
        self, 
        segment: Segment
    ) -> tuple[str, float]:
        """为单个片段生成音频，返回 (音频路径, 精确时长)"""
        output_path = os.path.join(
            self.output_dir, 
            f"segment_{segment.segment_id}.mp3"
        )
        
        # 生成音频
        communicate = edge_tts.Communicate(segment.tts_text, self.voice)
        await communicate.save(output_path)
        
        # 获取精确时长
        audio = MP3(output_path)
        duration = audio.info.length
        
        # 更新 segment
        segment.audio_path = output_path
        segment.audio_duration = duration
        
        return output_path, duration
    
    async def generate_all_segments(
        self, 
        script: Script
    ) -> Script:
        """为所有片段生成音频，更新 script 中的音频时长"""
        # 清理旧的音频片段文件，防止复用旧文件（仅在任务专属目录中清理）
        if self.task_id:
            # 任务专属目录，清理该任务的文件
            cleanup_segment_files(self.output_dir, "segment_*.mp3")
        else:
            # 向后兼容：清理全局目录的文件
            cleanup_segment_files(self.output_dir, "segment_*.mp3")
        
        tasks = [
            self.generate_segment_audio(seg) 
            for seg in script.segments
        ]
        await asyncio.gather(*tasks)
        return script
