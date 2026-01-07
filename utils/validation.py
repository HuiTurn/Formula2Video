"""数据验证工具（含 LaTeX 验证）"""
import re
import ast
from typing import List, Tuple


class LaTeXValidator:
    """LaTeX 语法验证器"""
    
    @staticmethod
    def validate_formula(formula: str) -> Tuple[bool, str]:
        """
        验证 LaTeX 公式语法
        返回 (是否有效, 错误信息)
        """
        # 检查花括号匹配
        open_braces = formula.count('{')
        close_braces = formula.count('}')
        if open_braces != close_braces:
            return False, f"花括号不匹配: 开括号 {open_braces}, 闭括号 {close_braces}"
        
        # 检查常见命令
        commands = ['\\sqrt', '\\frac', '\\sum', '\\int', '\\lim']
        for cmd in commands:
            if cmd in formula:
                # 检查命令后是否有参数
                pattern = rf'{re.escape(cmd)}\s*[^{{]*$'
                if re.search(pattern, formula):
                    return False, f"命令 {cmd} 缺少参数"
        
        return True, ""
    
    @staticmethod
    def extract_formulas_from_code(code: str) -> List[Tuple[str, str]]:
        """
        从代码中提取公式字典
        返回 [(key, formula), ...]
        使用 ast 模块正确解析 Python 字典
        """
        try:
            # 解析整个代码文件
            tree = ast.parse(code)
            
            # 查找 FORMULAS 变量的赋值
            formulas = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'FORMULAS':
                            if isinstance(node.value, ast.Dict):
                                # 解析字典
                                keys = node.value.keys
                                values = node.value.values
                                
                                for key_node, value_node in zip(keys, values):
                                    if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                                        key = key_node.value
                                        
                                        # 提取值（处理字符串常量）
                                        if isinstance(value_node, ast.Constant):
                                            formula = value_node.value
                                            if isinstance(formula, str):
                                                formulas.append((key, formula))
                                        
            return formulas
        except (SyntaxError, ValueError) as e:
            # 如果解析失败，返回空列表
            return []
    
    @staticmethod
    def validate_code_formulas(code: str) -> Tuple[bool, List[str]]:
        """
        验证代码中的所有公式
        返回 (是否全部有效, 错误列表)
        """
        formulas = LaTeXValidator.extract_formulas_from_code(code)
        errors = []
        
        for key, formula in formulas:
            is_valid, error_msg = LaTeXValidator.validate_formula(formula)
            if not is_valid:
                errors.append(f"公式 {key}: {error_msg}")
        
        return len(errors) == 0, errors
