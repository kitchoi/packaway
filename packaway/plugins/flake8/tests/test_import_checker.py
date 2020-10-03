import ast
import contextlib
import os
import tempfile
import unittest

from packaway.plugins.flake8.import_checker import ImportChecker


def get_results(source, filename="dummy.py"):
    tree = ast.parse(source)
    plugin = ImportChecker(tree=tree, filename=filename)
    return [
        f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()
    ]


@contextlib.contextmanager
def change_dir(dir):
    cwd = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(cwd)


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

    def test_good_example_with_absolute_import(self):
        results = get_results(
            source="import package.name",
        )
        self.assertEqual(results, [])

    def test_bad_example_with_absolute_import(self):
        results = get_results(
            source="import package._name",
        )
        self.assertEqual(
            results,
            ["1:0 DEP401 Importing private name 'package._name'."]
        )

    def test_different_top_level_dir(self):
        # Test setting --top-level-dir to support absolute import
        # while running flake8 from a different directory.
        with tempfile.TemporaryDirectory(prefix="_") as tmp_dir, \
                restore_plugin_global_states(), \
                change_dir(tmp_dir):

            with open(os.path.join(tmp_dir, "module.py"), "w"):
                pass

            _, dir_name = os.path.split(tmp_dir)
            ImportChecker._top_level_dir = ".."
            results = get_results(
                source=f"from {dir_name}._module import api",
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
