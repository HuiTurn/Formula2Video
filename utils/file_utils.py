"""文件操作工具"""
import json
import os
from pathlib import Path
from typing import Any, Dict


def ensure_dir(dir_path: str) -> None:
    """确保目录存在"""
    Path(dir_path).mkdir(parents=True, exist_ok=True)


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