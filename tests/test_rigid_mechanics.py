from manim import *
from manim_physics import __version__
from manim_physics.rigid_mechanics import *

class OneObjectFalling(Scene):
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

        self.play(DrawBorderThenFill(circle), DrawBorderThenFill(rect))
        self.make_rigid_body(rect, circle)  # Mobjects will move with gravity
        self.make_static_body(walls)  # Mobjects will stay in place
        self.wait(10)
        # during wait time, the circle and rect would move according to the simulate updater


class TexFalling(SpaceScene):
    def construct(self):
        ground = Line(LEFT * 5, RIGHT * 5, color=GREEN).shift(DOWN)
        self.play(FadeIn(ground))
        self.make_static_body(ground)
        forms = [
            r"e^{i\pi}+1=0",
            r"\cos(x+y)=\cos x \cos y - \sin x \sin y",
            r"\displaystyle \int_{-\infty }^{\infty }e^{-x^{2}}\,dx={\sqrt {\pi }}",
        ]
        cols = [RED, BLUE, YELLOW]
        for f, col in zip(forms, cols):
            text = MathTex(f, color=col)
            self.play(Write(text))
            self.make_rigid_body(text[0])
            self.wait(2)
        # Some characters can pass through a static body if the frame rate is low.
        # Try increasing frame rate by rendering at a higher quality.
