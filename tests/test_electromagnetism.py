from manim import *
from manim_physics.electromagnetism import *


class ElectricFieldExampleScene(Scene):
    def construct(self):
        charge1 = Charge(-1, LEFT * 2 + DOWN)
        charge2 = Charge(2, RIGHT * 2 + DOWN)
        charge3 = Charge(-1, UP * 2)
        field = ElectricField(charge1, charge2, charge3)
        self.add(field, charge1, charge2, charge3)