"""主程序入口"""

import argparse
import re
import sys
from pathlib import Path

from config.prompt_template import PromptTemplate
from utils.formula_parser import FormulaParser
from utils.ai_code_generator import AICodeGenerator
from utils.code_validator import CodeValidator
from utils.path_manager import PathManager
from utils.grade_converter import convert_grade_to_standard, convert_subject_to_chinese


def generate_scene_class_name(formula_latex: str, formula_name: str) -> str:
    """
    从公式生成场景类名（PascalCase格式）
    
    Args:
        formula_latex: 公式LaTeX
        formula_name: 公式中文名
        
    Returns:
        场景类名
    """
    # 尝试从LaTeX生成类名（优先）
    latex_cleaned = re.sub(r'[^a-zA-Z0-9]', '', formula_latex)
    
    if latex_cleaned and len(latex_cleaned) >= 2:
        # 使用LaTeX生成类名
        # 转换为PascalCase
        class_name = latex_cleaned[0].upper() + latex_cleaned[1:] if latex_cleaned else "Formula"
    else:
        # 从中文名生成（使用拼音映射或简化处理）
        # 移除特殊字符
        name_cleaned = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', formula_name)
        
        # 常见公式名称映射
        formula_name_map = {
            "勾股定理": "PythagoreanTheorem",
            "圆的面积": "CircleArea",
            "圆的面积公式": "CircleArea",
            "质能方程": "MassEnergy",
            "牛顿第二定律": "NewtonSecondLaw",
            "万有引力": "Gravitation",
            "导数": "Derivative",
            "积分": "Integral",
        }
        
        if name_cleaned in formula_name_map:
            class_name = formula_name_map[name_cleaned]
        else:
            # 使用通用名称
            class_name = "FormulaScene"
    
    # 确保以字母开头
    if not re.match(r'^[a-zA-Z]', class_name):
        class_name = "Formula" + class_name
    
    # 确保是有效的Python标识符
    class_name = re.sub(r'[^a-zA-Z0-9_]', '', class_name)
    if not class_name or not class_name[0].isalpha():
        class_name = "FormulaScene"
    
    return class_name


