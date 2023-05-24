"""Electrostatics module"""

__all__ = [
    "Charge",
    "ElectricField",
]

from manim.constants import ORIGIN, TAU, UP
from manim.mobject.geometry.arc import Arc, Dot
from manim.mobject.geometry.line import Vector
from manim.mobject.geometry.polygram import Rectangle
from manim.mobject.types.vectorized_mobject import VGroup
from manim.mobject.vector_field import ArrowVectorField
from manim.utils.color import BLUE, RED, RED_A, RED_D, color_gradient
import numpy as np


class Charge(VGroup):
    def __init__(
        self,
        magnitude: float = 1,
        point: np.ndarray = ORIGIN,
        add_glow: bool = True,
        **kwargs,
    ) -> None:
        """An electrostatic charge object. Commonly used for :class:`~ElectricField`.

        Parameters
        ----------
        magnitude
            The strength of the electrostatic charge.
        point
            The position of the charge.
        add_glow
            Whether to add a glowing effect. Adds rings of
            varying opacities to simulate glowing effect.
        kwargs
            Additional parameters to be passed to ``VGroup``.
        """
        VGroup.__init__(self, **kwargs)
        self.magnitude = magnitude
        self.point = point
        self.radius = (abs(magnitude) * 0.4 if abs(magnitude) < 2 else 0.8) * 0.3

        if magnitude > 0:
            label = VGroup(
                Rectangle(width=0.32 * 1.1, height=0.006 * 1.1).set_z_index(1),
                Rectangle(width=0.006 * 1.1, height=0.32 * 1.1).set_z_index(1),
            )
            color = RED
            layer_colors = [RED_D, RED_A]
            layer_radius = 4
        else:
            label = Rectangle(width=0.27, height=0.003)
            color = BLUE
            layer_colors = ["#3399FF", "#66B2FF"]
            layer_radius = 2

        if add_glow:  # use many arcs to simulate glowing
            layer_num = 80
            color_list = color_gradient(layer_colors, layer_num)
            opacity_func = lambda t: 1500 * (1 - abs(t - 0.009) ** 0.0001)
            rate_func = lambda t: t**2

            for i in range(layer_num):
                self.add(
                    Arc(
                        radius=layer_radius * rate_func((0.5 + i) / layer_num),
                        angle=TAU,
                        color=color_list[i],
                        stroke_width=101
                        * (rate_func((i + 1) / layer_num) - rate_func(i / layer_num))
                        * layer_radius,
                        stroke_opacity=opacity_func(rate_func(i / layer_num)),
                    ).shift(point)
                )

        self.add(Dot(point=self.point, radius=self.radius, color=color))
        self.add(label.scale(self.radius / 0.3).shift(point))
        for mob in self:
            mob.set_z_index(1)


class ElectricField(ArrowVectorField):
    def __init__(self, *charges: Charge, **kwargs) -> None:
        """An electric field.

        Parameters
        ----------
        charges
            The charges affecting the electric field.
        kwargs
            Additional parameters to be passed to ``ArrowVectorField``.

        Examples
        --------
        .. manim:: ElectricFieldExampleScene
            :save_last_frame:

            from manim_physics import *

            class ElectricFieldExampleScene(Scene):
                def construct(self):
                    charge1 = Charge(-1, LEFT + DOWN)
                    charge2 = Charge(2, RIGHT + DOWN)
                    charge3 = Charge(-1, UP)
                    field = ElectricField(charge1, charge2, charge3)
                    self.add(charge1, charge2, charge3)
                    self.add(field)
        """
        self.charges = charges
        super().__init__(lambda p: self._field_func(p), **kwargs)

    def _field_func(self, p: np.ndarray) -> np.ndarray:
        direction = np.zeros(3)
        pos = []
        for charge in self.charges:
            p0, mag = charge.get_center(), charge.magnitude
            pos.append(p0)
            x, y, z = p - p0
            dist = (x**2 + y**2) ** 1.5
            if any((p - p0) ** 2 > 0.05):
                direction += mag * np.array([x / dist, y / dist, 0])
            else:
                direction += np.zeros(3)
        for p0 in pos:
            if all((p - p0) ** 2 <= 0.05):
                direction = np.zeros(3)
        return direction

    def get_force_on_charge(self, charge: Charge, **kwargs) -> Vector:
        """Returns a vector corresponding to the force
        of the electric field on the charge.
        """
        p = charge.get_center()
        direction = np.zeros(3)
        for other_charge in self.charges:
            if other_charge == charge:
                continue
            p0, mag = other_charge.get_center(), other_charge.magnitude
            x, y, z = p - p0
            dist = np.linalg.norm(p - p0) ** 3
            if (x**2) > 0.01 or (y**2) > 0.01:
                direction += mag * np.array([x / dist, y / dist, 0])
            else:
                direction += np.zeros(3)
        length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        vec_start = (
            Vector(direction / length * charge.radius).shift(charge.point).get_end()
        )
        return Vector(direction, **kwargs).shift(vec_start)
