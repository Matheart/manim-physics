__all__ = [
    "LinearWave",
    "RadialWave",
    "StandingWave",
]

from manim import *


class LinearWave(ParametricSurface):
    def __init__(
        self,
        wavelength=1,
        period=1,
        amplitude=0.1,
        x_range=[-5, 5],
        y_range=[-5, 5],
        **kwargs
    ):
        self.wavelength = wavelength
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.extra = {**kwargs}
        self.u_min = x_range[0]
        self.u_max = x_range[1]
        self.v_min = y_range[0]
        self.v_max = y_range[1]

        super().__init__(
            lambda u, v: np.array(
                [
                    u,
                    v,
                    amplitude
                    * np.sin((2 * PI / wavelength) * u - 2 * PI * self.time / period),
                ]
            ),
            u_min=self.u_min,
            u_max=self.u_max,
            v_min=self.v_min,
            v_max=self.v_max,
            **kwargs
        )

    def update_wave(self, mob, dt):
        self.time += dt
        mob.become(
            ParametricSurface(
                lambda u, v: np.array(
                    [
                        u,
                        v,
                        self.amplitude
                        * np.sin(
                            (2 * PI / self.wavelength) * u
                            - 2 * PI * self.time / self.period
                        ),
                    ]
                ),
                u_min=self.u_min,
                u_max=self.u_max,
                v_min=self.v_min,
                v_max=self.v_max,
                **self.extra
            )
        )

    def start_wave(self):
        self.add_updater(self.update_wave)

    def stop_wave(self):
        self.remove_updater(self.update_wave)


class RadialWave(ParametricSurface):
    def __init__(
        self,
        *sources,
        wavelength=1,
        period=1,
        amplitude=0.1,
        x_range=[-5, 5],
        y_range=[-5, 5],
        **kwargs
    ):
        self.wavelength = wavelength
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.extra = {**kwargs}
        self.sources = sources
        self.u_min = x_range[0]
        self.u_max = x_range[1]
        self.v_min = y_range[0]
        self.v_max = y_range[1]
        super().__init__(
            lambda u, v: np.array([u, v, self.wave_z(u, v, *sources)]),
            u_min=self.u_min,
            u_max=self.u_max,
            v_min=self.v_min,
            v_max=self.v_max,
            **kwargs
        )

    def wave_z(self, u, v, *sources):
        z = 0
        for source in sources:
            x0, y0, z0 = source
            z += self.amplitude * np.sin(
                (2 * PI / self.wavelength) * ((u - x0) ** 2 + (v - y0) ** 2) ** 0.5
                - 2 * PI * self.time / self.period
            )
        return z

    def update_wave(self, mob, dt):
        self.time += dt
        mob.become(
            ParametricSurface(
                lambda u, v: np.array([u, v, self.wave_z(u, v, *self.sources)]),
                u_min=self.u_min,
                u_max=self.u_max,
                v_min=self.v_min,
                v_max=self.v_max,
                **self.extra
            )
        )

    def start_wave(self):
        self.add_updater(self.update_wave)

    def stop_wave(self):
        self.remove_updater(self.update_wave)


class StandingWave(ParametricFunction):
    def __init__(self, n=2, length=4, period=1, amplitude=1, **kwargs):
        self.n = n
        self.length = length
        self.period = period
        self.amplitude = amplitude
        self.time = 0
        self.extra = {**kwargs}

        super().__init__(
            lambda t: np.array([t, amplitude * np.sin(n * PI * t / length), 0]),
            t_range=[0, length],
            **kwargs
        )
        self.shift([-self.length / 2, 0, 0])

    def update_wave(self, mob, dt):
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
                **self.extra
            ).shift(self.wave_center + [-self.length / 2, 0, 0])
        )

    def start_wave(self):
        self.wave_center = self.get_center()
        self.add_updater(self.update_wave)

    def stop_wave(self):
        self.remove_updater(self.update_wave)
