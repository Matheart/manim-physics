Example Gallery
===============
Some examples made with ``manim-phyics``

.. manim:: TexFalling
    :ref_classes: SpaceScene

    from manim_physics import *

    class TexFalling(SpaceScene):
        def construct(self):
            ground = Line(LEFT * 5, RIGHT * 5, color=ORANGE).shift(DOWN)
            self.add(ground)
            self.make_static_body(ground)
            forms = [
                r"e^{i\pi}+1=0",
                r"\cos(x+y)=\cos x \cos y - \sin x \sin y",
                r"\displaystyle \int_{-\infty }^{\infty }e^{-x^{2}}\,dx={\sqrt {\pi }}",
            ]
            cols = [RED, BLUE, YELLOW]
            for f, col in zip(forms, cols):
                text = MathTex(f, color=col)
                self.add(text)
                self.make_rigid_body(text[0])
                self.wait(2)
            # Some characters can pass through a static body if the frame rate is low.
            # Try increasing frame rate by rendering at a higher quality.
