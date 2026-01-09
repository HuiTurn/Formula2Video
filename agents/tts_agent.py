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
        """从文本中提取 JSON，支持 markdown 代码块格式"""
        import re
        
        # 1. 首先尝试匹配完整的 JSON markdown 代码块
        json_block_match = re.search(r'```(?:json)?\s*(.*?)```', text, re.DOTALL)
        if json_block_match:
            json_str = json_block_match.group(1).strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                logger.warning(f"从代码块中提取的 JSON 无法解析，尝试其他方法...")
        
        # 2. 如果没有完整的代码块，尝试移除 markdown 标记
        cleaned_text = text
        # 移除开头的 ```json 或 ```
        cleaned_text = re.sub(r'^```(?:json)?\s*', '', cleaned_text, flags=re.MULTILINE)
        # 移除结尾的 ```
        cleaned_text = re.sub(r'```\s*$', '', cleaned_text, flags=re.MULTILINE)
        cleaned_text = cleaned_text.strip()
        
        # 3. 尝试在清理后的文本中匹配 JSON 对象（更健壮的方法）
        # 使用平衡括号匹配来找到完整的 JSON 对象
        start_pos = cleaned_text.find('{')
        if start_pos != -1:
            # 从第一个 { 开始，找到匹配的 }
            brace_count = 0
            for i in range(start_pos, len(cleaned_text)):
                if cleaned_text[i] == '{':
                    brace_count += 1
                elif cleaned_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_str = cleaned_text[start_pos:i+1]
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            # 继续尝试其他位置
                            break
        
        # 4. 尝试直接解析清理后的整个文本
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            logger.error(f"无法解析 JSON: {cleaned_text[:200]}...")
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
