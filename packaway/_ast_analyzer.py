
import ast

from packaway.violation import ImportRuleViolation


class ImportAnalyzer(ast.NodeVisitor):
    """ NodeVisitor for analyzing an AST.

    Parameters
    ----------
    module_name : str or None
        The module name (full path) associated with the Python source
        being parsed. None if this is unknown.
    import_rules : list of callable
        List of callables which return true if the import is valid.
        Each callable has a signature of
        ``(source_module: str, target_module: str, level:int)``
        First argument is the current module name.
        Second argument is the module name to be imported.
        Last argument specifies whether to use absolute or relative
        imports. 0 (the default) means only perform absolute
        imports.
    """

    def __init__(self, module_name=None, import_rules=None):
        self.module_name = module_name
        self.import_rules = [] if import_rules is None else import_rules
        self._errors = []

    def visit_Import(self, node):
        for alias in node.names:
            target = alias.name
            for import_rule in self.import_rules:
                if not import_rule(self.module_name, target, level=0):
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
            for import_rule in self.import_rules:
                if not import_rule(self.module_name, target, level=node.level):
                    self._errors.append(
                        ImportRuleViolation(
                            lineno=node.lineno,
                            col_offset=node.col_offset,
                            message=f"Importing private name {target!r}.",
                        )
                    )
        self.generic_visit(node)
