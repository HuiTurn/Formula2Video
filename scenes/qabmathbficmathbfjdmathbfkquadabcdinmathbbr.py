import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class QabmathbficmathbfjdmathbfkquadabcdinmathbbR(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "real_imaginary": "audios/real_imaginary.mp3",
            "quaternion_form": "audios/quaternion_form.mp3",
            "i_j_k": "audios/i_j_k.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "同学们好，今天我们来学习一个有趣的数学概念——四元数。",
            "real_imaginary": "我们先回忆一下学过的复数。复数有一个实部和一个虚部，比如3加2i。",
            "quaternion_form": "四元数就像是复数的升级版，它有一个实部和三个虚部。",
            "i_j_k": "这三个虚部单位i、j、k，就像是三个不同方向的旋转轴，它们有特殊的乘法规则。",
            "summary": "所以四元数q等于a加bi加cj加dk，其中a、b、c、d都是实数。它主要用来描述三维空间中的旋转。"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e1e"
        
        # 1. 引入标题
        self.add_sound(self.audios["intro"])
        title = Text("四元数", font_size=60, color=BLUE_A)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait(self.get_duration(self.audios["intro"]) - 1)
        
        # 2. 回顾复数（从已知到未知）
        self.add_sound(self.audios["real_imaginary"])
        complex_title = Text("复数（复习）", font_size=48, color=TEAL_A)
        complex_title.next_to(title, DOWN, buff=0.8)
        
        complex_formula = MathTex(r"z = a + b\mathbf{i}", font_size=56, color=WHITE)
        complex_formula.next_to(complex_title, DOWN, buff=0.8)
        
        # 添加解释文字
        real_part_text = Text("实部", font_size=32, color=GREEN_A)
        imaginary_part_text = Text("虚部", font_size=32, color=YELLOW_A)
        
        # 定位解释文字
        real_part_text.next_to(complex_formula[0][2:4], DOWN, buff=0.3)
        imaginary_part_text.next_to(complex_formula[0][5:], DOWN, buff=0.3)
        
        # 添加指向箭头
        real_arrow = Arrow(real_part_text.get_top(), complex_formula[0][2:4].get_bottom(), 
                          color=GREEN_A, buff=0.1)
        imaginary_arrow = Arrow(imaginary_part_text.get_top(), complex_formula[0][5:].get_bottom(), 
                               color=YELLOW_A, buff=0.1)
        
        self.play(FadeIn(complex_title))
        self.play(Write(complex_formula))
        self.play(
            Write(real_part_text),
            Create(real_arrow),
            Write(imaginary_part_text),
            Create(imaginary_arrow)
        )
        self.wait(self.get_duration(self.audios["real_imaginary"]) - 2)
        
        # 清理复数部分
        self.play(
            FadeOut(complex_title),
            FadeOut(complex_formula),
            FadeOut(real_part_text),
            FadeOut(real_arrow),
            FadeOut(imaginary_part_text),
            FadeOut(imaginary_arrow)
        )
        
        # 3. 引入四元数概念
        self.add_sound(self.audios["quaternion_form"])
        quaternion_title = Text("四元数", font_size=48, color=BLUE_A)
        quaternion_title.next_to(title, DOWN, buff=0.8)
        
        # 逐步显示四元数公式
        formula_parts = VGroup(
            MathTex(r"q = ", font_size=56, color=WHITE),
            MathTex(r"a", font_size=56, color=GREEN_A),
            MathTex(r" + ", font_size=56, color=WHITE),
            MathTex(r"b\mathbf{i}", font_size=56, color=YELLOW_A),
            MathTex(r" + ", font_size=56, color=WHITE),
            MathTex(r"c\mathbf{j}", font_size=56, color=GOLD_A),
            MathTex(r" + ", font_size=56, color=WHITE),
            MathTex(r"d\mathbf{k}", font_size=56, color=RED_A)
        ).arrange(RIGHT, buff=0.2)
        formula_parts.next_to(quaternion_title, DOWN, buff=1.0)
        
        # 添加条件
        condition = MathTex(r"(a, b, c, d \in \mathbb{R})", font_size=40, color=GRAY_A)
        condition.next_to(formula_parts, DOWN, buff=0.5)
        
        self.play(FadeIn(quaternion_title))
        
        # 逐步显示公式各部分
        self.play(Write(formula_parts[0]))  # q =
        self.wait(0.5)
        self.play(Write(formula_parts[1]))  # a
        self.wait(0.5)
        self.play(Write(formula_parts[2:4]))  # + bi
        self.wait(0.5)
        self.play(Write(formula_parts[4:6]))  # + cj
        self.wait(0.5)
        self.play(Write(formula_parts[6:]))  # + dk
        self.wait(0.5)
        self.play(Write(condition))
        
        # 添加解释文字（叠加在公式上）
        real_part_label = Text("实部", font_size=28, color=GREEN_A)
        real_part_label.next_to(formula_parts[1], UP, buff=0.2)
        
        i_part_label = Text("虚部1", font_size=28, color=YELLOW_A)
        i_part_label.next_to(formula_parts[3], UP, buff=0.2)
        
        j_part_label = Text("虚部2", font_size=28, color=GOLD_A)
        j_part_label.next_to(formula_parts[5], UP, buff=0.2)
        
        k_part_label = Text("虚部3", font_size=28, color=RED_A)
        k_part_label.next_to(formula_parts[7], UP, buff=0.2)
        
        self.play(
            FadeIn(real_part_label),
            FadeIn(i_part_label),
            FadeIn(j_part_label),
            FadeIn(k_part_label)
        )
        
        self.wait(self.get_duration(self.audios["quaternion_form"]) - 3)
        
        # 清理解释文字
        self.play(
            FadeOut(real_part_label),
            FadeOut(i_part_label),
            FadeOut(j_part_label),
            FadeOut(k_part_label)
        )
        
        # 4. 解释i, j, k单位
        self.add_sound(self.audios["i_j_k"])
        
        # 创建三个轴表示i, j, k
        axes_group = VGroup()
        
        # i轴（X轴）
        i_axis = Arrow(LEFT * 2, RIGHT * 2, color=YELLOW_A, stroke_width=4)
        i_label = MathTex(r"\mathbf{i}", font_size=40, color=YELLOW_A)
        i_label.next_to(i_axis.get_end(), RIGHT, buff=0.2)
        i_text = Text("旋转轴1", font_size=28, color=YELLOW_A)
        i_text.next_to(i_axis, UP, buff=0.3)
        
        # j轴（Y轴）
        j_axis = Arrow(DOWN * 2, UP * 2, color=GOLD_A, stroke_width=4)
        j_label = MathTex(r"\mathbf{j}", font_size=40, color=GOLD_A)
        j_label.next_to(j_axis.get_end(), UP, buff=0.2)
        j_text = Text("旋转轴2", font_size=28, color=GOLD_A)
        j_text.next_to(j_axis, RIGHT, buff=0.3)
        
        # k轴（Z轴方向，用斜线表示）
        k_axis = Line(LEFT * 1.5 + DOWN * 1.5, RIGHT * 1.5 + UP * 1.5, 
                     color=RED_A, stroke_width=4)
        k_label = MathTex(r"\mathbf{k}", font_size=40, color=RED_A)
        k_label.next_to(k_axis.get_end(), UP + RIGHT, buff=0.2)
        k_text = Text("旋转轴3", font_size=28, color=RED_A)
        k_text.next_to(k_axis.get_center(), LEFT, buff=0.3)
        
        axes_group.add(i_axis, i_label, i_text, j_axis, j_label, j_text, k_axis, k_label, k_text)
        axes_group.scale(0.8)
        axes_group.move_to(ORIGIN)
        
        # 移动公式到上方
        formula_group = VGroup(quaternion_title, formula_parts, condition)
        formula_group.generate_target()
        formula_group.target.shift(UP * 1.5)
        
        self.play(
            MoveToTarget(formula_group),
            FadeIn(axes_group)
        )
        
        # 添加乘法规则说明
        rules_text = Text("乘法规则：", font_size=36, color=BLUE_A)
        rules_text.to_edge(LEFT, buff=1.0)
        rules_text.shift(DOWN * 1.0)
        
        rule1 = MathTex(r"\mathbf{i}^2 = \mathbf{j}^2 = \mathbf{k}^2 = -1", 
                       font_size=32, color=WHITE)
        rule1.next_to(rules_text, DOWN, buff=0.3, aligned_edge=LEFT)
        
        rule2 = MathTex(r"\mathbf{ij} = \mathbf{k}, \quad \mathbf{jk} = \mathbf{i}, \quad \mathbf{ki} = \mathbf{j}", 
                       font_size=32, color=WHITE)
        rule2.next_to(rule1, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(rules_text))
        self.wait(0.5)
        self.play(Write(rule1))
        self.wait(0.5)
        self.play(Write(rule2))
        
        self.wait(self.get_duration(self.audios["i_j_k"]) - 4)
        
        # 清理图形和规则
        self.play(
            FadeOut(axes_group),
            FadeOut(rules_text),
            FadeOut(rule1),
            FadeOut(rule2)
        )
        
        # 5. 总结
        self.add_sound(self.audios["summary"])
        
        # 移动公式回中心
        formula_group.generate_target()
        formula_group.target.move_to(ORIGIN)
        
        self.play(MoveToTarget(formula_group))
        
        # 添加应用说明
        application = Text("应用：三维空间旋转", font_size=42, color=TEAL_A)
        application.next_to(formula_parts, DOWN, buff=1.0)
        
        example = Text("例如：3D游戏、机器人控制", font_size=36, color=GRAY_A)
        example.next_to(application, DOWN, buff=0.5)
        
        self.play(Write(application))
        self.wait(0.5)
        self.play(Write(example))
        
        # 最后突出显示整个公式
        surrounding_box = SurroundingRectangle(formula_parts, color=BLUE_A, buff=0.2)
        self.play(Create(surrounding_box))
        self.wait(1)
        
        self.wait(self.get_duration(self.audios["summary"]) - 2)
        
        # 淡出所有内容
        self.play(
            FadeOut(title),
            FadeOut(formula_group),
            FadeOut(application),
            FadeOut(example),
            FadeOut(surrounding_box)
        )
    
    def ensure_in_bounds(self, obj, max_w=12.0, max_h=7.0):
        if obj.get_width() > max_w: 
            obj.scale(max_w / obj.get_width())
        if obj.get_height() > max_h: 
            obj.scale(max_h / obj.get_height())