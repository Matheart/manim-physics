__module_test__ = "waves"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.wave import *


@frames_comparison(base_scene=ThreeDScene)
def test_linearwave(scene):
    scene.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
    wave = LinearWave()
    scene.add(wave)
    wave.start_wave()
    scene.wait()
    wave.stop_wave()


@frames_comparison(base_scene=ThreeDScene)
def test_radialwave(scene):
    scene.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
    wave = RadialWave(
        LEFT * 2 + DOWN * 5,  # Two source of waves
        RIGHT * 2 + DOWN * 5,
        checkerboard_colors=[BLUE_D],
        stroke_width=0,
    )
    scene.add(wave)
    wave.start_wave()
    scene.wait()
    wave.stop_wave()


@frames_comparison
def test_standingwave(scene):
    wave1 = StandingWave(1)
    wave2 = StandingWave(2)
    wave3 = StandingWave(3)
    wave4 = StandingWave(4)
    waves = VGroup(wave1, wave2, wave3, wave4)
    waves.arrange(DOWN).move_to(ORIGIN)
    scene.add(waves)
    for wave in waves:
        wave.start_wave()
    scene.wait()
