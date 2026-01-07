from manim import *
from pathlib import Path
import edge_tts
import asyncio
import subprocess
import os

class QabmathbficmathbfjdmathbfkabcdinmathbbRmathbfi2mathbfj2mathbfk2mathbfimathbfjmathbfk1(Scene):
    def construct(self):
        # 音频文件路径
        audio_files = []
        
        # 第一部分：介绍四元数概念
        title = Text("四元数是什么？", font_size=48, color=BLUE)
        title.to_edge(UP)
        
        # 生成音频1
        audio_text1 = "同学们好！今天我们来学习一个有趣的数学概念：四元数。"
        audio_file1 = self.generate_audio(audio_text1, "part1")
        audio_files.append(audio_file1)
        
        self.play(FadeIn(title))
        self.wait(0.5)
        
        # 播放音频1
        self.add_sound(audio_file1)
        self.wait(len(audio_text1)/15 + 1)
        
        # 清理标题
        self.play(FadeOut(title))
        self.wait(0.5)
        
        # 第二部分：从复数到四元数
        subtitle = Text("从复数到四元数", font_size=40, color=GREEN)
        subtitle.to_edge(UP)
        
        # 生成音频2
        audio_text2 = "我们知道复数有一个实部和一个虚部，比如a加bi。"
        audio_file2 = self.generate_audio(audio_text2, "part2")
        audio_files.append(audio_file2)
        
        self.play(FadeIn(subtitle))
        self.wait(0.5)
        
        # 显示复数公式
        complex_formula = MathTex("z = a + b", "i", font_size=36)
        complex_formula.next_to(subtitle, DOWN, buff=0.8)
        
        # 生成音频3
        audio_text3 = "四元数就像是复数的升级版，它有一个实部和三个虚部。"
        audio_file3 = self.generate_audio(audio_text3, "part3")
        audio_files.append(audio_file3)
        
        self.play(Write(complex_formula))
        self.wait(0.5)
        
        self.add_sound(audio_file2)
        self.wait(len(audio_text2)/15 + 1)
        
        self.add_sound(audio_file3)
        self.wait(len(audio_text3)/15 + 1)
        
        # 清理复数公式
        self.play(FadeOut(complex_formula))
        self.wait(0.5)
        
        # 第三部分：显示四元数公式
        quaternion_formula = MathTex(
            "q = a + b", "\\mathbf{i}", " + c", "\\mathbf{j}", " + d", "\\mathbf{k}",
            font_size=36
        )
        quaternion_formula.next_to(subtitle, DOWN, buff=0.8)
        
        # 生成音频4
        audio_text4 = "看，这就是四元数的公式：q等于a加b乘以i，加c乘以j，再加d乘以k。"
        audio_file4 = self.generate_audio(audio_text4, "part4")
        audio_files.append(audio_file4)
        
        self.play(Write(quaternion_formula))
        self.wait(0.5)
        
        self.add_sound(audio_file4)
        self.wait(len(audio_text4)/15 + 1)
        
        # 高亮显示各个部分
        real_part = quaternion_formula[0:2]  # a
        i_part = quaternion_formula[2:4]     # b\mathbf{i}
        j_part = quaternion_formula[4:6]     # c\mathbf{j}
        k_part = quaternion_formula[6:]      # d\mathbf{k}
        
        # 生成音频5
        audio_text5 = "其中a是实部，b、c、d是三个虚部的系数，i、j、k是三个不同的虚数单位。"
        audio_file5 = self.generate_audio(audio_text5, "part5")
        audio_files.append(audio_file5)
        
        self.play(
            real_part.animate.set_color(YELLOW),
            i_part.animate.set_color(RED),
            j_part.animate.set_color(GREEN),
            k_part.animate.set_color(BLUE)
        )
        self.wait(0.5)
        
        self.add_sound(audio_file5)
        self.wait(len(audio_text5)/15 + 1)
        
        # 清理高亮
        self.play(
            real_part.animate.set_color(WHITE),
            i_part.animate.set_color(WHITE),
            j_part.animate.set_color(WHITE),
            k_part.animate.set_color(WHITE)
        )
        self.wait(0.5)
        
        # 第四部分：显示实数条件
        condition = MathTex("a, b, c, d \\in \\mathbb{R}", font_size=32)
        condition.next_to(quaternion_formula, DOWN, buff=0.5)
        
        # 生成音频6
        audio_text6 = "注意，a、b、c、d都是实数。"
        audio_file6 = self.generate_audio(audio_text6, "part6")
        audio_files.append(audio_file6)
        
        self.play(Write(condition))
        self.wait(0.5)
        
        self.add_sound(audio_file6)
        self.wait(len(audio_text6)/15 + 1)
        
        # 清理条件
        self.play(FadeOut(condition))
        self.wait(0.5)
        
        # 第五部分：虚数单位的性质
        properties_title = Text("虚数单位的性质", font_size=36, color=ORANGE)
        properties_title.next_to(quaternion_formula, DOWN, buff=0.8)
        
        # 生成音频7
        audio_text7 = "这三个虚数单位有一些特殊的性质。"
        audio_file7 = self.generate_audio(audio_text7, "part7")
        audio_files.append(audio_file7)
        
        self.play(FadeIn(properties_title))
        self.wait(0.5)
        
        self.add_sound(audio_file7)
        self.wait(len(audio_text7)/15 + 1)
        
        # 显示性质公式
        properties = VGroup(
            MathTex("\\mathbf{i}^2 = -1", font_size=32),
            MathTex("\\mathbf{j}^2 = -1", font_size=32),
            MathTex("\\mathbf{k}^2 = -1", font_size=32),
            MathTex("\\mathbf{i}\\mathbf{j}\\mathbf{k} = -1", font_size=32)
        )
        
        properties.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        properties.next_to(properties_title, DOWN, buff=0.5)
        
        # 生成音频8
        audio_text8 = "它们平方都等于负一，而且i、j、k相乘也等于负一。"
        audio_file8 = self.generate_audio(audio_text8, "part8")
        audio_files.append(audio_file8)
        
        for prop in properties:
            self.play(Write(prop))
            self.wait(0.3)
        
        self.wait(0.5)
        
        self.add_sound(audio_file8)
        self.wait(len(audio_text8)/15 + 1)
        
        # 第六部分：应用举例
        # 清理性质部分
        self.play(
            FadeOut(properties_title),
            FadeOut(properties),
            FadeOut(subtitle)
        )
        self.wait(0.5)
        
        application = Text("四元数有什么用？", font_size=40, color=PURPLE)
        application.to_edge(UP)
        
        # 生成音频9
        audio_text9 = "那么四元数有什么用呢？它主要用来表示三维空间中的旋转。"
        audio_file9 = self.generate_audio(audio_text9, "part9")
        audio_files.append(audio_file9)
        
        self.play(FadeIn(application))
        self.wait(0.5)
        
        self.add_sound(audio_file9)
        self.wait(len(audio_text9)/15 + 1)
        
        # 显示旋转应用
        example_text = Text("比如：3D游戏、机器人控制、航天导航", font_size=28, color=YELLOW)
        example_text.next_to(application, DOWN, buff=0.8)
        
        # 生成音频10
        audio_text10 = "比如在3D游戏、机器人控制和航天导航中，都会用到四元数来计算旋转。"
        audio_file10 = self.generate_audio(audio_text10, "part10")
        audio_files.append(audio_file10)
        
        self.play(Write(example_text))
        self.wait(0.5)
        
        self.add_sound(audio_file10)
        self.wait(len(audio_text10)/15 + 1)
        
        # 第七部分：总结
        # 清理应用部分
        self.play(
            FadeOut(application),
            FadeOut(example_text),
            FadeOut(quaternion_formula)
        )
        self.wait(0.5)
        
        summary = Text("总结一下：", font_size=36, color=BLUE)
        summary.to_edge(UP)
        
        # 生成音频11
        audio_text11 = "总结一下：四元数是复数的扩展，有一个实部和三个虚部，用来表示三维旋转。"
        audio_file11 = self.generate_audio(audio_text11, "part11")
        audio_files.append(audio_file11)
        
        self.play(FadeIn(summary))
        self.wait(0.5)
        
        summary_points = VGroup(
            Text("1. 四元数：q = a + bi + cj + dk", font_size=28),
            Text("2. a,b,c,d是实数", font_size=28),
            Text("3. i²=j²=k²=ijk=-1", font_size=28),
            Text("4. 用于3D旋转计算", font_size=28)
        )
        
        summary_points.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        summary_points.next_to(summary, DOWN, buff=0.8)
        
        for point in summary_points:
            self.play(FadeIn(point))
            self.wait(0.3)
        
        self.wait(0.5)
        
        self.add_sound(audio_file11)
        self.wait(len(audio_text11)/15 + 1)
        
        # 结束语
        ending = Text("你学会了吗？", font_size=40, color=GREEN)
        
        # 生成音频12
        audio_text12 = "你学会了吗？四元数其实并不难，记住它的公式和用途就可以了。"
        audio_file12 = self.generate_audio(audio_text12, "part12")
        audio_files.append(audio_file12)
        
        self.play(FadeOut(summary), FadeOut(summary_points))
        self.wait(0.5)
        
        self.play(Write(ending))
        self.wait(0.5)
        
        self.add_sound(audio_file12)
        self.wait(len(audio_text12)/15 + 1)
        
        # 淡出结束
        self.play(FadeOut(ending))
        self.wait(1)
        
        # 清理音频文件
        self.cleanup_audio_files(audio_files)
    
    def generate_audio(self, text: str, filename: str) -> str:
        """生成音频文件并返回文件路径"""
        output_file = f"temp_{filename}.mp3"
        
        async def async_tts():
            communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
            await communicate.save(output_file)
        
        # 运行异步函数
        asyncio.run(async_tts())
        
        return output_file
    
    def cleanup_audio_files(self, audio_files: list):
        """清理临时音频文件"""
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                os.remove(audio_file)

# 运行脚本
if __name__ == "__main__":
    scene = QabmathbficmathbfjdmathbfkabcdinmathbbRmathbfi2mathbfj2mathbfk2mathbfimathbfjmathbfk1()
    scene.construct()