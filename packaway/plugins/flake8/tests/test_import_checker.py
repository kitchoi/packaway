import ast
import contextlib
import os
import unittest

from packaway.plugins.flake8.import_checker import ImportChecker


def get_results(source, filename="dummy.py"):
    tree = ast.parse(source)
    plugin = ImportChecker(tree=tree, filename=filename)
    return [
        f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()
    ]


@contextlib.contextmanager
def restore_plugin_global_states():
    """ Context manager to make sure plugin class variables are restored when
    the context exits.
    """
    top_level_dir = ImportChecker._top_level_dir
    deduce_path = ImportChecker._deduce_path
    try:
        yield
    finally:
        ImportChecker._top_level_dir = top_level_dir
        ImportChecker._deduce_path = deduce_path


class TestImportCheckPlugin(unittest.TestCase):

    def test_good_example(self):
        results = get_results(
            source="from . import module",
        )
        self.assertEqual(results, [])

    def test_bad_example(self):
        results = get_results(
            source="from .module import _name",
        )
        self.assertEqual(
            results,
            ["1:0 DEP401 Importing private name 'module._name'."]
        )

    def test_good_example_with_filename(self):
        results = get_results(
            source="from package import _name",
            filename=os.path.join("package", "module.py"),
        )
        self.assertEqual(results, [])

    def test_different_top_level_dir(self):
        with restore_plugin_global_states():
            ImportChecker._top_level_dir = "_package"
            results = get_results(
                source="from _package._module import api",
                filename="module.py",
            )
            self.assertEqual(results, [])

    def test_no_deduce_path(self):
        with restore_plugin_global_states():
            ImportChecker._deduce_path = False
            results = get_results(
                source="from package import _name",
                filename=os.path.join("package", "module.py"),
            )
            self.assertEqual(
                results,
                ["1:0 DEP401 Importing private name 'package._name'."]
            )
