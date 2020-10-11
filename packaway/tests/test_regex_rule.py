import ast
import unittest

from packaway.regex_rule import collect_errors


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
