import os
import pathlib

from packaway import __version__
from packaway.import_analyzer import collect_errors


class ImportChecker:
    """ Flake8 plugin for checking disallowed imports following
    the packaging rules.
    """

    # Name of the plugin (visible via flake8)
    name = "packaway-import"

    # Version of the plugin
    version = __version__

    # Error code when a violation occurs
    _code = "DEP401"

    # Top level directory to use when composing module names from file paths.
    # Used for handling absolute imports. Not used if _deduce_path is false.
    _top_level_dir = None

    # Flag to switch off deducing module names from file paths.
    _deduce_path = True

    def __init__(self, tree, filename):
        self._tree = tree

        if self._deduce_path:
            path = pathlib.PurePath(filename)
            if self._top_level_dir is not None:
                path = (
                    pathlib.PurePath(self._top_level_dir).joinpath(path)
                )
            parts = list(path.parts)
            parts[-1], _ = os.path.splitext(parts[-1])
            self._module_name = ".".join(parts)
        else:
            self._module_name = None

    def run(self):
        for error in collect_errors(self._tree, self._module_name):
            yield (
                error.lineno,
                error.col_offset,
                self._code + " " + error.message,
                type(self),
            )

    @classmethod
    def add_options(cls, option_manager):
        option_manager.add_option(
            "--no-deduce-path",
            dest="no_deduce_path",
            action="store_true",
            help="Switch off parsing file paths as module names.",
        )
        option_manager.add_option(
            "--top-level-dir",
            dest="top_level_dir",
            default=None,
            help="Top level directory for parsing file paths as module names.",
        )

    @classmethod
    def parse_options(cls, options):
        cls._top_level_dir = options.top_level_dir
        cls._deduce_path = not options.no_deduce_path
