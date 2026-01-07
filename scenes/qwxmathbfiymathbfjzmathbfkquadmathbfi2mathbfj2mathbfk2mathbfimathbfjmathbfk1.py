import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Qwxmathbfiymathbfjzmathbfkquadmathbfi2mathbfj2mathbfk2mathbfimathbfjmathbfk1(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "step1": "audios/step1.mp3",
            "step2": "audios/step2.mp3",
            "step3": "audios/step3.mp3",
            "step4": "audios/step4.mp3",
            "step5": "audios/step5.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "大家好！今天我们来学习一个有趣的数学概念——四元数。",
            "step1": "首先，我们来看四元数长什么样。它就像一个数字小团队，由四个部分组成。",
            "step2": "第一个部分是普通的数字w，就像我们平时数数用的数字。",
            "step3": "后面三个部分很特别，它们分别叫做i、j、k，就像三个有魔法的数字精灵。",
            "step4": "这些精灵有一个神奇的规则：i的平方等于负1，j的平方也等于负1，k的平方还是等于负1。",
            "step5": "最神奇的是，当i、j、k三个精灵按顺序相乘时，结果也是负1。",
            "summary": "总结一下，四元数就是四个数字的组合，其中三个特殊的数字i、j、k有神奇的乘法规则。记住这个公式，你就掌握了四元数的基本形式！"
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
        title = Text("四元数公式", font_size=48, color=BLUE).to_edge(UP, buff=0.8)
        subtitle = Text("Grade 9 数学", font_size=32, color=GRAY).next_to(title, DOWN, buff=0.3)
        
        # 介绍
        self.add_sound(self.audios["intro"])
        self.play(Write(title), Write(subtitle))
        self.wait(self.get_duration(self.audios["intro"]) + 0.5)
        
        # 步骤1：展示四元数公式
        self.add_sound(self.audios["step1"])
        formula = MathTex(r"q = w + x\,\mathbf{i} + y\,\mathbf{j} + z\,\mathbf{k}", font_size=40)
        formula_bg = BackgroundRectangle(formula, color=BLACK, fill_opacity=0.8, buff=0.3)
        formula_group = VGroup(formula_bg, formula)
        formula_group.move_to(ORIGIN)
        
        # 添加说明文字
        explain1 = Text("四元数 = 四个部分的组合", font_size=28, color=YELLOW)
        explain1.next_to(formula, DOWN, buff=0.8)
        
        self.play(Create(formula_bg), Write(formula), Write(explain1))
        self.wait(self.get_duration(self.audios["step1"]) + 0.5)
        
        # 步骤2：解释w部分
        self.add_sound(self.audios["step2"])
        w_part = MathTex(r"w", font_size=60, color=GREEN).move_to(LEFT * 4 + UP * 0.5)
        w_arrow = Arrow(formula[0][2].get_center(), w_part.get_bottom(), color=GREEN, buff=0.2)
        w_text = Text("普通数字，像1、2、3...", font_size=24, color=GREEN)
        w_text.next_to(w_part, DOWN, buff=0.3)
        
        self.play(Create(w_arrow), Write(w_part), Write(w_text))
        self.wait(self.get_duration(self.audios["step2"]) + 0.5)
        
        # 步骤3：解释i、j、k部分
        self.add_sound(self.audios["step3"])
        i_part = MathTex(r"x\,\mathbf{i}", font_size=60, color=RED).move_to(LEFT * 1.5 + UP * 0.5)
        j_part = MathTex(r"y\,\mathbf{j}", font_size=60, color=BLUE).move_to(RIGHT * 1.5 + UP * 0.5)
        k_part = MathTex(r"z\,\mathbf{k}", font_size=60, color=PURPLE).move_to(RIGHT * 4 + UP * 0.5)
        
        i_arrow = Arrow(formula[0][4:6].get_center(), i_part.get_bottom(), color=RED, buff=0.2)
        j_arrow = Arrow(formula[0][7:9].get_center(), j_part.get_bottom(), color=BLUE, buff=0.2)
        k_arrow = Arrow(formula[0][10:12].get_center(), k_part.get_bottom(), color=PURPLE, buff=0.2)
        
        magic_text = Text("三个有魔法的数字精灵！", font_size=28, color=YELLOW)
        magic_text.next_to(formula, DOWN, buff=1.5)
        
        self.play(
            Create(i_arrow), Create(j_arrow), Create(k_arrow),
            Write(i_part), Write(j_part), Write(k_part),
            Transform(explain1, magic_text)
        )
        self.wait(self.get_duration(self.audios["step3"]) + 0.5)
        
        # 步骤4：展示乘法规则1
        self.add_sound(self.audios["step4"])
        rule1 = MathTex(r"\mathbf{i}^2 = \mathbf{j}^2 = \mathbf{k}^2 = -1", font_size=40)
        rule1_bg = BackgroundRectangle(rule1, color=BLACK, fill_opacity=0.8, buff=0.3)
        rule1_group = VGroup(rule1_bg, rule1)
        rule1_group.next_to(formula, DOWN, buff=2.5)
        
        # 创建视觉辅助
        i_square = VGroup(
            MathTex(r"\mathbf{i}^2", font_size=36, color=RED),
            Text("=", font_size=28),
            Text("-1", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.2).move_to(LEFT * 4 + DOWN * 2)
        
        j_square = VGroup(
            MathTex(r"\mathbf{j}^2", font_size=36, color=BLUE),
            Text("=", font_size=28),
            Text("-1", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.2).move_to(ORIGIN + DOWN * 2)
        
        k_square = VGroup(
            MathTex(r"\mathbf{k}^2", font_size=36, color=PURPLE),
            Text("=", font_size=28),
            Text("-1", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.2).move_to(RIGHT * 4 + DOWN * 2)
        
        self.play(
            Create(rule1_bg), Write(rule1),
            Write(i_square), Write(j_square), Write(k_square)
        )
        self.wait(self.get_duration(self.audios["step4"]) + 0.5)
        
        # 步骤5：展示乘法规则2
        self.add_sound(self.audios["step5"])
        rule2 = MathTex(r"\mathbf{i}\mathbf{j}\mathbf{k} = -1", font_size=40)
        rule2_bg = BackgroundRectangle(rule2, color=BLACK, fill_opacity=0.8, buff=0.3)
        rule2_group = VGroup(rule2_bg, rule2)
        rule2_group.next_to(rule1, DOWN, buff=0.8)
        
        # 创建动画效果
        ijk_group = VGroup(
            MathTex(r"\mathbf{i}", font_size=36, color=RED),
            MathTex(r"\mathbf{j}", font_size=36, color=BLUE),
            MathTex(r"\mathbf{k}", font_size=36, color=PURPLE),
            Text("=", font_size=28),
            Text("-1", font_size=36, color=GREEN)
        ).arrange(RIGHT, buff=0.2).move_to(ORIGIN + DOWN * 3.5)
        
        self.play(
            Create(rule2_bg), Write(rule2),
            Write(ijk_group)
        )
        self.wait(self.get_duration(self.audios["step5"]) + 0.5)
        
        # 总结
        self.add_sound(self.audios["summary"])
        summary_text = Text(
            "记住：四元数 = w + xi + yj + zk\ni² = j² = k² = ijk = -1",
            font_size=32,
            color=YELLOW
        )
        summary_bg = BackgroundRectangle(summary_text, color=BLACK, fill_opacity=0.9, buff=0.5)
        summary_group = VGroup(summary_bg, summary_text)
        summary_group.move_to(ORIGIN).to_edge(DOWN, buff=1.0)
        
        # 高亮公式
        box = SurroundingRectangle(formula, color=YELLOW, stroke_width=3)
        
        self.play(
            Create(summary_bg), Write(summary_text),
            Create(box)
        )
        self.wait(self.get_duration(self.audios["summary"]) + 1.0)
        
        # 结束
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.5)