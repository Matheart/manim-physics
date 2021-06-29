# manim-physics
A 2D physics simulation plugin based on Pymunk, with this plugin you could generate complicated physics scenes without struggling to use many updaters.

Contributed by [**pdcxs**](https://github.com/pdcxs) and [**Matheart**](https://github.com/Matheart)

## Installation
Follow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin

## Usage
In order to use manim-physics to generate physics animations, you should be familar with pymunk.
You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference.

## A simple Example 

```py
class TwoObjectsFalling(Scene):
    def construct(self):
        space = Space(dt = 1 / self.camera.frame_rate) 
        # space is the basic unit of simulation (just like scene)
        # you can add rigid bodies, shapes and joints to it 
        # and then step them all forward together through time
        self.add(space)

        circle = Circle().shift(UP)
        circle.set_fill(RED, 1)
        circle.shift(DOWN + RIGHT)

        circle.body = pymunk.Body() # add a rigid body to the circle
        circle.body.position = \
            circle.get_center()[0], \
            circle.get_center()[1]
        circle.shape = pymunk.Circle(
            body = circle.body,
            radius = circle.width / 2
        ) # set the shape of the circle in pymunk
        circle.shape.elasticity = 0.8
        circle.shape.density = 1
        circle.angle = 0

        rect = Square().shift(UP)
        rect.rotate(PI/4)
        rect.set_fill(YELLOW_A, 1)
        rect.shift(UP*2)
        rect.scale(0.5)

        rect.body = pymunk.Body()
        rect.body.position = \
            rect.get_center()[0], \
            rect.get_center()[1]
        rect.body.angle = PI / 4
        rect.shape = pymunk.Poly.create_box(rect.body, (1, 1))
        rect.shape.elasticity = 0.4
        rect.shape.density = 2
        rect.shape.friction = 0.8
        rect.angle = PI / 4

        ground = Rectangle(width = 8, height = 0.1, color = GREEN).set_fill(GREEN, 1)
        ground.shift(3.5*DOWN)
        ground.body = space.space.static_body 
        # static body means the object keeps static even after collision
        ground.shape = pymunk.Segment(ground.body, (-4, -3.5), (4, -3.5), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        wall1 = Rectangle(width = 0.1, height = 7, color = GREEN).set_fill(GREEN, 1)
        wall1.shift(3.95*LEFT)
        wall1.body = space.space.static_body
        wall1.shape = pymunk.Segment(wall1.body, (-4, -5), (-4, 5), 0.1)
        wall1.shape.elasticity = 0.99
        self.add(wall1)

        wall2 = Rectangle(width = 0.1, height = 7, color = GREEN).set_fill(GREEN, 1)
        wall2.shift(3.95*RIGHT) 
        wall2.body = space.space.static_body
        wall2.shape = pymunk.Segment(wall2.body, (4, -5), (4, 5), 0.1)
        wall2.shape.elasticity = 0.99
        self.add(wall2)

        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(rect))
        self.wait()

        space.add_body(circle)
        space.add_body(rect)
        space.add_body(ground)
        space.add_body(wall1)
        space.add_body(wall2)

        space.add_updater(step)
        circle.add_updater(simulate)
        rect.add_updater(simulate)
        self.wait(10)
        # during wait time, the circle and rect would move according to the simulate updater
```




https://user-images.githubusercontent.com/47732475/123754164-2e442a00-d8ed-11eb-811d-4c86619e7cca.mp4



## Other beautiful animations based on manim-physics

https://user-images.githubusercontent.com/47732475/123754200-38febf00-d8ed-11eb-937a-b93bc490f85a.mp4


https://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4