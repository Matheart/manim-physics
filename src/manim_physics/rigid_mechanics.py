__all__ = ["Space", "step", "simulate", "get_shape", "get_angle", "SpaceScene"]

from manim.mobject.opengl_compatibility import ConvertToOpenGL
import pymunk
from manim import *


class Space(Mobject, metaclass=ConvertToOpenGL):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.space = pymunk.Space()
        self.space.gravity = 0, -9.8
        self.space.sleep_time_threshold = 5


class SpaceScene(Scene):
    def __init__(self, renderer=None, **kwargs):
        self.space = Space()
        super().__init__(renderer=renderer, **kwargs)

    def setup(self):
        self.add(self.space)
        self.space.add_updater(step)

    def add_body(self, body):
        if body.body != self.space.space.static_body:
            self.space.space.add(body.body)
        self.space.space.add(body.shape)

    def make_rigid_body(
        self,
        *mobs,
        elasticity=0.8,
        density=1,
        friction=0.8,
    ):
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
                    p.add_updater(simulate)

            else:
                if mob.body.is_sleeping:
                    mob.body.activate()

    def make_static_body(self, *mobs, elasticity=1, friction=0.8):
        for mob in mobs:
            if isinstance(mob, VGroup or Group):
                return self.make_static_body(*mob)
            mob.body = self.space.space.static_body
            get_shape(mob)
            mob.shape.elasticity = elasticity
            mob.shape.friction = friction
            self.add_body(mob)

    def stop_rigidity(self, *mobs):
        for mob in mobs:
            if isinstance(mob, VGroup or Group):
                self.stop_rigidity(*mob)
            if hasattr(mob, "body"):
                mob.body.sleep()


def step(space, dt):
    space.space.step(dt)


def simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle


def get_shape(mob):
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


def get_angle(mob):
    if issubclass(type(mob), Polygon):
        vec1 = mob.get_vertices()[0] - mob.get_vertices()[1]
        vec2 = type(mob)().get_vertices()[0] - type(mob)().get_vertices()[1]
        mob.angle = angle_between_vectors(vec1, vec2)
    elif isinstance(mob, Line):
        mob.angle = mob.get_angle()
