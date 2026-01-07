"""代码版本兼容性验证器"""

import ast
import re
from typing import List, Tuple, Optional


class CodeValidator:
    """代码验证器"""
    
    def __init__(self):
        """初始化验证器"""
        # edge-tts>=7.2.7 的正确API
        self.edge_tts_valid_apis = [
            "edge_tts.Communicate",
            "edge_tts.list_voices",
            "edge_tts.Communicate.create",
        ]
        
        # edge-tts 已废弃的API
        self.edge_tts_deprecated = [
            "edge_tts.communicate",  # 小写，旧版本
        ]
        
        # manim>=0.19.1 的正确API
        self.manim_valid_imports = [
            "from manim import",
            "import manim",
        ]
        
        self.manim_valid_classes = [
            "Scene",
            "MathTex",
            "Text",
            "Animation",
            "Write",
            "Transform",
            "FadeIn",
            "FadeOut",
            "Create",
        ]
        
        # manim 已废弃的API
        self.manim_deprecated = [
            # 可以添加已废弃的API
        ]
    
    def validate(self, code: str) -> Tuple[bool, List[str]]:
        """
        验证代码
        
        Args:
            code: 要验证的代码
            
        Returns:
            (是否通过, 错误列表)
        """
        errors = []
        
        # 1. 语法检查
        syntax_ok, syntax_errors = self._check_syntax(code)
        if not syntax_ok:
            errors.extend(syntax_errors)
            return False, errors
        
        # 2. edge-tts API检查
        edge_tts_ok, edge_tts_errors = self._check_edge_tts(code)
        if not edge_tts_ok:
            errors.extend(edge_tts_errors)
        
        # 3. manim API检查
        manim_ok, manim_errors = self._check_manim(code)
        if not manim_ok:
            errors.extend(manim_errors)
        
        return len(errors) == 0, errors
    
    def _check_syntax(self, code: str) -> Tuple[bool, List[str]]:
        """
        检查语法
        
        Args:
            code: 代码
            
        Returns:
            (是否通过, 错误列表)
        """
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"语法错误：{e.msg} (行 {e.lineno})")
            return False, errors
        except Exception as e:
            errors.append(f"解析错误：{str(e)}")
            return False, errors
        
        return True, []
    
    def _check_edge_tts(self, code: str) -> Tuple[bool, List[str]]:
        """
        检查edge-tts API
        
        Args:
            code: 代码
            
        Returns:
            (是否通过, 错误列表)
        """
        errors = []
        
        # 检查是否使用了已废弃的API
        for deprecated in self.edge_tts_deprecated:
            if deprecated in code:
                errors.append(f"使用了已废弃的edge-tts API: {deprecated}")
        
        # 检查是否使用了edge_tts
        if "edge_tts" in code or "edge-tts" in code:
            # 检查是否使用了错误的API
            if "save_audio" in code:
                errors.append("edge-tts API使用错误：'save_audio()' 方法不存在，请使用 'save()' 方法（await communicate.save(filename)）")
            
            # 检查是否使用了正确的API
            has_valid_api = any(api in code for api in self.edge_tts_valid_apis)
            has_save_method = "await" in code and ".save(" in code
            
            if not has_valid_api and not has_save_method:
                # 检查是否有edge_tts的使用
                if re.search(r'edge_tts\.\w+', code):
                    errors.append("edge-tts API使用可能不正确，请使用 edge_tts.Communicate() 然后 await communicate.save(filename)")
        
        return len(errors) == 0, errors
    
    def _check_manim(self, code: str) -> Tuple[bool, List[str]]:
        """
        检查manim API
        
        Args:
            code: 代码
            
        Returns:
            (是否通过, 错误列表)
        """
        errors = []
        
        # 检查导入
        has_manim_import = any(imp in code for imp in self.manim_valid_imports)
        if not has_manim_import:
            errors.append("缺少manim导入语句，请使用 'from manim import *' 或 'import manim'")
        
        # 检查是否使用了已废弃的API
        for deprecated in self.manim_deprecated:
            if deprecated in code:
                errors.append(f"使用了已废弃的manim API: {deprecated}")
        
        # 检查基本类是否存在
        if has_manim_import:
            # 检查Scene类
            if "class" in code and "Scene" in code:
                if "Scene" not in code.split("class")[1].split("(")[0]:
                    # 检查是否继承自Scene
                    if not re.search(r'class\s+\w+\s*\([^)]*Scene', code):
                        errors.append("场景类必须继承自 manim.Scene")
            
            # 检查是否使用了外部图片文件
            if re.search(r'ImageMobject\s*\(["\']\w+\.(jpg|jpeg|png|gif)', code):
                errors.append("不要使用外部图片文件（如ImageMobject('pizza.jpg')），请使用Manim内置图形（Circle、Rectangle等）")
            
            # 检查是否使用了错误的音频播放API
            if "PlaySound" in code:
                errors.append("Manim 0.19.1中不存在PlaySound类，请使用self.add_sound(sound_file)方法播放音频")
            
            # 检查Sector的错误使用
            if re.search(r'Sector\s*\([^)]*outer_radius', code):
                errors.append("Sector类使用错误：应使用radius参数，不是outer_radius（如：Sector(radius=2, angle=1.0, start_angle=0.0)）")
        
        return len(errors) == 0, errors
    
    def get_validation_report(self, code: str) -> str:
        """
        获取验证报告
        
        Args:
            code: 代码
            
        Returns:
            验证报告
        """
        is_valid, errors = self.validate(code)
        
        if is_valid:
            return "✓ 代码验证通过，符合edge-tts>=7.2.7和manim>=0.19.1的要求"
        else:
            report = "✗ 代码验证失败，发现以下问题：\n"
            for i, error in enumerate(errors, 1):
                report += f"  {i}. {error}\n"
            return report

