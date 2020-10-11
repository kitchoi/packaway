import ast
import unittest

from packaway.rules.regex_rule import collect_errors


class TestRegexRule(unittest.TestCase):
    """ Test collect_errors for regex rule."""

    def test_disallowed_regex_errors(self):
        disallowed = r"^gui_package"
        source = "from gui_package.api import x"
        tree = ast.parse(source)
        errors = collect_errors(
            tree,
            module_name=None,
            disallowed_patterns=[disallowed],
        )
        self.assertEqual(len(errors), 1)
        error, = errors
        self.assertEqual(
            error.message,
            "Import 'gui_package.api.x' violates pattern: '^gui_package'",
            error.message,
        )

    def test_disallowed_many_regex(self):
        disallowed_patterns = [
            r".*\.gui\..*",
            r".*\.web\..*",
        ]
        bad_sources = [
            "from package.gui.api import x",
            "from .subpackage.web.api import x",
        ]
        for source in bad_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree=tree,
                    module_name=None,
                    disallowed_patterns=disallowed_patterns,
                )
                self.assertEqual(len(errors), 1)

    def test_disallowed_many_regex_with_module_name(self):
        # Test when the source module name is known.
        source_module = "package.module2"
        disallowed_patterns = [
            r".*\.gui\..*",
            r".*\.web\..*",
        ]
        bad_sources = [
            "from package.gui.api import x",
            "from .web.api import x",  # resolve to 'package.web.api'
        ]
        for source in bad_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree=tree,
                    module_name=source_module,
                    disallowed_patterns=disallowed_patterns,
                )
                self.assertEqual(len(errors), 1)

    def test_disallowed_none_match(self):
        disallowed_patterns = [
            r".*\.gui\..*",
            r".*\.web\..*",
        ]
        good_sources = [
            "from package.api import x",
            "from .web.api import x",   # resolve to just 'web.api.x'
        ]
        for source in good_sources:
            with self.subTest(source=source):
                tree = ast.parse(source)
                errors = collect_errors(
                    tree=tree,
                    module_name=None,
                    disallowed_patterns=disallowed_patterns,
                )
                self.assertEqual(len(errors), 0)
