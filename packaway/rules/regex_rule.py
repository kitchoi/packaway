""" This module supports disallowing imports using regular expressions.
"""

from functools import partial
import re

from packaway.rules._ast_analyzer import ImportAnalyzer


def _is_valid_import(source_module, target_module, disallowed):
    """ Return whether an import is allowed.

    Parameters
    ----------
    source_module : str
        Name of the module where the import statement is.
    target_module : str
        Name being imported.
    disallowed : str
        Regular expression pattern to match. If matched, then the import is
        invalid.

    Returns
    -------
    valid : bool
    """
    return (
        not re.match(disallowed, target_module),
        f"Import {target_module!r} violates pattern: {disallowed!r}",
    )


def collect_errors(tree, module_name=None, disallowed_patterns=None):
    """ Top level function to detect violation of import rules.

    Parameters
    ----------
    tree : ast.AST
        The AST tree to be analyzed.
    module_name : str or None
        The absolute module name from which the source represents.
        Default is None which means unknown. If given, it can be used
        to analyze absolute imports.
    disallowed_patterns : list of str
        Regex patterns of imports to be banned.

    Returns
    -------
    errors : list of ImportRuleViolation
        Occurrences of import violation.
    """
    if not disallowed_patterns:
        return []

    analyzer = ImportAnalyzer(
        module_name=module_name,
        import_rules=[
            partial(_is_valid_import, disallowed=pattern)
            for pattern in disallowed_patterns
        ],
    )
    analyzer.visit(tree)
    return analyzer._errors
