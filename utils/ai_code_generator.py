"""AI代码生成器 - 使用ModelScope API生成Manim代码"""

import os
import re
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AICodeGenerator:
    """AI代码生成器"""
    
    def __init__(self):
        """初始化AI代码生成器"""
        api_key = os.getenv("MODELSCOPE_API_KEY")
        base_url = os.getenv("MODELSCOPE_BASE_URL")
        model = os.getenv("MODELSCOPE_MODEL")
        
        if not all([api_key, base_url, model]):
            raise ValueError("缺少ModelScope API配置，请检查.env文件")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
        self.max_retries = 3
    
    def generate_code(
        self,
        system_prompt: str,
        user_prompt: str,
        max_retries: Optional[int] = None,
    ) -> str:
        """
        生成代码
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            max_retries: 最大重试次数
            
        Returns:
            生成的代码
        """
        if max_retries is None:
            max_retries = self.max_retries


        extra_body = {
            # enable thinking, set to False to disable
            "enable_thinking": True
        }
        
        for attempt in range(max_retries):
            try:
                # ModelScope API要求使用流式模式
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    stream=True,  # 启用流式模式
                )
                
                # 处理流式响应
                code = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        code += chunk.choices[0].delta.content
                
                code = code.strip()
                
                # 提取代码块
                code = self._extract_code(code)
                
                return code
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"生成代码失败（已重试{max_retries}次）：{str(e)}")
                continue
        
        raise Exception("生成代码失败")
    
    def _extract_code(self, text: str) -> str:
        """
        从文本中提取代码
        
        Args:
            text: 包含代码的文本
            
        Returns:
            提取的代码
        """
        # 尝试提取```python代码块
        python_block = re.search(r'```python\s*\n(.*?)```', text, re.DOTALL)
        if python_block:
            return python_block.group(1).strip()
        
        # 尝试提取```代码块
        code_block = re.search(r'```\s*\n(.*?)```', text, re.DOTALL)
        if code_block:
            return code_block.group(1).strip()
        
        # 如果没有代码块标记，返回原文本
        return text.strip()
    
    def clean_code(self, code: str) -> str:
        """
        清理代码
        
        Args:
            code: 原始代码
            
        Returns:
            清理后的代码
        """
        # 移除多余的空白行
        lines = code.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            cleaned_lines.append(line)
            prev_empty = is_empty
        
        return '\n'.join(cleaned_lines)

