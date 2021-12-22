Contributing
============

The manim-physics plugin contains objects that are classified
into several main branches, now including rigid mechanics
simulation, electromagnetism and wave.

If you want to add more objects to the plugin, The classes
of the objects should be placed in the python file of
corresponding branch, for example, ``wave.py``, and place it under
the folder ``src\manim_physics``. The tests of objects should be
named as ``test_thefilename.py`` such as ``test_wave.py``, with some
documentation, so the maintainer of this repo could ensure
that it runs as expected.
