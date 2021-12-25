"""A lensing module.

Currently only shows refraction in lenses and not
total internal reflection.
"""

__all__ = [
    "Lens",
    "Ray",
]

from manim import *
from typing import Iterable, Optional
from manim.mobject.opengl_compatibility import ConvertToOpenGL
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
                        b := Circle(r).shift(RIGHT * (r + d / 2)),
                    ),
                    a := Circle(r).shift(LEFT * (r + d / 2)),
                )
                .insert_n_curves(50)
                .points
            )
        self.add(VectorizedPoint(a.get_center()), VectorizedPoint(b.get_center()))

    @property
    def C(self) -> Iterable[Iterable[float]]:
        """Returns a tuple of two points corresponding to the centers of curvature."""
        if config.renderer !='opengl':
            return self[1].points[0], self[2].points[0]  # why is this confusing
        else:
            return self[0].points[0], self[1].points[0]


class Ray(Line):
    def __init__(
        self,
        start: Iterable[float],
        direction: Iterable[float],
        init_length: float = 5,
        propagate: Optional[Iterable[Lens]] = None,
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
            (Must be in order of propagation)

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
        """Lenses has to be in the order
        which the ray passes the lens.

        Parameters
        ----------
        lenses
            All the lenses for the ray to propagate through
        """
        # TODO: make modular(?) Clean up logic
        for lens in lenses:
            intersects = intersection(lens, self)
            if len(intersects) == 0:
                continue
            if not self.propagated:
                self.put_start_and_end_on(
                    self.start,
                    intersects[0],
                )
            else:
                nppcc = (
                    self.n_points_per_cubic_curve
                    if config.renderer != "opengl"
                    else self.n_points_per_curve
                )
                self.points = self.points[:-nppcc]
                self.add_line_to(intersects[0])
            self.end = intersects[0]
            i_ang = np.angle(R3_to_complex(self.end - lens.C[0])) - np.angle(
                R3_to_complex(self.start - self.end)
            )
            r_ang = snell(i_ang, lens.n)
            r_ang *= 1 if lens.f < 0 else -1
            ref_ray = rotation_matrix(r_ang, OUT) @ (lens.C[0] - self.end)
            ref_ray *= -1 if lens.f < 0 else 1
            intersects = intersection(
                lens, Line(self.end, self.end + ref_ray * self.init_length)
            )
            if len(intersects) == 0:
                continue
            i = 1 if len(intersects) > 1 else 0
            self.add_line_to(intersects[i])
            self.start = self.end
            self.end = intersects[i]
            i_ang = np.angle(R3_to_complex(self.end - lens.C[1])) - np.angle(
                R3_to_complex(self.start - self.end),
            )
            if np.abs(np.sin(i_ang)) < 1 / lens.n:
                r_ang = antisnell(i_ang, lens.n)
                r_ang *= -1 if lens.f < 0 else 1
                ref_ray = -(rotation_matrix(r_ang, OUT) @ (lens.C[1] - self.end))
                ref_ray *= -1 if lens.f < 0 else 1
                self.add_line_to(self.end + ref_ray * self.init_length)
                self.start = self.end
                self.end = self.end + ref_ray * self.init_length
            self.propagated = True
