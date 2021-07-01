# manim-physics (Under Active Development)
## Introduction
This is a 2D physics simulation plugin that allows you to generate complicated scenes in various branches of Physics such as rigid mechanics, electromagnetism, wave etc.

Contributors: [**pdcxs**](https://github.com/pdcxs), [**Matheart**](https://github.com/Matheart)

## Installation
Follow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin. 

**Warnings: Please do not directly clone the github repo! The repo is still under development and it is not a stable version, download manim-physics through pypi.**

## Usage
In order to use `rigid_mechanics.py`, you should be familar with pymunk. You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference. There is also a good [Youtube tutorial](https://youtu.be/pRk---rdrbo ) to let you better understand pymunk.

## Contribution Guidelines
The manim-physics plugin contains objects that are classified into **several main branches**, now including rigid mechanics simulation, electromagnetism and wave. 

If you want to add more objects to the plugin, The classes of the objects should be placed in the python file of corresponding branch, for example, `wave.py`, and place it under the folder src\manim_physics. The tests of objects should be named as `test_thefilename.py` such as `test_wave.py`, with some documentation, so the maintainer of this repo could ensure that it runs as expected.

## A simple Example 

```py
class OneObjectsFalling(Scene):
    def construct(self):
        space = Space(dt = 1 / self.camera.frame_rate) 
        # space is the basic unit of simulation (just like scene)
        # you can add rigid bodies, shapes and joints to it 
        # and then step them all forward together through time
        self.add(space)

        circle = Circle().shift(UP).set_fill(RED, 1).shift(DOWN + RIGHT)
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

        ground = Rectangle(width = 8, height = 0.1, color = GREEN).set_fill(GREEN, 1)
        ground.shift(3.5*DOWN)
        ground.body = space.space.static_body 
        # static body means the object keeps stationary even after collision
        ground.shape = pymunk.Segment(ground.body, (-4, -3.5), (4, -3.5), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        self.add(circle)
        space.add_body(circle)
        space.add_body(ground)

        space.add_updater(step)
        circle.add_updater(simulate)
        self.wait(10)
        # during wait time, the circle would move according to the simulate updater
```

https://user-images.githubusercontent.com/47732475/124072981-1519b580-da74-11eb-8f36-12652bfc80e0.mp4


## Other beautiful animations based on manim-physics

https://user-images.githubusercontent.com/47732475/123754200-38febf00-d8ed-11eb-937a-b93bc490f85a.mp4



https://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4
