"""
This package is an example to demonstrate the use of regular expressions for
enforcing import rules.

In this example, some business logic code tries to import from the presentation
package. Such an import is disallowed (see setup.cfg for the configuration).

Running the flake8 plugin 'packaway-import' should result in a number of
errors::

    $ flake8 .
    ./business/subpackage/bad.py:1:1: DEP501 Import 'web.api.main' violates pattern: 'web.*'

"""  # noqa: E501
