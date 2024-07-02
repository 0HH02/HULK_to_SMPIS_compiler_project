"""
"""

from multipledispatch import dispatch

from ...parser.ast.ast import LetVar


class HulkTranspiler:
    """
    The HulkTranspiler class is responsible for transpiling HULK code to HULK code
    for a better way to test the ast.
    """

    @staticmethod
    @dispatch(LetVar)
    def transpile_node(node: LetVar):
        """
        Visits a LetVar node and performs a transformation on its declarations and body.
        """
        if len(node.declarations) > 1:
            other_declarations = node.declarations[1:]
            other_body = node.body
            node.declarations = [node.declarations[0]]
            node.body = LetVar(other_declarations, other_body)
            HulkTranspiler.transpile_node(node.body)
