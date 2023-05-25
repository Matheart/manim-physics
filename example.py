from manim_physics import *


class MagneticFieldExample(ThreeDScene):
    def construct(self):
        wire = Wire(Circle(2).rotate(PI / 2, UP))
        mag_field = MagneticField(wire)
        self.set_camera_orientation(PI / 3, PI / 4)
        self.add(wire, mag_field)
