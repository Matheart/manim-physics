__module_test__ = "waves"

from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

from manim_physics.wave import *


@frames_comparison()
def test_linearwave(scene):
    wave = LinearWave()
    wave.set_time(2)
    scene.add(wave)


@frames_comparison()
def test_radialwave(scene):
    wave = RadialWave(
        LEFT * 2 + DOWN * 5,  # Two source of waves
        RIGHT * 2 + DOWN * 5,
        checkerboard_colors=[BLUE_D],
        stroke_width=0,
    )
    wave.set_time(2)
    scene.add(wave)


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
