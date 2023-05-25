"""Magnetostatics module"""

from __future__ import annotations
import itertools as it
from typing import Iterable, Tuple

from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from manim.mobject.types.vectorized_mobject import VMobject
from manim.mobject.vector_field import ArrowVectorField
import numpy as np


__all__ = ["Wire", "MagneticField"]


class Wire(VMobject, metaclass=ConvertToOpenGL):
    """An abstract class denoting a current carrying wire to produce a
    :class:`~MagneticField`.

    Parameters
    ----------
    stroke
        The original wire ``VMobject``. The resulting wire takes its form.
    current
        The magnitude of current flowing in the wire.
    samples
        The number of segments of the wire used to create the
        :class:`~MagneticField`.
    kwargs
        Additional parameters passed to ``VMobject``.


    .. note::

        See :class:`~MagneticField` for examples.

    """

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
    """A magnetic field.

    Parameters
    ----------
    wires
        All wires contributing to the total field.
    kwargs
        Additional parameters to be passed to ``ArrowVectorField``.

    Example
    -------
    .. manim:: MagneticFieldExample
        :save_last_frame:

        from manim_physics import *

        class MagneticFieldExample(ThreeDScene):
            def construct(self):
                wire = Wire(Circle(2).rotate(PI / 2, UP))
                mag_field = MagneticField(
                    wire,
                    x_range=[-4, 4],
                    y_range=[-4, 4],
                )
                self.set_camera_orientation(PI / 3, PI / 4)
                self.add(wire, mag_field)

    """

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
