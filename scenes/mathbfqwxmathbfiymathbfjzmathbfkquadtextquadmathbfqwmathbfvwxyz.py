from manim import *
from pathlib import Path
import edge_tts
import asyncio
import subprocess
import os

class Mathbfqwxmathbfiymathbfjzmathbfkquadtextquadmathbfqwmathbfvwxyz(Scene):
    def construct(self):
        # 音频文件路径
        audio_files = []
        temp_dir = Path("temp_audio")
        temp_dir.mkdir(exist_ok=True)
        
        # 1. 引入概念：从熟悉的复数开始
        title = Text("什么是四元数？", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        
        # 生成音频1
        audio1 = self.generate_audio("同学们好！今天我们来学习一个有趣的数学概念：四元数。", "audio1.mp3")
        self.add_sound(audio1)
        self.wait(2)
        
        self.play(FadeOut(title))
        
        # 2. 从复数扩展到四元数
        complex_text = Text("我们先回忆一下复数：", font_size=36, color=YELLOW)
        complex_formula = MathTex("z = a + bi", font_size=40)
        complex_group = VGroup(complex_text, complex_formula).arrange(DOWN, buff=0.5)
        complex_group.to_edge(UP)
        
        self.play(Write(complex_text))
        self.wait(0.5)
        self.play(Write(complex_formula))
        self.wait(1)
        
        # 生成音频2
        audio2 = self.generate_audio("复数有一个实部a和一个虚部b，用i表示虚数单位。", "audio2.mp3")
        self.add_sound(audio2)
        self.wait(2)
        
        # 3. 展示四元数公式
        quat_text = Text("四元数就像复数的升级版：", font_size=36, color=GREEN)
        quat_formula1 = MathTex(r"\mathbf{q} = w + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}", font_size=40)
        quat_formula2 = MathTex(r"\mathbf{q} = (w, \mathbf{v}) = (w, x, y, z)", font_size=40)
        
        quat_group = VGroup(quat_text, quat_formula1, quat_formula2).arrange(DOWN, buff=0.5)
        quat_group.next_to(complex_group, DOWN, buff=1)
        
        self.play(Write(quat_text))
        self.wait(0.5)
        self.play(Write(quat_formula1))
        self.wait(1)
        
        # 生成音频3
        audio3 = self.generate_audio("四元数有一个实部w和三个虚部x、y、z，分别对应三个虚数单位i、j、k。", "audio3.mp3")
        self.add_sound(audio3)
        self.wait(2)
        
        self.play(Write(quat_formula2))
        self.wait(1)
        
        # 生成音频4
        audio4 = self.generate_audio("也可以写成(w, v)的形式，其中v是一个三维向量(x, y, z)。", "audio4.mp3")
        self.add_sound(audio4)
        self.wait(2)
        
        # 4. 用生活化的类比解释
        analogy_text = Text("想象一下：", font_size=36, color=ORANGE)
        analogy1 = Text("复数就像2D平面上的一个点", font_size=32, color=WHITE)
        analogy2 = Text("四元数就像3D空间中的一个点加上旋转", font_size=32, color=WHITE)
        
        analogy_group = VGroup(analogy_text, analogy1, analogy2).arrange(DOWN, buff=0.5)
        analogy_group.next_to(quat_group, DOWN, buff=1)
        
        self.play(FadeOut(complex_group))
        self.play(Write(analogy_text))
        self.wait(0.5)
        self.play(Write(analogy1))
        self.wait(1)
        
        # 生成音频5
        audio5 = self.generate_audio("复数可以表示平面上的位置，就像地图上的坐标。", "audio5.mp3")
        self.add_sound(audio5)
        self.wait(2)
        
        self.play(Write(analogy2))
        self.wait(1)
        
        # 生成音频6
        audio6 = self.generate_audio("四元数可以表示空间中的位置和方向，就像游戏角色的位置和朝向。", "audio6.mp3")
        self.add_sound(audio6)
        self.wait(2)
        
        # 5. 突出各部分含义
        highlight_text = Text("各部分含义：", font_size=36, color=PINK)
        w_part = Text("w：实部，表示大小或缩放", font_size=28, color=RED)
        x_part = Text("x：i分量，控制绕x轴旋转", font_size=28, color=GREEN)
        y_part = Text("y：j分量，控制绕y轴旋转", font_size=28, color=BLUE)
        z_part = Text("z：k分量，控制绕z轴旋转", font_size=28, color=YELLOW)
        
        parts_group = VGroup(highlight_text, w_part, x_part, y_part, z_part).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        parts_group.next_to(analogy_group, DOWN, buff=0.8)
        
        self.play(FadeOut(quat_group))
        self.play(Write(highlight_text))
        self.wait(0.5)
        
        for part in [w_part, x_part, y_part, z_part]:
            self.play(Write(part))
            self.wait(0.5)
        
        # 生成音频7
        audio7 = self.generate_audio("实部w就像物体的尺寸，虚部x、y、z分别控制物体绕x、y、z轴的旋转。", "audio7.mp3")
        self.add_sound(audio7)
        self.wait(3)
        
        # 6. 总结应用
        summary_text = Text("四元数的应用：", font_size=36, color=TEAL)
        app1 = Text("• 3D游戏中的角色旋转", font_size=28, color=WHITE)
        app2 = Text("• 机器人手臂的运动控制", font_size=28, color=WHITE)
        app3 = Text("• 手机陀螺仪的方向检测", font_size=28, color=WHITE)
        
        summary_group = VGroup(summary_text, app1, app2, app3).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_group.next_to(parts_group, DOWN, buff=0.8)
        
        self.play(FadeOut(analogy_group))
        self.play(Write(summary_text))
        self.wait(0.5)
        
        for app in [app1, app2, app3]:
            self.play(Write(app))
            self.wait(0.5)
        
        # 生成音频8
        audio8 = self.generate_audio("四元数在3D游戏、机器人控制和手机导航中都有广泛应用。", "audio8.mp3")
        self.add_sound(audio8)
        self.wait(3)
        
        # 7. 最终总结
        final_text = Text("记住：四元数 = 1个实部 + 3个虚部", font_size=40, color=GOLD)
        final_text.move_to(ORIGIN)
        
        self.play(FadeOut(parts_group), FadeOut(summary_group))
        self.play(Write(final_text))
        self.wait(1)
        
        # 生成音频9
        audio9 = self.generate_audio("简单来说，四元数就是由一个实部和三个虚部组成的数学对象，专门用来处理三维空间中的旋转问题。", "audio9.mp3")
        self.add_sound(audio9)
        self.wait(3)
        
        # 清理临时音频文件
        self.cleanup_audio(audio_files)
        
    def generate_audio(self, text: str, filename: str) -> str:
        """生成音频文件并返回路径"""
        async def _generate():
            voice = "zh-CN-XiaoxiaoNeural"
            output_path = Path("temp_audio") / filename
            tts = edge_tts.Communicate(text, voice)
            await tts.save(str(output_path))
            return str(output_path)
        
        # 同步运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_path = loop.run_until_complete(_generate())
        loop.close()
        
        return audio_path
    
    def cleanup_audio(self, audio_files):
        """清理临时音频文件"""
        temp_dir = Path("temp_audio")
        if temp_dir.exists():
            for file in temp_dir.glob("*.mp3"):
                try:
                    file.unlink()
                except:
                    pass
            try:
                temp_dir.rmdir()
            except:
                pass

# 运行脚本
if __name__ == "__main__":
    scene = Mathbfqwxmathbfiymathbfjzmathbfkquadtextquadmathbfqwmathbfvwxyz()
    scene.render()