from manim import *
from manim_physics.pendulum import *


class PendulumExampleScene(Scene):
    def construct(self):
        pendulum = Pendulum()
        self.add(pendulum)
        pendulum.start_swinging()
        self.wait(pendulum.time_for_osc(3))
        pendulum.end_swinging()