def register_scene_class(scene_file_path: Path, class_name: str):
    """
    注册场景类到scenes/__init__.py
    
    Args:
        scene_file_path: 场景文件路径
        class_name: 类名
    """
    scenes_init = Path("scenes/__init__.py")
    
    # 读取现有内容
    if scenes_init.exists():
        content = scenes_init.read_text(encoding="utf-8")
    else:
        content = '"""场景模块 - AI生成的场景类会自动注册到这里"""\n\n__all__ = []\n'
    
    # 生成导入语句
    module_name = scene_file_path.stem
    import_line = f"from scenes.{module_name} import {class_name}"
    
    # 检查是否已存在
    if import_line not in content and f'"{class_name}"' not in content:
        # 添加到__all__
        if "__all__" in content:
            # 更新__all__
            if f'"{class_name}"' not in content:
                content = re.sub(
                    r'(__all__\s*=\s*\[)(.*?)(\])',
                    lambda m: f'{m.group(1)}{m.group(2)}, "{class_name}"{m.group(3)}' if m.group(2).strip() else f'{m.group(1)}"{class_name}"{m.group(3)}',
                    content,
                )
        else:
            content += f'\n__all__ = ["{class_name}"]\n'
        
        # 添加导入
        if f"from scenes.{module_name}" not in content:
            # 在文件末尾添加导入
            content = content.rstrip() + "\n\n" + import_line + "\n"
        
        scenes_init.write_text(content, encoding="utf-8")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="公式教学视频生成工具 - 输入公式自动生成Manim教学视频代码"
    )
    
    parser.add_argument(
        "formula",
        type=str,
        help="公式输入（支持LaTeX或中文描述，如：'E=mc^2' 或 '圆的面积公式'）"
    )
    
    parser.add_argument(
        "--subject",
        type=str,
        default="math",
        choices=["math", "physics", "chemistry"],
        help="学科（math/physics/chemistry，默认：math）"
    )
    
    parser.add_argument(
        "--grade",
        type=str,
        default="grade9",
        help="年级（支持中文或英文，如：'小学'/'初中'/'高中'/'大学' 或 grade1-grade12/university，默认：grade9）"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="输出目录根路径（默认：output/）"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新生成（即使文件已存在）"
    )
    
    args = parser.parse_args()
    
    try:
        print(f"正在解析公式：{args.formula}")
        
        # 1. 解析公式
        formula_parser = FormulaParser()
        formula_info = formula_parser.parse(args.formula)
        
        formula_latex = formula_info["latex"]
        formula_name = formula_info["chinese_name"]
        formula_description = formula_info["description"]
        
        print(f"✓ 公式解析完成")
        print(f"  - LaTeX: {formula_latex}")
        print(f"  - 中文名: {formula_name}")
        print(f"  - 描述: {formula_description}")
        
        # 2. 生成场景类名
        scene_class_name = generate_scene_class_name(formula_latex, formula_name)
        print(f"  - 场景类名: {scene_class_name}")
        
        # 3. 设置路径管理器
        path_manager = PathManager(base_output_dir=args.output)
        
        # 4. 准备提示词
        print("\n正在准备提示词...")
        prompt_template = PromptTemplate()
        prompts = prompt_template.get_full_prompt(
            formula_latex=formula_latex,
            formula_name=formula_name,
            formula_description=formula_description,
            subject=args.subject,
            grade=args.grade,
            scene_class_name=scene_class_name,
        )
        print("✓ 提示词准备完成")
        
        # 5. 生成代码
        print("\n正在生成代码...")
        code_generator = AICodeGenerator()
        generated_code = code_generator.generate_code(
            system_prompt=prompts["system"],
            user_prompt=prompts["user"],
        )
        generated_code = code_generator.clean_code(generated_code)
        print("✓ 代码生成完成")
        
        # 6. 验证代码
        print("\n正在验证代码...")
        validator = CodeValidator()
        is_valid, errors = validator.validate(generated_code)
        
        if not is_valid:
            print("✗ 代码验证失败：")
            for error in errors:
                print(f"  - {error}")
            print("\n生成的代码：")
            print("=" * 80)
            print(generated_code)
            print("=" * 80)
            sys.exit(1)
        
        print("✓ 代码验证通过")
        
        # 7. 保存代码文件
        scene_file_name = f"{scene_class_name.lower()}.py"
        scenes_dir = Path("scenes")
        scenes_dir.mkdir(exist_ok=True)
        scene_file_path = scenes_dir / Path(scene_file_name)
        
        if scene_file_path.exists() and not args.force:
            print(f"\n⚠ 文件已存在：{scene_file_path}")
            print("使用 --force 参数强制重新生成")
            sys.exit(1)
        
        scene_file_path.write_text(generated_code, encoding="utf-8")
        print(f"✓ 代码已保存到：{scene_file_path}")
        
        # 8. 注册场景类（可选，如果代码中已经定义了类）
        try:
            register_scene_class(scene_file_path, scene_class_name)
            print(f"✓ 场景类已注册：{scene_class_name}")
        except Exception as e:
            print(f"⚠ 场景类注册失败（可忽略）：{str(e)}")
        
        # 9. 输出路径信息
        formula_dir = path_manager.get_formula_dir(
            formula_chinese_name=formula_name,
            grade=args.grade,
            subject=args.subject,
        )
        audio_dir = path_manager.get_audio_dir(
            formula_chinese_name=formula_name,
            grade=args.grade,
            subject=args.subject,
        )
        video_dir = path_manager.get_video_dir(
            formula_chinese_name=formula_name,
            grade=args.grade,
            subject=args.subject,
        )
        
        print("\n" + "=" * 80)
        print("生成完成！")
        print("=" * 80)
        print(f"公式目录：{formula_dir}")
        print(f"音频目录：{audio_dir}")
        print(f"视频目录：{video_dir}")
        print(f"场景文件：{scene_file_path}")
        print(f"场景类名：{scene_class_name}")
        print("\n下一步：")
        print(f"  运行 manim 命令生成视频：")
        print(f"    uv run manim -pql {scene_file_path} {scene_class_name}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ 错误：{str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

