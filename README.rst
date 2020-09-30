Packaging Static Checker
========================

Packaway is a tool for enforcing encapsulation and access control in Python
using static code checkers.

Currently the distribution supplies a flake8 plugin.

Installing
----------

To install::

    $ pip install .

To lint your file::

    $ flake8 example.py

Packaging rules
---------------

Whether a module is internal or not is indicated by whether its name has a
single preceding underscore. If it does, then it is only "visible" within the
package the module resides. Similarly, a function whose name has a preceding
underscore is only "visible" to members with in the same module where the
function is defined.

Suppose a project has the following structure::

    ./package
        ./person
            __init__.py
            api.py
            _greeting.py
            _reading.py
        ./office
            __init__.py
            api.py
            ./_legal
                __init__.py
                api.py
                _compliance.py
            ./_accounting
                __init__.py
                api.py
                _booking.py

Take ``package.office._legal._complicance`` for example, it is only visible to
modules within ``package.office._legal`` but not modules outside of
``package.office._legal``. e.g. Importing ``package.office._legal._complicance``
in ``package.person.api`` would be a violation of the encapsulation intended.

Motivation
----------
Encapsulation is a concept not restricted to object-oriented programming, it
is an idea of lowering coupling and inter-module dependencies by hiding
information.

Many programming languages (e.g. Java, C#, C++) offer programmers way to
control over what is hidden and what is accessible via "access modifiers"
or keywords such as "public", "private" and "internal". These protections are
enforced by the compilers, but can be overruled with some efforts.

Python does not enforce encapsulations. While this is enpowering for use cases
where encapsulation matters little (e.g. scripting) and has made Python hugely
accessible to beginners, this means more disciplines are required for
developers working on large systems (with great powers come great
responsibilities).

Python developers often rely on implicit naming conventions such as a name with
a preceding underscore to signal something being hidden. However this can only
be enforced by vigorous code review, and for a team of developers with
different skill levels, this is difficult to achieve for a large project.
Even the most seasoned developer with the best intention could still make
mistakens, especially if the intended visibility of a software component isn't
obvious.
