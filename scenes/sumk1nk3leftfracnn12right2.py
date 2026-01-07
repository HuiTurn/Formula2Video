import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Sumk1nk3leftfracnn12right2(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "step1": "audios/step1.mp3",
            "step2": "audios/step2.mp3",
            "step3": "audios/step3.mp3",
            "step4": "audios/step4.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "大家好！今天我们来学习一个神奇的数学公式——立方和公式。",
            "step1": "首先，什么是立方呢？比如2的立方就是2乘2乘2等于8。",
            "step2": "立方和就是把1的立方、2的立方、一直到n的立方全部加起来。",
            "step3": "神奇的是，这个和竟然等于从1加到n的和的平方！",
            "step4": "让我们用n等于3来验证一下：左边是1加8加27等于36，右边是6的平方，也是36！",
            "summary": "立方和公式告诉我们，前n个自然数的立方和等于它们和的平方。记住这个美丽的公式吧！"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 标题
        title = Text("立方和公式", font_size=60, color=BLUE).to_edge(UP, buff=0.5)
        
        # 主公式
        formula = MathTex(
            r"\sum_{k=1}^{n} k^{3}=\left[\frac{n(n+1)}{2}\right]^{2}",
            font_size=56
        ).move_to(ORIGIN)
        
        # 解释文字
        explain1 = Text("1³ + 2³ + 3³ + ... + n³", font_size=36, color=YELLOW)
        explain1.next_to(formula, UP, buff=1.2)
        
        explain2 = Text("= (1 + 2 + 3 + ... + n)²", font_size=36, color=GREEN)
        explain2.next_to(formula, DOWN, buff=1.2)
        
        # 示例部分
        example_n = MathTex(r"n = 3", font_size=48, color=GOLD)
        example_n.to_edge(DOWN, buff=0.5)
        
        left_side = MathTex(r"1^3 + 2^3 + 3^3", font_size=40, color=YELLOW)
        left_side.shift(LEFT * 3 + DOWN * 2)
        
        right_side = MathTex(r"\left[\frac{3 \times 4}{2}\right]^2", font_size=40, color=GREEN)
        right_side.shift(RIGHT * 3 + DOWN * 2)
        
        # 动画开始
        self.add_sound(self.audios["intro"])
        self.play(Write(title))
        self.wait(self.get_duration(self.audios["intro"]) + 0.5)
        
        self.add_sound(self.audios["step1"])
        self.play(Write(formula))
        self.wait(self.get_duration(self.audios["step1"]) + 0.5)
        
        self.add_sound(self.audios["step2"])
        self.play(Write(explain1))
        self.wait(1)
        self.play(Write(explain2))
        self.wait(self.get_duration(self.audios["step2"]) + 0.5)
        
        self.add_sound(self.audios["step3"])
        # 高亮公式
        self.play(
            formula.animate.set_color_by_gradient(BLUE, GREEN),
            run_time=2
        )
        self.wait(self.get_duration(self.audios["step3"]) + 0.5)
        
        self.add_sound(self.audios["step4"])
        # 显示示例
        self.play(
            FadeIn(example_n),
            FadeIn(left_side),
            FadeIn(right_side)
        )
        
        # 计算过程
        calc1 = MathTex(r"= 1 + 8 + 27", font_size=36, color=YELLOW)
        calc1.next_to(left_side, DOWN, buff=0.3)
        
        calc2 = MathTex(r"= 36", font_size=36, color=YELLOW)
        calc2.next_to(calc1, DOWN, buff=0.3)
        
        calc3 = MathTex(r"= 6^2", font_size=36, color=GREEN)
        calc3.next_to(right_side, DOWN, buff=0.3)
        
        calc4 = MathTex(r"= 36", font_size=36, color=GREEN)
        calc4.next_to(calc3, DOWN, buff=0.3)
        
        self.play(Write(calc1), Write(calc3))
        self.wait(0.5)
        self.play(Write(calc2), Write(calc4))
        
        # 显示等号
        equals = MathTex("=", font_size=60, color=RED)
        equals.move_to(DOWN * 2.5)
        self.play(FadeIn(equals))
        
        self.wait(self.get_duration(self.audios["step4"]) + 0.5)
        
        self.add_sound(self.audios["summary"])
        # 总结动画
        self.play(
            Circumscribe(formula, color=GOLD, stroke_width=4),
            run_time=2
        )
        self.wait(self.get_duration(self.audios["summary"]) + 0.5)
        
        # 淡出
        self.play(
            FadeOut(title),
            FadeOut(formula),
            FadeOut(explain1),
            FadeOut(explain2),
            FadeOut(example_n),
            FadeOut(left_side),
            FadeOut(right_side),
            FadeOut(calc1),
            FadeOut(calc2),
            FadeOut(calc3),
            FadeOut(calc4),
            FadeOut(equals)
        )