from manim import *
from manim_physics.wave import *

class LinearWaveExampleScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(60*DEGREES,-45*DEGREES)
        wave = LinearWave()
        self.add(wave)
        wave.start_wave()
        self.wait()
        wave.stop_wave()