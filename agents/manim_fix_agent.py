"""Manim 代码修复 Agent"""
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE_URL
from utils.logger import get_logger
from utils.file_utils import load_file_content

logger = get_logger(__name__)


class ManimFixAgent:
    """Manim 代码修复 Agent"""
    
    def __init__(self):
        extra_body = {
            "enable_thinking": False
        }
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.2,  # 更低温度，确保修复准确性
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL,
            extra_body=extra_body
        )
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        """加载修复 prompt 模板"""
        prompt_text = load_file_content("prompts/manim_fix_prompt.txt")
        
        # 转义所有非模板变量的大括号
        # 模板变量：{error_message}, {original_code}, {attempt_number}
        
        # 定义模板变量列表
        template_vars = ["error_message", "original_code", "attempt_number"]
        
        # 保护模板变量（临时替换为特殊标记）
        protected_vars = {}
        for var in template_vars:
            placeholder = f"__TEMPLATE_VAR_{var.upper()}__"
            prompt_text = prompt_text.replace(f"{{{var}}}", placeholder)
            protected_vars[placeholder] = f"{{{var}}}"
        
        # 转义所有剩余的单大括号（但跳过已经是双大括号的）
        # 使用正则表达式匹配单个大括号（前后都不是大括号）
        prompt_text = re.sub(r'(?<!\{)\{(?!\{)', '{{', prompt_text)
        prompt_text = re.sub(r'(?<!\})\}(?!\})', '}}', prompt_text)
        
        # 恢复模板变量
        for placeholder, var in protected_vars.items():
            prompt_text = prompt_text.replace(placeholder, var)
        
        return ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的 Manim 代码修复专家。你的任务是分析错误并修复代码，保持代码结构和功能不变。"),
            ("user", prompt_text)
        ])
    
    def fix(
        self,
        code: str,
        error_message: str,
        attempt: int = 1
    ) -> str:
        """修复 Manim 代码"""
        logger.info(f"开始修复 Manim 代码 (第 {attempt} 次尝试)")
        
        # 构建 prompt
        messages = self.prompt_template.format_messages(
            original_code=code,
            error_message=error_message,
            attempt_number=attempt
        )
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        fixed_code = response.content
        
        # 提取代码块（如果有 markdown 代码块）
        fixed_code = self._extract_code(fixed_code)
        
        logger.info(f"代码修复完成，修复后代码长度: {len(fixed_code)} 字符")
        return fixed_code
    
    def _extract_code(self, text: str) -> str:
        """从文本中提取代码"""
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
