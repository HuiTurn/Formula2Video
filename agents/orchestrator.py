"""主编排器（音频先行流程）"""
from agents.script_agent import ScriptAgent
from agents.tts_agent import TTSAgent
from agents.manim_agent import ManimAgent
from agents.manim_fix_agent import ManimFixAgent
from tools.tts_generator import TTSGenerator
from tools.manim_executor import ManimExecutor
from tools.video_splitter import VideoSplitter
from tools.video_merger import VideoMerger
from models.script_model import Script
from utils.logger import get_logger
from utils.file_utils import save_json
from config import OUTPUT_SCRIPTS_DIR, OUTPUT_MANIM_CODE_DIR

logger = get_logger(__name__)


class VideoOrchestrator:
    """主编排器，实现音频先行策略"""
    
    def __init__(self):
        self.script_agent = ScriptAgent()
        self.tts_agent = TTSAgent()
        self.manim_agent = ManimAgent()
        self.tts_generator = TTSGenerator()
        self.manim_executor = ManimExecutor()
        self.video_splitter = VideoSplitter()
        self.video_merger = VideoMerger()
    
    async def generate_video(
        self,
        formula: str,
        duration: int = 60,
        style: str = "3Blue1Brown"
    ) -> dict:
        """生成视频的主流程"""
        logger.info(f"开始生成视频: {formula}")
        
        try:
            # 1. 生成剧本
            logger.info("步骤 1/8: 生成剧本")
            script = self.script_agent.generate(formula, duration, style)
            
            # 保存剧本
            script_path = f"{OUTPUT_SCRIPTS_DIR}/{script.title.replace(' ', '_')}.json"
            save_json(script.model_dump(), script_path)
            logger.info(f"剧本已保存: {script_path}")
            
            # 2. 生成 TTS 文案
            logger.info("步骤 2/8: 生成 TTS 文案")
            script = self.tts_agent.convert_script(script)
            
            # 3. 【音频先行】立即生成音频，获取精确时长
            logger.info("步骤 3/8: 生成音频（音频先行策略）")
            script = await self.tts_generator.generate_all_segments(script)
            
            logger.info(f"音频生成完成，各片段时长: {[f'{seg.audio_duration:.2f}s' for seg in script.segments]}")
            
            # 4. 将音频时长传给 Manim Agent
            logger.info("步骤 4/8: 生成 Manim 代码")
            audio_durations = {
                f"audio_duration_{i+1}": seg.audio_duration 
                for i, seg in enumerate(script.segments)
            }
            manim_code = self.manim_agent.generate(script, audio_durations)
            
            # 保存 Manim 代码
            code_path = f"{OUTPUT_MANIM_CODE_DIR}/{script.title.replace(' ', '_')}.py"
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(manim_code)
            logger.info(f"Manim 代码已保存: {code_path}")
            
            # 5. 执行 Manim 代码（带错误修复）
            logger.info("步骤 5/8: 执行 Manim 代码")
            max_fix_attempts = 3  # 最多修复 3 次
            fix_attempt = 0
            video_path = None
            last_error = None
            
            # 第一次尝试执行
            try:
                video_path = self.manim_executor.execute_scene(
                    manim_code, 
                    scene_name="ProjectScene",
                    output_filename=script.title.replace(" ", "_")
                )
                logger.info(f"Manim 视频已生成: {video_path}")
            except (RuntimeError, ValueError) as e:
                last_error = e
                
                # 如果第一次失败，进入修复循环
                while fix_attempt < max_fix_attempts:
                    fix_attempt += 1
                    logger.warning(f"Manim 执行失败，尝试修复 (第 {fix_attempt}/{max_fix_attempts} 次)")
                    
                    # 提取错误信息
                    error_message = str(last_error)
                    if hasattr(self.manim_executor, 'extract_error_info'):
                        error_info = self.manim_executor.extract_error_info(error_message)
                        error_message = error_info.get("full_traceback", error_message)
                    
                    # 修复代码
                    fix_agent = ManimFixAgent()
                    manim_code = fix_agent.fix(
                        code=manim_code,
                        error_message=error_message,
                        attempt=fix_attempt
                    )
                    
                    # 更新保存的代码
                    with open(code_path, 'w', encoding='utf-8') as f:
                        f.write(manim_code)
                    logger.info(f"修复后的代码已保存: {code_path}")
                    
                    # 重新尝试执行
                    try:
                        video_path = self.manim_executor.execute_scene(
                            manim_code, 
                            scene_name="ProjectScene",
                            output_filename=script.title.replace(" ", "_")
                        )
                        logger.info(f"代码修复成功，Manim 视频已生成: {video_path}")
                        break
                    except (RuntimeError, ValueError) as e:
                        last_error = e
                        if fix_attempt >= max_fix_attempts:
                            logger.error(f"Manim 执行失败，已尝试修复 {max_fix_attempts} 次，放弃修复")
                            raise
            
            if video_path is None:
                raise RuntimeError(f"Manim 执行失败: {last_error}")
            
            # 6. 切割视频片段
            logger.info("步骤 6/8: 切割视频片段")
            video_segments = self.video_splitter.split_by_segments(video_path, script)
            logger.info(f"视频切割完成，共 {len(video_segments)} 个片段")
            
            # 7. 准备音频片段
            logger.info("步骤 7/8: 准备音频片段")
            audio_segments = [
                (seg.segment_id, seg.audio_path, seg.audio_duration)
                for seg in script.segments
            ]
            
            # 8. 合并视频和音频
            logger.info("步骤 8/8: 合并视频和音频")
            output_path = self.video_merger.merge_with_freeze_frame(
                video_segments, 
                audio_segments, 
                script, 
                output_filename=script.title.replace(" ", "_") + ".mp4"
            )
            
            total_duration = script.get_total_duration()
            logger.info(f"视频生成完成: {output_path}, 总时长: {total_duration:.2f}秒")
            
            return {
                "video_path": output_path,
                "script": script,
                "total_duration": total_duration,
                "script_path": script_path,
                "code_path": code_path
            }
            
        except Exception as e:
            logger.error(f"视频生成失败: {e}", exc_info=True)
            raise
