"""
"""

from multipledispatch import dispatch

from ...parser.ast.ast import (
    LetVar,
    For,
    VariableDeclaration,
    While,
    FunctionCall,
    Identifier,
    Invocation,
    ComprehensionVector,
    Vector,
    LiteralNode,
    DestructiveAssign,
    IndexNode,
)
from ..types import BooleanType

# pylint: disable=function-redefined


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

    @staticmethod
    @dispatch(For)
    def transpile_node(node: For):
        transpiled_node = LetVar(
            [VariableDeclaration("iterable", node.iterable)],
            While(
                FunctionCall(
                    Identifier("iterable", node.iterable.inferred_type),
                    Invocation("next", [], BooleanType()),
                ),
                LetVar(
                    [
                        VariableDeclaration(
                            f"{node.index_identifier}",
                            FunctionCall(
                                Identifier("iterable", node.iterable.inferred_type),
                                Invocation("current", [], node.index_identifier_type),
                            ),
                            inferred_type=node.index_identifier_type,
                        )
                    ],
                    node.body,
                    node.body.inferred_type,
                ),
            ),
        )
        return transpiled_node

    @staticmethod
    @dispatch(ComprehensionVector)
    def transpile_node(node: ComprehensionVector):
        transpiled_node = LetVar(
            [
                VariableDeclaration(
                    "list",
                    Vector(
                        [
                            LiteralNode(0, None)
                            for x in range(
                                int(node.iterator.arguments[0].value),
                                int(node.iterator.arguments[1].value),
                            )
                        ]
                    ),
                )
            ],
            For(
                node.identifier,
                None,
                node.iterator,
                DestructiveAssign(
                    IndexNode(Identifier("list"), Identifier("x")), node.generator
                ),
            ),
        )

        return transpiled_node
