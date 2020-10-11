import ast

from packaway.violation import ImportRuleViolation


def _is_valid_import(source_module, target_module, level=0):
    """ Return whether an import is allowed.

    Parameters
    ----------
    source_module : str or None
        Name of the module where the import is written.
        If given, this name should be absolute.
    target_module : str
        Name of the module being imported.
        This name can be absolute or relative depending on the value
        of ``level``.
    level : int, optional
        level specifies whether to use absolute or relative
        imports. 0 (the default) means only perform absolute
        imports. Positive values for level indicate the number
        of parent directories to search relative to the directory
        of the module calling import.
    """
    target_parts = target_module.split(".")

    if source_module is None:
        source_parts = []
    else:
        source_parts = source_module.split(".")

        if level > len(source_parts):
            raise ValueError("Level is too deep.")

        target_parts = source_parts[:-level] + target_parts

    pairs = zip(
        source_parts,
        target_parts,
    )
    n_common_levels = 0
    for source_part, target_part in pairs:
        if source_part != target_part:
            break
        n_common_levels += 1

    for part in target_parts[n_common_levels + 1:]:
        if part.startswith("_"):
            return False
    else:
        return True


class _ImportAnalyzer(ast.NodeVisitor):
    """ NodeVisitor for analyzing an AST.

    Parameters
    ----------
    module_name : str or None
        The module name (full path) associated with the Python source
        being parsed. None if this is unknown.
    """

    def __init__(self, module_name=None):
        self.module_name = module_name
        self._errors = []

    def visit_Import(self, node):
        for alias in node.names:
            target = alias.name
            if not _is_valid_import(self.module_name, target):
                self._errors.append(
                    ImportRuleViolation(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        message=f"Importing private name {target!r}.",
                    )
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):

        for alias in node.names:
            if node.module is None:
                target = alias.name
            else:
                target = ".".join([node.module, alias.name])

            if not _is_valid_import(self.module_name, target, node.level):
                self._errors.append(
                    ImportRuleViolation(
                        lineno=node.lineno,
                        col_offset=node.col_offset,
                        message=f"Importing private name {target!r}.",
                    )
                )
        self.generic_visit(node)


def collect_errors(tree, module_name=None):
    """ Top level function to detect violation of import rules.

    Parameters
    ----------
    tree : ast.AST
        The AST tree to be analyzed.
    module_name : str or None
        The absolute module name from which the source represents.
        Default is None which means unknown. If given, it can be used
        to analyze absolute imports.

    Returns
    -------
    errors : list of ImportRuleViolation
        Occurrences of import violation.
    """
    analyzer = _ImportAnalyzer(module_name=module_name)
    analyzer.visit(tree)
    return analyzer._errors
