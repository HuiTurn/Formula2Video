import asyncio
import edge_tts
from mutagen.mp3 import MP3
from manim import *

class FormulaScene(Scene):
    def __init__(self):
        super().__init__()
        self.audios = {
            "step1": "audios/step1.mp3",
            "step2": "audios/step2.mp3",
            "step3": "audios/step3.mp3",
            "step4": "audios/step4.mp3",
            "step5": "audios/step5.mp3"
        }
        asyncio.run(self.generate_all_audios())
    
    async def generate_all_audios(self):
        texts = {
            "step1": "嗨！今天我们来认识一个超酷的数学概念——四元数。",
            "step2": "想象你正在玩3D游戏，角色可以前后、左右、上下移动，还能旋转。四元数就是专门用来描述这种3D旋转的神奇工具！",
            "step3": "四元数就像一个超级坐标，由一个实数w和三个虚数x i、y j、z k组成。就像你的游戏角色有生命值w，还有三个方向的旋转值。",
            "step4": "虚单位i、j、k就像游戏里的特殊技能，它们相乘时有特别的规则：i乘j等于k，j乘k等于i，k乘i等于j，但反过来就会变负哦！",
            "step5": "所以四元数就是q等于w加x i加y j加z k。记住这个公式，你就能驾驭3D世界的旋转啦！"
        }
        for key, text in texts.items():
            await self.generate_audio(text, self.audios[key])
    
    async def generate_audio(self, text, filename, voice="zh-CN-XiaoxiaoNeural", rate="+5%"):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(filename)
    
    def get_duration(self, filename):
        return MP3(filename).info.length
    
    def construct(self):
        # 1. 标题
        title = Text("四元数公式", font_size=60, color=YELLOW).to_edge(UP, buff=0.5)
        self.ensure_in_bounds(title)
        
        # 2. 生活化类比：游戏手柄
        gamepad = RoundedRectangle(height=3, width=4, corner_radius=0.3, color=BLUE)
        gamepad.set_fill(BLUE, opacity=0.3)
        gamepad.move_to(ORIGIN + UP*0.5)
        
        # 添加按钮
        button1 = Circle(radius=0.2, color=RED).move_to(gamepad.get_center() + LEFT*0.8 + UP*0.5)
        button2 = Circle(radius=0.2, color=GREEN).move_to(gamepad.get_center() + RIGHT*0.8 + UP*0.5)
        button3 = Circle(radius=0.2, color=YELLOW).move_to(gamepad.get_center() + LEFT*0.8 + DOWN*0.5)
        button4 = Circle(radius=0.2, color=BLUE).move_to(gamepad.get_center() + RIGHT*0.8 + DOWN*0.5)
        
        gamepad_group = VGroup(gamepad, button1, button2, button3, button4)
        
        # 3. 四元数公式
        formula = MathTex(r"q = w + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}", font_size=48)
        formula.next_to(gamepad, DOWN, buff=1.0)
        
        # 4. 实部和虚部说明
        real_part = Text("实部：w（生命值）", font_size=28, color=GREEN)
        imag_part = Text("虚部：xi + yj + zk（旋转值）", font_size=28, color=PURPLE)
        parts_group = VGroup(real_part, imag_part).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        parts_group.to_edge(LEFT, buff=1.0)
        parts_group.shift(UP*1.5)
        
        # 5. 乘法规则
        rules_text = Text("虚单位乘法规则：", font_size=32, color=ORANGE)
        rule1 = MathTex(r"\mathbf{i} \times \mathbf{j} = \mathbf{k}", font_size=36)
        rule2 = MathTex(r"\mathbf{j} \times \mathbf{k} = \mathbf{i}", font_size=36)
        rule3 = MathTex(r"\mathbf{k} \times \mathbf{i} = \mathbf{j}", font_size=36)
        rule4 = MathTex(r"\mathbf{j} \times \mathbf{i} = -\mathbf{k}", font_size=36)
        
        rules_group = VGroup(rules_text, rule1, rule2, rule3, rule4)
        rules_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rules_group.to_edge(RIGHT, buff=1.0)
        rules_group.shift(UP*0.5)
        
        # 6. 动画开始
        self.add_sound(self.audios["step1"])
        self.play(Write(title))
        self.wait(self.get_duration(self.audios["step1"]) + 0.5)
        
        self.add_sound(self.audios["step2"])
        self.play(Create(gamepad), run_time=1.5)
        self.play(*[Create(btn) for btn in [button1, button2, button3, button4]], run_time=1)
        self.wait(self.get_duration(self.audios["step2"]) + 0.5)
        
        self.add_sound(self.audios["step3"])
        self.play(Write(formula), run_time=2)
        self.wait(0.5)
        self.play(Write(real_part), Write(imag_part), run_time=1.5)
        self.wait(self.get_duration(self.audios["step3"]) + 0.5)
        
        self.add_sound(self.audios["step4"])
        self.play(Write(rules_text), run_time=1)
        self.play(*[Write(rule) for rule in [rule1, rule2, rule3, rule4]], run_time=2)
        self.wait(self.get_duration(self.audios["step4"]) + 0.5)
        
        self.add_sound(self.audios["step5"])
        # 高亮公式
        box = SurroundingRectangle(formula, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=1.5)
        self.wait(self.get_duration(self.audios["step5"]) + 0.5)
        
        # 结束
        self.play(FadeOut(box), run_time=1)
        self.wait(2)
    
    def ensure_in_bounds(self, obj, max_w=12.0, max_h=7.0):
        if obj.get_width() > max_w: obj.scale(max_w / obj.get_width())
        if obj.get_height() > max_h: obj.scale(max_h / obj.get_height())