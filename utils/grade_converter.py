"""年级转换工具"""

# 年级映射：中文 -> 标准格式
GRADE_MAPPING = {
    # 中文年级
    "小学": "elementary",
    "初中": "middle",
    "高中": "high",
    "大学": "university",
    # 英文标准格式
    "grade1": "elementary",
    "grade2": "elementary",
    "grade3": "elementary",
    "grade4": "elementary",
    "grade5": "elementary",
    "grade6": "elementary",
    "grade7": "middle",
    "grade8": "middle",
    "grade9": "middle",
    "grade10": "high",
    "grade11": "high",
    "grade12": "high",
    "university": "university",
}

# 年级级别描述映射
GRADE_LEVEL_MAPPING = {
    "elementary": "小学",
    "middle": "初中",
    "high": "高中",
    "university": "大学",
}


def convert_grade_to_standard(grade: str) -> str:
    """
    将年级转换为标准格式
    
    Args:
        grade: 年级（中文或英文格式）
        
    Returns:
        标准格式的年级（elementary/middle/high/university）
    """
    grade_lower = grade.lower().strip()
    
    # 检查是否在映射中
    if grade_lower in GRADE_MAPPING:
        return GRADE_MAPPING[grade_lower]
    
    # 检查是否是gradeX格式
    if grade_lower.startswith("grade"):
        # 提取数字
        try:
            grade_num = int(grade_lower.replace("grade", ""))
            if 1 <= grade_num <= 6:
                return "elementary"
            elif 7 <= grade_num <= 9:
                return "middle"
            elif 10 <= grade_num <= 12:
                return "high"
        except ValueError:
            pass
    
    # 默认返回middle（初中）
    return "middle"


def get_grade_level(grade: str) -> str:
    """
    获取年级级别描述（中文）
    
    Args:
        grade: 年级（中文或英文格式）
        
    Returns:
        年级级别描述（小学/初中/高中/大学）
    """
    standard_grade = convert_grade_to_standard(grade)
    return GRADE_LEVEL_MAPPING.get(standard_grade, "初中")


def convert_subject_to_chinese(subject: str) -> str:
    """
    将学科转换为中文
    
    Args:
        subject: 学科（math/physics/chemistry）
        
    Returns:
        中文学科名称
    """
    subject_mapping = {
        "math": "数学",
        "physics": "物理",
        "chemistry": "化学",
    }
    return subject_mapping.get(subject.lower(), "数学")

