"""
This package is an example that shows a number of allowed and disallowed
imports.

Running the flake8 plugin 'packaway-import' should result in a number of
errors::

    $ flake8 --ignore F401 .
    ./office/api.py:7:1: DEP401 Importing private name 'person._reading'.
    ./office/api.py:13:1: DEP401 Importing private name '_legal._compliance'.
    ./office/_hours.py:2:1: DEP401 Importing private name '_accounting._booking'.
    ./office/_legal/_compliance.py:8:1: DEP401 Importing private name '_accounting._booking'.
    ./person/_greeting.py:5:1: DEP401 Importing private name '_reading._private_name'.
    ./person/api.py:5:1: DEP401 Importing private name '_reading._private_name'.

For demo purposes, imports are unused and therefore the F401 error code is
ignored.
"""
