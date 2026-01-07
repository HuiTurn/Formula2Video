# 公式教学视频生成系统

基于 LangChain 的多 Agent 系统，实现自动化生成数学公式教学视频。

## 功能特点

- 🎬 **三步走流程**：剧本生成 → TTS 文案转换 → Manim 代码生成
- 🎯 **音频先行策略**：先生成音频获取精确时长，确保音画完美同步
- 🎨 **单 Scene 架构**：避免状态丢失和闪烁，提升渲染性能
- ✅ **LaTeX 验证**：预校验公式语法，独立定义便于修正
- 🎞️ **平滑过渡**：冻结帧填充，解决视频跳变问题

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

```bash
# 简单输入
python main.py "勾股定理"

# 详细参数
python main.py "勾股定理的几何证明" -d 60 -s "3Blue1Brown"
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

1. **剧本生成**：根据输入的数学公式/主题，生成结构化的视听剧本
2. **TTS 文案转换**：将剧本中的数学符号转换为中文口语
3. **音频生成**：使用 edge-tts 生成音频，获取精确时长
4. **Manim 代码生成**：根据剧本和音频时长生成 Manim 代码
5. **视频渲染**：执行 Manim 代码生成视频
6. **视频切割**：根据时间标记切割视频片段
7. **音画合并**：合并视频和音频，生成最终视频

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

## 许可证

MIT License
