"""A gravity simulation space.

Most objects can be made into a rigid body (moves according to gravity
and collision) or a static body (stays still within the scene).

To use this feature, the :class:`~SpaceScene` must be used, to access
the specific functions of the space.

.. note::
    *   This feature utilizes the pymunk package. Although unnecessary,
        it might make it easier if you knew a few things on how to use it.

        `Official Documentation <http://www.pymunk.org/en/latest/pymunk.html>`_

        `Youtube Tutorial <https://youtu.be/pRk---rdrbo>`_

    *   A low frame rate might cause some objects to pass static objects as
        they don't register collisions finely enough. Trying to increase the
        config frame rate might solve the problem.

Examples
--------
.. manim:: TwoObjectsFalling
        
        from manim_physics import *
        # use a SpaceScene to utilize all specific rigid-mechanics methods
        class TwoObjectsFalling(SpaceScene):
            def construct(self):
                circle = Circle().shift(UP)
                circle.set_fill(RED, 1)
                circle.shift(DOWN + RIGHT)

                rect = Square().shift(UP)
                rect.rotate(PI / 4)
                rect.set_fill(YELLOW_A, 1)
                rect.shift(UP * 2)
                rect.scale(0.5)

                ground = Line([-4, -3.5, 0], [4, -3.5, 0])
                wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
                wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
                walls = VGroup(ground, wall1, wall2)
                self.add(walls)

                self.play(
                    DrawBorderThenFill(circle),
                    DrawBorderThenFill(rect),
                )
                self.make_rigid_body(rect, circle)  # Mobjects will move with gravity
                self.make_static_body(walls)  # Mobjects will stay in place
                self.wait(5)
                # during wait time, the circle and rect would move according to the simulate updater
"""

__all__ = [
    "Space",
    "_step",
    "_simulate",
    "get_shape",
    "get_angle",
    "SpaceScene",
]

from manim.mobject.opengl_compatibility import ConvertToOpenGL
import pymunk
from manim import *


class Space(Mobject, metaclass=ConvertToOpenGL):
    def __init__(self, gravity: tuple[float, float] = (0, -9.81), **kwargs):
        """An Abstract object for gravity.

        Parameters
        ----------
        gravity
            The direction and strength of gravity.
        """
        super().__init__(**kwargs)
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.sleep_time_threshold = 5


class SpaceScene(Scene):
    GRAVITY: tuple[float, float] = 0, -9.81

    def __init__(self, renderer=None, **kwargs):
        """A basis scene for all of rigid mechanics. The gravity vector
        can be adjusted with ``self.GRAVITY``.
        """
        self.space = Space(gravity=self.GRAVITY)
        super().__init__(renderer=renderer, **kwargs)

    def setup(self):
        """Used internally"""
        self.add(self.space)
        self.space.add_updater(_step)

    def add_body(self, body: Mobject):
        """Bodies refer to pymunk's object.
        This method ties Mobjects to their Bodies.
        """
        if body.body != self.space.space.static_body:
            self.space.space.add(body.body)
        self.space.space.add(body.shape)

    def make_rigid_body(
        self,
        *mobs: Mobject,
        elasticity: float = 0.8,
        density: float = 1,
        friction: float = 0.8,
    ):
        """Make any mobject movable by gravity.
        Equivalent to ``Scene``'s ``add`` function.

        Parameters
        ----------
        mobs
            The mobs to be made rigid.
        elasticity
        density
        friction
            The attributes of the mobjects in regards to
            interacting with other rigid and static objects.
        """
        for mob in mobs:
            if isinstance(mob, VGroup):
                return self.make_rigid_body(*mob)
            if not hasattr(mob, "body"):
                parts = mob.family_members_with_points()
                for p in parts:
                    self.add(p)
                    p.body = pymunk.Body()
                    p.body.position = p.get_x(), p.get_y()
                    get_angle(p)
                    if not hasattr(p, "angle"):
                        p.angle = 0
                    p.body.angle = p.angle
                    get_shape(p)
                    p.shape.density = density
                    p.shape.elasticity = elasticity
                    p.shape.friction = friction
                    p.spacescene = self

                    self.add_body(p)
                    p.add_updater(_simulate)

            else:
                if mob.body.is_sleeping:
                    mob.body.activate()

    def make_static_body(
        self, *mobs: Mobject, elasticity: float = 1, friction: float = 0.8
    ) -> None:
        """Make any mobject interactable by rigid objects.

        Parameters
        ----------
        mobs
            The mobs to be made static.
        elasticity
        friction
            The attributes of the mobjects in regards to
            interacting with rigid objects.
        """
        for mob in mobs:
            if isinstance(mob, VGroup or Group):
                return self.make_static_body(*mob)
            mob.body = self.space.space.static_body
            get_shape(mob)
            mob.shape.elasticity = elasticity
            mob.shape.friction = friction
            self.add_body(mob)

    def stop_rigidity(self, *mobs: Mobject) -> None:
        """Stop the mobjects rigidity"""
        for mob in mobs:
            if isinstance(mob, VGroup or Group):
                self.stop_rigidity(*mob)
            if hasattr(mob, "body"):
                mob.body.sleep()


def _step(space, dt):
    space.space.step(dt)


def _simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle


def get_shape(mob: VMobject) -> None:
    """Obtains the shape of the body from the mobject"""
    if isinstance(mob, Circle):
        mob.shape = pymunk.Circle(body=mob.body, radius=mob.radius)
    elif isinstance(mob, Line):
        mob.shape = pymunk.Segment(
            mob.body,
            (mob.get_start()[0], mob.get_start()[1]),
            (mob.get_end()[0], mob.get_end()[1]),
            mob.stroke_width - 3.95,
        )
    elif issubclass(type(mob), Rectangle):
        width = np.linalg.norm(mob.get_vertices()[1] - mob.get_vertices()[0])
        height = np.linalg.norm(mob.get_vertices()[2] - mob.get_vertices()[1])
        mob.shape = pymunk.Poly.create_box(mob.body, (width, height))
    elif issubclass(type(mob), Polygram):
        vertices = [(a, b) for a, b, c in mob.get_vertices() - mob.get_center()]
        mob.shape = pymunk.Poly(mob.body, vertices)
    else:
        mob.shape = pymunk.Poly.create_box(mob.body, (mob.width, mob.height))


def get_angle(mob: VMobject) -> None:
    """Obtains the angle of the body from the mobject.
    Used internally for updaters.
    """
    if issubclass(type(mob), Polygon):
        vec1 = mob.get_vertices()[0] - mob.get_vertices()[1]
        vec2 = type(mob)().get_vertices()[0] - type(mob)().get_vertices()[1]
        mob.angle = angle_between_vectors(vec1, vec2)
    elif isinstance(mob, Line):
        mob.angle = mob.get_angle()
