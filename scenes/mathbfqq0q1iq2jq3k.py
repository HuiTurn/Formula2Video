import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Mathbfqq0q1iq2jq3k(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "explain": "audios/explain.mp3",
            "parts": "audios/parts.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "今天我们来学习一个有趣的数学概念：四元数",
            "explain": "四元数就像一个四维的超复数，它有一个实部和三个虚部",
            "parts": "q0是实部，就像我们熟悉的实数。q1、q2、q3是三个虚部，分别乘以i、j、k",
            "example": "想象一下，四元数就像一个有四个轮子的车。实部是车身，三个虚部是三个轮子，它们一起让车能在三维空间里灵活转动",
            "summary": "四元数常用于三维旋转的表示，在计算机图形学和机器人学中非常有用"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+0%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 设置深色背景
        self.camera.background_color = "#1e1e1e"
        
        # 1. 引入标题
        self.add_sound(self.audios["intro"])
        title = Text("四元数", font_size=60, color=BLUE_A)
        subtitle = Text("Quaternion", font_size=40, color=GRAY_A)
        
        title.to_edge(UP, buff=0.8)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        self.wait(self.get_duration(self.audios["intro"]) - 2)
        
        # 淡出标题，准备进入主要内容
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # 2. 展示完整公式
        self.add_sound(self.audios["explain"])
        formula = MathTex(
            r"\mathbf{q} = q_0 + q_1 i + q_2 j + q_3 k",
            font_size=72,
            color=WHITE
        )
        
        # 公式居中显示
        formula.move_to(ORIGIN)
        
        # 添加公式说明文字
        explanation = Text("四维超复数：一个实部 + 三个虚部", 
                          font_size=36, 
                          color=YELLOW_A)
        explanation.next_to(formula, DOWN, buff=0.8)
        
        self.play(Write(formula))
        self.wait(0.5)
        self.play(Write(explanation))
        self.wait(self.get_duration(self.audios["explain"]) - 3)
        
        # 3. 分解讲解各个部分
        self.add_sound(self.audios["parts"])
        
        # 创建分解后的公式部分
        q0_part = MathTex(r"q_0", font_size=60, color=GREEN_A)
        q1_part = MathTex(r"q_1 i", font_size=60, color=BLUE_A)
        q2_part = MathTex(r"q_2 j", font_size=60, color=RED_A)
        q3_part = MathTex(r"q_3 k", font_size=60, color=ORANGE)
        
        plus1 = MathTex(r"+", font_size=60, color=WHITE)
        plus2 = MathTex(r"+", font_size=60, color=WHITE)
        plus3 = MathTex(r"+", font_size=60, color=WHITE)
        
        # 排列分解后的部分
        decomposed_formula = VGroup(
            q0_part, plus1, q1_part, plus2, q2_part, plus3, q3_part
        ).arrange(RIGHT, buff=0.3)
        decomposed_formula.move_to(ORIGIN)
        
        # 添加各部分说明
        q0_label = Text("实部（实数部分）", font_size=28, color=GREEN_A)
        q1_label = Text("虚部 i", font_size=28, color=BLUE_A)
        q2_label = Text("虚部 j", font_size=28, color=RED_A)
        q3_label = Text("虚部 k", font_size=28, color=ORANGE)
        
        q0_label.next_to(q0_part, DOWN, buff=0.3)
        q1_label.next_to(q1_part, DOWN, buff=0.3)
        q2_label.next_to(q2_part, DOWN, buff=0.3)
        q3_label.next_to(q3_part, DOWN, buff=0.3)
        
        # 变换动画：从完整公式到分解公式
        self.play(
            Transform(formula, decomposed_formula),
            FadeOut(explanation)
        )
        
        # 逐个显示标签
        self.play(Write(q0_label))
        self.wait(0.5)
        self.play(Write(q1_label))
        self.wait(0.5)
        self.play(Write(q2_label))
        self.wait(0.5)
        self.play(Write(q3_label))
        
        self.wait(self.get_duration(self.audios["parts"]) - 4)
        
        # 4. 生活化例子
        self.add_sound(self.audios["example"])
        
        # 清除之前的标签
        self.play(
            FadeOut(q0_label),
            FadeOut(q1_label),
            FadeOut(q2_label),
            FadeOut(q3_label)
        )
        
        # 创建汽车类比图形
        car_body = Rectangle(width=2, height=1, color=GREEN_A, fill_opacity=0.3)
        wheel1 = Circle(radius=0.2, color=BLUE_A, fill_opacity=0.3).shift(LEFT * 0.8 + DOWN * 0.6)
        wheel2 = Circle(radius=0.2, color=RED_A, fill_opacity=0.3).shift(RIGHT * 0.8 + DOWN * 0.6)
        wheel3 = Circle(radius=0.2, color=ORANGE, fill_opacity=0.3).shift(UP * 0.3)
        
        car = VGroup(car_body, wheel1, wheel2, wheel3)
        car.scale(0.8)
        car.next_to(decomposed_formula, DOWN, buff=1.2)
        
        # 添加标签
        body_label = Text("车身 = 实部 q₀", font_size=24, color=GREEN_A)
        wheel1_label = Text("轮子1 = q₁ i", font_size=24, color=BLUE_A)
        wheel2_label = Text("轮子2 = q₂ j", font_size=24, color=RED_A)
        wheel3_label = Text("轮子3 = q₃ k", font_size=24, color=ORANGE)
        
        body_label.next_to(car_body, UP, buff=0.2)
        wheel1_label.next_to(wheel1, DOWN, buff=0.2)
        wheel2_label.next_to(wheel2, DOWN, buff=0.2)
        wheel3_label.next_to(wheel3, UP, buff=0.2)
        
        # 显示汽车和标签
        self.play(FadeIn(car))
        self.wait(0.5)
        
        self.play(Write(body_label))
        self.wait(0.3)
        self.play(Write(wheel1_label))
        self.wait(0.3)
        self.play(Write(wheel2_label))
        self.wait(0.3)
        self.play(Write(wheel3_label))
        
        # 添加说明文字
        analogy_text = Text("就像汽车需要四个部分才能灵活运动", 
                          font_size=32, 
                          color=YELLOW_A)
        analogy_text.next_to(car, DOWN, buff=0.5)
        
        self.play(Write(analogy_text))
        
        self.wait(self.get_duration(self.audios["example"]) - 5)
        
        # 5. 总结
        self.add_sound(self.audios["summary"])
        
        # 清除汽车图形
        self.play(
            FadeOut(car),
            FadeOut(body_label),
            FadeOut(wheel1_label),
            FadeOut(wheel2_label),
            FadeOut(wheel3_label),
            FadeOut(analogy_text)
        )
        
        # 回到完整公式
        final_formula = MathTex(
            r"\mathbf{q} = q_0 + q_1 i + q_2 j + q_3 k",
            font_size=72,
            color=WHITE
        )
        final_formula.move_to(ORIGIN)
        
        # 添加应用说明
        application = Text("应用：三维旋转表示", font_size=40, color=BLUE_A)
        fields = Text("计算机图形学 · 机器人学 · 游戏开发", font_size=32, color=GREEN_A)
        
        application.next_to(final_formula, DOWN, buff=0.8)
        fields.next_to(application, DOWN, buff=0.4)
        
        # 变换动画
        self.play(
            Transform(decomposed_formula, final_formula),
            Write(application),
            Write(fields)
        )
        
        # 突出显示公式
        self.play(
            Circumscribe(final_formula, color=YELLOW, buff=0.2, time_width=2)
        )
        
        self.wait(self.get_duration(self.audios["summary"]) - 2)
        
        # 6. 结束淡出
        self.play(
            FadeOut(final_formula),
            FadeOut(application),
            FadeOut(fields)
        )
        self.wait(1)
    
    def ensure_in_bounds(self, obj, max_w=12.0, max_h=7.0):
        if obj.get_width() > max_w: 
            obj.scale(max_w / obj.get_width())
        if obj.get_height() > max_h: 
            obj.scale(max_h / obj.get_height())