"""文件操作工具"""
import json
import os
import re
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional


def ensure_dir(dir_path: str) -> None:
    """确保目录存在"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除或替换所有 Windows 不允许的字符"""
    # Windows 不允许的字符：< > : " / \ | ? *
    invalid_chars = r'[<>:"/\\|?*]'
    # 替换所有非法字符为下划线
    sanitized = re.sub(invalid_chars, '_', filename)
    # 移除首尾空格和下划线
    sanitized = sanitized.strip(' _')
    # 处理连续的下划线，替换为单个下划线
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """保存 JSON 文件"""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str) -> Dict[str, Any]:
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_file_content(file_path: str) -> str:
    """加载文件内容（支持相对路径）"""
    # 如果是相对路径，从项目根目录开始
    if not os.path.isabs(file_path):
        # 获取项目根目录（假设 utils 在项目根目录下）
        project_root = Path(__file__).parent.parent
        file_path = project_root / file_path
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def cleanup_segment_files(directory: str, pattern: str = "segment_*") -> int:
    """
    清理指定目录下的片段文件
    
    Args:
        directory: 要清理的目录路径
        pattern: 文件匹配模式，默认为 "segment_*"
    
    Returns:
        删除的文件数量
    """
    import glob
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    
    if not os.path.exists(directory):
        logger.debug(f"目录不存在，跳过清理: {directory}")
        return 0
    
    # 构建完整的匹配模式
    pattern_path = os.path.join(directory, pattern)
    
    # 查找匹配的文件
    files_to_delete = glob.glob(pattern_path)
    
    deleted_count = 0
    for file_path in files_to_delete:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1
                logger.debug(f"已删除旧文件: {file_path}")
        except Exception as e:
            logger.warning(f"删除文件失败 {file_path}: {e}")
    
    if deleted_count > 0:
        logger.info(f"清理目录 {directory}，删除 {deleted_count} 个片段文件")
    
    return deleted_count


def cleanup_directory(directory: str, force: bool = False) -> bool:
    """
    清理指定目录（删除目录及其所有内容）
    
    Args:
        directory: 要清理的目录路径
        force: 如果为 True，即使目录不存在也不报错
    
    Returns:
        是否成功删除（如果目录不存在且 force=True，返回 True）
    """
    import shutil
    from utils.logger import get_logger
    
    logger = get_logger(__name__)
    
    if not os.path.exists(directory):
        if force:
            logger.debug(f"目录不存在，跳过清理: {directory}")
            return True
        logger.warning(f"目录不存在: {directory}")
        return False
    
    try:
        shutil.rmtree(directory)
        logger.info(f"已删除目录: {directory}")
        return True
    except Exception as e:
        logger.warning(f"删除目录失败 {directory}: {e}")
        return False


def generate_task_id(formula: str) -> str:
    """
    基于公式名称生成任务ID（16位MD5哈希值）
    
    相同公式会生成相同的任务ID，便于复用已生成的文件
    
    Args:
        formula: 数学公式或主题名称
    
    Returns:
        16位十六进制字符串作为任务ID
    """
    hash_obj = hashlib.md5(formula.encode('utf-8'))
    return hash_obj.hexdigest()[:16]


def get_task_temp_dir(task_id: str, base_temp_dir: Optional[str] = None) -> str:
    """
    获取任务的临时目录路径
    
    Args:
        task_id: 任务ID
        base_temp_dir: 临时目录基础路径，如果为None则使用默认值
    
    Returns:
        任务临时目录路径
    """
    if base_temp_dir is None:
        base_temp_dir = "./temp"
    return os.path.join(base_temp_dir, task_id)


def get_task_subdir(task_id: str, subdir: str, base_temp_dir: Optional[str] = None) -> str:
    """
    获取任务临时目录下的子目录路径
    
    Args:
        task_id: 任务ID
        subdir: 子目录名称（如 'manim_code', 'audio_segments' 等）
        base_temp_dir: 临时目录基础路径，如果为None则使用默认值
    
    Returns:
        子目录完整路径
    """
    task_dir = get_task_temp_dir(task_id, base_temp_dir)
    subdir_path = os.path.join(task_dir, subdir)
    ensure_dir(subdir_path)
    return subdir_path