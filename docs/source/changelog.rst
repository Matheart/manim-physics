==========
Changelogs
==========

v0.2.4 
======
-2021.12.25

New Features
------------
*   :class:`~SpaceScene` can now specify the gravity vector.
*   Combined ``BarMagneticField`` with ``CurrentMagneticField`` into :class:`~MagneticField` .
*   Fixed ``ConvertToOpenGL`` import error for ``manim v0.15.0``.

Improvements
------------
*   Hosted `official documentation <https://manim-physics.readthedocs.io/en/latest/>`_ on readthedocs.
    The readme might be restructured due to redundancy.
*   Improved the updaters for ``pendulum`` module. Low frame rate won't show any lagging in the pendulum rods.

Bugfixes
--------
*   Updated deprecated parameters in the ``wave`` module.

v0.2.3
======
-14.07.2021

Bugfixes
--------
*   Fix the small arrow bug in :class:`~ElectricField`

v0.2.2
======
-06.07.2021

New Objects
-----------
*   Rigid Mechanics: Pendulum

Bugfixes
--------
*   Fix the ``__all__`` bug, now ``rigid_mechanics.py`` can run normally.

Improvements
------------
*   Rewrite ``README.md`` to improve its readability

v0.2.1
======
-03.07.2021

New Objects
-----------
*   Electromagnetism: Charge, ElectricField, Current, CurrentMagneticField,
    BarMagnet, and BarMagnetField
*   Wave: LinearWave, RadialWave, StandingWave

Bugfixes
--------
*   Fix typo

v0.2.0
======
-01.07.2021

Breaking Changes
----------------
*   Objects in the manim-physics plugin are classified into several main
    branches including rigid mechanics simulation, electromagnetism and wave.
