import ast
import unittest

from packaway.underscore_rule import (   # noqa: DEP401
    _is_valid_import,
    collect_errors,
)


class TestValidImport(unittest.TestCase):
    """ Test _is_valid_import """

    def test_is_valid_import_okay(self):
        good_examples = [
            # List of (source_module, target_module)
            ("package.module1", "package.module2"),
            ("package.module1", "package._module2"),
            ("package.subpackage.module1", "package.subpackage._module2"),
        ]
        for source, target_module in good_examples:
            with self.subTest(source=source, target_module=target_module):
                self.assertTrue(
                    _is_valid_import(
                        source_module=source,
                        target_module=target_module,
                    )
                )

    def test_is_valid_import_not_okay(self):
        bad_examples = [
            # List of (source_module, target_module)
            ("package.module1", "package.subpackage._module3"),
            ("package.subpackage1.module1", "package.subpackage2._module2"),
        ]
        for source, target_module in bad_examples:
            with self.subTest(source=source, target_module=target_module):
                self.assertFalse(
                    _is_valid_import(
                        source_module=source,
                        target_module=target_module,
                    )
                )

    def test_relative_import_okay(self):
        # With level 1, means the source is importing
        # target with code like `from .package import module`
        good_examples = [
            # List of (source_module, target_module, level)
            ("package.module1", "module2", 1),
            ("package.module1", "_module2", 1),
            ("package.subpackage.module1", "_module2", 1),
            ("package.subpackage.module2", "subpackage._module1.name", 2),
        ]
        for source, target_module, level in good_examples:
            with self.subTest(
                    source=source,
                    target_module=target_module,
                    level=level):
                self.assertTrue(
                    _is_valid_import(
                        source_module=source,
                        target_module=target_module,
                        level=level,
                    )
                )

    def test_relative_import_not_okay_level_1(self):
        # With level 1, means the source is importing
        # target with code like `from .package import module`
        bad_examples = [
            # List of (source_module, target_module)
            # The target is actually 'package.package._module2' if
            # it was an absolute name.
            ("package.module1", "package._module2"),
        ]
        for source, target_module in bad_examples:
            with self.subTest(source=source, target_module=target_module):
                self.assertFalse(
                    _is_valid_import(
                        source_module=source,
                        target_module=target_module,
                        level=1,
                    )
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
