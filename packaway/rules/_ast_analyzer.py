
import ast

from packaway.violation import ImportRuleViolation


class ImportAnalyzer(ast.NodeVisitor):
    """ NodeVisitor for analyzing an AST.

    Parameters
    ----------
    module_name : str or None
        The module name (full path) associated with the Python source
        being parsed. None if this is unknown.
    import_rules : list of callable(str, str) -> tuple(bool, str)
        List of callables for validating the import.
        First argument is the current module name.
        Second argument is the (absolute) module name to be imported.
        The callable should return (valid, reason) where the first value
        is whether the import is valid, and the second value is the reason
        if there is a violation (not used if the import is valid.)
    """

    def __init__(self, module_name=None, import_rules=None):
        self.module_name = module_name
        self.import_rules = [] if import_rules is None else import_rules
        self._errors = []

    def visit_Import(self, node):
        """ Reimplemented NodeVisitor.visit_Import """
        for alias in node.names:
            target = alias.name
            for import_rule in self.import_rules:
                is_valid, reason = import_rule(self.module_name, target)
                if not is_valid:
                    self._errors.append(
                        ImportRuleViolation(
                            lineno=node.lineno,
                            col_offset=node.col_offset,
                            message=reason,
                        )
                    )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """ Reimplemented NodeVisitor.visit_ImportFrom """

        for alias in node.names:
            if node.module is None:
                target = alias.name
            else:
                target = ".".join([node.module, alias.name])

            target = _normalize_target_module(
                self.module_name, target, node.level
            )
            for import_rule in self.import_rules:
                is_valid, reason = import_rule(self.module_name, target)
                if not is_valid:
                    self._errors.append(
                        ImportRuleViolation(
                            lineno=node.lineno,
                            col_offset=node.col_offset,
                            message=reason,
                        )
                    )
        self.generic_visit(node)


def _normalize_target_module(source_module, target_module, level):
    """ Normalize relative import, to absolute import if possible.

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

    Returns
    -------
    module_name : str
        Normalized import name
    """
    if source_module is None or level == 0:
        return target_module

    source_parts = source_module.split(".")
    if level > len(source_parts):
        raise ValueError("Level is too deep.")
    target_parts = source_parts[:-level] + target_module.split(".")
    return ".".join(target_parts)
