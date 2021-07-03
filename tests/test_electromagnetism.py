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
        self.wait(2)

        #vec = field.get_force_on_charge(charge2) 
        #self.play(Create(vec))