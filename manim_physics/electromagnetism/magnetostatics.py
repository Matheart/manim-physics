"""Magnetostatics module"""

__all__ = ["Wire", "MagneticField"]


import itertools as it
from typing import Iterable, Tuple

from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from manim.mobject.types.vectorized_mobject import VMobject
from manim.mobject.vector_field import ArrowVectorField
import numpy as np


class Wire(VMobject, metaclass=ConvertToOpenGL):
    def __init__(
        self,
        stroke: VMobject,
        current: float = 1,
        samples: int = 16,
        **kwargs,
    ):
        self.current = current
        self.samples = samples

        super().__init__(**kwargs)
        self.set_points(stroke.points)


class MagneticField(ArrowVectorField):
    def __init__(self, *wires: Wire, **kwargs):
        dls = []
        currents = []
        for wire in wires:
            points = [
                wire.point_from_proportion(i)
                for i in np.linspace(0, 1, wire.samples + 1)
            ]
            dls.append(list(zip(points, points[1:])))
            currents.append(wire.current)
        super().__init__(
            lambda p: MagneticField._field_func(p, dls, currents), **kwargs
        )

    @staticmethod
    def _field_func(
        p: np.ndarray,
        dls: Iterable[Tuple[np.ndarray, np.ndarray]],
        currents: Iterable[float],
    ):
        B_field = np.zeros(3)
        for (r0, r1), I in it.product(*dls, currents):
            dl = r1 - r0
            r = p - r0
            dist = np.linalg.norm(r)
            if dist < 0.1:
                return np.zeros(3)
            B_field += np.cross(dl, r) * I / dist**4
        return B_field
