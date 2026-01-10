"""Manim 代码生成 Agent"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.script_model import Script
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE_URL
from utils.logger import get_logger
from utils.file_utils import load_file_content

logger = get_logger(__name__)


class ManimAgent:
    """Manim 代码生成 Agent"""
    
    def __init__(self):
        extra_body = {
            "enable_thinking": False
        }
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.1,  # 极低温度，确保严格遵循剧本坐标，提高精确性
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL,
            extra_body=extra_body
        )
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        """加载 prompt 模板"""
        prompt_text = load_file_content("prompts/manim_prompt.txt")
        return ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的 Manim 代码生成专家。"),
            ("user", prompt_text)
        ])
    
    async def generate(
        self, 
        script: Script, 
        audio_durations: dict
    ) -> str:
        """生成 Manim 代码"""
        logger.info(f"开始生成 Manim 代码: {script.title}")
        
        # 将 script 转换为 JSON 字符串
        script_json = script.model_dump_json(indent=2)
        
        # 格式化音频时长信息
        audio_durations_text = "\n".join([
            f"- {key}: {value}秒" 
            for key, value in audio_durations.items()
        ])
        
        # 构建 prompt
        messages = self.prompt_template.format_messages(
            script_json=script_json,
            audio_durations=audio_durations_text
        )
        
        # 调用 LLM（异步）
        response = await self.llm.ainvoke(messages)
        code = response.content
        
        # 提取代码块（如果有 markdown 代码块）
        code = self._extract_code(code)
        
        logger.info(f"Manim 代码生成完成，代码长度: {len(code)} 字符")
        return code
    
    def _extract_code(self, text: str) -> str:
        """从文本中提取代码"""
        import re
        
        # 首先尝试匹配完整的 Python 代码块
        code_match = re.search(r'```(?:python)?\s*(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # 如果没有完整的代码块，尝试移除开头的 markdown 标记
        # 移除开头的 ```python 或 ```
        text = re.sub(r'^```(?:python)?\s*', '', text, flags=re.MULTILINE)
        # 移除结尾的 ```
        text = re.sub(r'```\s*$', '', text, flags=re.MULTILINE)
        
        # 再次尝试匹配（处理嵌套情况）
        code_match = re.search(r'```(?:python)?\s*(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # 如果还是没有匹配到，返回清理后的文本
        return text.strip()
