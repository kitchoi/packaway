import ast
import contextlib
import os
import tempfile
import unittest

from flake8.options.manager import OptionManager

from packaway.plugins.flake8.import_checker import ImportChecker


def get_results(source, filename="dummy.py", plugin_class=ImportChecker):
    tree = ast.parse(source)
    plugin = plugin_class(tree=tree, filename=filename)
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


def parse_args(plugin_class, args):
    """ Return a new plugin class with the argument options parsed.

    Parameters
    ----------
    plugin_class : type
        The object to be used as a flake8 extension.
    args : list of str
        Argument options to be parsed.

    Returns
    -------
    new_plugin_class : subclass of plugin_class
    """

    class TmpPlugin(plugin_class):
        pass

    prog = "flake8"
    manager = OptionManager(prog, TmpPlugin.version)
    TmpPlugin.add_options(manager)
    options, _ = manager.parse_args(args)
    TmpPlugin.parse_options(options)
    return TmpPlugin


class TestImportCheckPluginUnderscoreRule(unittest.TestCase):
    """ Test Underscore rule (DEP401) provided by the plugin."""

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
                change_dir(tmp_dir):

            with open(os.path.join(tmp_dir, "module.py"), "w"):
                pass

            _, dir_name = os.path.split(tmp_dir)
            results = get_results(
                source=f"from {dir_name}._module import api",
                filename="module.py",
                plugin_class=parse_args(
                    ImportChecker, ["--top-level-dir", ".."]
                ),
            )
            self.assertEqual(results, [])

    def test_no_deduce_path(self):
        results = get_results(
            source="from package import _name",
            filename=os.path.join("package", "module.py"),
            plugin_class=parse_args(
                ImportChecker, ["--no-deduce-path"]
            ),
        )
        self.assertEqual(
            results,
            ["1:0 DEP401 Importing private name 'package._name'."]
        )
