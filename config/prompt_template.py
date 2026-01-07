"""提示词模板管理器"""

import os
from pathlib import Path
from typing import Dict, Optional
from utils.grade_converter import get_grade_level, convert_subject_to_chinese


class PromptTemplate:
    """提示词模板管理器"""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """
        初始化提示词模板管理器
        
        Args:
            prompts_dir: 提示词文件目录，默认为项目根目录下的prompts
        """
        if prompts_dir is None:
            # 获取项目根目录
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            prompts_dir = project_root / "prompts"
        else:
            prompts_dir = Path(prompts_dir)
        
        self.prompts_dir = prompts_dir
        self.system_prompt_file = prompts_dir / "system_prompt.txt"
        self.user_prompt_file = prompts_dir / "user_prompt.txt"
        
        # 加载提示词
        self._system_prompt = None
        self._user_prompt_template = None
    
    def load_system_prompt(self) -> str:
        """
        加载系统提示词
        
        Returns:
            系统提示词内容
        """
        if self._system_prompt is None:
            if not self.system_prompt_file.exists():
                raise FileNotFoundError(f"系统提示词文件不存在：{self.system_prompt_file}")
            
            with open(self.system_prompt_file, "r", encoding="utf-8") as f:
                self._system_prompt = f.read()
        
        return self._system_prompt
    
    def load_user_prompt_template(self) -> str:
        """
        加载用户提示词模板
        
        Returns:
            用户提示词模板内容
        """
        if self._user_prompt_template is None:
            if not self.user_prompt_file.exists():
                raise FileNotFoundError(f"用户提示词模板文件不存在：{self.user_prompt_file}")
            
            with open(self.user_prompt_file, "r", encoding="utf-8") as f:
                self._user_prompt_template = f.read()
        
        return self._user_prompt_template
    
    def fill_user_prompt(
        self,
        formula_latex: str,
        formula_name: str,
        formula_description: str,
        subject: str,
        grade: str,
        scene_class_name: str,
    ) -> str:
        """
        填充用户提示词模板
        
        Args:
            formula_latex: 公式LaTeX表达式
            formula_name: 公式名称（中文）
            formula_description: 公式描述
            subject: 学科（math/physics/chemistry）
            grade: 年级（标准格式或中文）
            scene_class_name: 场景类名
            
        Returns:
            填充后的用户提示词
        """
        template = self.load_user_prompt_template()
        
        # 获取年级级别描述
        grade_level = get_grade_level(grade)
        
        # 填充占位符
        user_prompt = template.format(
            formula_latex=formula_latex,
            formula_name=formula_name,
            formula_description=formula_description,
            subject=convert_subject_to_chinese(subject),
            grade=grade,
            grade_level=grade_level,
            scene_class_name=scene_class_name,
        )
        
        return user_prompt
    
    def get_full_prompt(
        self,
        formula_latex: str,
        formula_name: str,
        formula_description: str,
        subject: str,
        grade: str,
        scene_class_name: str,
    ) -> Dict[str, str]:
        """
        获取完整的提示词（系统提示词 + 用户提示词）
        
        Args:
            formula_latex: 公式LaTeX表达式
            formula_name: 公式名称（中文）
            formula_description: 公式描述
            subject: 学科（math/physics/chemistry）
            grade: 年级（标准格式或中文）
            scene_class_name: 场景类名
            
        Returns:
            包含system和user的字典
        """
        system_prompt = self.load_system_prompt()
        user_prompt = self.fill_user_prompt(
            formula_latex=formula_latex,
            formula_name=formula_name,
            formula_description=formula_description,
            subject=subject,
            grade=grade,
            scene_class_name=scene_class_name,
        )
        
        return {
            "system": system_prompt,
            "user": user_prompt,
        }

