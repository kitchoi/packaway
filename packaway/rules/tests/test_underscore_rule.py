import ast
import unittest

from packaway.rules.underscore_rule import (
    collect_errors,
)


class TestAnalyzerAPI(unittest.TestCase):
    """ Test the top-level analyzer behaviour using the packaging rules."""

    def test_ok_examples(self):
        good_sources = [
            "from . import module",
            "from .subpackage.module import name",
            "from ._subpackage.module import name",
            "from package.module import name",
            "from ..subpackage.module import name",
            "from .._subpackage import name",
            "from __future__ import print_function",
        ]
        for source in good_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(tree)
                self.assertEqual(errors, [])

    def test_ok_examples_with_module_name(self):
        module_name = "package.subpackage.module"
        good_sources = [
            "from . import _module2",
            "from ._module2 import name",
            # actually in the same subpackage and therefore
            # the private module is visible.
            "from ..subpackage._module2 import name",
            "from package._module import name",
        ]
        for source in good_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree,
                    module_name=module_name,
                )
                self.assertEqual(errors, [])

    def test_error_examples(self):
        bad_sources = [
            "from .._subpackage import _name",
            "from ._subpackage._module import name",
        ]
        for source in bad_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree,
                    module_name=None,
                )
                self.assertEqual(len(errors), 1)

    def test_error_examples_with_module_name(self):
        module_name = "package.subpackage.module"
        bad_sources = [
            "from .._subpackage import _name",
            "from ._subpackage._module import name",
        ]
        for source in bad_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree,
                    module_name=module_name,
                )
                self.assertEqual(len(errors), 1)
