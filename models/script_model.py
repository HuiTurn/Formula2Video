"""剧本数据模型"""
from pydantic import BaseModel
from typing import List, Optional


class Segment(BaseModel):
    """视频片段"""
    segment_id: int
    visual: str                  # 视觉画面描述
    narration: str              # 讲解文案
    tts_text: str               # TTS 转换后的文本
    audio_path: Optional[str] = None      # 音频文件路径
    audio_duration: Optional[float] = None # 精确音频时长（秒）
    start_time: Optional[float] = None     # 在最终视频中的开始时间
    end_time: Optional[float] = None       # 在最终视频中的结束时间


class Script(BaseModel):
    """剧本"""
    title: str
    segments: List[Segment]
    
    def get_total_duration(self) -> float:
        """计算总时长（基于音频时长）"""
        return sum(seg.audio_duration for seg in self.segments if seg.audio_duration)
