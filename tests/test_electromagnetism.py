from manim import *

from manim_physics.electromagnetism import *


class ElectricFieldExampleScene(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT + DOWN)
        charge2 = Charge(2, RIGHT + DOWN)
        charge3 = Charge(-1, UP)
        field = ElectricField(charge1, charge2, charge3)
        self.add(charge1, charge2, charge3)
        self.add(field)


class MagnetismExampleScene(Scene):
    def construct(self):
        magnet1 = BarMagnet().shift(LEFT * 2.5)
        magnet2 = Current(RIGHT * 2.5, direction=IN)
        field = MagneticField(magnet1, magnet2)
        self.add(field, magnet1, magnet2)
