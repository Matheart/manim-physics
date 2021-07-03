# manim-physics (Under Active Development)
## Introduction
This is a 2D physics simulation plugin that allows you to generate complicated scenes in various branches of Physics such as rigid mechanics, electromagnetism, wave etc.

Contributors: [**pdcxs**](https://github.com/pdcxs), [**Matheart**](https://github.com/Matheart), [**Iced-Tea3**](https://github.com/Iced-Tea3)

## Installation
Follow this guide: https://docs.manim.community/en/stable/installation/plugins.html?highlight=plugin. 

**Warnings: Please do not directly clone the github repo! The repo is still under development and it is not a stable version, download manim-physics through pypi.**

## Usage
In order to use `rigid_mechanics.py`, you should be familiar with pymunk. You could check [the official documentation](http://www.pymunk.org/en/latest/pymunk.html) of pymunk for reference. There is also a good [Youtube tutorial](https://youtu.be/pRk---rdrbo ) to let you better understand pymunk.

## Contribution Guidelines
The manim-physics plugin contains objects that are classified into **several main branches**, now including rigid mechanics simulation, electromagnetism and wave. 

If you want to add more objects to the plugin, The classes of the objects should be placed in the python file of corresponding branch, for example, `wave.py`, and place it under the folder src\manim_physics. The tests of objects should be named as `test_thefilename.py` such as `test_wave.py`, with some documentation, so the maintainer of this repo could ensure that it runs as expected.

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

https://user-images.githubusercontent.com/47732475/124072981-1519b580-da74-11eb-8f36-12652bfc80e0.mp4


## Other beautiful animations based on manim-physics


https://user-images.githubusercontent.com/47732475/124342625-baa96200-dbf7-11eb-996a-1f27b3625602.mp4

https://user-images.githubusercontent.com/47732475/123754200-38febf00-d8ed-11eb-937a-b93bc490f85a.mp4



https://user-images.githubusercontent.com/47732475/123754252-44ea8100-d8ed-11eb-94e9-1f6b01d8c2f8.mp4
