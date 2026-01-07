import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class Qabicjdk(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "complex": "audios/complex.mp3",
            "quaternion": "audios/quaternion.mp3",
            "units": "audios/units.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "同学们好！今天我们来认识一个有趣的数学概念：四元数。",
            "complex": "首先，回忆一下我们学过的复数。复数就像平面上的一个点，比如 a + bi，其中 a 是实数部分，b 是虚数部分，i 是虚数单位，满足 i² = -1。",
            "quaternion": "四元数可以看作是复数的升级版。它不再局限于平面，而是可以描述三维空间中的旋转。它的标准形式是 q = a + bi + cj + dk。",
            "units": "这里的 i, j, k 是三个不同的虚数单位。它们和 i 一样，平方都等于 -1。但它们之间相乘的规则很特别，比如 i × j = k， j × k = i， k × i = j。",
            "example": "我们可以把四元数想象成一个超级版的复数。a 是实部，就像你现在的楼层。bi, cj, dk 是三个虚部，分别代表你在楼里向东、向北、向上走了多少步。合起来就能精确定位你在三维楼宇中的位置和朝向。",
            "summary": "总结一下：四元数 q = a + bi + cj + dk，包含一个实部和三个虚部。它在计算机图形学、机器人学中非常有用，可以漂亮地处理3D旋转。是不是很神奇？"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def safe_layout(self, elements, max_per_row=4, h_spacing=0.8, v_spacing=0.6):
        group = VGroup(*elements)
        if len(elements) > max_per_row:
            rows = []
            for i in range(0, len(elements), max_per_row):
                row_group = VGroup(*elements[i:i+max_per_row]).arrange(RIGHT, buff=h_spacing)
                rows.append(row_group)
            group = VGroup(*rows).arrange(DOWN, buff=v_spacing)
        else:
            group.arrange(RIGHT, buff=h_spacing)
        
        frame_width = config.frame_width - 1
        frame_height = config.frame_height - 1
        if group.get_width() > frame_width or group.get_height() > frame_height:
            group.scale_to_fit_width(frame_width * 0.9)
            if group.get_height() > frame_height * 0.9:
                group.scale_to_fit_height(frame_height * 0.9)
        
        return group
    
    def construct(self):
        # 步骤1：引入标题和公式
        title = Text("四元数", font_size=48, color=BLUE).to_edge(UP)
        formula_latex = MathTex(r"q = a + bi + cj + dk", font_size=40, color=WHITE)
        formula_latex.next_to(title, DOWN, buff=0.5)
        
        self.add_sound(self.audios["intro"])
        self.play(FadeIn(title), FadeIn(formula_latex))
        self.wait(2)
        
        # 步骤2：回顾复数（作为基础）
        self.play(FadeOut(title), FadeOut(formula_latex))
        self.wait(0.5)
        
        complex_title = Text("我们先从复数说起", font_size=36, color=YELLOW).to_edge(UP)
        complex_formula = MathTex(r"z = a + bi", font_size=40, color=GREEN)
        complex_formula.next_to(complex_title, DOWN, buff=0.4)
        
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).scale(0.8)
        plane.next_to(complex_formula, DOWN, buff=0.5)
        
        dot = Dot(plane.coords_to_point(2, 1), color=RED)
        dot_label = MathTex(r"(a, b)", font_size=28, color=RED).next_to(dot, UR, buff=0.1)
        
        self.add_sound(self.audios["complex"])
        self.play(FadeIn(complex_title), FadeIn(complex_formula))
        self.wait(1)
        self.play(Create(plane))
        self.wait(1)
        self.play(FadeIn(dot), Write(dot_label))
        self.wait(2)
        
        # 步骤3：引入四元数公式
        self.play(FadeOut(complex_title), FadeOut(complex_formula), FadeOut(plane), FadeOut(dot), FadeOut(dot_label))
        self.wait(0.5)
        
        quat_title = Text("四元数：复数的升级版", font_size=36, color=BLUE).to_edge(UP)
        quat_formula = MathTex(r"q = a + bi + cj + dk", font_size=40, color=MAROON)
        quat_formula.next_to(quat_title, DOWN, buff=0.4)
        
        self.add_sound(self.audios["quaternion"])
        self.play(FadeIn(quat_title), FadeIn(quat_formula))
        self.wait(3)
        
        # 步骤4：解释虚数单位 i, j, k
        units_title = Text("三个特别的虚数单位", font_size=32, color=ORANGE)
        units_title.next_to(quat_formula, DOWN, buff=0.6)
        
        i_eq = MathTex(r"i^2 = -1", font_size=32, color=PINK)
        j_eq = MathTex(r"j^2 = -1", font_size=32, color=PINK)
        k_eq = MathTex(r"k^2 = -1", font_size=32, color=PINK)
        
        mult_eq1 = MathTex(r"i \times j = k", font_size=32, color=LIGHT_BROWN)
        mult_eq2 = MathTex(r"j \times k = i", font_size=32, color=LIGHT_BROWN)
        mult_eq3 = MathTex(r"k \times i = j", font_size=32, color=LIGHT_BROWN)
        
        units_group = self.safe_layout([i_eq, j_eq, k_eq], max_per_row=3, h_spacing=1.2)
        units_group.next_to(units_title, DOWN, buff=0.4)
        
        mult_group = self.safe_layout([mult_eq1, mult_eq2, mult_eq3], max_per_row=3, h_spacing=1.2)
        mult_group.next_to(units_group, DOWN, buff=0.4)
        
        self.add_sound(self.audios["units"])
        self.play(FadeIn(units_title))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(eq) for eq in [i_eq, j_eq, k_eq]], lag_ratio=0.3))
        self.wait(1.5)
        self.play(LaggedStart(*[FadeIn(eq) for eq in [mult_eq1, mult_eq2, mult_eq3]], lag_ratio=0.3))
        self.wait(3)
        
        # 步骤5：生活化例子（三维楼宇）
        self.play(FadeOut(quat_title), FadeOut(quat_formula), FadeOut(units_title), FadeOut(units_group), FadeOut(mult_group))
        self.wait(0.5)
        
        example_title = Text("一个生活化的比喻", font_size=36, color=GREEN).to_edge(UP)
        
        building = VGroup(
            Rectangle(height=3, width=2, color=BLUE, fill_opacity=0.1),
            Line(ORIGIN, UP*0.5, color=BLUE).next_to(Rectangle(height=3, width=2), UP, buff=0)
        )
        building_label = Text("三维楼宇", font_size=24, color=BLUE).next_to(building, DOWN, buff=0.2)
        
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-1, 3, 1])
        axes.scale(0.6)
        
        components = VGroup(
            Text("a: 楼层", font_size=24, color=RED),
            Text("bi: 向东步数", font_size=24, color=YELLOW),
            Text("cj: 向北步数", font_size=24, color=PURPLE),
            Text("dk: 向上步数", font_size=24, color=TEAL)
        )
        components.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        layout_group = self.safe_layout([building, axes, components], max_per_row=3, h_spacing=1.5)
        layout_group.next_to(example_title, DOWN, buff=0.6)
        
        self.add_sound(self.audios["example"])
        self.play(FadeIn(example_title))
        self.wait(0.5)
        self.play(FadeIn(building), Write(building_label))
        self.wait(1)
        self.play(Create(axes))
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(comp) for comp in components], lag_ratio=0.3))
        self.wait(3)
        
        # 步骤6：总结
        self.play(FadeOut(example_title), FadeOut(layout_group), FadeOut(building_label))
        self.wait(0.5)
        
        summary_title = Text("总结回顾", font_size=40, color=GOLD).to_edge(UP)
        final_formula = MathTex(r"q = a + bi + cj + dk", font_size=44, color=MAROON)
        final_formula.next_to(summary_title, DOWN, buff=0.5)
        
        key_points = VGroup(
            Text("• 一个实部 a", font_size=28, color=WHITE),
            Text("• 三个虚部 bi, cj, dk", font_size=28, color=WHITE),
            Text("• 用于3D旋转和定位", font_size=28, color=WHITE),
            Text("• 游戏和机器人中常用", font_size=28, color=WHITE)
        )
        key_points.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        key_points.next_to(final_formula, DOWN, buff=0.8)
        
        self.add_sound(self.audios["summary"])
        self.play(FadeIn(summary_title))
        self.wait(0.5)
        self.play(Write(final_formula))
        self.wait(1)
        self.play(LaggedStart(*[FadeIn(point) for point in key_points], lag_ratio=0.4))
        self.wait(3)
        
        # 淡出结束
        self.play(FadeOut(summary_title), FadeOut(final_formula), FadeOut(key_points))
        self.wait(1)