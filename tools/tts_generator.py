"""edge-tts 语音生成工具（返回精确时长）"""
import edge_tts
import asyncio
import os
from mutagen.mp3 import MP3
from models.script_model import Script, Segment
from config import TTS_OUTPUT_DIR, TTS_VOICE
from utils.file_utils import ensure_dir


class TTSGenerator:
    """TTS 生成器"""
    
    def __init__(self, voice: str = TTS_VOICE, output_dir: str = TTS_OUTPUT_DIR):
        self.voice = voice
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
        tasks = [
            self.generate_segment_audio(seg) 
            for seg in script.segments
        ]
        await asyncio.gather(*tasks)
        return script
