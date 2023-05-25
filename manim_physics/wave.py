"""3D and 2D Waves module."""

from __future__ import annotations
from typing import Iterable, Optional

from manim import *

__all__ = [
    "LinearWave",
    "RadialWave",
    "StandingWave",
]


try:
    # For manim < 0.15.0
    from manim.mobject.opengl_compatibility import ConvertToOpenGL
except ModuleNotFoundError:
    # For manim >= 0.15.0
    from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL


class RadialWave(Surface, metaclass=ConvertToOpenGL):
    def __init__(
        self,
        *sources: Optional[np.ndarray],
        wavelength: float = 1,
        period: float = 1,
        amplitude: float = 0.1,
        x_range: Iterable[float] = [-5, 5],
        y_range: Iterable[float] = [-5, 5],
        **kwargs,
    ) -> None:
        """A 3D Surface with waves moving radially.

        Parameters
        ----------
        sources
            The sources of disturbance.
        wavelength
            The wavelength of the wave.
        period
            The period of the wave.
        amplitude
            The amplitude of the wave.
        x_range
            The range of the wave in the x direction.
        y_range
            The range of the wave in the y direction.
        kwargs
            Additional parameters to be passed to :class:`~Surface`.

        Examples
        --------
        .. manim:: RadialWaveExampleScene

            class RadialWaveExampleScene(ThreeDScene):
                def construct(self):
                    self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
                    wave = RadialWave(
                        LEFT * 2 + DOWN * 5,  # Two source of waves
                        RIGHT * 2 + DOWN * 5,
                        checkerboard_colors=[BLUE_D],
                        stroke_width=0,
                    )
                    self.add(wave)
                    wave.start_wave()
                    self.wait()
                    wave.stop_wave()
        """
        self.wavelength = wavelength
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.kwargs = kwargs
        self.sources = sources

        super().__init__(
            lambda u, v: np.array([u, v, self._wave_z(u, v, sources)]),
            u_range=x_range,
            v_range=y_range,
            **kwargs,
        )

    def _wave_z(self, u: float, v: float, sources: Iterable[np.ndarray]) -> float:
        z = 0
        for source in sources:
            x0, y0, _ = source
            z += self.amplitude * np.sin(
                (2 * PI / self.wavelength) * ((u - x0) ** 2 + (v - y0) ** 2) ** 0.5
                - 2 * PI * self.time / self.period
            )
        return z

    def _update_wave(self, mob: Mobject, dt: float) -> None:
        self.time += dt
        mob.match_points(
            Surface(
                lambda u, v: np.array([u, v, self._wave_z(u, v, self.sources)]),
                u_range=self.u_range,
                v_range=self.v_range,
                **self.kwargs,
            )
        )

    def start_wave(self):
        """Animate the wave propagation."""
        self.add_updater(self._update_wave)

    def stop_wave(self):
        """Stop animating the wave propagation."""
        self.remove_updater(self._update_wave)


class LinearWave(RadialWave):
    def __init__(
        self,
        wavelength: float = 1,
        period: float = 1,
        amplitude: float = 0.1,
        x_range: Iterable[float] = [-5, 5],
        y_range: Iterable[float] = [-5, 5],
        **kwargs,
    ) -> None:
        """A 3D Surface with waves in one direction.

        Parameters
        ----------
        wavelength
            The wavelength of the wave.
        period
            The period of the wave.
        amplitude
            The amplitude of the wave.
        x_range
            The range of the wave in the x direction.
        y_range
            The range of the wave in the y direction.
        kwargs
            Additional parameters to be passed to :class:`~Surface`.

        Examples
        --------
        .. manim:: LinearWaveExampleScene

            class LinearWaveExampleScene(ThreeDScene):
                def construct(self):
                    self.set_camera_orientation(60 * DEGREES, -45 * DEGREES)
                    wave = LinearWave()
                    self.add(wave)
                    wave.start_wave()
                    self.wait()
                    wave.stop_wave()
        """
        super().__init__(
            ORIGIN,
            wavelength=wavelength,
            period=period,
            amplitude=amplitude,
            x_range=x_range,
            y_range=y_range,
            **kwargs,
        )

    def _wave_z(self, u: float, v: float, sources: Iterable[np.ndarray]) -> float:
        return self.amplitude * np.sin(
            (2 * PI / self.wavelength) * u - 2 * PI * self.time / self.period
        )


class StandingWave(ParametricFunction):
    def __init__(
        self,
        n: int = 2,
        length: float = 4,
        period: float = 1,
        amplitude: float = 1,
        **kwargs,
    ) -> None:
        """A 2D standing wave.

        Parameters
        ----------
        n
            Harmonic number.
        length
            The length of the wave.
        period
            The time taken for one full oscillation.
        amplitude
            The maximum height of the wave.
        kwargs
            Additional parameters to be passed to :class:`~ParametricFunction`.

        Examples
        --------
        .. manim:: StandingWaveExampleScene

            from manim_physics import *

            class StandingWaveExampleScene(Scene):
                def construct(self):
                    wave1 = StandingWave(1)
                    wave2 = StandingWave(2)
                    wave3 = StandingWave(3)
                    wave4 = StandingWave(4)
                    waves = VGroup(wave1, wave2, wave3, wave4)
                    waves.arrange(DOWN).move_to(ORIGIN)
                    self.add(waves)
                    for wave in waves:
                        wave.start_wave()
                    self.wait()
        """
        self.n = n
        self.length = length
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.kwargs = {**kwargs}

        super().__init__(
            lambda t: np.array([t, amplitude * np.sin(n * PI * t / length), 0]),
            t_range=[0, length],
            **kwargs,
        )
        self.shift([-self.length / 2, 0, 0])

    def _update_wave(self, mob: Mobject, dt: float) -> None:
        self.time += dt
        mob.become(
            ParametricFunction(
                lambda t: np.array(
                    [
                        t,
                        self.amplitude
                        * np.sin(self.n * PI * t / self.length)
                        * np.cos(2 * PI * self.time / self.period),
                        0,
                    ]
                ),
                t_range=[0, self.length],
                **self.kwargs,
            ).shift(self.wave_center + [-self.length / 2, 0, 0])
        )

    def start_wave(self):
        self.wave_center = self.get_center()
        self.add_updater(self._update_wave)

    def stop_wave(self):
        self.remove_updater(self._update_wave)
