from manim import *

from manim_physics.electromagnetism import *


class ElectricityExampleScene(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT * 2 + DOWN)
        charge2 = Charge(2, RIGHT * 2 + DOWN)
        charge3 = Charge(-1, UP * 2)
        field = ElectricField(charge1, charge2, charge3)
        self.add(field, charge1, charge2, charge3)


class MagnetismExample(Scene):
    def construct(self):
        current1 = Current(LEFT * 2.5)
        current2 = Current(RIGHT * 2.5, direction=IN)
        field = CurrentMagneticField(current1, current2)
        self.add(field, current1, current2)


class BarMagnetExample(Scene):
    def construct(self):
        bar1 = BarMagnet().rotate(PI / 2).shift(LEFT * 3.5)
        bar2 = BarMagnet().rotate(PI / 2).shift(RIGHT * 3.5)
        self.add(BarMagneticField(bar1, bar2))
        self.add(bar1, bar2)
