=========
Changelog
=========

**v0.3.0**
==========
Breaking Changes
----------------
- Huge library refactor.

  - :class:`~.MagneticField` now takes a :class:`~.Wire` parameter. This allows
    for a 3D field.
  - Optimized field functions for both :class:`~.ElectricField` and
    :class:`~.MagneticField`.

**v0.2.5**
==========
Bugfixes
--------
- ``VGroup`` s can be whole rigid bodies. Support for ``SVGMobject`` s

**v0.2.4**
==========
2021.12.25

New Features
------------
- Hosted `official documentation
  <https://manim-physics.readthedocs.io/en/latest/>`_ on
  readthedocs. The readme might be restructured due to redundancy.
- New ``lensing`` module: Mobjects including ``Lens`` and ``Ray`` 
- ``SpaceScene`` can now specify the gravity vector.
- Fixed ``ConvertToOpenGL`` import error for ``manim v0.15.0``.

Improvements
-------------
- Combined ``BarMagneticField`` with ``CurrentMagneticField`` into
  ``MagneticField``.
- Improved the updaters for ``pendulum`` module. Frame rate won't show any
  lagging in the pendulum rods.

Bugfixes
---------
- Updated deprecated parameters in the ``wave`` module.

**v0.2.3**
==========
2021.07.14

Bugfixes
--------
- Fix the small arrow bug in ``ElectricField``

**v0.2.2**
==========
2021.07.06

New objects
-----------
- **Rigid Mechanics**: Pendulum

Bugfixes
--------
- Fix the ``__all__`` bug, now ``rigid_mechanics.py`` can run normally.

Improvements
------------
- Rewrite README.md to improve its readability

**v0.2.1**
==========
2021.07.03

New objects
-----------
- **Electromagnetism**: Charge, ElectricField, Current, CurrentMagneticField,
  BarMagnet, and BarMagnetField
- **Wave**: LinearWave, RadialWave, StandingWave

Bugfixes
--------
- Fix typo

Improvements
------------
- Simplify rigid-mechanics

**v0.2.0**
==========
2021.07.01

Breaking Changes
----------------
- Objects in the manim-physics plugin are classified into several **main
  branches** including rigid mechanics simulation, electromagnetism and wave.
