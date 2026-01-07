import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

config.background_color = "#1e1e1e"
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60

class QwxmathbfiymathbfjzmathbfkquadwxyzinmathbbRmathbfi2mathbfj2mathbfk2mathbfimathbfjmathbfk1(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "step1": "audios/step1.mp3",
            "step2": "audios/step2.mp3",
            "step3": "audios/step3.mp3",
            "step4": "audios/step4.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "step1": "大家好，今天我们来认识一种神奇的数，叫四元数。",
            "step2": "它像一座小房子，有四个房间，一个实数房间和三个特别的虚数房间。",
            "step3": "这三个房间的名字分别叫 i、j、k，它们有自己独特的乘法小规则。",
            "step4": "记住口诀：i j k 转一圈，结果等于负一，四元数就这样简单！"
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
        title = Text("什么是四元数？", font_size=60, color=WHITE).to_edge(UP, buff=0.5)
        
        # 公式
        formula = MathTex(
            r"q = w + x\,\mathbf{i} + y\,\mathbf{j} + z\,\mathbf{k}",
            r"\quad w,x,y,z\in\mathbb{R}",
            r"\;\mathbf{i}^2=\mathbf{j}^2=\mathbf{k}^2=\mathbf{i}\mathbf{j}\mathbf{k}=-1",
            font_size=48
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        
        # 房子图形
        house = self.create_house().scale(0.8).next_to(formula, UP, buff=0.8)
        
        # 标签
        label_w = Text("实部 w", font_size=28, color=BLUE).move_to(house[0]).shift(UP*0.3)
        label_ijk = Text("虚部 i j k", font_size=28, color=GREEN).move_to(house[1]).shift(DOWN*0.3)
        
        # 动画
        self.play(Write(title))
        self.wait(0.5)
        
        self.add_sound(self.audios["step1"])
        self.play(FadeIn(house, shift=UP), run_time=1.5)
        self.wait(self.get_duration(self.audios["step1"]))
        
        self.add_sound(self.audios["step2"])
        self.play(Write(label_w), Write(label_ijk))
        self.wait(self.get_duration(self.audios["step2"]))
        
        self.add_sound(self.audios["step3"])
        self.play(Write(formula[0]), run_time=2)
        self.wait(self.get_duration(self.audios["step3"]))
        
        self.add_sound(self.audios["step4"])
        self.play(Write(formula[1]), Write(formula[2]))
        self.wait(self.get_duration(self.audios["step4"]))
        
        # 高亮
        box = SurroundingRectangle(formula, color=GOLD, buff=0.2, stroke_width=3)
        self.play(Create(box))
        self.wait(1)
        
        # 结束
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)
    
    def create_house(self):
        walls = Rectangle(width=4, height=2.5, color=WHITE, stroke_width=4)
        roof = Polygon(
            walls.get_top()+UP*0.5,
            walls.get_corner(UL)+LEFT*0.5+UP*0.5,
            walls.get_corner(UR)+RIGHT*0.5+UP*0.5,
            color=WHITE, stroke_width=4
        )
        door = Rectangle(width=0.8, height=1.2, color=BLUE, stroke_width=3).move_to(walls.get_bottom())
        window = Square(side_length=0.7, color=TEAL_A, stroke_width=3).move_to(walls.get_left()+RIGHT*0.7+UP*0.4)
        chimney = Rectangle(width=0.4, height=1, color=RED, stroke_width=3).move_to(roof.get_right()+LEFT*0.6+UP*0.3)
        return VGroup(walls, roof, door, window, chimney)