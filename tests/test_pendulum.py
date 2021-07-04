from manim import *
from manim_physics import *


class PendulumExample(SpaceScene):
    def construct(self):
        p = MultiPendulum(RIGHT, LEFT)
        self.add(p)
        self.make_rigid_body(p.bobs)
        p.start_swinging()
        self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
        self.wait(10)
