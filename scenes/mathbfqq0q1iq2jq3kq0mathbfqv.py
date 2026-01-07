from manim import *
import asyncio
import edge_tts
import subprocess
import os
from pathlib import Path

class Mathbfqq0q1iq2jq3kq0mathbfqv(Scene):
    def construct(self):
        # 音频生成和播放函数
        async def generate_and_play_audio(text, filename):
            """生成并播放音频"""
            try:
                # 生成音频文件
                communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
                await communicate.save(filename)
                
                # 播放音频（异步）
                def play_audio():
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", filename], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # 在新线程中播放音频
                import threading
                thread = threading.Thread(target=play_audio)
                thread.start()
                return thread
            except Exception as e:
                print(f"音频生成失败: {e}")
                return None
        
        def safe_layout(elements, max_per_row=4, spacing=0.5):
            """安全布局函数，防止元素拥挤和超出边界"""
            if len(elements) == 0:
                return VGroup()
            
            # 分组排列
            rows = []
            for i in range(0, len(elements), max_per_row):
                row_elements = elements[i:i+max_per_row]
                row = VGroup(*row_elements).arrange(RIGHT, buff=spacing)
                rows.append(row)
            
            # 垂直排列行
            group = VGroup(*rows).arrange(DOWN, buff=0.3)
            
            # 检查边界
            frame_width = config.frame_width - 1
            frame_height = config.frame_height - 1
            
            # 缩放调整
            if group.get_width() > frame_width or group.get_height() > frame_height:
                scale_factor = min(frame_width/group.get_width(), frame_height/group.get_height()) * 0.8
                group.scale(scale_factor)
            
            return group
        
        # 清理临时音频文件
        temp_files = []
        
        # 步骤1：引入概念 - 什么是四元数？
        title = Text("什么是四元数？", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        
        # 音频文本1
        audio_text1 = "同学们好！今天我们来学习一个有趣的数学概念：四元数。"
        audio_thread1 = asyncio.run(generate_and_play_audio(audio_text1, "audio1.mp3"))
        temp_files.append("audio1.mp3")
        
        self.play(FadeIn(title, shift=UP))
        self.wait(2)
        
        # 步骤2：用生活化的例子解释
        example_text = Text("想象一下，你有一个魔法盒子", font_size=36, color=YELLOW)
        example_text.next_to(title, DOWN, buff=0.5)
        
        # 音频文本2
        audio_text2 = "想象一下，你有一个魔法盒子，里面可以装四种不同的东西。"
        audio_thread2 = asyncio.run(generate_and_play_audio(audio_text2, "audio2.mp3"))
        temp_files.append("audio2.mp3")
        
        self.play(Write(example_text))
        self.wait(2)
        
        # 创建魔法盒子
        box = Square(side_length=2, color=GREEN, fill_opacity=0.3)
        box_label = Text("魔法盒子", font_size=24, color=GREEN)
        box_label.next_to(box, DOWN, buff=0.2)
        box_group = VGroup(box, box_label)
        box_group.next_to(example_text, DOWN, buff=0.5)
        
        self.play(Create(box), Write(box_label))
        self.wait(1)
        
        # 步骤3：展示盒子里的四种东西
        items = [
            Text("1个实数", font_size=28, color=RED),
            Text("3个虚数", font_size=28, color=BLUE),
        ]
        
        # 布局物品
        items_group = safe_layout(items, max_per_row=2)
        items_group.next_to(box_group, DOWN, buff=0.5)
        
        # 音频文本3
        audio_text3 = "这个盒子里可以装一个实数和三个虚数。实数就像我们平时用的数字，虚数就像有特殊能力的数字。"
        audio_thread3 = asyncio.run(generate_and_play_audio(audio_text3, "audio3.mp3"))
        temp_files.append("audio3.mp3")
        
        self.play(FadeIn(items_group, shift=UP))
        self.wait(3)
        
        # 清理画面
        self.play(
            FadeOut(title),
            FadeOut(example_text),
            FadeOut(box_group),
            FadeOut(items_group)
        )
        self.wait(0.5)
        
        # 步骤4：正式介绍四元数公式
        formula_title = Text("四元数的公式", font_size=48, color=BLUE)
        formula_title.to_edge(UP, buff=0.5)
        
        # 音频文本4
        audio_text4 = "现在，我们来看看四元数的正式公式。"
        audio_thread4 = asyncio.run(generate_and_play_audio(audio_text4, "audio4.mp3"))
        temp_files.append("audio4.mp3")
        
        self.play(FadeIn(formula_title, shift=UP))
        self.wait(1)
        
        # 显示完整公式
        formula = MathTex(
            r"\mathbf{q} = q_0 + q_1 i + q_2 j + q_3 k",
            font_size=40,
            color=WHITE
        )
        formula.next_to(formula_title, DOWN, buff=0.5)
        
        # 音频文本5
        audio_text5 = "四元数q等于q0加上q1乘以i，加上q2乘以j，加上q3乘以k。"
        audio_thread5 = asyncio.run(generate_and_play_audio(audio_text5, "audio5.mp3"))
        temp_files.append("audio5.mp3")
        
        self.play(Write(formula))
        self.wait(3)
        
        # 步骤5：分解解释公式各部分
        explanation_text = Text("让我们分解来看：", font_size=36, color=YELLOW)
        explanation_text.next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(explanation_text))
        self.wait(1)
        
        # 创建解释部分
        parts = [
            VGroup(
                MathTex(r"q_0", font_size=32, color=RED),
                Text("实数部分", font_size=24, color=RED)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                MathTex(r"q_1 i", font_size=32, color=BLUE),
                Text("第一个虚数", font_size=24, color=BLUE)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                MathTex(r"q_2 j", font_size=32, color=GREEN),
                Text("第二个虚数", font_size=24, color=GREEN)
            ).arrange(DOWN, buff=0.1),
            VGroup(
                MathTex(r"q_3 k", font_size=32, color=PURPLE),
                Text("第三个虚数", font_size=24, color=PURPLE)
            ).arrange(DOWN, buff=0.1),
        ]
        
        # 布局解释部分
        parts_group = safe_layout(parts, max_per_row=4, spacing=0.8)
        parts_group.next_to(explanation_text, DOWN, buff=0.5)
        
        # 音频文本6
        audio_text6 = "q0是实数部分，就像普通数字。q1乘以i，q2乘以j，q3乘以k是三个虚数部分，每个都有自己的特殊单位。"
        audio_thread6 = asyncio.run(generate_and_play_audio(audio_text6, "audio6.mp3"))
        temp_files.append("audio6.mp3")
        
        # 逐个显示解释
        for i, part in enumerate(parts_group):
            self.play(FadeIn(part, shift=UP))
            self.wait(0.5)
        
        self.wait(2)
        
        # 步骤6：简化表示
        simplified_title = Text("更简单的写法", font_size=36, color=YELLOW)
        simplified_title.next_to(parts_group, DOWN, buff=0.5)
        
        self.play(Write(simplified_title))
        self.wait(1)
        
        simplified_formula = MathTex(
            r"\mathbf{q} = q_0 + \mathbf{q}_v",
            font_size=40,
            color=WHITE
        )
        simplified_formula.next_to(simplified_title, DOWN, buff=0.3)
        
        # 添加解释
        simplified_explanation = Text("把三个虚数部分打包成一个向量", font_size=28, color=GREEN)
        simplified_explanation.next_to(simplified_formula, DOWN, buff=0.2)
        
        # 音频文本7
        audio_text7 = "我们也可以把三个虚数部分打包在一起，写成q0加上qv。这样更简洁！"
        audio_thread7 = asyncio.run(generate_and_play_audio(audio_text7, "audio7.mp3"))
        temp_files.append("audio7.mp3")
        
        self.play(Write(simplified_formula))
        self.wait(1)
        self.play(Write(simplified_explanation))
        self.wait(3)
        
        # 步骤7：总结和应用
        self.play(
            FadeOut(formula_title),
            FadeOut(formula),
            FadeOut(explanation_text),
            FadeOut(parts_group),
            FadeOut(simplified_title),
            FadeOut(simplified_formula),
            FadeOut(simplified_explanation)
        )
        self.wait(0.5)
        
        summary_title = Text("四元数有什么用？", font_size=48, color=BLUE)
        summary_title.to_edge(UP, buff=0.5)
        
        self.play(FadeIn(summary_title, shift=UP))
        self.wait(1)
        
        # 应用例子
        applications = [
            Text("• 3D游戏中的角色旋转", font_size=32, color=YELLOW),
            Text("• 手机陀螺仪的姿态计算", font_size=32, color=YELLOW),
            Text("• 机器人手臂的运动控制", font_size=32, color=YELLOW),
        ]
        
        # 布局应用例子
        apps_group = VGroup(*applications).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        apps_group.next_to(summary_title, DOWN, buff=0.5)
        
        # 音频文本8
        audio_text8 = "四元数在3D游戏、手机陀螺仪和机器人控制中非常有用，可以很好地表示三维旋转。"
        audio_thread8 = asyncio.run(generate_and_play_audio(audio_text8, "audio8.mp3"))
        temp_files.append("audio8.mp3")
        
        for app in apps_group:
            self.play(Write(app))
            self.wait(1)
        
        self.wait(2)
        
        # 最终总结
        final_text = Text("四元数 = 1个实数 + 3个虚数", font_size=40, color=GREEN)
        final_text.next_to(apps_group, DOWN, buff=0.5)
        
        # 音频文本9
        audio_text9 = "记住，四元数就是一个实数加上三个虚数。很简单吧！"
        audio_thread9 = asyncio.run(generate_and_play_audio(audio_text9, "audio9.mp3"))
        temp_files.append("audio9.mp3")
        
        self.play(Write(final_text))
        self.wait(3)
        
        # 淡出所有内容
        self.play(
            FadeOut(summary_title),
            FadeOut(apps_group),
            FadeOut(final_text)
        )
        
        # 等待音频播放完成
        self.wait(1)
        
        # 清理临时文件
        for file in temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except:
                pass

# 运行场景
if __name__ == "__main__":
    scene = Mathbfqq0q1iq2jq3kq0mathbfqv()
    scene.render()