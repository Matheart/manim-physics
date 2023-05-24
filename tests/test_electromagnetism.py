__module_test__ = "electromagnetism"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.electromagnetism import *


@frames_comparison
def test_electric_field(scene):
    charge1 = Charge(-1, LEFT + DOWN)
    charge2 = Charge(2, RIGHT + DOWN)
    charge3 = Charge(-1, UP)
    field = ElectricField(charge1, charge2, charge3)
    scene.add(charge1, charge2, charge3)
    scene.add(field)


@frames_comparison
def test_magnetic_field(scene):
    magnet1 = BarMagnet().shift(LEFT * 2.5)
    magnet2 = Current(RIGHT * 2.5, direction=IN)
    field = MagneticField(magnet1, magnet2)
    scene.add(field, magnet1, magnet2)
