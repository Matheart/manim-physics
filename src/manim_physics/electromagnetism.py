__all__ = [
    "Charge",
    "ElectricField",
]

from manim import *


class Charge(Dot, VGroup):
    def __init__(self, magnitude=1, point=ORIGIN, **kwargs):
        self.magnitude = magnitude
        radius = abs(magnitude) * 0.5 if abs(magnitude) < 2 else 1
        super().__init__(point=point, radius=radius * 0.3)
        if magnitude > 0:
            label = MathTex("+")
            color = RED
        else:
            label = MathTex("-")
            color = BLUE
        self.set_color(color)
        self.add(label.scale(radius).shift(point))


class ElectricField(ArrowVectorField):
    def __init__(self, *charges: Charge, **kwargs):
        super().__init__(lambda p: self.field_func(p, *charges), **kwargs)

    def field_func(self, p, *charges):
        direction = np.zeros(3)
        for charge in charges:
            p0, mag = charge.get_center(), charge.magnitude
            x, y, z = p - p0
            dist = (x ** 2 + y ** 2 + z ** 2) ** 1.5
            if (x ** 2) > 0.05 or (y ** 2) > 0.05:
                direction += mag * np.array([x / dist, y / dist, z / dist])
            else:
                direction += np.zeros(3)
        return direction

    def get_force_on_charge(self, charge):
        p0 = charge.get_center()
        return (
            Vector((self.get_vector(p0).get_end() - p0) * charge.magnitude)
            .shift(p0)
            .set_color(self.get_vector(p0).color)
        )
