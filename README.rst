Packaging Static Checker
========================

This is a project for experimenting with ways to (optionally) enforce
encapsulation and access control with Python, using static code analysis.

The ``examples`` folder contains Python distributions for illustrating
different packaging scenarios.

To install
----------

To use the optional Flake8 plugin, one should have ``flake8`` installed in
their environment, and then install ``packaway`` from the source here::

    $ pip install .


Examples
--------

Trying to run the flake8 plugin with the ``examples/test_and_trace`` folder
should result in two errors.

For a module ``_duration`` under this absolute name::

    test_and_trace.screening._symptom_checker._algorithm._duration

This import is okay::

    from test_and_trace.screening._symptom_checker._symptom_names import NAMES

This is because ``_symptom_checker`` is visible to anything within
``_symptom_checker``, and the ``_duration`` is within the ``_symptom_checker``
package.

But this is not allowed::

    from test_and_trace.screening._urgency_checker import _priority

Because although ``_urgency_checker`` is visible to anything within
``screening``, this import is accessing a private name ``_priority`` within
``_urgency_checker`` and ``_priority`` should only be visible
within ``_urgency_checker``.

But this is okay::

    from test_and_trace.screening._urgency_checker import api

Because ``api`` is public, it is just as visible as ``_urgency_checker`` is
to anything within ``screening``.

(See ``examples/test_and_trace/screening/_symptom_checker/_algorithm/_duration.py``)
