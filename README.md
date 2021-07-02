# manim-physics
A 2D physics simulation plugin based on Pymunk, with this plugin you could generate complicated physics scenes without struggling to use many updaters.

Contributed by [**pdcxs**](https://github.com/pdcxs) and [**Matheart**](https://github.com/Matheart)

## Installation
Follow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin

## Usage
In order to use manim-physics to generate physics animations, you should be familiar with pymunk.
You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference.

## A simple Example 

```py
# use a SpaceScene to utilize all specific rigid-mechanics methods
class TestScene(SpaceScene):
    def construct(self):
        circle = Circle().set_fill(RED, 1).shift(RIGHT)
        ground = Line(LEFT*4,RIGHT*4,color=GREEN).shift(DOWN*3.5)
        self.add(circle,ground)

        self.make_rigid_body(circle) # Mobjects will move with gravity
        self.make_static_body(ground) # Mobjects will stay in place
        self.wait(10)
        # during wait time, the circle would move according to the simulate updater
```




https://user-images.githubusercontent.com/47732475/123754164-2e442a00-d8ed-11eb-811d-4c86619e7cca.mp4



## Other beautiful animations based on manim-physics

https://user-images.githubusercontent.com/47732475/123754200-38febf00-d8ed-11eb-937a-b93bc490f85a.mp4



https://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4
