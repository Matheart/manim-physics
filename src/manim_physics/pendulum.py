r"""Pendulums.

:class:`~MultiPendulum` and :class:`~Pendulum` both stem from the
:py:mod:`~rigid_mechanics` feature.

.. note::
    Sometimes the updaters lag behind the intended target. This may
    be solved by increasing config frame rate.

    ``config.frame_rate = 60``

"""

__all__ = [
    "Pendulum",
    "MultiPendulum",
]

from typing import Iterable
import pymunk
from manim import *
from .rigid_mechanics import *


class MultiPendulum(VGroup):
    def __init__(
        self,
        *bobs: Iterable[np.ndarray],
        pivot_point: np.ndarray = UP * 2,
        rod_style: dict = {},
        bob_style: dict = {
            "radius": 0.1,
            "color": ORANGE,
            "fill_opacity": 1,
        },
        **kwargs
    ) -> None:
        """A multipendulum.

        Parameters
        ----------
        bobs
            Positions of pendulum bobs.
        pivot_point
            Position of the pivot.
        rod_style
            Parameters for ``Line``.
        bob_style
            Parameters for ``Circle``.
        kwargs
            Additional parameters for ``VGroup``.

        Examples
        --------
        .. manim:: MultiPendulumExample

            from manim_physics import *
            class MultiPendulumExample(SpaceScene):
                def construct(self):
                    p = MultiPendulum(RIGHT, LEFT)
                    self.add(p)
                    self.make_rigid_body(p.bobs)
                    p.start_swinging()
                    self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
                    self.wait(10)
        """
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
                    Line(
                        self.bobs[i].get_center(),
                        self.bobs[i + 1].get_center(),
                        **rod_style
                    )
                    for i in range(len(bobs) - 1)
                )
            )
        )

        super().__init__(**kwargs)
        self.add(self.rods, self.bobs)

    def _make_joints(
        self, mob1: Mobject, mob2: Mobject, spacescene: SpaceScene
    ) -> None:
        a = mob1.body
        if type(mob2) == np.ndarray:
            b = pymunk.Body(body_type=pymunk.Body.STATIC)
            b.position = mob2[0], mob2[1]
        else:
            b = mob2.body
        joint = pymunk.PinJoint(a, b)
        spacescene.space.space.add(joint)

    def start_swinging(self) -> None:
        """Start swinging."""
        spacescene = self.bobs[0].spacescene
        pins = [self.pivot_point]
        pins += self.bobs

        for i in range(len(pins) - 1):
            spacescene.make_rigid_body(pins[i + 1])
            self._make_joints(pins[i + 1], pins[i], spacescene)

    def end_swinging(self) -> None:
        """Stop swinging."""
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
        """A pendulum.

        Parameters
        ----------
        length
            The length of the pendulum.
        initial_theta
            The initial angle of deviation.
        rod_style
            Parameters for ``Line``.
        bob_style
            Parameters for ``Circle``.
        kwargs
            Additional parameters for ``VGroup``.

        Examples
        --------
        .. manim:: PendulumExample

            from manim_physics import *
            class PendulumExample(SpaceScene):
                def construct(self):
                    pends = VGroup(*[Pendulum(i) for i in np.linspace(1, 5, 7)])
                    self.add(pends)
                    for p in pends:
                        self.make_rigid_body(p.bobs)
                        p.start_swinging()
                    self.wait(10)
        """
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
