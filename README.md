# 公式教学视频生成系统

基于 LangChain 的多 Agent 系统，实现自动化生成数学公式教学视频。

## 功能特点

- 🎬 **三步走流程**：剧本生成 → TTS 文案转换 → Manim 代码生成
- 🎯 **音频先行策略**：先生成音频获取精确时长，确保音画完美同步
- 🎨 **单 Scene 架构**：避免状态丢失和闪烁，提升渲染性能
- ✅ **LaTeX 验证**：预校验公式语法，独立定义便于修正
- 🎞️ **平滑过渡**：冻结帧填充，解决视频跳变问题
- 📦 **批量处理**：支持并发批量生成多个视频，提高效率
- 🛡️ **错误隔离**：单个任务失败不影响其他任务，确保批量处理稳定性
- 🔧 **智能 JSON 提取**：支持从 Markdown 代码块中提取 JSON，提升 LLM 响应解析成功率

## 安装

1. 安装依赖：
```bash
uv sync
# 或
pip install -e .
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 OpenAI API Key
```

## 使用方法

### 命令行使用

#### 单个任务

```bash
# 简单输入
uv run main.py "勾股定理"

# 详细参数
uv run main.py "勾股定理的几何证明" -d 60 -s "3Blue1Brown"
```

#### 批量处理

```bash
# 批量处理多个公式（使用命令行参数）
uv run main.py --batch "勾股定理" "圆的面积" "一元一次方程" --max-concurrent 3

# 从 JSON 文件批量处理
# 创建 tasks.json 文件：
# [
#   {"formula": "勾股定理", "duration": 60, "style": "3Blue1Brown"},
#   {"formula": "圆的面积", "duration": 60, "style": "3Blue1Brown"},
#   {"formula": "一元一次方程", "duration": 60, "style": "3Blue1Brown"}
# ]
uv run main.py --json tasks.json --max-concurrent 3

# 批量处理参数说明
# --batch: 批量模式，传入多个公式（用空格分隔）
# --json: 从 JSON 文件读取批量任务
# --max-concurrent: 最大并发数，默认 3
# -d, --duration: 视频时长（秒），批量模式下作为默认值
# -s, --style: 讲解风格，批量模式下作为默认值
```

### Python API 使用

```python
import asyncio
from main import FormulaVideoGenerator

async def main():
    generator = FormulaVideoGenerator()
    result = await generator.generate(
        formula="勾股定理的几何证明",
        duration=60,
        style="3Blue1Brown"
    )
    print(f"视频已生成: {result['video_path']}")

asyncio.run(main())
```

## 工作流程

### 单个视频生成流程

1. **剧本生成**：根据输入的数学公式/主题，生成结构化的视听剧本
2. **TTS 文案转换**：将剧本中的数学符号转换为中文口语
3. **音频生成**：使用 edge-tts 生成音频，获取精确时长（音频先行策略）
4. **Manim 代码生成**：根据剧本和音频时长生成 Manim 代码
5. **视频渲染**：执行 Manim 代码生成视频（支持自动修复）
6. **视频切割**：根据时间标记切割视频片段
7. **音画合并**：合并视频和音频，生成最终视频

### 批量处理流程

- **并发控制**：使用信号量控制最大并发数，避免资源耗尽
- **错误隔离**：每个任务独立运行，单个任务失败不影响其他任务
- **结果汇总**：批量处理完成后自动汇总成功和失败的任务
- **任务隔离**：每个任务使用独立的 `task_id` 和临时目录，避免文件冲突

## 输出目录

- `output/scripts/` - 生成的剧本 JSON
- `output/tts_texts/` - TTS 文案文本
- `output/manim_code/` - 生成的 Manim 代码
- `output/video_segments/` - 切割的视频片段
- `output/videos/` - 最终视频文件
- `audio/segments/` - 音频片段
- `media/videos/` - Manim 生成的视频

## 配置说明

在 `.env` 文件中可以配置：

- `OPENAI_API_KEY` - OpenAI API 密钥（必需）
- `OPENAI_MODEL` - 使用的模型，默认 `gpt-4`
- `MANIM_QUALITY` - Manim 渲染质量：`low_quality`, `medium_quality`, `high_quality`
- `TTS_VOICE` - TTS 语音，默认 `zh-CN-XiaoxiaoNeural`

## 技术架构

- **LangChain** - Agent 框架
- **OpenAI GPT-4** - 文本生成
- **Manim Community** - 数学动画
- **edge-tts** - 语音合成
- **moviepy** - 视频处理

## 注意事项

1. 确保已安装 Manim 并配置正确
2. 需要有效的 OpenAI API Key
3. 首次运行可能需要较长时间（Manim 渲染）
4. 建议使用 `medium_quality` 或 `low_quality` 进行测试
5. 批量处理时，建议根据系统资源调整 `--max-concurrent` 参数
6. 单个任务失败不会中断批量处理，所有任务完成后会显示详细结果
7. 每个任务都有独立的临时目录，避免文件冲突

## 错误处理

### 自动修复机制

- **Manim 代码修复**：如果生成的 Manim 代码执行失败，系统会自动尝试修复（最多 3 次）
- **JSON 提取增强**：支持从 Markdown 代码块中提取 JSON，提高 LLM 响应解析成功率
- **错误隔离**：批量处理时，单个任务的错误不会影响其他任务

### 常见问题

1. **Manim 执行失败**：系统会自动尝试修复，如果修复失败会在日志中显示详细错误信息
2. **JSON 解析失败**：系统会尝试多种方法提取 JSON，包括处理 Markdown 代码块格式
3. **批量处理部分失败**：所有任务完成后会显示成功和失败的统计信息

## 许可证

MIT License
