
""" This module supports disallowing imports using leading underscores and
packaging structures.
"""

from packaway.rules._ast_analyzer import ImportAnalyzer


def _is_valid_import(source_module, target_module):
    """ Return whether an import is allowed.

    Parameters
    ----------
    source_module : str or None
        Name of the module where the import is written.
        If given, this name should be absolute.
    target_module : str
        Name of the module being imported.
        The name should be an absolute name.

    Returns
    -------
    valid : bool
    """

    if source_module is None:
        source_parts = []
    else:
        source_parts = source_module.split(".")

    target_parts = target_module.split(".")

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
            return False, f"Importing private name {target_module!r}.",
    else:
        return True, ""


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
    analyzer = ImportAnalyzer(
        module_name=module_name,
        import_rules=[_is_valid_import],
    )
    analyzer.visit(tree)
    return analyzer._errors
