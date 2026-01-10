"""Manim 代码执行工具（单 Scene 支持）"""
import subprocess
import asyncio
import os
from typing import Optional
from utils.validation import LaTeXValidator
from config import MANIM_OUTPUT_DIR, MANIM_QUALITY, TEMP_BASE_DIR
from utils.file_utils import ensure_dir, get_task_subdir
from utils.logger import get_logger

logger = get_logger(__name__)


class ManimExecutor:
    """Manim 执行器"""
    
    def __init__(
        self, 
        output_dir: str = MANIM_OUTPUT_DIR, 
        quality: str = MANIM_QUALITY,
        task_id: Optional[str] = None
    ):
        self.output_dir = output_dir
        self.quality = quality
        self.task_id = task_id
        ensure_dir(output_dir)
    
    def validate_code(self, code: str) -> tuple[bool, list[str]]:
        """验证 Manim 代码（包括 LaTeX）"""
        # 1. LaTeX 验证
        latex_valid, latex_errors = LaTeXValidator.validate_code_formulas(code)
        if not latex_valid:
            return False, latex_errors
        
        # 2. Python 语法验证
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return False, [f"Python 语法错误: {e}"]
        
        return True, []
    
    def extract_error_info(self, stderr: str) -> dict:
        """从 stderr 中提取错误信息"""
        import re
        
        error_info = {
            "error_type": "Unknown",
            "error_message": "",
            "error_location": "",
            "full_traceback": stderr
        }
        
        # 提取错误类型（IndexError, AttributeError, TypeError 等）
        error_type_patterns = [
            r'(\w+Error):',
            r'(\w+Warning):',
            r'(\w+Exception):',
        ]
        
        for pattern in error_type_patterns:
            match = re.search(pattern, stderr)
            if match:
                error_info["error_type"] = match.group(1)
                break
        
        # 提取错误位置（文件名:行号）
        location_patterns = [
            r'File "([^"]+)", line (\d+)',
            r'([^:]+):(\d+):',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, stderr)
            if match:
                error_info["error_location"] = f"{match.group(1)}:{match.group(2)}"
                break
        
        # 提取错误消息（通常是最后一行或错误类型后的文本）
        error_message_patterns = [
            r'{}\s*:\s*(.+)'.format(error_info["error_type"]),
            r'Error:\s*(.+)',
            r'Exception:\s*(.+)',
        ]
        
        for pattern in error_message_patterns:
            match = re.search(pattern, stderr)
            if match:
                error_info["error_message"] = match.group(1).strip()
                break
        
        # 如果没有找到具体错误消息，使用最后一行
        if not error_info["error_message"]:
            lines = stderr.strip().split('\n')
            if lines:
                error_info["error_message"] = lines[-1]
        
        return error_info
    
    async def execute_scene(
        self, 
        code: str, 
        scene_name: str = "ProjectScene",
        output_filename: str = None
    ) -> str:
        """执行单个 Scene，生成视频（异步）"""
        # 1. 验证代码
        is_valid, errors = self.validate_code(code)
        if not is_valid:
            raise ValueError(f"代码验证失败: {errors}")
        
        # 2. 保存代码到临时文件（异步）
        # 如果有 task_id，使用任务专属目录；否则使用默认目录（向后兼容）
        if self.task_id:
            manim_code_dir = get_task_subdir(self.task_id, "manim_code", TEMP_BASE_DIR)
            temp_file = os.path.join(manim_code_dir, f"{scene_name.lower()}_temp.py")
        else:
            temp_file = os.path.join("./output/manim_code", f"{scene_name.lower()}_temp.py")
            ensure_dir(os.path.dirname(temp_file))
        
        # 使用异步文件写入
        await asyncio.to_thread(self._write_file, temp_file, code)
        
        logger.info(f"Manim 代码已保存到: {temp_file}")
        
        # 3. 确定输出文件名
        if output_filename is None:
            output_filename = scene_name
        
        # 4. 确定质量参数
        quality_map = {
            "low_quality": "-ql",
            "medium_quality": "-qm",
            "high_quality": "-qh"
        }
        quality_flag = quality_map.get(self.quality, "-qm")
        
        # 5. 执行 manim 命令（异步）
        cmd = [
            "manim",
            quality_flag,
            temp_file,
            scene_name
        ]
        
        logger.info(f"执行 Manim 命令: {' '.join(cmd)}")
        
        # 使用异步子进程执行
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            stderr_text = stderr.decode('utf-8') if stderr else ""
            error_info = self.extract_error_info(stderr_text)
            logger.error(f"Manim 执行失败: {error_info['error_type']} - {error_info['error_message']}")
            raise RuntimeError(f"Manim 执行失败: {stderr_text}")
        
        stdout_text = stdout.decode('utf-8') if stdout else ""
        
        # 6. 查找生成的视频文件
        # 从临时文件名提取基础名称（去掉 _temp.py 后缀）
        temp_basename = os.path.splitext(os.path.basename(temp_file))[0]  # projectscene_temp
        temp_dirname = temp_basename.replace("_temp", "")  # projectscene
        
        # Manim 质量目录映射
        quality_to_dir = {
            "low_quality": ["480p15", "low"],
            "medium_quality": ["720p30", "medium"],
            "high_quality": ["1080p60", "high"]
        }
        quality_dirs = quality_to_dir.get(self.quality, ["720p30", "medium"])
        quality_name = self.quality.replace("_quality", "")
        
        # 构建可能的路径列表（优先级从高到低）
        possible_dirs = []
        
        # 如果有 task_id，优先在任务专属目录中查找
        if self.task_id:
            task_manim_output_dir = get_task_subdir(self.task_id, "manim_output", TEMP_BASE_DIR)
            for q_dir in quality_dirs:
                possible_dirs.append(os.path.join(task_manim_output_dir, temp_basename, q_dir))
                possible_dirs.append(os.path.join(task_manim_output_dir, temp_dirname, q_dir))
            possible_dirs.append(os.path.join(task_manim_output_dir, temp_basename))
            possible_dirs.append(os.path.join(task_manim_output_dir, temp_dirname))
        
        # 1. 基于临时文件名的路径（最高优先级）
        for q_dir in quality_dirs:
            possible_dirs.append(os.path.join("media", "videos", temp_basename, q_dir))
            possible_dirs.append(os.path.join("media", "videos", temp_dirname, q_dir))
        
        # 2. 基于临时文件名但不带质量目录
        possible_dirs.append(os.path.join("media", "videos", temp_basename))
        possible_dirs.append(os.path.join("media", "videos", temp_dirname))
        
        # 3. 基于 scene_name 的路径（向后兼容）
        for q_dir in quality_dirs:
            possible_dirs.append(os.path.join("media", "videos", scene_name, q_dir))
        possible_dirs.append(os.path.join("media", "videos", scene_name, quality_name))
        possible_dirs.append(os.path.join("media", "videos", scene_name, self.quality))
        possible_dirs.append(os.path.join("media", "videos", scene_name))
        
        # 4. 基于 output_dir 的路径
        for q_dir in quality_dirs:
            possible_dirs.append(os.path.join(self.output_dir, temp_basename, q_dir))
            possible_dirs.append(os.path.join(self.output_dir, scene_name, q_dir))
        possible_dirs.append(os.path.join(self.output_dir, temp_basename))
        possible_dirs.append(os.path.join(self.output_dir, scene_name))
        possible_dirs.append(self.output_dir)
        
        # 搜索目录
        for media_dir in possible_dirs:
            if os.path.exists(media_dir):
                video_files = [f for f in os.listdir(media_dir) if f.endswith('.mp4')]
                if video_files:
                    # 选择最新的文件（如果多个）
                    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(media_dir, x)), reverse=True)
                    video_path = os.path.join(media_dir, video_files[0])
                    logger.info(f"视频已生成: {video_path}")
                    return video_path
        
        # 如果还是找不到，尝试直接查找文件名
        possible_paths = []
        for q_dir in quality_dirs:
            possible_paths.append(os.path.join("media", "videos", temp_basename, q_dir, f"{scene_name}.mp4"))
            possible_paths.append(os.path.join("media", "videos", temp_dirname, q_dir, f"{scene_name}.mp4"))
            possible_paths.append(os.path.join("media", "videos", scene_name, q_dir, f"{scene_name}.mp4"))
        possible_paths.extend([
            os.path.join("media", "videos", temp_basename, f"{scene_name}.mp4"),
            os.path.join("media", "videos", scene_name, quality_name, f"{scene_name}.mp4"),
            os.path.join("media", "videos", scene_name, f"{scene_name}.mp4"),
            os.path.join(self.output_dir, f"{scene_name}.mp4"),
        ])
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"视频已生成: {path}")
                return path
        
        # 从 stdout 中提取路径信息（改进的解析）
        import re
        
        # 尝试多种格式
        path_patterns = [
            r'File ready at[^\n]*\n([^\n]+)',
            r'Animation \d+ : Partial[^\n]*\n([^\n]+)',
            r'movie file written in[^\n]*\n([^\n]+)',
            r'([A-Za-z]:[^\n]*\.mp4)',  # Windows 绝对路径
            r'(media[^\n]*\.mp4)',  # 相对路径
        ]
        
        for pattern in path_patterns:
            matches = re.findall(pattern, stdout_text, re.MULTILINE)
            for match in matches:
                video_path = match.strip().strip("'\"")
                # 清理路径中的换行符（保留空格，因为路径可能包含空格）
                video_path = video_path.replace('\n', '').replace('\r', '')
                if video_path.endswith('.mp4') and os.path.exists(video_path):
                    logger.info(f"从输出中提取视频路径: {video_path}")
                    return video_path
        
        # 最后尝试递归搜索 media/videos 目录
        media_videos_dir = os.path.join("media", "videos")
        if os.path.exists(media_videos_dir):
            all_videos = []
            for root, dirs, files in os.walk(media_videos_dir):
                for file in files:
                    if file.endswith('.mp4') and scene_name in file:
                        full_path = os.path.join(root, file)
                        all_videos.append((os.path.getmtime(full_path), full_path))
            
            if all_videos:
                # 按修改时间排序，返回最新的
                all_videos.sort(reverse=True)
                video_path = all_videos[0][1]
                logger.info(f"通过递归搜索找到视频: {video_path}")
                return video_path
        
        raise FileNotFoundError(
            f"无法找到生成的视频文件。\n"
            f"尝试的目录: {possible_dirs[:10]}...\n"
            f"临时文件名: {temp_basename}\n"
            f"Scene 名称: {scene_name}\n"
            f"Manim 输出: {stdout_text[:1000]}"
        )
    
    def _write_file(self, file_path: str, content: str) -> None:
        """同步文件写入辅助方法（用于 asyncio.to_thread）"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
