"""公式教学视频生成系统 - 主入口"""
import asyncio
import argparse
from agents.orchestrator import VideoOrchestrator
from utils.logger import get_logger

logger = get_logger(__name__)


class FormulaVideoGenerator:
    """公式视频生成器"""
    
    def __init__(self):
        self.orchestrator = VideoOrchestrator()
    
    async def generate(
        self,
        formula: str,
        duration: int = 60,
        style: str = "3Blue1Brown"
    ) -> dict:
        """
        生成公式教学视频
        
        Args:
            formula: 数学公式或主题（如 "勾股定理" 或 "勾股定理的几何证明"）
            duration: 视频时长（秒），默认 60 秒
            style: 讲解风格，默认 "3Blue1Brown"
        
        Returns:
            dict: 包含视频路径、剧本、总时长等信息
        """
        return await self.orchestrator.generate_video(formula, duration, style)


async def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="公式教学视频生成系统")
    parser.add_argument(
        "formula",
        type=str,
        help="数学公式或主题（如：勾股定理）"
    )
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=60,
        help="视频时长（秒），默认 60"
    )
    parser.add_argument(
        "-s", "--style",
        type=str,
        default="3Blue1Brown",
        help="讲解风格，默认 3Blue1Brown"
    )
    
    args = parser.parse_args()
    
    generator = FormulaVideoGenerator()
    
    try:
        result = await generator.generate(
            formula=args.formula,
            duration=args.duration,
            style=args.style
        )
        
        print("\n" + "="*50)
        print("视频生成成功！")
        print("="*50)
        print(f"视频路径: {result['video_path']}")
        print(f"总时长: {result['total_duration']:.2f} 秒")
        print(f"剧本路径: {result.get('script_path', 'N/A')}")
        print(f"代码路径: {result.get('code_path', 'N/A')}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"生成失败: {e}", exc_info=True)
        print(f"\n错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
