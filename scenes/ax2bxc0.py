import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *
import numpy as np

class Ax2bxc0(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "standard_form": "audios/standard_form.mp3",
            "coefficients": "audios/coefficients.mp3",
            "a_not_zero": "audios/a_not_zero.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "同学们好，今天我们来学习一元二次方程。",
            "standard_form": "一元二次方程的标准形式是：a x 平方，加 b x，加 c，等于零。",
            "coefficients": "这里的 a、b、c 是常数，就像配方里的固定材料。a 是二次项系数，b 是一次项系数，c 是常数项。",
            "a_not_zero": "特别注意，a 不能等于零。如果 a 等于零，x 平方项就消失了，这就不是二次方程了。",
            "example": "举个例子，2x平方减3x加1等于0，就是一个一元二次方程。这里 a 等于2，b 等于负3，c 等于1。",
            "summary": "总结一下，一元二次方程有三个关键：一是只有一个未知数 x，二是最高次数是2，三是标准形式 a x 平方加 b x 加 c 等于零，且 a 不等于零。"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+0%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_audio_duration(self, filename):
        try:
            audio = MP3(filename)
            return audio.info.length
        except:
            return 2.0
    
    def safe_layout(self, elements, max_per_row=3, h_spacing=0.8, v_spacing=0.5):
        """安全布局函数，防止元素拥挤和超出边界"""
        group = VGroup(*elements)
        
        # 如果元素太多，分行排列
        if len(elements) > max_per_row:
            rows = []
            for i in range(0, len(elements), max_per_row):
                row_elements = elements[i:i+max_per_row]
                row_group = VGroup(*row_elements).arrange(RIGHT, buff=h_spacing)
                rows.append(row_group)
            
            group = VGroup(*rows).arrange(DOWN, buff=v_spacing)
        else:
            group.arrange(RIGHT, buff=h_spacing)
        
        # 检查边界
        frame_width = config.frame_width - 1
        frame_height = config.frame_height - 1
        
        left_bound = group.get_left()[0]
        right_bound = group.get_right()[0]
        top_bound = group.get_top()[1]
        bottom_bound = group.get_bottom()[1]
        
        # 如果超出边界，自动缩放
        if (abs(left_bound) > frame_width/2 or abs(right_bound) > frame_width/2 or
            abs(top_bound) > frame_height/2 or abs(bottom_bound) > frame_height/2):
            group.scale(0.8)
        
        return group
    
    def construct(self):
        # 第一步：引入概念
        title = Text("一元二次方程", font_size=48, color=BLUE)
        subtitle = Text("Quadratic Equation in One Variable", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(0.5)
        
        # 播放介绍音频
        intro_duration = self.get_audio_duration(self.audios["intro"])
        self.add_sound(self.audios["intro"])
        self.wait(intro_duration)
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # 第二步：显示标准形式
        equation = MathTex("ax^2 + bx + c = 0", font_size=60, color=WHITE)
        equation_label = Text("标准形式", font_size=32, color=YELLOW)
        equation_label.next_to(equation, UP, buff=0.5)
        
        self.play(Write(equation), FadeIn(equation_label))
        self.wait(0.5)
        
        # 播放标准形式音频
        standard_duration = self.get_audio_duration(self.audios["standard_form"])
        self.add_sound(self.audios["standard_form"])
        self.wait(standard_duration)
        
        # 第三步：解释系数
        a_box = SurroundingRectangle(equation[0][0:1], color=RED, buff=0.1)  # a
        b_box = SurroundingRectangle(equation[0][5:6], color=GREEN, buff=0.1)  # b
        c_box = SurroundingRectangle(equation[0][8:9], color=BLUE, buff=0.1)  # c
        
        a_label = Text("二次项系数", font_size=24, color=RED)
        b_label = Text("一次项系数", font_size=24, color=GREEN)
        c_label = Text("常数项", font_size=24, color=BLUE)
        
        a_label.next_to(a_box, DOWN, buff=0.3)
        b_label.next_to(b_box, DOWN, buff=0.3)
        c_label.next_to(c_box, DOWN, buff=0.3)
        
        self.play(
            Create(a_box),
            Create(b_box),
            Create(c_box),
            FadeIn(a_label),
            FadeIn(b_label),
            FadeIn(c_label)
        )
        self.wait(0.5)
        
        # 播放系数解释音频
        coeff_duration = self.get_audio_duration(self.audios["coefficients"])
        self.add_sound(self.audios["coefficients"])
        self.wait(coeff_duration)
        
        self.play(
            FadeOut(a_box), FadeOut(b_box), FadeOut(c_box),
            FadeOut(a_label), FadeOut(b_label), FadeOut(c_label)
        )
        self.wait(0.5)
        
        # 第四步：强调a≠0
        a_part = equation[0][0:1].copy()
        a_part.set_color(RED)
        
        not_zero_eq = MathTex("a \\neq 0", font_size=48, color=RED)
        not_zero_eq.next_to(equation, DOWN, buff=0.8)
        
        explanation = Text("如果 a=0，方程就变成一次方程了", font_size=28, color=YELLOW)
        explanation.next_to(not_zero_eq, DOWN, buff=0.3)
        
        self.play(
            a_part.animate.scale(1.2),
            Write(not_zero_eq),
            FadeIn(explanation)
        )
        self.wait(0.5)
        
        # 播放a≠0音频
        a_not_zero_duration = self.get_audio_duration(self.audios["a_not_zero"])
        self.add_sound(self.audios["a_not_zero"])
        self.wait(a_not_zero_duration)
        
        self.play(
            FadeOut(a_part),
            FadeOut(not_zero_eq),
            FadeOut(explanation)
        )
        self.wait(0.5)
        
        # 第五步：举例说明
        example_eq = MathTex("2x^2 - 3x + 1 = 0", font_size=60, color=WHITE)
        example_label = Text("例子", font_size=32, color=ORANGE)
        example_label.next_to(example_eq, UP, buff=0.5)
        
        self.play(
            Transform(equation, example_eq),
            Transform(equation_label, example_label)
        )
        self.wait(0.5)
        
        # 标注例子中的系数
        example_a = MathTex("a = 2", font_size=36, color=RED)
        example_b = MathTex("b = -3", font_size=36, color=GREEN)
        example_c = MathTex("c = 1", font_size=36, color=BLUE)
        
        coeff_group = self.safe_layout([example_a, example_b, example_c], max_per_row=3)
        coeff_group.next_to(example_eq, DOWN, buff=0.8)
        
        self.play(FadeIn(coeff_group))
        self.wait(0.5)
        
        # 播放例子音频
        example_duration = self.get_audio_duration(self.audios["example"])
        self.add_sound(self.audios["example"])
        self.wait(example_duration)
        
        self.play(FadeOut(coeff_group))
        self.wait(0.5)
        
        # 第六步：总结
        self.play(
            Transform(equation, MathTex("ax^2 + bx + c = 0", font_size=60, color=WHITE)),
            Transform(equation_label, Text("总结", font_size=32, color=PURPLE))
        )
        
        # 创建总结要点
        point1 = Text("1. 只有一个未知数 x", font_size=28, color=GREEN)
        point2 = Text("2. 最高次数是 2", font_size=28, color=YELLOW)
        point3 = Text("3. 标准形式: ax² + bx + c = 0", font_size=28, color=BLUE)
        point4 = Text("4. a ≠ 0", font_size=28, color=RED)
        
        points_group = VGroup(point1, point2, point3, point4).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        points_group.next_to(equation, DOWN, buff=1.0)
        
        self.play(LaggedStart(
            FadeIn(point1, shift=UP),
            FadeIn(point2, shift=UP),
            FadeIn(point3, shift=UP),
            FadeIn(point4, shift=UP),
            lag_ratio=0.3
        ))
        self.wait(0.5)
        
        # 播放总结音频
        summary_duration = self.get_audio_duration(self.audios["summary"])
        self.add_sound(self.audios["summary"])
        self.wait(summary_duration)
        
        # 最后淡出
        self.play(
            FadeOut(equation),
            FadeOut(equation_label),
            FadeOut(point1),
            FadeOut(point2),
            FadeOut(point3),
            FadeOut(point4)
        )
        self.wait(1)