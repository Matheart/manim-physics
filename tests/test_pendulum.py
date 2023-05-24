__module_test__ = "pendulum"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.pendulum import *


@frames_comparison(base_scene=SpaceScene)
def test_pendulum(scene: SpaceScene):
    pends = VGroup(*[Pendulum(i) for i in np.linspace(1, 5, 7)])
    scene.add(pends)
    for p in pends:
        scene.make_rigid_body(*p.bobs)
        p.start_swinging()
        scene.wait(10)


@frames_comparison(base_scene=SpaceScene)
def test_multipendulum(scene):
    p = MultiPendulum(RIGHT, LEFT)
    scene.add(p)
    scene.make_rigid_body(*p.bobs)
    p.start_swinging()
    scene.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
    scene.wait(10)
