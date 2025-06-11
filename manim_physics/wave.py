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
    def __init__(self,*sources:Optional[np.ndarray],amplitude = 1, wavelength = 1, angular_frequency = 2*PI, x_range:Iterable [float]  =  [-5,5], y_range:Iterable [float] = [-5,5],start_when = 0 ,angle_range =[0,TAU], radial_distance=1,**kwargs):
    
        """
        This class aims to provide a highly flexible way to simulate radial waves.
        You can chose to simply update an already propagated wave or make it propagate with time from any coordinate (source coordinate is recommended for obvious reasons).
        You may choose to define it in a rectangular region or a circular region
        If there are multiple sources in a singular scene and you wish the sources to NOT emit waves at same time, you can do that using the start_when parameter. 
        #### NOTE: x_range and y_range are used to define a rectangular region. angle_range and radial_distance are used if you want a Circular Domain/Region ####
    Parameters
    ----------
    *sources : Optional[np.ndarray]
        One or more 3D coordinates (as NumPy arrays) representing wave sources.
        Each source emits a radial wave centered at its position.
    
    amplitude : float, default=1
        Maximum height (z-displacement) of the wave. Controls the intensity of oscillation.
    
    wavelength : float, default=1
        Spatial wavelength of the wave. Affects the spacing between wavefronts.
    
    angular_frequency : float, default=2 * PI
        Angular frequency in radians per second. Determines how fast the wave oscillates with time.
    
    x_range : Iterable[float], default=[-5, 5]
        Range along the x-axis defining the horizontal extent of the wave surface.
    
    y_range : Iterable[float], default=[-5, 5]
        Range along the y-axis defining the vertical extent of the wave surface.

        
    
    start_when : float, default=0
        Time (in seconds) after which the wave source begins emitting. Useful when there are multiple sources in a scene but one source emits after another source
    
    angle_range : Iterable[float], default=[0, TAU]
        Angular emission range in radians. Defines the directionality of the source (e.g., for simulating diffraction through slits or apertures).
        # Use it if you want a Circular Domain / Describing the wave in polar coordinate#
        
    radial_distance: 
        The radial coordinate measured outward from the propagation_center (mentioned later), used when expressing the wave surface in polar coordinates.
    """

        self.angle_range = angle_range
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.angular_frequency = angular_frequency
        self.time = 0
        self.kwargs = kwargs
        self.sources = sources
        self.wave_speed = angular_frequency*wavelength/(2*PI)
        self.start_when=start_when
        self.radial_distance = radial_distance
        if (start_when==0): 
            super().__init__(
                lambda u, v: np.array([u, v, self._radial_wave(u, v, sources)]),
                u_range=x_range,
                v_range=y_range,
                **kwargs,
            )
        else: #If you want the wave to start after a delay, this block is executed, it creates a surface with 0 sq unit area 
            super().__init__(
                lambda u, v: np.array([u, v, 0]),
                u_range=[0,0],
                v_range=[0,0],
                **kwargs,
            )


    """
    #Radial wave with rectangular domain
    #This method takes care of Principle of Superposition"""
    def _radial_wave(self, u:float, v:float, sources:Iterable[np.ndarray]): 
        z = 0
        for each_source in sources:
            x0, y0, _ = each_source
            z += self.amplitude * np.sin( (2*PI/self.wavelength) * np.sqrt( (u-x0)**2 + (v-y0)**2 ) - self.angular_frequency * self.time)
        return z



    """
    Radial wave but with circular domain i.e wave `z` is a function of r and θ (theta) and time t
    z(r,θ,t) = A sin(kr - wt)/sqrt(r+1)
    r+1 to avoid singularity at r=0    
    This method takes care of Principle of Superposition 
    """
    def _radial_wave_radially(self, u:float, v:float, sources:Iterable[np.ndarray]): 
        z=0
        for each_source in sources:
                r = u
                theta = v
                x0 , y0 , _ = each_source
                x = self.propagation_center[0] + r*np.cos(theta)
                y = self.propagation_center[1] + r*np.sin(theta)
                z += self.amplitude * np.sin( (2*PI/self.wavelength) *  np.sqrt((x-x0)**2 + (y-y0)**2) - self.angular_frequency * self.time)
        return np.array([x,y,z])
 

    """Updating the wave (with rectangular domain)"""
    def wave_updater(self,mob,dt):
        self.time += dt
        mob.match_points(
            Surface(
                lambda u,v: ([u,v,self._radial_wave(u,v,self.sources)]),
                u_range = self.u_range,
                v_range = self.v_range,
                **self.kwargs
            )
        )

    """Updating the wave (circular domain)"""
    def wave_updater_radially(self,mob,dt):
        self.time += dt
            
        mob.match_points(
        Surface(
            lambda u,v: (self._radial_wave_radially(u,v,self.sources)),
            u_range = [0, self.radial_distance],
            v_range = [self.angle_range[0] , self.angle_range[1]],
            **self.kwargs
            )
        )

    """    #Updating the wave (with rectangular domain) AS it is PROPAGATING with time after a specific amount of time that has passed"""    
    def _propagate_updater(self,mob,dt):
        self.time += dt
        dist_travelled = self.wave_speed * self.time 
        tempx = dist_travelled - self.propagation_center[0]
        tempy = dist_travelled - self.propagation_center[1]
    
        
        if self.time >= self.start_when:
            mob.match_points(
            Surface(
                lambda u,v: ([u,v,self._radial_wave(u,v,self.sources)]),
                u_range = [-tempx + self.propagation_center[0] , tempx + self.propagation_center[0]],
                v_range = [-tempy + self.propagation_center[1] , tempy + self.propagation_center[1]],
                **self.kwargs
                )
            )


    """    #Updating the wave (with circular domain) AS it is PROPAGATING with time after a specific amount of time that has passed"""
    def _propagate_radially_updater(self,mob,dt):
        
        self.time += dt
        if self.time - self.start_when >= 0:
            
            mob.match_points(
            Surface(
                lambda u,v: (self._radial_wave_radially(u,v,self.sources)),
                u_range = [0, (self.time - self.start_when)*self.wave_speed],
                v_range = [self.angle_range[0] , self.angle_range[1]],
                **self.kwargs
                )
            )


    """
    Parameter
    propagation_center: It is the point from which you want the wave to propagate outwards. 
                        Passing in the source point is recommended in case of a wave due to singular point source
                        In case of a wave formed due to superimposing two waves (or more) pass the coordinates where those 2 (or more) waves interact with each other
    This wave has a rectangular domain
    """
    def propagate_with_time(self,propagation_center:Optional[np.ndarray]):
        self.propagation_center = propagation_center
        self.add_updater(self._propagate_updater)


    """
    Same method as previous one except the wave in this case has a circular domain
    """
    def propagate_radially_with_time(self,propagation_center:Optional[np.ndarray]):
        self.propagation_center = propagation_center
        self.add_updater(self._propagate_radially_updater)

        
    """Add the updater to the wave (with rectangular domain)"""
    def start_updating_wave(self):
        self.add_updater(self.wave_updater)


    """Add the updater to the wave (with circular domain)"""
    def start_updating_wave_radially(self):
        self.add_updater(self.wave_updater_radially)

    """Remove the updaters"""
    def stop_updating(self):
        self.remove_updater(self.wave_updater)
        self.remove_updater(self.wave_updater_radially)


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
