from manim import *
import pymunk


class Space(Mobject):
    def __init__(self, dt, **kargs):
        Mobject.__init__(self, **kargs)
        self.space = pymunk.Space()
        self.space.gravity = 0, -9.8
        self.dt = dt

    def add_body(self, body):
        if body.body != self.space.static_body:
            self.space.add(body.body)
        self.space.add(body.shape)


def step(space, dt):
    space.space.step(dt)


def simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle
