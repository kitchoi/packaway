import os
import pathlib
import re
import tokenize
from packaway.import_analyzer import collect_errors


_KEYWORD = "packaway.name: "
_PATTERN = r"^#\s*packaway\.name\s*:\s*([\w\.]*)\s*"


def _find_module_name(tokens):
    for token in tokens:
        if token.type == tokenize.COMMENT:
            matched = re.match(_PATTERN, token.string)
            if matched:
                return matched.groups()[0]
    return None


class ImportChecker:

    name = "packaway-import"
    version = "0.1.0"
    _code = "DEP401"
    _top_level_dir = None
    _deduce_path = True

    def __init__(self, tree, file_tokens, filename):
        self._tree = tree
        self._module_name = _find_module_name(file_tokens)

        if self._deduce_path and self._module_name is None:
            path = pathlib.PurePath(filename)
            if self._top_level_dir is not None:
                path = path.relative_to(self._top_level_dir)
            parts = list(path.parts)
            parts[-1], _ = os.path.splitext(parts[-1])
            self._module_name = ".".join(parts)

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
