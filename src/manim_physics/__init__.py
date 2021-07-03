__version__ = "0.2.1"
__all__ = [
    "Space", "step", "simulate", "get_shape", "get_angle", "SpaceScene", # rigid_mechanics
    "Charge", "ElectricField", "Current", "CurrentMagneticField", "BarMagnet", "BarMagneticField",  # electromagnetism
    "LinearWave", "RadialWave", "StandingWave" # Wave
]

from .electromagnetism import *
from .rigid_mechanics import *
from .wave import *
