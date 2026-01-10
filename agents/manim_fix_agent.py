"""Manim 代码修复 Agent（增强版 - 带 API 验证）"""
import re
import inspect
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE_URL
from utils.logger import get_logger
from utils.file_utils import load_file_content

logger = get_logger(__name__)


class ManimFixAgent:
    """Manim 代码修复 Agent（带 API 验证）"""
    
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
        self._manim_api_cache: Dict[str, Any] = {}
    
    def _inspect_manim_api(self, class_name: str) -> Optional[str]:
        """检查 Manim API 的实际签名"""
        try:
            # 动态导入 manim
            import manim
            
            # 获取类
            if not hasattr(manim, class_name):
                return None
            
            cls = getattr(manim, class_name)
            
            # 获取 __init__ 方法的签名
            sig = inspect.signature(cls.__init__)
            
            # 格式化参数信息
            params = []
            for name, param in sig.parameters.items():
                if name == 'self':
                    continue
                param_info = name
                if param.default != inspect.Parameter.empty:
                    try:
                        # 安全地处理默认值
                        default_repr = repr(param.default)
                        # 如果默认值太长，截断
                        if len(default_repr) > 50:
                            default_repr = default_repr[:47] + "..."
                        param_info += f"={default_repr}"
                    except Exception:
                        # 如果无法表示默认值，跳过
                        pass
                if param.annotation != inspect.Parameter.empty:
                    try:
                        # 安全地处理类型注解
                        if hasattr(param.annotation, '__name__'):
                            param_info += f": {param.annotation.__name__}"
                        elif hasattr(param.annotation, '__qualname__'):
                            param_info += f": {param.annotation.__qualname__}"
                        else:
                            # 尝试转换为字符串，但捕获异常
                            annotation_str = str(param.annotation)
                            # 如果字符串太长，截断
                            if len(annotation_str) > 50:
                                annotation_str = annotation_str[:47] + "..."
                            param_info += f": {annotation_str}"
                    except Exception:
                        # 如果无法表示类型，跳过
                        pass
                params.append(param_info)
            
            return f"{class_name}({', '.join(params)})"
        except Exception as e:
            # 只在调试模式下输出详细错误，避免警告日志过多
            logger.debug(f"无法检查 {class_name} 的 API: {e}")
            return None
    
    def _extract_api_info_from_error(self, error_message: str) -> Dict[str, str]:
        """从错误信息中提取需要检查的 API"""
        api_info = {}
        
        # 检查 Sector 相关错误
        if "Sector" in error_message or "AnnularSector" in error_message or "outer_radius" in error_message:
            sector_info = self._inspect_manim_api("Sector")
            if sector_info:
                api_info["Sector"] = sector_info
            api_info["Sector_Note"] = "Sector 类使用 `radius` 参数，不是 `outer_radius`。正确用法：Sector(radius=3, angle=PI/6, start_angle=0)"
        
        # 检查 MathTex 相关错误（中文或 LaTeX 错误）
        if ("MathTex" in error_message and 
            ("中文" in error_message or "latex error" in error_message.lower() or "dvi" in error_message.lower())):
            api_info["MathTex_Note"] = "MathTex 不支持中文，应使用 Text() 类。包含中文的文本必须使用 Text()，如 Text('面积 = 高 × 宽', font_size=24)"
        
        # 检查其他常见类
        common_classes = ["Circle", "Rectangle", "Text", "MathTex", "Tex", "AnnularSector"]
        for cls_name in common_classes:
            if cls_name in error_message:
                cls_info = self._inspect_manim_api(cls_name)
                if cls_info:
                    api_info[cls_name] = cls_info
        
        return api_info
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        """加载修复 prompt 模板"""
        prompt_text = load_file_content("prompts/manim_fix_prompt.txt")
        
        # 转义所有非模板变量的大括号
        # 模板变量：{error_message}, {original_code}, {attempt_number}, {api_info}
        
        # 定义模板变量列表
        template_vars = ["error_message", "original_code", "attempt_number", "api_info"]
        
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
    
    async def fix(
        self,
        code: str,
        error_message: str,
        attempt: int = 1
    ) -> str:
        """修复 Manim 代码（带 API 验证）"""
        logger.info(f"开始修复 Manim 代码 (第 {attempt} 次尝试)")
        
        # 提取 API 信息
        api_info = self._extract_api_info_from_error(error_message)
        
        # 格式化 API 信息
        api_info_text = self._format_api_info(api_info)
        
        # 构建 prompt（包含 API 信息）
        messages = self.prompt_template.format_messages(
            original_code=code,
            error_message=error_message,
            attempt_number=attempt,
            api_info=api_info_text
        )
        
        # 调用 LLM（异步）
        response = await self.llm.ainvoke(messages)
        fixed_code = response.content
        
        # 提取代码块（如果有 markdown 代码块）
        fixed_code = self._extract_code(fixed_code)
        
        logger.info(f"代码修复完成，修复后代码长度: {len(fixed_code)} 字符")
        return fixed_code
    
    def _format_api_info(self, api_info: Dict[str, str]) -> str:
        """格式化 API 信息为字符串"""
        if not api_info:
            return "无相关 API 信息"
        
        lines = ["**Manim v0.19.1 API 信息：**"]
        for key, value in api_info.items():
            if key.endswith("_Note"):
                lines.append(f"- {value}")
            else:
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
    
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
