"""日志工具"""
import logging
import sys


def setup_logger(name: str = "formula2video", level: int = logging.INFO) -> logging.Logger:
    """配置日志系统"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """获取日志器"""
    if name is None:
        name = "formula2video"
    return setup_logger(name)