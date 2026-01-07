"""配置管理模块"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Manim 配置
MANIM_OUTPUT_DIR = os.getenv("MANIM_OUTPUT_DIR", "./media/videos")
MANIM_QUALITY = os.getenv("MANIM_QUALITY", "medium_quality")  # low_quality, medium_quality, high_quality

# TTS 配置
TTS_OUTPUT_DIR = os.getenv("TTS_OUTPUT_DIR", "./audio/segments")
TTS_VOICE = os.getenv("TTS_VOICE", "zh-CN-XiaoxiaoNeural")

# 输出目录配置
OUTPUT_SCRIPTS_DIR = "./output/scripts"
OUTPUT_TTS_TEXTS_DIR = "./output/tts_texts"
OUTPUT_MANIM_CODE_DIR = "./output/manim_code"
OUTPUT_VIDEOS_DIR = "./output/videos"
OUTPUT_VIDEO_SEGMENTS_DIR = "./output/video_segments"
OUTPUT_AUDIO_SEGMENTS_DIR = "./output/audio_segments"
