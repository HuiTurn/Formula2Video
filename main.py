"""公式教学视频生成系统 - 主入口"""
import asyncio
import argparse
import json
from typing import List, Dict, Optional
from agents.orchestrator import VideoOrchestrator
from utils.logger import get_logger
from utils.file_utils import generate_task_id, load_json

logger = get_logger(__name__)


class FormulaVideoGenerator:
    """公式视频生成器"""
    
    def __init__(self):
        self.orchestrator = VideoOrchestrator()
    
    async def generate(
        self,
        formula: str,
        duration: int = 60,
        style: str = "3Blue1Brown",
        task_id: Optional[str] = None
    ) -> dict:
        """
        生成公式教学视频
        
        Args:
            formula: 数学公式或主题（如 "勾股定理" 或 "勾股定理的几何证明"）
            duration: 视频时长（秒），默认 60 秒
            style: 讲解风格，默认 "3Blue1Brown"
            task_id: 任务ID，如果为None则自动生成
        
        Returns:
            dict: 包含视频路径、剧本、总时长等信息
        """
        # 如果没有提供 task_id，自动生成
        if task_id is None:
            task_id = generate_task_id(formula)
        
        return await self.orchestrator.generate_video(formula, duration, style, task_id=task_id)


async def process_single_task(
    formula: str,
    duration: int,
    style: str,
    task_id: Optional[str] = None
) -> Dict:
    """处理单个任务"""
    if task_id is None:
        task_id = generate_task_id(formula)
    
    generator = FormulaVideoGenerator()
    try:
        result = await generator.generate(
            formula=formula,
            duration=duration,
            style=style,
            task_id=task_id
        )
        return {"success": True, "formula": formula, "task_id": task_id, "result": result}
    except Exception as e:
        logger.error(f"生成失败 [{formula}]: {e}", exc_info=True)
        return {"success": False, "formula": formula, "task_id": task_id, "error": str(e)}


