import asyncio
import edge_tts
import os
from mutagen.mp3 import MP3
from manim import *

class Qabmathbficmathbfjdmathbfk(Scene):
    def __init__(self):
        super().__init__()
        self.audio_dir = "audios"
        os.makedirs(self.audio_dir, exist_ok=True)
        
        self.audios = {
            "intro": f"{self.audio_dir}/intro.mp3",
            "real_part": f"{self.audio_dir}/real_part.mp3",
            "i_part": f"{self.audio_dir}/i_part.mp3",
            "j_part": f"{self.audio_dir}/j_part.mp3",
            "k_part": f"{self.audio_dir}/k_part.mp3",
            "summary": f"{self.audio_dir}/summary.mp3"
        }
        
        # 异步生成音频
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        """生成所有音频文件"""
        texts = {
            "intro": "同学们好！今天我们来认识一个特别的数，叫做四元数。",
            "real_part": "四元数就像一个有四个房间的房子。第一个房间住着实数a，这是最普通的数。",
            "i_part": "第二个房间住着b乘以i，这里的i是一个特殊的单位，就像我们学过的虚数单位。",
            "j_part": "第三个房间住着c乘以j，j是另一个特殊的单位。",
            "k_part": "第四个房间住着d乘以k，k也是特殊的单位。i、j、k这三个单位之间有着特别的乘法关系。",
            "summary": "所以，四元数q等于a加上b乘以i，加上c乘以j，再加上d乘以k。它就像是一个有四个部分的超级复数！"
        }
        
        tasks = []
        for key, text in texts.items():
            tasks.append(self.generate_audio(text, self.audios[key]))
        
        await asyncio.gather(*tasks)
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        """生成单个音频文件"""
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_audio_duration(self, filename):
        """获取音频时长"""
        audio = MP3(filename)
        return audio.info.length
    
    def safe_layout(self, elements, max_per_row=4, spacing=0.5):
        """安全布局函数，防止元素拥挤"""
        if len(elements) == 0:
            return VGroup()
        
        # 分组排列
        rows = []
        for i in range(0, len(elements), max_per_row):
            row = elements[i:i+max_per_row]
            row_group = VGroup(*row).arrange(RIGHT, buff=spacing)
            rows.append(row_group)
        
        # 垂直排列
        if len(rows) > 1:
            final_group = VGroup(*rows).arrange(DOWN, buff=spacing*0.6)
        else:
            final_group = rows[0]
        
        # 检查边界
        frame_width = config.frame_width
        frame_height = config.frame_height
        
        left_bound = final_group.get_left()[0]
        right_bound = final_group.get_right()[0]
        top_bound = final_group.get_top()[1]
        bottom_bound = final_group.get_bottom()[1]
        
        # 如果超出边界，进行缩放
        if (abs(left_bound) > frame_width/2 - 1 or 
            abs(right_bound) > frame_width/2 - 1 or
            abs(top_bound) > frame_height/2 - 1 or
            abs(bottom_bound) > frame_height/2 - 1):
            final_group.scale(0.8)
        
        return final_group
    
    def construct(self):
        # 第一步：介绍四元数
        title = Text("四元数", font_size=48, color=BLUE)
        subtitle = Text("一个特别的超级复数", font_size=32, color=YELLOW)
        
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP)
        
        self.play(FadeIn(title_group))
        
        # 播放介绍音频
        self.add_sound(self.audios["intro"])
        audio_duration = self.get_audio_duration(self.audios["intro"])
        self.wait(audio_duration + 1)
        
        # 清理画面
        self.play(FadeOut(title_group))
        
        # 第二步：展示四元数公式
        formula = MathTex(r"q = a + b\mathbf{i} + c\mathbf{j} + d\mathbf{k}", font_size=40)
        formula.set_color_by_tex("a", GREEN)
        formula.set_color_by_tex("b", RED)
        formula.set_color_by_tex("c", ORANGE)
        formula.set_color_by_tex("d", PURPLE)
        
        # 添加解释文字
        explanation = Text("四元数有四个部分：", font_size=28, color=WHITE)
        explanation.next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(formula))
        self.play(Write(explanation))
        self.wait(2)
        
        # 第三步：逐步解释每个部分
        
        # 3.1 实部a
        real_part = MathTex(r"a", font_size=36, color=GREEN)
        real_label = Text("实数部分（普通数）", font_size=24, color=GREEN)
        real_label.next_to(real_part, DOWN, buff=0.2)
        real_group = VGroup(real_part, real_label)
        real_group.shift(LEFT*3 + UP*1.5)
        
        self.play(FadeIn(real_group))
        
        # 播放实部音频
        self.add_sound(self.audios["real_part"])
        audio_duration = self.get_audio_duration(self.audios["real_part"])
        self.wait(audio_duration + 1)
        
        # 3.2 i部分
        i_part = MathTex(r"b\mathbf{i}", font_size=36, color=RED)
        i_label = Text("第一个虚数单位", font_size=24, color=RED)
        i_label.next_to(i_part, DOWN, buff=0.2)
        i_group = VGroup(i_part, i_label)
        i_group.shift(LEFT*1 + UP*1.5)
        
        self.play(FadeIn(i_group))
        
        # 播放i部分音频
        self.add_sound(self.audios["i_part"])
        audio_duration = self.get_audio_duration(self.audios["i_part"])
        self.wait(audio_duration + 1)
        
        # 3.3 j部分
        j_part = MathTex(r"c\mathbf{j}", font_size=36, color=ORANGE)
        j_label = Text("第二个虚数单位", font_size=24, color=ORANGE)
        j_label.next_to(j_part, DOWN, buff=0.2)
        j_group = VGroup(j_part, j_label)
        j_group.shift(RIGHT*1 + UP*1.5)
        
        self.play(FadeIn(j_group))
        
        # 播放j部分音频
        self.add_sound(self.audios["j_part"])
        audio_duration = self.get_audio_duration(self.audios["j_part"])
        self.wait(audio_duration + 1)
        
        # 3.4 k部分
        k_part = MathTex(r"d\mathbf{k}", font_size=36, color=PURPLE)
        k_label = Text("第三个虚数单位", font_size=24, color=PURPLE)
        k_label.next_to(k_part, DOWN, buff=0.2)
        k_group = VGroup(k_part, k_label)
        k_group.shift(RIGHT*3 + UP*1.5)
        
        self.play(FadeIn(k_group))
        
        # 播放k部分音频
        self.add_sound(self.audios["k_part"])
        audio_duration = self.get_audio_duration(self.audios["k_part"])
        self.wait(audio_duration + 1)
        
        # 第四步：展示完整公式和关系
        self.play(FadeOut(real_group), FadeOut(i_group), 
                  FadeOut(j_group), FadeOut(k_group), FadeOut(explanation))
        
        # 重新显示公式并高亮
        self.play(formula.animate.scale(1.2).move_to(ORIGIN))
        
        # 创建四个彩色方块代表四个部分
        box_a = Square(side_length=0.8, color=GREEN, fill_opacity=0.3)
        box_a.next_to(formula.get_part_by_tex("a"), DOWN, buff=0.3)
        label_a = Text("实数", font_size=20, color=GREEN)
        label_a.next_to(box_a, DOWN, buff=0.1)
        
        box_b = Square(side_length=0.8, color=RED, fill_opacity=0.3)
        box_b.next_to(formula.get_part_by_tex("b"), DOWN, buff=0.3)
        label_b = Text("i部分", font_size=20, color=RED)
        label_b.next_to(box_b, DOWN, buff=0.1)
        
        box_c = Square(side_length=0.8, color=ORANGE, fill_opacity=0.3)
        box_c.next_to(formula.get_part_by_tex("c"), DOWN, buff=0.3)
        label_c = Text("j部分", font_size=20, color=ORANGE)
        label_c.next_to(box_c, DOWN, buff=0.1)
        
        box_d = Square(side_length=0.8, color=PURPLE, fill_opacity=0.3)
        box_d.next_to(formula.get_part_by_tex("d"), DOWN, buff=0.3)
        label_d = Text("k部分", font_size=20, color=PURPLE)
        label_d.next_to(box_d, DOWN, buff=0.1)
        
        boxes = [box_a, box_b, box_c, box_d]
        labels = [label_a, label_b, label_c, label_d]
        
        for box, label in zip(boxes, labels):
            self.play(Create(box), Write(label))
            self.wait(0.5)
        
        # 第五步：总结
        summary_text = Text("四元数就像一个有四个房间的房子：", font_size=28, color=YELLOW)
        summary_text.to_edge(DOWN)
        
        self.play(Write(summary_text))
        
        # 播放总结音频
        self.add_sound(self.audios["summary"])
        audio_duration = self.get_audio_duration(self.audios["summary"])
        self.wait(audio_duration + 1)
        
        # 第六步：淡出所有元素
        all_elements = [formula] + boxes + labels + [summary_text]
        self.play(*[FadeOut(elem) for elem in all_elements])
        
        # 最终显示结束语
        ending = Text("四元数学习完成！", font_size=40, color=BLUE)
        self.play(FadeIn(ending))
        self.wait(2)
        self.play(FadeOut(ending))

# 运行场景
if __name__ == "__main__":
    scene = Qabmathbficmathbfjdmathbfk()
    scene.render()