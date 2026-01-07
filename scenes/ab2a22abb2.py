import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Ab2a22abb2(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "formula": "audios/formula.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "今天我们要学习一个非常重要的数学公式：完全平方公式。这个公式可以帮助我们快速展开像(a + b)的平方这样的表达式。",
            "formula": "完全平方公式是：(a + b)的平方等于a的平方加上2ab再加上b的平方。我们可以用图形来理解这个公式。",
            "example": "想象一个边长为a + b的正方形。这个正方形可以分成四个部分：一个边长为a的正方形，两个长宽分别为a和b的矩形，以及一个边长为b的正方形。",
            "summary": "通过这个图形分解，我们可以看到(a + b)的平方确实等于a的平方+2ab+b的平方。这就是完全平方公式的几何解释。"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 1. 创建对象
        title = Text("完全平方公式", font_size=48).to_edge(UP, buff=0.5)
        subtitle = Text("初中数学 · 九年级", font_size=24).to_edge(UP, buff=0.5).next_to(title, DOWN, buff=0.2)
        
        formula = MathTex(r"(a + b)^2 = a^2 + 2ab + b^2", font_size=60).move_to(ORIGIN)
        
        # 几何示意图
        square = Square(side_length=3).shift(LEFT*3)
        a_label = Text("a", font_size=24).next_to(square, UP)
        b_label = Text("b", font_size=24).next_to(square, RIGHT)
        
        # 分解图形
        a2_square = Square(side_length=1.5).set_color(BLUE).move_to(LEFT*3)
        ab_rect1 = Rectangle(width=1.5, height=1.5).set_color(GREEN).next_to(a2_square, RIGHT, buff=0)
        ab_rect2 = Rectangle(width=1.5, height=1.5).set_color(GREEN).next_to(a2_square, DOWN, buff=0)
        b2_square = Square(side_length=1.5).set_color(YELLOW).next_to(ab_rect1, DOWN, buff=0)
        
        # 文字说明
        explanation = Text("这个大正方形的面积等于：\n1个a² + 2个ab + 1个b²", font_size=28).to_edge(RIGHT, buff=1)
        
        # 2. 边界检查
        self.ensure_in_bounds(title)
        self.ensure_in_bounds(formula)
        self.ensure_in_bounds(square)
        self.ensure_in_bounds(explanation)
        
        # 3. 布局定位
        formula.move_to(ORIGIN)
        square.shift(LEFT*3)
        explanation.to_edge(RIGHT, buff=1)
        
        # 4. 动画序列
        self.play(Write(title), Write(subtitle))
        self.wait(self.get_duration(self.audios["intro"]) + 0.5)
        
        self.play(Write(formula))
        self.wait(self.get_duration(self.audios["formula"]) + 0.5)
        
        self.play(Create(square), Write(a_label), Write(b_label))
        self.wait(self.get_duration(self.audios["example"]) + 0.5)
        
        self.play(
            Create(a2_square),
            Create(ab_rect1),
            Create(ab_rect2),
            Create(b2_square)
        )
        self.play(Write(explanation))
        self.wait(self.get_duration(self.audios["summary"]) + 1.0)
        
        self.play(FadeOut(*self.mobjects))
    
    def ensure_in_bounds(self, obj, max_w=12.0, max_h=7.0):
        if obj.get_width() > max_w: obj.scale(max_w / obj.get_width())
        if obj.get_height() > max_h: obj.scale(max_h / obj.get_height())