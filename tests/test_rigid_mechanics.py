from manim import *
from manim_physics import __version__
from manim_physics.rigid_mechanics import *


def test_version():
    assert __version__ == "0.1.1"


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
