import ast
import os
import sys


class ImportAnalyzer(ast.NodeVisitor):

    def visit_ImportFrom(self, node):
        module = node.module

        # leading underscore in module is okay
        if any(part.startswith("_") for part in module.split(".")[1:]):
            print("Import private module: ", module)

        self.generic_visit(node)

    def visit_alias(self, node):
        if any(part.startswith("_") for part in node.name):
            print("Import private name: ", node.name)
        self.generic_visit(node)


if __name__ == "__main__":
    filepath = sys.argv[1]
    filepath = os.path.normpath(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    analyzer = ImportAnalyzer()
    analyzer.visit(tree)
