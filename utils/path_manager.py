"""路径管理器 - 管理输出路径"""

import os
from pathlib import Path
from typing import Optional
from utils.grade_converter import get_grade_level, convert_subject_to_chinese


class PathManager:
    """路径管理器"""
    
    def __init__(self, base_output_dir: str = "output"):
        """
        初始化路径管理器
        
        Args:
            base_output_dir: 基础输出目录
        """
        self.base_output_dir = Path(base_output_dir)
    
    def get_formula_dir(
        self,
        formula_chinese_name: str,
        grade: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> Path:
        """
        获取公式目录路径
        
        Args:
            formula_chinese_name: 公式中文名
            grade: 年级（可选）
            subject: 学科（可选）
            
        Returns:
            公式目录路径
        """
        path_parts = [self.base_output_dir]
        
        # 如果指定了年级，添加到路径
        if grade:
            grade_level = get_grade_level(grade)
            path_parts.append(grade_level)
        
        # 如果指定了学科，添加到路径
        if subject:
            subject_chinese = convert_subject_to_chinese(subject)
            path_parts.append(subject_chinese)
        
        # 添加公式目录
        path_parts.append(formula_chinese_name)
        
        formula_dir = Path(*path_parts)
        
        # 创建目录
        formula_dir.mkdir(parents=True, exist_ok=True)
        
        return formula_dir
    
    def get_audio_dir(
        self,
        formula_chinese_name: str,
        grade: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> Path:
        """
        获取音频目录路径
        
        Args:
            formula_chinese_name: 公式中文名
            grade: 年级（可选）
            subject: 学科（可选）
            
        Returns:
            音频目录路径
        """
        formula_dir = self.get_formula_dir(formula_chinese_name, grade, subject)
        audio_dir = formula_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        return audio_dir
    
    def get_video_dir(
        self,
        formula_chinese_name: str,
        grade: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> Path:
        """
        获取视频目录路径
        
        Args:
            formula_chinese_name: 公式中文名
            grade: 年级（可选）
            subject: 学科（可选）
            
        Returns:
            视频目录路径
        """
        formula_dir = self.get_formula_dir(formula_chinese_name, grade, subject)
        video_dir = formula_dir / "videos"
        video_dir.mkdir(parents=True, exist_ok=True)
        return video_dir
    
    def get_audio_file_path(
        self,
        formula_chinese_name: str,
        step: int,
        grade: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> Path:
        """
        获取音频文件路径
        
        Args:
            formula_chinese_name: 公式中文名
            step: 步骤编号
            grade: 年级（可选）
            subject: 学科（可选）
            
        Returns:
            音频文件路径
        """
        audio_dir = self.get_audio_dir(formula_chinese_name, grade, subject)
        return audio_dir / f"step{step}.mp3"
    
    def get_video_file_path(
        self,
        formula_chinese_name: str,
        video_name: str,
        grade: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> Path:
        """
        获取视频文件路径
        
        Args:
            formula_chinese_name: 公式中文名
            video_name: 视频文件名
            grade: 年级（可选）
            subject: 学科（可选）
            
        Returns:
            视频文件路径
        """
        video_dir = self.get_video_dir(formula_chinese_name, grade, subject)
        return video_dir / video_name

