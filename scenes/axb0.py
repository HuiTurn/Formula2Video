import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Axb0(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "step1": "audios/step1.mp3",
            "step2": "audios/step2.mp3",
            "step3": "audios/step3.mp3",
            "outro": "audios/outro.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "大家好，今天我们来学习一元一次方程。",
            "step1": "一元一次方程就像天平，左边和右边要平衡。",
            "step2": "比如，小明买铅笔，一支铅笔三元，他付了十元，找回四元。我们可以写成三x加六等于十。",
            "step3": "解方程就像拆礼物，一步一步把x找出来。最后我们得到x等于负b除以a。",
            "outro": "记住，一元一次方程就是找平衡，让x现身！"
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
        title = Text("一元一次方程", font_size=60, color=BLUE).to_edge(UP, buff=0.5)
        subtitle = Text("ax + b = 0", font_size=48, color=WHITE).next_to(title, DOWN, buff=0.3)
        
        # 天平类比图形
        balance_beam = Line(LEFT*3, RIGHT*3, color=GRAY, stroke_width=8).shift(DOWN*0.5)
        fulcrum = Triangle(fill_opacity=1, color=GRAY).scale(0.3).next_to(balance_beam, DOWN, buff=0)
        left_pan = Rectangle(width=1.5, height=0.2, color=GRAY).next_to(balance_beam.get_left(), DOWN, buff=0.1)
        right_pan = Rectangle(width=1.5, height=0.2, color=GRAY).next_to(balance_beam.get_right(), DOWN, buff=0.1)
        balance = VGroup(balance_beam, fulcrum, left_pan, right_pan).shift(DOWN*2)
        
        # 生活例子
        example_text = Text("小明买铅笔：3元一支，付了10元，找回4元", font_size=28, color=YELLOW)
        example_eq = MathTex("3x + 6 = 10", font_size=36, color=YELLOW)
        example_group = VGroup(example_text, example_eq).arrange(DOWN, buff=0.3).next_to(balance, UP, buff=1)
        
        # 解方程步骤
        step1 = MathTex("ax + b = 0", font_size=48, color=WHITE)
        step2 = MathTex("ax = -b", font_size=48, color=GREEN)
        step3 = MathTex("x = -\\frac{b}{a}", font_size=48, color=GOLD)
        steps = VGroup(step1, step2, step3).arrange(DOWN, buff=0.8).shift(LEFT*3 + DOWN*0.5)
        
        # 重点框
        highlight_box = SurroundingRectangle(step3, color=GOLD, buff=0.2, stroke_width=4)
        
        # 动画开始
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(0.5)
        
        self.add_sound(self.audios["intro"])
        self.wait(self.get_duration(self.audios["intro"]) + 0.5)
        
        # 天平动画
        self.add_sound(self.audios["step1"])
        self.play(Create(balance), run_time=2)
        self.wait(self.get_duration(self.audios["step1"]) - 2 + 0.5)
        
        # 生活例子
        self.add_sound(self.audios["step2"])
        self.play(FadeIn(example_text), FadeIn(example_eq))
        self.wait(self.get_duration(self.audios["step2"]) + 0.5)
        
        # 解方程步骤
        self.add_sound(self.audios["step3"])
        self.play(Write(step1))
        self.wait(1)
        self.play(TransformMatchingTex(step1.copy(), step2))
        self.wait(1)
        self.play(TransformMatchingTex(step2.copy(), step3))
        self.wait(0.5)
        self.play(Create(highlight_box))
        self.wait(self.get_duration(self.audios["step3"]) - 3 + 0.5)
        
        # 结尾
        self.add_sound(self.audios["outro"])
        outro_text = Text("记住：解方程就是找平衡！", font_size=40, color=BLUE)
        outro_text.next_to(step3, DOWN, buff=1)
        self.play(FadeIn(outro_text))
        self.wait(self.get_duration(self.audios["outro"]) + 0.5)
        
        # 淡出
        self.play(FadeOut(Group(*self.mobjects)))