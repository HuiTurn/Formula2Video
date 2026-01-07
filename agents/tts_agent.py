"""edge-tts 文案生成 Agent"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.script_model import Script
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE_URL
from utils.logger import get_logger
from utils.file_utils import load_file_content

logger = get_logger(__name__)


class TTSAgent:
    """TTS 文案转换 Agent"""
    
    def __init__(self):
        extra_body = {
            "enable_thinking": False
        }
        self.llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.5,
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL,
            extra_body=extra_body
        )
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        """加载 prompt 模板"""
        prompt_text = load_file_content("prompts/tts_prompt.txt")
        return ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的文本转换专家，擅长将数学公式转换为自然的中文口语。"),
            ("user", prompt_text)
        ])
    
    def convert_script(self, script: Script) -> Script:
        """将剧本中的讲解文案转换为 TTS 友好的文本"""
        logger.info(f"开始转换 TTS 文案: {script.title}")
        
        # 将 script 转换为 JSON 字符串
        script_json = script.model_dump_json(indent=2)
        
        # 构建 prompt
        messages = self.prompt_template.format_messages(
            script_json=script_json
        )
        
        # 调用 LLM
        response = self.llm.invoke(messages)
        content = response.content
        
        # 提取 JSON
        script_data = self._extract_json(content)
        
        # 更新 script 中的 tts_text
        updated_script = self._update_tts_text(script, script_data)
        
        logger.info("TTS 文案转换完成")
        return updated_script
    
    def _extract_json(self, text: str) -> dict:
        """从文本中提取 JSON"""
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.error(f"无法解析 JSON: {text[:200]}")
            raise ValueError("无法从 LLM 响应中提取有效的 JSON")
    
    def _update_tts_text(self, script: Script, data: dict) -> Script:
        """更新 script 中的 tts_text"""
        segments_data = data.get("segments", [])
        
        # 创建 segment_id 到数据的映射
        segment_map = {seg.get("segment_id"): seg for seg in segments_data}
        
        # 更新每个 segment
        for segment in script.segments:
            if segment.segment_id in segment_map:
                segment.tts_text = segment_map[segment.segment_id].get("tts_text", segment.narration)
            else:
                # 如果没有找到，使用原始 narration
                segment.tts_text = segment.narration
        
        return script
