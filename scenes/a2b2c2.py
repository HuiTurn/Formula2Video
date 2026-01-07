import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class A2b2c2(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "what": "audios/what.mp3",
            "triangle": "audios/triangle.mp3",
            "formula": "audios/formula.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "同学们好！今天我们来学习一个非常重要的数学公式——勾股定理。",
            "what": "勾股定理告诉我们，在直角三角形里，两条直角边的平方和，等于斜边的平方。",
            "triangle": "先认识一下直角三角形：它有一个90度的直角，最长的那条边叫做斜边。",
            "formula": "用公式表示就是：a的平方加b的平方等于c的平方。其中a和b是直角边，c是斜边。",
            "example": "比如，一条直角边是3厘米，另一条是4厘米，那么斜边就是5厘米。因为3的平方加4的平方等于5的平方。",
            "summary": "记住这个定理，它能帮我们解决很多生活中的测量问题。多练习，你一定能掌握！"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 1. 标题页
        title = Text("勾股定理", font_size=60, color=BLUE).to_edge(UP, buff=0.8)
        subtitle = Text("直角三角形的秘密", font_size=36, color=WHITE).next_to(title, DOWN, buff=0.5)
        grade_info = Text("初中数学 九年级", font_size=28, color=YELLOW).next_to(subtitle, DOWN, buff=0.8)
        
        self.add_sound(self.audios["intro"])
        self.play(Write(title), Write(subtitle), Write(grade_info))
        self.wait(self.get_duration(self.audios["intro"]) + 0.5)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(grade_info))
        
        # 2. 什么是勾股定理
        what_text = Text("什么是勾股定理？", font_size=48, color=GREEN).to_edge(UP, buff=0.8)
        
        self.add_sound(self.audios["what"])
        self.play(Write(what_text))
        self.wait(self.get_duration(self.audios["what"]) + 0.5)
        
        # 3. 直角三角形介绍
        triangle_text = Text("认识直角三角形", font_size=42, color=BLUE).to_edge(UP, buff=0.8)
        
        # 画直角三角形
        triangle = Polygon(
            ORIGIN, 
            3*RIGHT, 
            3*RIGHT + 4*UP,
            color=WHITE,
            stroke_width=4
        ).move_to(ORIGIN)
        
        # 标记直角
        right_angle = Square(side_length=0.3, color=RED, fill_opacity=1).move_to(triangle.get_vertices()[1] + 0.15*LEFT + 0.15*DOWN)
        
        # 边标签
        a_label = MathTex("a", font_size=36, color=YELLOW).next_to(triangle.get_edge_center(DOWN), DOWN, buff=0.3)
        b_label = MathTex("b", font_size=36, color=YELLOW).next_to(triangle.get_edge_center(RIGHT), RIGHT, buff=0.3)
        c_label = MathTex("c", font_size=36, color=RED).move_to(triangle.get_edge_center(UP+LEFT) + 0.5*UP + 0.5*LEFT)
        
        self.add_sound(self.audios["triangle"])
        self.play(
            ReplacementTransform(what_text, triangle_text),
            Create(triangle),
            Create(right_angle)
        )
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(self.get_duration(self.audios["triangle"]) + 0.5)
        
        # 4. 公式展示
        formula_text = Text("勾股定理公式", font_size=42, color=BLUE).to_edge(UP, buff=0.8)
        
        # 创建公式
        formula = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=72)
        formula_bg = BackgroundRectangle(formula, color=BLACK, fill_opacity=0.8, buff=0.5)
        
        # 公式说明
        explanation = VGroup(
            Text("a 和 b 是直角边", font_size=32, color=YELLOW),
            Text("c 是斜边（最长的边）", font_size=32, color=RED)
        ).arrange(DOWN, buff=0.3).next_to(formula, DOWN, buff=1.0)
        
        self.add_sound(self.audios["formula"])
        self.play(
            ReplacementTransform(triangle_text, formula_text),
            FadeOut(triangle),
            FadeOut(right_angle),
            FadeOut(a_label),
            FadeOut(b_label),
            FadeOut(c_label)
        )
        self.play(Create(formula_bg), Write(formula))
        self.play(Write(explanation))
        self.wait(self.get_duration(self.audios["formula"]) + 0.5)
        
        # 5. 具体例子
        example_text = Text("举个例子", font_size=42, color=BLUE).to_edge(UP, buff=0.8)
        
        # 例子三角形
        example_triangle = Polygon(
            ORIGIN,
            3*RIGHT,
            3*RIGHT + 4*UP,
            color=WHITE,
            stroke_width=4
        ).scale(0.8).move_to(ORIGIN)
        
        # 例子标签
        example_a = MathTex("3", font_size=36, color=YELLOW).next_to(example_triangle.get_edge_center(DOWN), DOWN, buff=0.3)
        example_b = MathTex("4", font_size=36, color=YELLOW).next_to(example_triangle.get_edge_center(RIGHT), RIGHT, buff=0.3)
        example_c = MathTex("5", font_size=36, color=RED).move_to(example_triangle.get_edge_center(UP+LEFT) + 0.4*UP + 0.4*LEFT)
        
        # 计算过程
        calc_text = VGroup(
            MathTex("3^2 + 4^2 = 5^2", font_size=36),
            MathTex("9 + 16 = 25", font_size=36),
            MathTex("25 = 25", font_size=36, color=GREEN)
        ).arrange(DOWN, buff=0.3).next_to(example_triangle, RIGHT, buff=1.5)
        
        self.add_sound(self.audios["example"])
        self.play(
            ReplacementTransform(formula_text, example_text),
            FadeOut(formula_bg),
            FadeOut(formula),
            FadeOut(explanation)
        )
        self.play(Create(example_triangle), Write(example_a), Write(example_b), Write(example_c))
        self.play(Write(calc_text[0]))
        self.play(Write(calc_text[1]))
        self.play(Write(calc_text[2]))
        self.wait(self.get_duration(self.audios["example"]) + 0.5)
        
        # 6. 总结
        summary_text = Text("记住勾股定理！", font_size=48, color=GREEN).to_edge(UP, buff=0.8)
        
        final_formula = MathTex("a^2 + b^2 = c^2", font_size=60, color=BLUE)
        final_formula_bg = BackgroundRectangle(final_formula, color=BLACK, fill_opacity=0.8, buff=0.5)
        
        tip_text = Text("多练习，你一定能掌握！", font_size=36, color=YELLOW).next_to(final_formula, DOWN, buff=1.0)
        
        self.add_sound(self.audios["summary"])
        self.play(
            ReplacementTransform(example_text, summary_text),
            FadeOut(example_triangle),
            FadeOut(example_a),
            FadeOut(example_b),
            FadeOut(example_c),
            FadeOut(calc_text)
        )
        self.play(Create(final_formula_bg), Write(final_formula))
        self.play(Write(tip_text))
        self.wait(self.get_duration(self.audios["summary"]) + 1.0)
        
        # 结束
        self.play(FadeOut(summary_text), FadeOut(final_formula_bg), FadeOut(final_formula), FadeOut(tip_text))