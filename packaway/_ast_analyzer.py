
import ast

from packaway.violation import ImportRuleViolation


class ImportAnalyzer(ast.NodeVisitor):
    """ NodeVisitor for analyzing an AST.

    Parameters
    ----------
    module_name : str or None
        The module name (full path) associated with the Python source
        being parsed. None if this is unknown.
    import_rules : list of callable`(source_module: str, target_module: str)
        List of callables which return true if the import is valid.
        First argument is the current module name.
        Second argument is the (absolute) module name to be imported.
    """

    def __init__(self, module_name=None, import_rules=None):
        self.module_name = module_name
        self.import_rules = [] if import_rules is None else import_rules
        self._errors = []

    def visit_Import(self, node):
        for alias in node.names:
            target = alias.name
            for import_rule in self.import_rules:
                if not import_rule(self.module_name, target):
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

            target = _normalize_target_module(
                self.module_name, target, node.level
            )
            for import_rule in self.import_rules:
                if not import_rule(self.module_name, target):
                    self._errors.append(
                        ImportRuleViolation(
                            lineno=node.lineno,
                            col_offset=node.col_offset,
                            message=f"Importing private name {target!r}.",
                        )
                    )
        self.generic_visit(node)


def _normalize_target_module(source_module, target_module, level):
    """ Normalize relative import to absolute import.

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
    if source_module is None or level == 0:
        return target_module

    source_parts = source_module.split(".")
    if level > len(source_parts):
        raise ValueError("Level is too deep.")
    target_parts = source_parts[:-level] + target_module.split(".")
    return ".".join(target_parts)
