__all__ = [
    "Pendulum",
    "MultiPendulum",
]

import pymunk
from manim import *
from manim_physics.rigid_mechanics import *


class MultiPendulum(VGroup):
    def __init__(
        self,
        *bobs,
        pivot_point=UP * 2,
        rod_style={},
        bob_style={
            "radius": 0.1,
            "color": ORANGE,
            "fill_opacity": 1,
        },
        **kwargs
    ):
        self.pivot_point = pivot_point
        self.bobs = VGroup(*[Circle(**bob_style).move_to(i) for i in bobs])
        self.pins = [pivot_point]
        self.pins += bobs
        self.rods = VGroup()
        self.rods += always_redraw(
            lambda: Line(self.pivot_point, self.bobs[0].get_center(), **rod_style)
        )
        self.rods += always_redraw(
            lambda: VGroup(
                *(
                    Line(self.bobs[i].get_center(), self.bobs[i + 1].get_center(), **rod_style)
                    for i in range(len(bobs) - 1)
                )
            )
        )

        super().__init__(**kwargs)
        self.add(self.rods, self.bobs)

    def make_joints(self, mob1, mob2, spacescene: SpaceScene):
        a = mob1.body
        if type(mob2) == np.ndarray:
            b = pymunk.Body(body_type=pymunk.Body.STATIC)
            b.position = mob2[0], mob2[1]
        else:
            b = mob2.body
        joint = pymunk.PinJoint(a, b)
        spacescene.space.space.add(joint)

    def start_swinging(self):
        spacescene = self.bobs[0].spacescene
        pins = [self.pivot_point]
        pins += self.bobs

        for i in range(len(pins) - 1):
            spacescene.make_rigid_body(pins[i + 1])
            self.make_joints(pins[i + 1], pins[i], spacescene)

    def end_swinging(self):
        spacescene = self.bobs[0].spacescene
        spacescene.stop_rigidity(self.bobs)


class Pendulum(MultiPendulum):
    def __init__(
        self,
        length=3.5,
        initial_theta=0.3,
        pivot_point=UP * 2,
        rod_style={},
        bob_style={
            "radius": 0.25,
            "color": ORANGE,
            "fill_opacity": 1,
        },
        **kwargs
    ):
        self.length = length
        self.pivot_point = pivot_point

        point = self.pivot_point + (
            RIGHT * np.sin(initial_theta) * length
            + DOWN * np.cos(initial_theta) * length
        )
        super().__init__(
            point,
            pivot_point=self.pivot_point,
            rod_style=rod_style,
            bob_style=bob_style,
            **kwargs
        )
