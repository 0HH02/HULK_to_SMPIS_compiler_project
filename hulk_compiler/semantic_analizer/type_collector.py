"""
    This module contains the AST visitor class.
"""

from multipledispatch import dispatch
from .types import Method, IdentifierVar, UnknownType, Protocol, Type
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
    @dispatch(Program, Context)
    def visit_node(node: Program, context: Context):
        for class_def in node.defines:
            TypeCollector.visit_node(class_def, context)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def visit_node(node: ProtocolDeclaration, context: Context):
        methods = []

        for method in node.functions:
            declarated_method: Method = TypeCollector.visit_node(method, context)
            methods.append(declarated_method)

        for extend in node.extends:
            protocol: Protocol | None = context.get_protocol(extend)

            if protocol:
                for method in protocol:
                    declarated_method: Method = TypeCollector.visit_node(
                        method, context
                    )
                    methods.append(declarated_method)

        context.define_protocol(Protocol(node.identifier, methods))

    @staticmethod
    @dispatch(FunctionDeclaration, Context)
    def visit_node(node: FunctionDeclaration, _: Context):

        params = []

        for param in node.params:
            params.append(IdentifierVar(param.identifier, param.static_type))

        return Method(node.identifier, params, UnknownType())

    @staticmethod
    @dispatch(TypeDeclaration, Context)
    def visit_node(node: TypeDeclaration, context: Context):
        params = []
        attributes = []
        methods = []

        for param in node.params:
            params.append(IdentifierVar(param.identifier, param.static_type))

        for attr in node.attributes:
            attributes.append(IdentifierVar(attr.identifier, attr.static_type))

        for method in node.functions:
            methods.append(TypeCollector.visit_node(method, context))

        context.define_type(
            Type(
                node.identifier,
                params=params,
                attributes=attributes,
                methods=methods,
            )
        )
