__module_test__ = "electromagnetism"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.electromagnetism.electrostatics import *
from manim_physics.electromagnetism.magnetostatics import *


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
    wire = Wire(Circle(2).rotate(PI / 2, UP))
    field = MagneticField(wire)
    scene.add(field, wire)


@frames_comparison(base_scene=ThreeDScene)
def test_magnetic_field_multiple_wires(scene):
    wire1 = Wire(Circle(2).rotate(PI / 2, RIGHT).shift(UP * 2))
    wire2 = Wire(Circle(2).rotate(PI / 2, RIGHT).shift(UP * -2))
    mag_field = MagneticField(wire1, wire2)
    scene.set_camera_orientation(PI / 3, PI / 4)
    scene.add(wire1, wire2, mag_field)
