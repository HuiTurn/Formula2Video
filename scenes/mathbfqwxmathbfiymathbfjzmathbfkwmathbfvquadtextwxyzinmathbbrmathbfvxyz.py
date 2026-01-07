import asyncio
import edge_tts
import os
from mutagen.mp3 import MP3
from manim import *

# 创建音频目录
if not os.path.exists("audios"):
    os.makedirs("audios")

class QuaternionForBeginners(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "intro": "audios/intro.mp3",
            "complex": "audios/complex.mp3", 
            "quaternion": "audios/quaternion.mp3",
            "vector": "audios/vector.mp3",
            "example": "audios/example.mp3",
            "summary": "audios/summary.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        """生成所有音频文件"""
        texts = {
            "intro": "大家好！今天我们来学习一个有趣的数学概念：四元数。",
            "complex": "首先，回忆一下复数。复数有实部和虚部，比如3加4i。",
            "quaternion": "四元数是复数的扩展，它有四个部分：一个实部和三个虚部。",
            "vector": "这三个虚部可以看作一个三维向量，就像空间中的一个箭头。",
            "example": "想象一下，用四元数可以描述三维旋转，就像游戏中的角色转动。",
            "summary": "总结一下：四元数是一个实部加一个三维向量，用于三维旋转。"
        }
        
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        """生成单个音频文件"""
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def safe_layout(self, elements, max_per_row=4, spacing=0.5):
        """安全布局函数，防止元素拥挤和超出边界"""
        group = VGroup(*elements)
        
        # 如果元素太多，分行排列
        if len(elements) > max_per_row:
            rows = []
            for i in range(0, len(elements), max_per_row):
                row = VGroup(*elements[i:i+max_per_row]).arrange(RIGHT, buff=spacing)
                rows.append(row)
            group = VGroup(*rows).arrange(DOWN, buff=spacing*0.8)
        else:
            group.arrange(RIGHT, buff=spacing)
        
        # 检查边界
        frame_width = config.frame_width - 1
        frame_height = config.frame_height - 1
        
        # 获取组的边界
        left = group.get_left()[0]
        right = group.get_right()[0]
        top = group.get_top()[1]
        bottom = group.get_bottom()[1]
        
        # 如果超出边界，缩放调整
        if abs(left) > frame_width/2 or abs(right) > frame_width/2 or \
           abs(top) > frame_height/2 or abs(bottom) > frame_height/2:
            scale_factor = 0.8
            group.scale(scale_factor)
        
        return group
    
    def construct(self):
        # 第一步：介绍四元数概念
        self.play_audio("intro")
        title = Text("四元数是什么？", font_size=48, color=BLUE)
        title.to_edge(UP)
        
        self.play(FadeIn(title))
        self.wait(1)
        
        # 第二步：从复数开始讲解
        self.play_audio("complex")
        complex_text = Text("从复数开始", font_size=36, color=YELLOW)
        complex_text.next_to(title, DOWN, buff=0.5)
        
        complex_formula = MathTex(r"z = a + bi", font_size=40)
        complex_formula.next_to(complex_text, DOWN, buff=0.3)
        
        # 用颜色区分实部和虚部
        complex_formula.set_color_by_tex("a", GREEN)
        complex_formula.set_color_by_tex("bi", RED)
        
        self.play(FadeIn(complex_text))
        self.wait(0.5)
        self.play(Write(complex_formula))
        self.wait(2)
        
        # 第三步：引入四元数
        self.play_audio("quaternion")
        quaternion_text = Text("四元数：复数的扩展", font_size=36, color=YELLOW)
        quaternion_text.move_to(complex_text)
        
        quaternion_formula = MathTex(r"\mathbf{q} = w + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}", font_size=40)
        quaternion_formula.next_to(quaternion_text, DOWN, buff=0.3)
        
        # 用不同颜色标记各部分
        quaternion_formula.set_color_by_tex("w", GREEN)
        quaternion_formula.set_color_by_tex("x", RED)
        quaternion_formula.set_color_by_tex("y", BLUE)
        quaternion_formula.set_color_by_tex("z", PURPLE)
        
        self.play(
            FadeOut(complex_text),
            FadeOut(complex_formula),
            FadeIn(quaternion_text)
        )
        self.wait(0.5)
        self.play(Write(quaternion_formula))
        self.wait(2)
        
        # 第四步：展示向量表示
        self.play_audio("vector")
        vector_text = Text("向量表示法", font_size=36, color=YELLOW)
        vector_text.move_to(quaternion_text)
        
        vector_formula = MathTex(r"\mathbf{q} = (w, \mathbf{v})", font_size=40)
        vector_formula.next_to(vector_text, DOWN, buff=0.3)
        
        where_formula = MathTex(r"\text{其中 } \mathbf{v} = (x, y, z)", font_size=36)
        where_formula.next_to(vector_formula, DOWN, buff=0.2)
        
        vector_formula.set_color_by_tex("w", GREEN)
        vector_formula.set_color_by_tex(r"\mathbf{v}", ORANGE)
        where_formula.set_color_by_tex(r"\mathbf{v}", ORANGE)
        
        self.play(
            FadeOut(quaternion_text),
            FadeOut(quaternion_formula),
            FadeIn(vector_text)
        )
        self.wait(0.5)
        self.play(Write(vector_formula))
        self.wait(1)
        self.play(Write(where_formula))
        self.wait(2)
        
        # 第五步：生活化例子
        self.play_audio("example")
        example_text = Text("生活中的例子：三维旋转", font_size=36, color=YELLOW)
        example_text.move_to(vector_text)
        
        # 创建一个简单的三维坐标系
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            z_length=4
        )
        axes.scale(0.6)
        axes.next_to(example_text, DOWN, buff=0.5)
        
        # 创建一个箭头表示向量
        arrow = Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array([1, 1, 0.5]),
            color=ORANGE,
            thickness=0.02
        )
        arrow.next_to(axes, DOWN, buff=0.3)
        
        rotation_text = Text("四元数可以描述这个箭头的旋转", font_size=28, color=WHITE)
        rotation_text.next_to(arrow, DOWN, buff=0.2)
        
        self.play(
            FadeOut(vector_text),
            FadeOut(vector_formula),
            FadeOut(where_formula),
            FadeIn(example_text)
        )
        self.wait(0.5)
        self.play(Create(axes))
        self.wait(1)
        self.play(GrowArrow(arrow))
        self.wait(1)
        self.play(Write(rotation_text))
        
        # 简单旋转动画
        self.play(
            Rotate(arrow, angle=PI/2, axis=UP, run_time=2)
        )
        self.wait(2)
        
        # 第六步：总结
        self.play_audio("summary")
        summary_text = Text("总结", font_size=36, color=YELLOW)
        summary_text.move_to(example_text)
        
        summary_points = VGroup(
            Text("1. 四元数有四个部分：w, x, y, z", font_size=28),
            Text("2. 可以写成：q = w + xi + yj + zk", font_size=28),
            Text("3. 也可以写成：q = (w, v)，v是三维向量", font_size=28),
            Text("4. 常用于三维旋转，如游戏开发", font_size=28)
        )
        
        summary_points.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary_points.scale(0.8)
        summary_points.next_to(summary_text, DOWN, buff=0.5)
        
        self.play(
            FadeOut(example_text),
            FadeOut(axes),
            FadeOut(arrow),
            FadeOut(rotation_text),
            FadeIn(summary_text)
        )
        self.wait(0.5)
        
        # 逐条显示总结点
        for point in summary_points:
            self.play(FadeIn(point))
            self.wait(1)
        
        self.wait(2)
        
        # 淡出所有内容
        self.play(
            FadeOut(title),
            FadeOut(summary_text),
            FadeOut(summary_points)
        )
    
    def play_audio(self, audio_key):
        """播放音频并等待结束"""
        audio_file = self.audios[audio_key]
        
        # 获取音频时长
        try:
            audio = MP3(audio_file)
            duration = audio.info.length
        except:
            duration = 2  # 默认2秒
        
        # 添加音频到场景
        self.add_sound(audio_file)
        
        # 等待音频播放完毕
        self.wait(duration + 0.5)  # 额外等待0.5秒

# 运行场景
if __name__ == "__main__":
    scene = QuaternionForBeginners()
    scene.render()