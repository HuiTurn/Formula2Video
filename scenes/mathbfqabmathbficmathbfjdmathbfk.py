import asyncio
import edge_tts
import os
from mutagen.mp3 import MP3
from manim import *

class Mathbfqabmathbficmathbfjdmathbfk(Scene):
    def __init__(self):
        super().__init__()
        self.audio_dir = "audios"
        os.makedirs(self.audio_dir, exist_ok=True)
        
        self.audios = {
            "intro": os.path.join(self.audio_dir, "intro.mp3"),
            "complex": os.path.join(self.audio_dir, "complex.mp3"),
            "quaternion": os.path.join(self.audio_dir, "quaternion.mp3"),
            "parts": os.path.join(self.audio_dir, "parts.mp3"),
            "example": os.path.join(self.audio_dir, "example.mp3"),
            "conclusion": os.path.join(self.audio_dir, "conclusion.mp3")
        }
        
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "intro": "大家好！今天我们来学习一个很酷的数学概念——四元数。听起来有点复杂，但其实很简单！",
            "complex": "首先，我们知道复数，比如3加4i，它有一个实部3和一个虚部4i。复数可以表示平面上的点。",
            "quaternion": "四元数就像是复数的升级版！它有一个实部和三个虚部，可以表示三维空间中的旋转。",
            "parts": "看这个公式：q等于a加bi加cj加dk。a是实部，就像普通数字。bi、cj、dk是三个虚部，就像三个不同方向的虚数单位。",
            "example": "想象一下，你有一个魔方。用四元数可以描述魔方如何旋转！实部a表示旋转了多少，三个虚部表示在x、y、z三个方向上怎么转。",
            "conclusion": "所以，四元数就是有四个部分的数：一个实部，三个虚部。它特别适合描述三维空间中的旋转。是不是很有趣？"
        }
        
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_audio_duration(self, filename):
        audio = MP3(filename)
        return audio.info.length
    
    def safe_layout(self, elements, max_per_row=4):
        """安全布局函数，防止元素拥挤"""
        if len(elements) == 0:
            return VGroup()
        
        # 分组排列
        groups = []
        for i in range(0, len(elements), max_per_row):
            group = VGroup(*elements[i:i+max_per_row])
            group.arrange(RIGHT, buff=0.5)
            groups.append(group)
        
        # 垂直排列各组
        layout = VGroup(*groups)
        if len(groups) > 1:
            layout.arrange(DOWN, buff=0.3)
        
        # 检查边界
        frame_width = config.frame_width
        frame_height = config.frame_height
        
        left_bound = layout.get_left()[0]
        right_bound = layout.get_right()[0]
        top_bound = layout.get_top()[1]
        bottom_bound = layout.get_bottom()[1]
        
        # 如果超出边界，自动缩放
        if (abs(left_bound) > frame_width/2 - 1 or 
            abs(right_bound) > frame_width/2 - 1 or
            abs(top_bound) > frame_height/2 - 1 or
            abs(bottom_bound) > frame_height/2 - 1):
            layout.scale(0.8)
        
        return layout
    
    def construct(self):
        # 第一步：介绍四元数
        title = Text("四元数", font_size=48, color=BLUE)
        subtitle = Text("三维空间的旋转魔法", font_size=32, color=YELLOW)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(title_group))
        self.wait(1)
        
        # 播放介绍音频
        self.add_sound(self.audios["intro"])
        audio_duration = self.get_audio_duration(self.audios["intro"])
        self.wait(audio_duration)
        
        self.play(FadeOut(title_group))
        self.wait(0.5)
        
        # 第二步：回顾复数概念
        complex_title = Text("先复习：复数", font_size=40, color=GREEN)
        complex_formula = MathTex(r"z = a + bi", font_size=48)
        complex_example = MathTex(r"3 + 4i", font_size=48, color=YELLOW)
        
        complex_group = VGroup(complex_title, complex_formula, complex_example)
        complex_group.arrange(DOWN, buff=0.4)
        
        # 添加复数图形表示
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).scale(0.4)
        
        point = Dot(plane.coords_to_point(3, 4), color=RED)
        point_label = MathTex(r"3+4i", font_size=24).next_to(point, UR, buff=0.1)
        
        complex_visual = VGroup(plane, point, point_label)
        complex_visual.next_to(complex_group, DOWN, buff=0.5)
        
        full_complex_group = VGroup(complex_group, complex_visual)
        
        self.play(FadeIn(complex_group))
        self.wait(1)
        self.play(Create(plane), run_time=2)
        self.play(FadeIn(point), Write(point_label))
        self.wait(1)
        
        # 播放复数音频
        self.add_sound(self.audios["complex"])
        audio_duration = self.get_audio_duration(self.audios["complex"])
        self.wait(audio_duration)
        
        self.play(FadeOut(full_complex_group))
        self.wait(0.5)
        
        # 第三步：引入四元数
        quat_title = Text("四元数：复数的升级版", font_size=40, color=BLUE)
        quat_formula = MathTex(r"\mathbf{q} = a + b\mathbf{i} + c\mathbf{j} + d\mathbf{k}", 
                              font_size=48)
        
        quat_group = VGroup(quat_title, quat_formula).arrange(DOWN, buff=0.4)
        
        # 添加三维坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": GRAY}
        ).scale(0.5)
        
        # 添加旋转箭头
        rotation_arrow = Arc(
            radius=1,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=8
        ).move_to(axes.coords_to_point(1, 0, 0))
        
        rotation_label = Text("旋转", font_size=24, color=YELLOW).next_to(rotation_arrow, RIGHT)
        
        quat_visual = VGroup(axes, rotation_arrow, rotation_label)
        quat_visual.next_to(quat_group, DOWN, buff=0.5)
        
        full_quat_group = VGroup(quat_group, quat_visual)
        
        self.play(FadeIn(quat_group))
        self.wait(1)
        self.play(Create(axes), run_time=2)
        self.play(Create(rotation_arrow), Write(rotation_label))
        self.wait(1)
        
        # 播放四元数音频
        self.add_sound(self.audios["quaternion"])
        audio_duration = self.get_audio_duration(self.audios["quaternion"])
        self.wait(audio_duration)
        
        self.play(FadeOut(full_quat_group))
        self.wait(0.5)
        
        # 第四步：详细解释各部分
        parts_title = Text("四元数的四个部分", font_size=40, color=PURPLE)
        
        # 创建公式各部分
        formula = MathTex(r"\mathbf{q} = ", r"a", r" + ", r"b\mathbf{i}", r" + ", r"c\mathbf{j}", r" + ", r"d\mathbf{k}", 
                         font_size=48)
        
        # 添加解释标签
        real_part_label = Text("实部（普通数字）", font_size=24, color=GREEN)
        i_part_label = Text("虚部i（x方向）", font_size=24, color=RED)
        j_part_label = Text("虚部j（y方向）", font_size=24, color=BLUE)
        k_part_label = Text("虚部k（z方向）", font_size=24, color=YELLOW)
        
        # 布局标签
        real_part_label.next_to(formula[1], DOWN, buff=0.3)
        i_part_label.next_to(formula[3], DOWN, buff=0.3)
        j_part_label.next_to(formula[5], DOWN, buff=0.3)
        k_part_label.next_to(formula[7], DOWN, buff=0.3)
        
        labels = VGroup(real_part_label, i_part_label, j_part_label, k_part_label)
        
        # 添加颜色高亮
        formula[1].set_color(GREEN)  # a
        formula[3].set_color(RED)    # bi
        formula[5].set_color(BLUE)   # cj
        formula[7].set_color(YELLOW) # dk
        
        parts_group = VGroup(parts_title, formula, labels)
        parts_group.arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(parts_title))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 逐步显示标签
        self.play(FadeIn(real_part_label))
        self.wait(0.5)
        self.play(FadeIn(i_part_label))
        self.wait(0.5)
        self.play(FadeIn(j_part_label))
        self.wait(0.5)
        self.play(FadeIn(k_part_label))
        self.wait(1)
        
        # 播放各部分音频
        self.add_sound(self.audios["parts"])
        audio_duration = self.get_audio_duration(self.audios["parts"])
        self.wait(audio_duration)
        
        self.play(FadeOut(parts_group))
        self.wait(0.5)
        
        # 第五步：生活化例子
        example_title = Text("生活中的例子：魔方旋转", font_size=40, color=ORANGE)
        
        # 创建魔方示意图
        cube = Cube(side_length=1.5, fill_opacity=0.2, stroke_width=2)
        
        # 添加旋转动画
        rotation_animation = Rotating(
            cube,
            radians=PI/2,
            axis=UP + RIGHT,
            run_time=3,
            rate_func=linear
        )
        
        # 添加坐标轴
        example_axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": GRAY, "stroke_width": 1}
        ).scale(0.4)
        
        # 添加标签
        x_label = Text("x轴", font_size=20, color=RED).next_to(example_axes.coords_to_point(2, 0, 0), RIGHT)
        y_label = Text("y轴", font_size=20, color=GREEN).next_to(example_axes.coords_to_point(0, 2, 0), UP)
        z_label = Text("z轴", font_size=20, color=BLUE).next_to(example_axes.coords_to_point(0, 0, 2), OUT)
        
        axes_group = VGroup(example_axes, x_label, y_label, z_label)
        axes_group.next_to(cube, DOWN, buff=0.5)
        
        example_group = VGroup(example_title, cube, axes_group)
        example_group.arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(example_title))
        self.wait(0.5)
        self.play(FadeIn(cube))
        self.wait(0.5)
        self.play(FadeIn(axes_group))
        self.wait(1)
        
        # 播放旋转动画
        self.play(rotation_animation)
        self.wait(1)
        
        # 添加四元数表示
        quat_example = MathTex(r"\mathbf{q} = \cos\frac{\theta}{2} + \sin\frac{\theta}{2}(i + j + k)", 
                              font_size=36, color=YELLOW)
        quat_example.next_to(axes_group, DOWN, buff=0.3)
        
        self.play(Write(quat_example))
        self.wait(1)
        
        # 播放例子音频
        self.add_sound(self.audios["example"])
        audio_duration = self.get_audio_duration(self.audios["example"])
        self.wait(audio_duration)
        
        self.play(FadeOut(example_group), FadeOut(quat_example))
        self.wait(0.5)
        
        # 第六步：总结
        conclusion_title = Text("总结：四元数是什么？", font_size=40, color=GREEN)
        
        # 创建要点列表
        point1 = Text("1. 有四个部分的数", font_size=32)
        point2 = Text("2. 一个实部 + 三个虚部", font_size=32)
        point3 = Text("3. 特别适合描述三维旋转", font_size=32)
        point4 = Text("4. 在游戏、动画、机器人中广泛应用", font_size=32)
        
        points = VGroup(point1, point2, point3, point4)
        points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        # 添加最后的公式
        final_formula = MathTex(r"\mathbf{q} = a + b\mathbf{i} + c\mathbf{j} + d\mathbf{k}", 
                               font_size=48, color=BLUE)
        
        conclusion_group = VGroup(conclusion_title, points, final_formula)
        conclusion_group.arrange(DOWN, buff=0.5)
        
        self.play(FadeIn(conclusion_title))
        self.wait(0.5)
        
        # 逐步显示要点
        self.play(FadeIn(point1))
        self.wait(0.5)
        self.play(FadeIn(point2))
        self.wait(0.5)
        self.play(FadeIn(point3))
        self.wait(0.5)
        self.play(FadeIn(point4))
        self.wait(1)
        
        self.play(Write(final_formula))
        self.wait(1)
        
        # 播放总结音频
        self.add_sound(self.audios["conclusion"])
        audio_duration = self.get_audio_duration(self.audios["conclusion"])
        self.wait(audio_duration)
        
        # 淡出结束
        self.play(FadeOut(conclusion_group))
        self.wait(1)