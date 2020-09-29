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

    name = __name__
    version = "0.1.0"
    _code = "ARC1"

    def __init__(self, tree, file_tokens, filename):
        self._tree = tree
        self._module_name = _find_module_name(file_tokens)

        # TODO: Make this magic configurable!
        if self._module_name is None:
            parts = list(pathlib.PurePath(filename).parts)
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
