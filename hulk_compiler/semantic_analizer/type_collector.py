"""
    This module contains the AST visitor class.
"""

from multipledispatch import dispatch
from .types import Method, IdentifierVar
from .context import Context
from ..parser.ast.ast import (
    Program,
    TypeDeclaration,
    ProtocolDeclaration,
    FunctionDeclaration,
)
from ..core.i_visitor import IVisitor

# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=line-too-long


class TypeCollector(IVisitor):
    """
    A visitor class for collecting types in the AST.

    This class implements the `IVisitor` interface and provides methods for visiting
    different nodes in the AST to collect type information.

    Attributes:
        None

    Methods:
        visit_node(node: Program, context: Context): Visits a Program node and collects type information.
        visit_node(node: ProtocolDeclaration, context: Context): Visits a ProtocolDeclaration node and collects type information.
        visit_node(node: FunctionDeclaration, context: Context): Visits a FunctionDeclaration node and collects type information.
    """

    @staticmethod
    @dispatch(Program)
    def visit_node(node: Program, context: Context):
        for class_def in node.defines:
            TypeCollector.visit_node(class_def, context)

    @staticmethod
    @dispatch(ProtocolDeclaration)
    def visit_node(node: ProtocolDeclaration, context: Context):
        methods = []
        for method in node.functions:
            params: list[IdentifierVar] = []
            for param in method.params:
                if param.static_type is None:
                    raise Exception(f"Type not defined for param {param.name}")
                params.append(IdentifierVar(param.identifier, param.static_type))
            if method.return_type is None:
                raise Exception(
                    f"Return type not defined for method {method.identifier}"
                )

            methods.append(Method(method.identifier, params, method.return_type))

        context.define_protocol(node.identifier, methods)

    @staticmethod
    @dispatch(FunctionDeclaration)
    def visit_node(node: FunctionDeclaration, context: Context):
        function_context: Context = context.create_child_context()
