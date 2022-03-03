from __future__ import annotations

"""A lensing module.

Currently only shows refraction in lenses and not
total internal reflection.
"""

__all__ = [
    "Lens",
    "Ray",
]

from manim import *
from typing import Iterable, Tuple

try:
    # For manim < 0.15.0
    from manim.mobject.opengl_compatibility import ConvertToOpenGL
except ModuleNotFoundError:
    # For manim >= 0.15.0
    from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from shapely import geometry as gm


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
        elif f < 0:
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


class Ray(Line):
    def __init__(
        self,
        start: Iterable[float],
        direction: Iterable[float],
        init_length: float = 5,
        propagate: Iterable[Lens] | None = None,
        **kwargs,
    ) -> None:
        """A light ray.

        Parameters
        ----------
        start
            The start point of the ray
        direction
            The direction of the ray
        init_length
            The initial length of the ray. Once propagated,
            the length are lengthened to showcase lensing.
        propagate
            A list of lenses to propagate through.

        Example
        -------
        .. manim:: RayExampleScene
            :save_last_frame:

            class RayExampleScene(Scene):
                def construct(self):
                    lens_style = {"fill_opacity": 0.5, "color": BLUE}
                    a = Lens(-5, 1, **lens_style).shift(LEFT)
                    a2 = Lens(5, 1, **lens_style).shift(RIGHT)
                    b = [
                        Ray(LEFT * 5 + UP * i, RIGHT, 8, [a, a2], color=RED)
                        for i in np.linspace(-2, 2, 10)
                    ]
                    self.add(a, a2, *b)
        """
        self.init_length = init_length
        self.propagated = False
        super().__init__(start, start + direction * init_length, **kwargs)
        if propagate:
            self.propagate(*propagate)

    def propagate(self, *lenses: Lens) -> None:
        """Let the ray propagate through the list
        of lenses passed.

        Parameters
        ----------
        lenses
            All the lenses for the ray to propagate through
        """
        # TODO: make modular(?) Clean up logic
        sorted_lens = self._sort_lens(lenses)
        for lens in sorted_lens:
            intersects = intersection(lens, self)
            if len(intersects) == 0:
                continue
            intersects = self._sort_intersections(intersects)
            if not self.propagated:
                self.put_start_and_end_on(
                    self.start,
                    intersects[1],
                )
            else:
                nppcc = (
                    self.n_points_per_cubic_curve
                    if config.renderer != "opengl"
                    else self.n_points_per_curve
                )
                self.points = self.points[:-nppcc]
                self.add_line_to(intersects[1])
            self.end = intersects[1]
            i_ang = angle_of_vector(self.end - lens.C[0])
            i_ang -= angle_of_vector(self.start - self.end)
            r_ang = snell(i_ang, lens.n)
            r_ang *= -1 if lens.f > 0 else 1
            ref_ray = rotate_vector(lens.C[0] - self.end, r_ang)
            intersects = intersection(
                lens,
                Line(
                    self.end - ref_ray * self.init_length,
                    self.end + ref_ray * self.init_length,
                ),
            )
            intersects = self._sort_intersections(intersects)
            self.add_line_to(intersects[1])
            self.start = self.end
            self.end = intersects[1]
            i_ang = angle_of_vector(self.end - lens.C[1])
            i_ang -= angle_of_vector(self.start - self.end)
            if np.abs(np.sin(i_ang)) < 1 / lens.n:
                r_ang = antisnell(i_ang, lens.n)
                r_ang *= -1 if lens.f < 0 else 1
                ref_ray = rotate_vector(lens.C[1] - self.end, r_ang)
                ref_ray *= -1 if lens.f > 0 else 1
                self.add_line_to(self.end + ref_ray * self.init_length)
                self.start = self.end
                self.end = self.get_end()
            self.propagated = True

    def _sort_lens(self, lenses: Iterable[Lens]) -> Iterable[Lens]:
        dists = []
        for lens in lenses:
            try:
                dists += [
                    [np.linalg.norm(intersection(self, lens)[0] - self.start), lens]
                ]
            except:
                dists += [[np.inf, lens]]
        dists.sort(key=lambda x: x[0])
        return np.array(dists, dtype=object)[:, 1]

    def _sort_intersections(
        self, intersections: Iterable[Iterable[float]]
    ) -> Iterable[Iterable[float]]:
        result = []
        for inters in intersections:
            result.append([np.linalg.norm(inters - self.end), inters])
        result.sort(key=lambda x: x[0])
        return np.array(result, dtype=object)[:, 1]
