"""公式解析器 - 识别LaTeX或中文描述，双向转换"""

import re
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class FormulaParser:
    """公式解析器"""
    
    def __init__(self):
        """初始化公式解析器"""
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
    
    def is_latex(self, text: str) -> bool:
        """
        判断输入是否是LaTeX公式
        
        Args:
            text: 输入文本
            
        Returns:
            是否是LaTeX公式
        """
        # LaTeX特征：包含数学符号、等号、上下标等
        latex_patterns = [
            r'[=+\-*/]',  # 数学运算符
            r'\^',  # 上标
            r'_',  # 下标
            r'\\',  # LaTeX命令
            r'\{',  # 大括号
            r'\('  # 小括号（数学模式）
        ]
        
        # 如果包含明显的LaTeX命令
        if '\\' in text:
            return True
        
        # 如果包含数学符号且不是纯中文
        has_math_symbols = any(re.search(pattern, text) for pattern in latex_patterns)
        is_chinese_only = bool(re.match(r'^[\u4e00-\u9fa5]+$', text))
        
        return has_math_symbols and not is_chinese_only
    
    def latex_to_chinese(self, latex: str) -> Dict[str, str]:
        """
        将LaTeX公式转换为中文描述
        
        Args:
            latex: LaTeX公式
            
        Returns:
            包含LaTeX、中文名称、描述的字典
        """
        prompt = f"""请将以下LaTeX公式转换为中文描述。

LaTeX公式：{latex}

请提供：
1. 公式的中文名称（简洁，2-8个字）
2. 公式的简要描述（1-2句话，说明公式的含义）

格式：
名称：xxx
描述：xxx

只输出名称和描述，不要其他内容。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个数学公式专家，擅长将LaTeX公式转换为中文描述。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                stream=True,  # 启用流式模式
            )
            
            # 处理流式响应
            result = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    result += chunk.choices[0].delta.content
            result = result.strip()
            
            # 解析结果
            name_match = re.search(r'名称[：:]\s*(.+)', result)
            desc_match = re.search(r'描述[：:]\s*(.+)', result)
            
            name = name_match.group(1).strip() if name_match else latex
            description = desc_match.group(1).strip() if desc_match else f"公式：{latex}"
            
            return {
                "latex": latex,
                "chinese_name": name,
                "description": description,
            }
        except Exception as e:
            # 如果转换失败，使用LaTeX作为名称
            return {
                "latex": latex,
                "chinese_name": latex,
                "description": f"公式：{latex}",
            }
    
    def chinese_to_latex(self, chinese: str) -> Dict[str, str]:
        """
        将中文描述转换为LaTeX公式
        
        Args:
            chinese: 中文描述
            
        Returns:
            包含LaTeX、中文名称、描述的字典
        """
        prompt = f"""请将以下中文公式描述转换为LaTeX公式。

中文描述：{chinese}

请提供：
1. 公式的LaTeX表达式（只输出LaTeX，不要其他文字）
2. 公式的简要描述（1-2句话）

格式：
LaTeX：xxx
描述：xxx

只输出LaTeX和描述，不要其他内容。"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个数学公式专家，擅长将中文公式描述转换为LaTeX表达式。请直接输出LaTeX公式，不要添加任何解释。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                stream=True,  # 启用流式模式
            )
            
            # 处理流式响应
            result = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    result += chunk.choices[0].delta.content
            result = result.strip()
            
            # 解析结果
            latex_match = re.search(r'LaTeX[：:]\s*(.+)', result, re.MULTILINE)
            if not latex_match:
                # 尝试直接提取LaTeX（可能在单独的行）
                lines = result.split('\n')
                for line in lines:
                    if 'LaTeX' in line or '=' in line or '^' in line or '\\' in line:
                        latex_match = re.search(r'([^：:]+)', line)
                        if latex_match:
                            break
            
            desc_match = re.search(r'描述[：:]\s*(.+)', result, re.MULTILINE)
            
            latex = latex_match.group(1).strip() if latex_match else chinese
            # 清理LaTeX（移除可能的引号）
            latex = latex.strip('"\'')
            description = desc_match.group(1).strip() if desc_match else chinese
            
            return {
                "latex": latex,
                "chinese_name": chinese,
                "description": description,
            }
        except Exception as e:
            # 如果转换失败，使用中文作为名称
            return {
                "latex": chinese,
                "chinese_name": chinese,
                "description": chinese,
            }
    
    def parse(self, input_text: str) -> Dict[str, str]:
        """
        解析公式输入（自动识别LaTeX或中文）
        
        Args:
            input_text: 输入的公式（LaTeX或中文）
            
        Returns:
            包含LaTeX、中文名称、描述的字典
        """
        input_text = input_text.strip()
        
        if self.is_latex(input_text):
            # 是LaTeX，转换为中文
            return self.latex_to_chinese(input_text)
        else:
            # 是中文，转换为LaTeX
            return self.chinese_to_latex(input_text)

