# 使用说明

## 快速开始

### 1. 安装依赖

```bash
pip install -e .
```

或手动安装：

```bash
pip install edge-tts>=7.2.7 manim>=0.19.1 python-dotenv>=1.0.0 openai>=1.0.0 pyyaml>=6.0.0
```

### 2. 配置API密钥

创建 `.env` 文件（在项目根目录）：

```bash
MODELSCOPE_API_KEY=your-api-key-here
MODELSCOPE_BASE_URL=https://api-inference.modelscope.cn/v1
MODELSCOPE_MODEL=Qwen/QwQ-32B
```

**注意**：所有三个配置项都是必填的。

### 3. 使用工具

#### 基本用法

```bash
# 输入LaTeX公式
python main.py "E=mc^2"

# 输入中文描述（自动转换为LaTeX）
python main.py "圆的面积公式"
```

#### 指定学科和年级

```bash
# 使用英文年级
python main.py "F=ma" --subject physics --grade grade9

# 使用中文年级
python main.py "F=ma" --subject physics --grade "高中"

# 支持小学到大学
python main.py "1+1=2" --subject math --grade "小学"
python main.py "勾股定理" --subject math --grade "初中"
python main.py "导数" --subject math --grade "大学"
```

#### 指定输出目录

```bash
python main.py "a^2+b^2=c^2" --output ./my_videos
```

#### 强制重新生成

```bash
python main.py "E=mc^2" --force
```

## 输出目录结构

所有生成的文件统一输出到 `output/` 目录（或通过 `--output` 指定的根目录）：

```
output/
├── 大学/
│   ├── 物理/
│   │   ├── 质能方程/        # 公式的独立目录（中文名）
│   │   │   ├── audio/      # 该公式的所有音频文件
│   │   │   └── videos/     # 该公式的所有视频文件
│   │   └── 牛顿第二定律/    # 另一个公式的独立目录
│   │       ├── audio/
│   │       └── videos/
│   └── 数学/
│       ├── 勾股定理/
│       └── 圆的面积公式/
├── 高中/
│   ├── 物理/
│   └── 数学/
└── ...（其他年级和学科）
```

**规则说明**：
- 所有目录名都使用中文：年级、学科、公式名都是中文
- 每个公式都有独立的目录，避免多个公式的文件混在一起
- 如果用户输入LaTeX公式，会自动转换为中文描述用于目录命名

## 生成视频

生成代码后，使用manim命令生成视频：

```bash
# 查看生成的场景文件
ls scenes/

# 运行manim生成视频
manim -pql scenes/公式场景.py 场景类名
```

## 功能特性

- ✅ **支持LaTeX和中文输入**：可以直接输入公式LaTeX或中文描述
- ✅ **自动转换**：LaTeX和中文描述可以双向转换
- ✅ **年级适配**：支持小学到大学不同年级，自动调整教学风格
- ✅ **通俗易懂**：生成的教学视频适合基础差或0基础的学生
- ✅ **文字图像重叠**：文字叠加在公式/图形上显示
- ✅ **版本兼容**：自动验证代码是否符合edge-tts>=7.2.7和manim>=0.19.1的要求
- ✅ **目录管理**：自动组织输出文件，所有目录使用中文

## 注意事项

1. **API密钥**：需要配置ModelScope API密钥才能使用
2. **网络连接**：AI代码生成和音频生成需要网络连接
3. **视频生成**：生成的代码需要手动运行manim命令生成视频
4. **磁盘空间**：确保有足够的磁盘空间存储音频和视频文件

## 故障排除

### 问题：找不到API密钥

**解决方案**：创建 `.env` 文件并配置 `MODELSCOPE_API_KEY`、`MODELSCOPE_BASE_URL`、`MODELSCOPE_MODEL`

### 问题：代码生成失败

**解决方案**：
- 检查网络连接
- 确认API密钥正确
- 检查提示词文件是否存在（`prompts/system_prompt.txt` 和 `prompts/user_prompt.txt`）

### 问题：代码验证失败

**解决方案**：
- 查看错误信息，了解具体的不兼容问题
- 检查生成的代码是否符合edge-tts>=7.2.7和manim>=0.19.1的要求

