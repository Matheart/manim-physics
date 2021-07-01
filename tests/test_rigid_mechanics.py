from manim_physics import *
from manim_physics.rigid_mechanics import * 

def test_version():
    assert __version__ == '0.1.1'

class OneObjectsFalling(Scene):
    def construct(self):
        space = Space(dt = 1 / self.camera.frame_rate) 
        # space is the basic unit of simulation (just like scene)
        # you can add rigid bodies, shapes and joints to it 
        # and then step them all forward together through time
        self.add(space)

        circle = Circle().shift(UP).set_fill(RED, 1).shift(DOWN + RIGHT)
        circle.body = pymunk.Body() # add a rigid body to the circle
        circle.body.position = \
            circle.get_center()[0], \
            circle.get_center()[1]
        circle.shape = pymunk.Circle(
            body = circle.body,
            radius = circle.width / 2
        ) # set the shape of the circle in pymunk
        circle.shape.elasticity = 0.8
        circle.shape.density = 1
        circle.angle = 0

        ground = Rectangle(width = 8, height = 0.1, color = GREEN).set_fill(GREEN, 1)
        ground.shift(3.5*DOWN)
        ground.body = space.space.static_body 
        # static body means the object keeps stationary even after collision
        ground.shape = pymunk.Segment(ground.body, (-4, -3.5), (4, -3.5), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        self.add(circle)
        space.add_body(circle)
        space.add_body(ground)

        space.add_updater(step)
        circle.add_updater(simulate)
        self.wait(10)
        # during wait time, the circle would move according to the simulate updater

class TwoObjectsFalling(Scene):
    def construct(self):
        space = Space(dt = 1 / self.camera.frame_rate) 
        # space is the basic unit of simulation (just like scene)
        # you can add rigid bodies, shapes and joints to it 
        # and then step them all forward together through time
        self.add(space)

        circle = Circle().shift(UP)
        circle.set_fill(RED, 1)
        circle.shift(DOWN + RIGHT)

        circle.body = pymunk.Body() # add a rigid body to the circle
        circle.body.position = \
            circle.get_center()[0], \
            circle.get_center()[1]
        circle.shape = pymunk.Circle(
            body = circle.body,
            radius = circle.width / 2
        ) # set the shape of the circle in pymunk
        circle.shape.elasticity = 0.8
        circle.shape.density = 1
        circle.angle = 0

        rect = Square().shift(UP)
        rect.rotate(PI/4)
        rect.set_fill(YELLOW_A, 1)
        rect.shift(UP*2)
        rect.scale(0.5)

        rect.body = pymunk.Body()
        rect.body.position = \
            rect.get_center()[0], \
            rect.get_center()[1]
        rect.body.angle = PI / 4
        rect.shape = pymunk.Poly.create_box(rect.body, (1, 1))
        rect.shape.elasticity = 0.4
        rect.shape.density = 2
        rect.shape.friction = 0.8
        rect.angle = PI / 4

        ground = Rectangle(width = 8, height = 0.1, color = GREEN).set_fill(GREEN, 1)
        ground.shift(3.5*DOWN)
        ground.body = space.space.static_body 
        # static body means the object keeps stationary even after collision
        ground.shape = pymunk.Segment(ground.body, (-4, -3.5), (4, -3.5), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        wall1 = Rectangle(width = 0.1, height = 7, color = GREEN).set_fill(GREEN, 1)
        wall1.shift(3.95*LEFT)
        wall1.body = space.space.static_body
        wall1.shape = pymunk.Segment(wall1.body, (-4, -5), (-4, 5), 0.1)
        wall1.shape.elasticity = 0.99
        self.add(wall1)

        wall2 = Rectangle(width = 0.1, height = 7, color = GREEN).set_fill(GREEN, 1)
        wall2.shift(3.95*RIGHT) 
        wall2.body = space.space.static_body
        wall2.shape = pymunk.Segment(wall2.body, (4, -5), (4, 5), 0.1)
        wall2.shape.elasticity = 0.99
        self.add(wall2)

        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(rect))
        self.wait()

        space.add_body(circle)
        space.add_body(rect)
        space.add_body(ground)
        space.add_body(wall1)
        space.add_body(wall2)

        space.add_updater(step)
        circle.add_updater(simulate)
        rect.add_updater(simulate)
        self.wait(10)
        # during wait time, the circle and rect would move according to the simulate updater

class TexFalling(Scene):
    def construct(self):
        space = Space(1 / self.camera.frame_rate)
        self.add(space)
        space.add_updater(step)

        ground = Rectangle(width = 10, height = 0.08, color = GREEN).set_fill(GREEN, 1).shift(3 * DOWN)
        #ground = Line(5 * LEFT + 3 * DOWN, 5*RIGHT+3*DOWN)
        self.play(FadeIn(ground))
        ground.body = space.space.static_body
        ground.shape = pymunk.Segment(ground.body, (-5, -3), (5, -3), 0.08)
        ground.shape.elasticity = 0.9
        ground.shape.friction = 0.8
        space.add_body(ground)

        def add_physic(text):
            parts = text.family_members_with_points()
            for p in parts:
                self.add(p)
                p.body = pymunk.Body()
                p.body.position = \
                    p.get_center()[0], \
                    p.get_center()[1]
                p.shape = pymunk.Poly.create_box(
                    p.body, (p.width, p.height)
                )
                p.shape.elasticity = 0.4
                p.shape.density = 1
                p.shape.friction = 0.8

                p.angle = 0
                space.add_body(p)
                p.add_updater(simulate)

        forms = [
            r"e^{i\pi}+1=0",
            r"\cos(x+y)=\cos x \cos y - \sin x \sin y",
            r"\displaystyle \int_{-\infty }^{\infty }e^{-x^{2}}\,dx={\sqrt {\pi }}"
        ]
        cols = [RED, BLUE, YELLOW]
        for f, col in zip(forms, cols):
            text = MathTex(f, color = col)
            self.play(Write(text))
            self.remove(text)
            add_physic(text)

            self.wait(2)