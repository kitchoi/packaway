Release 0.2.0
=============

Features
--------
- Add ``--disallowed`` option in the flake8 (also configurable in file)
  for specifying disallowed imports using regular expressions.

Fixes
-----
- Fix excluding double preceding underscore in the packaging rule.
  Imports such as ``__version__`` is now considered a violation and may
  need to be excused locally.

Bugfix 0.1.3
============
- Fix missing author in setup.py
- Fix handling of --top-level-dir when running flake8 from
  a different directory and absolute imports.
- Add Changelog.

Release 0.1.0
=============

Initial release that contains a flake8 plugin.