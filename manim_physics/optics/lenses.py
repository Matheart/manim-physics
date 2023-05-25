"""Lenses for refracting Rays.
"""
from __future__ import annotations
from typing import Iterable, Tuple

from manim import config
from manim.constants import LEFT, RIGHT
from manim.mobject.geometry.arc import Circle
from manim.mobject.geometry.boolean_ops import Difference, Intersection
from manim.mobject.geometry.polygram import Square
from manim.mobject.types.vectorized_mobject import VMobject, VectorizedPoint
import numpy as np
from shapely import geometry as gm


__all__ = ["Lens"]


try:
    # For manim < 0.15.0
    from manim.mobject.opengl_compatibility import ConvertToOpenGL
except ModuleNotFoundError:
    # For manim >= 0.15.0
    from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL


def intersection(vmob1: VMobject, vmob2: VMobject) -> Iterable[Iterable[float]]:
    """intersection points of 2 curves"""
    a = gm.LineString(vmob1.points)
    b = gm.LineString(vmob2.points)
    intersects: gm.GeometryCollection = a.intersection(b)
    try:  # for intersections > 1
        return np.array(
            [[[x, y, z] for x, y, z in m.coords][0] for m in intersects.geoms]
        )
    except:  # else
        return np.array([[x, y, z] for x, y, z in intersects.coords])


def snell(i_ang: float, n: float) -> float:
    """accepts radians, returns radians"""
    return np.arcsin(np.sin(i_ang) / n)


def antisnell(r_ang: float, n: float) -> float:
    """accepts radians, returns radians"""
    return np.arcsin(np.sin(r_ang) * n)


class Lens(VMobject, metaclass=ConvertToOpenGL):
    def __init__(self, f: float, d: float, n: float = 1.52, **kwargs) -> None:
        """A lens. Commonly used with :class:`~Ray` .

        Parameters
        ----------
        f
            Focal length. This does not correspond correctly
            to the point of focus (Known issue). Positive f
            returns a convex lens, negative for concave.
        d
            Lens thickness
        n
            Refractive index. By default, glass.
        kwargs
            Additional parameters to be passed to :class:`~VMobject` .
        """
        super().__init__(**kwargs)
        self.f = f
        f *= 50 / 7 * f if f > 0 else -50 / 7 * f  # this is odd, but it works
        if f > 0:
            r = ((n - 1) ** 2 * f * d / n) ** 0.5
        else:
            r = ((n - 1) ** 2 * -f * d / n) ** 0.5
        self.d = d
        self.n = n
        self.r = r
        if f > 0:
            self.set_points(
                Intersection(
                    a := Circle(r).shift(RIGHT * (r - d / 2)),
                    b := Circle(r).shift(LEFT * (r - d / 2)),
                )
                .insert_n_curves(50)
                .points
            )
        else:
            self.set_points(
                Difference(
                    Difference(
                        Square(2 * 0.7 * r),
                        a := Circle(r).shift(LEFT * (r + d / 2)),
                    ),
                    b := Circle(r).shift(RIGHT * (r + d / 2)),
                )
                .insert_n_curves(50)
                .points
            )
        self.add(VectorizedPoint(a.get_center()), VectorizedPoint(b.get_center()))

    @property
    def C(self) -> Tuple[Iterable[float]]:
        """Returns a tuple of two points corresponding to the centers of curvature."""
        i = 0
        i += 1 if config.renderer != "opengl" else 0
        return self[i].points[0], self[i + 1].points[0]  # why is this confusing
