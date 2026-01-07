"""视听剧本生成 Agent"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.script_model import Script, Segment
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE_URL
from utils.logger import get_logger
from utils.file_utils import load_file_content

logger = get_logger(__name__)


class ScriptAgent:
    """剧本生成 Agent"""
    
    def __init__(self):
        extra_body = {
            "enable_thinking": False
        }
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL,
            extra_body=extra_body
        )
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        """加载 prompt 模板"""
        prompt_text = load_file_content("prompts/script_prompt.txt")
        return ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的数学教学视频编剧。"),
            ("user", prompt_text)
        ])
    
    def generate(
        self, 
        formula: str, 
        duration: int = 60, 
        style: str = "3Blue1Brown"
    ) -> Script:
        """生成剧本"""
        logger.info(f"开始生成剧本: {formula}, 时长: {duration}秒, 风格: {style}")
        
        # 构建 prompt
        messages = self.prompt_template.format_messages(
            formula=formula,
            duration=duration,
            style=style
        )
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        content = response.content
        
        # 尝试从响应中提取 JSON
        script_data = self._extract_json(content)
        
        # 转换为 Script 对象
        script = self._parse_script(script_data)
        
        logger.info(f"剧本生成完成: {script.title}, 共 {len(script.segments)} 个片段")
        return script
    
    def _extract_json(self, text: str) -> dict:
        """从文本中提取 JSON"""
        # 尝试找到 JSON 代码块
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # 如果找不到，尝试直接解析整个文本
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.error(f"无法解析 JSON: {text[:200]}")
            raise ValueError("无法从 LLM 响应中提取有效的 JSON")
    
    def _parse_script(self, data: dict) -> Script:
        """解析剧本数据"""
        segments = []
        for seg_data in data.get("segments", []):
            segment = Segment(
                segment_id=seg_data.get("segment_id", len(segments) + 1),
                visual=seg_data.get("visual", ""),
                narration=seg_data.get("narration", ""),
                tts_text=""  # 稍后由 TTS Agent 填充
            )
            segments.append(segment)
        
        return Script(
            title=data.get("title", "未命名视频"),
            segments=segments
        )
