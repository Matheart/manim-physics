__all__ = [
    "Pendulum",
]

from manim import *
import operator as op
from math import factorial as fc


class Pendulum(VGroup):
    rod_style = {
        "stroke_width": 3,
        "stroke_color": GREY,
    }
    weight_style = {
        "stroke_width": 0,
        "fill_opacity": 1,
        "fill_color": ORANGE,
    }
    dashed_line_config = {
        "num_dashes": 25,
        "stroke_color": WHITE,
        "stroke_width": 2,
    }
    angle_arc_config = {
        "radius": 1,
        "stroke_color": WHITE,
        "stroke_width": 2,
    }
    velocity_vector_config = {
        "color": RED,
    }

    def __init__(
        self, length=3, initial_theta=0.3, top_point=UP * 2, dampen=True, **kwargs
    ):
        self.length = length
        self.initial_theta = initial_theta
        self.top_point = top_point

        self.gravity = 9.8
        self.damping = 0.1 if dampen else 0
        self.weight_diameter = 0.5
        self.omega = 0

        self.theta_label_height = 0.25
        self.set_theta_label_height_cap = False
        self.n_steps_per_frame = 100
        self.include_theta_label = True
        self.include_velocity_vector = False
        self.velocity_vector_multiple = 0.5
        self.max_velocity_vector_length_to_length_ratio = 0.5

        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_rod()
        self.create_weight()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.create_dashed_line()
        self.create_angle_arc()
        if self.include_theta_label:
            self.add_theta_label()
        if self.include_velocity_vector:
            self.add_velocity_vector()

        self.set_theta(self.initial_theta)
        self.update()

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(self.top_point)
        self.add(self.fixed_point_tracker)
        return self

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.length)
        rod.set_style(**self.rod_style)
        rod.move_to(self.get_fixed_point(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Circle()
        weight.set_width(self.weight_diameter)
        weight.set_style(**self.weight_style)
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(
            self.get_fixed_point(),
            self.get_fixed_point() + self.length * DOWN,
            **self.dashed_line_config,
        )
        line.add_updater(lambda l: l.move_to(self.get_fixed_point(), UP))
        self.add_to_back(line)

    def create_angle_arc(self):
        self.angle_arc = always_redraw(
            lambda: Arc(
                arc_center=self.get_fixed_point(),
                start_angle=-90 * DEGREES,
                angle=self.get_arc_angle_theta(),
                **self.angle_arc_config,
            )
        )
        self.add(self.angle_arc)

    def get_arc_angle_theta(self):
        # Might be changed in certain scenes
        return self.get_theta()

    def add_velocity_vector(self):
        def make_vector():
            omega = self.get_omega()
            theta = self.get_theta()
            mvlr = self.max_velocity_vector_length_to_length_ratio
            max_len = mvlr * self.rod.get_length()
            vvm = self.velocity_vector_multiple
            multiple = np.clip(vvm * omega, -max_len, max_len)
            vector = Vector(
                multiple * RIGHT,
                **self.velocity_vector_config,
            )
            vector.rotate(theta, about_point=ORIGIN)
            vector.shift(self.rod.get_end())
            return vector

        self.velocity_vector = always_redraw(make_vector)
        self.add(self.velocity_vector)
        return self

    def add_theta_label(self):
        self.theta_label = always_redraw(self.get_label)
        self.add(self.theta_label)

    def get_label(self):
        label = MathTex("\\theta")
        label.set_height(self.theta_label_height)
        if self.set_theta_label_height_cap:
            max_height = self.angle_arc.get_width()
            if label.get_height() > max_height:
                label.set_height(max_height)
        top = self.get_fixed_point()
        arc_center = self.angle_arc.point_from_proportion(0.5)
        vect = arc_center - top
        norm = np.linalg.norm(vect)
        vect = normalize(vect) * (norm + self.theta_label_height)
        label.move_to(top + vect)
        return label

    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(theta - self.get_theta())
        self.rotating_group.shift(
            self.get_fixed_point() - self.rod.get_start(),
        )
        return self

    def get_omega(self):
        return self.omega

    def set_omega(self, omega):
        self.omega = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    def start_swinging(self):
        self.add_updater(Pendulum.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(Pendulum.update_by_gravity)

    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        nspf = self.n_steps_per_frame
        for x in range(nspf):
            d_theta = omega * dt / nspf
            d_omega = (
                op.add(
                    -self.damping * omega,
                    -(self.gravity / self.length) * np.sin(theta),
                )
                * dt
                / nspf
            )
            theta += d_theta
            omega += d_omega
        self.set_theta(theta)
        self.set_omega(omega)
        return self

    def time_for_osc(self, osc=1):
        def period_expansion(n):
            if n == 0:
                return 1
            else:
                return (fc(2 * n) / (2 ** (2 * n) * (fc(n)) ** 2)) ** 2 * (
                    np.sin(self.initial_theta / 2)
                ) ** (2 * n) + period_expansion(n - 1)

        return osc * 2 * PI * (self.length / self.gravity) ** 0.5 * period_expansion(50)
