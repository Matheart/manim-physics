__module_test__ = "rigid_mechanics"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.rigid_mechanics import *


@frames_comparison(base_scene=SpaceScene)
def test_rigid_mechanics(scene):
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
    scene.add(walls)

    scene.play(
        DrawBorderThenFill(circle),
        DrawBorderThenFill(rect),
    )
    scene.make_rigid_body(rect, circle)
    scene.make_static_body(walls)
    scene.wait(5)