async def process_batch_tasks(
    tasks: List[Dict],
    max_concurrent: int = 3
) -> List[Dict]:
    """批量处理任务，支持并发，确保错误隔离"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(task: Dict):
        """带信号量控制的包装函数，增强错误隔离"""
        try:
            async with semaphore:
                return await process_single_task(
                    formula=task.get("formula", ""),
                    duration=task.get("duration", 60),
                    style=task.get("style", "3Blue1Brown"),
                    task_id=task.get("task_id")
                )
        except Exception as e:
            # 额外的保护层，防止未预期的异常
            formula = task.get("formula", "未知")
            task_id = task.get("task_id", "未知")
            logger.error(f"任务处理异常 [{formula}]: {e}", exc_info=True)
            return {
                "success": False,
                "formula": formula,
                "task_id": task_id,
                "error": f"未预期的异常: {str(e)}"
            }
    
    # 使用 return_exceptions=True 确保所有任务都能完成
    results = await asyncio.gather(
        *[process_with_semaphore(task) for task in tasks],
        return_exceptions=True
    )
    
    # 处理可能的异常结果
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # 如果返回的是异常对象，转换为标准错误格式
            task = tasks[i]
            processed_results.append({
                "success": False,
                "formula": task.get("formula", "未知"),
                "task_id": task.get("task_id", "未知"),
                "error": f"未捕获的异常: {str(result)}"
            })
        else:
            processed_results.append(result)
    
    return processed_results


async def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="公式教学视频生成系统")
    
    # 单个公式（向后兼容）
    parser.add_argument(
        "formula",
        type=str,
        nargs="?",
        help="数学公式或主题（如：勾股定理）。如果使用 --batch 或 --json，则忽略此参数"
    )
    
    # 批量处理选项
    parser.add_argument(
        "--batch",
        type=str,
        nargs="+",
        metavar="FORMULA",
        help="批量处理模式，传入多个公式（用空格分隔）"
    )
    parser.add_argument(
        "--json",
        type=str,
        metavar="FILE",
        help="从JSON文件读取批量任务。JSON格式: [{\"formula\": \"...\", \"duration\": 60, \"style\": \"...\"}, ...]"
    )
    
    # 通用参数
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=60,
        help="视频时长（秒），默认 60。批量模式下作为默认值"
    )
    parser.add_argument(
        "-s", "--style",
        type=str,
        default="3Blue1Brown",
        help="讲解风格，默认 3Blue1Brown。批量模式下作为默认值"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=3,
        help="批量处理时的最大并发数，默认 3"
    )
    
    args = parser.parse_args()
    
    # 确定处理模式
    if args.json:
        # JSON文件模式
        try:
            tasks_data = load_json(args.json)
            if not isinstance(tasks_data, list):
                print(f"错误: JSON文件必须包含一个任务数组")
                return 1
            
            tasks = []
            for i, task in enumerate(tasks_data):
                if not isinstance(task, dict) or "formula" not in task:
                    print(f"警告: 跳过无效任务 #{i+1}")
                    continue
                tasks.append({
                    "formula": task["formula"],
                    "duration": task.get("duration", args.duration),
                    "style": task.get("style", args.style),
                    "task_id": task.get("task_id")
                })
            
            if not tasks:
                print("错误: 没有有效的任务")
                return 1
            
            print(f"\n开始批量处理 {len(tasks)} 个任务（最大并发数: {args.max_concurrent}）...")
            results = await process_batch_tasks(tasks, args.max_concurrent)
            
        except FileNotFoundError:
            print(f"错误: JSON文件不存在: {args.json}")
            return 1
        except json.JSONDecodeError as e:
            print(f"错误: JSON文件格式错误: {e}")
            return 1
        except Exception as e:
            logger.error(f"批量处理失败: {e}", exc_info=True)
            print(f"错误: {e}")
            return 1
    
    elif args.batch:
        # 批量模式（命令行列表）
        tasks = [
            {
                "formula": formula,
                "duration": args.duration,
                "style": args.style
            }
            for formula in args.batch
        ]
        
        print(f"\n开始批量处理 {len(tasks)} 个任务（最大并发数: {args.max_concurrent}）...")
        results = await process_batch_tasks(tasks, args.max_concurrent)
    
    else:
        # 单个任务模式（向后兼容）
        if not args.formula:
            parser.error("必须提供公式（formula）或使用 --batch/--json 进行批量处理")
        
        try:
            result = await process_single_task(
                formula=args.formula,
                duration=args.duration,
                style=args.style
            )
            results = [result]
        except Exception as e:
            logger.error(f"生成失败: {e}", exc_info=True)
            print(f"\n错误: {e}")
            return 1
    
    # 输出结果
    print("\n" + "="*50)
    if len(results) == 1:
        # 单个任务
        result = results[0]
        if result["success"]:
            print("视频生成成功！")
            print("="*50)
            print(f"视频路径: {result['result']['video_path']}")
            print(f"总时长: {result['result']['total_duration']:.2f} 秒")
            print(f"剧本路径: {result['result'].get('script_path', 'N/A')}")
            print(f"代码路径: {result['result'].get('code_path', 'N/A')}")
            print(f"任务ID: {result['task_id']}")
            print("="*50)
        else:
            print("视频生成失败！")
            print("="*50)
            print(f"公式: {result['formula']}")
            print(f"错误: {result['error']}")
            print("="*50)
            return 1
    else:
        # 批量任务
        success_count = sum(1 for r in results if r["success"])
        failed_count = len(results) - success_count
        
        print(f"批量处理完成: 成功 {success_count}/{len(results)}, 失败 {failed_count}/{len(results)}")
        print("="*50)
        
        if success_count > 0:
            print("\n成功任务:")
            for result in results:
                if result["success"]:
                    print(f"  ✓ {result['formula']} (任务ID: {result['task_id']})")
                    print(f"    视频: {result['result']['video_path']}")
        
        if failed_count > 0:
            print("\n失败任务:")
            for result in results:
                if not result["success"]:
                    print(f"  ✗ {result['formula']} (任务ID: {result['task_id']})")
                    print(f"    错误: {result['error']}")
        
        print("="*50)
        
        return 1 if failed_count > 0 else 0
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
