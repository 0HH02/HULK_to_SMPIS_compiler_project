"""
This module contains the ASTPrinter class, which is used to print the AST
"""

from ...core.i_visitor import IVisitor
from multipledispatch import dispatch
from .ast import (
    Program,
    While,
    If,
    Elif,
    For,
    LetVar,
    ExpressionBlock,
    AttributeCall,
    FunctionCall,
    Invocation,
    Identifier,
    NegativeNode,
    PositiveNode,
    NotNode,
    BinaryExpression,
    AttributeDeclaration,
    FunctionDeclaration,
    Inherits,
    LiteralNode,
    ProtocolDeclaration,
    IndexNode,
    Vector,
    VariableDeclaration,
    TypeDeclaration,
    Parameter,
    DestructiveAssign,
    Instanciate,
    ComprehensionVector,
)

# pylint: disable=function-redefined
# pylint: disable=arguments-differ


class ASTPrinter(IVisitor):
    """
    A class that provides methods to print the Abstract Syntax Tree (AST) nodes
    using the visitor pattern.
    """

    @staticmethod
    @dispatch(Program)
    def visit_node(node: Program, tabs: int = 0) -> None:
        """
        Visits a node in the AST and prints its representation.

        Args:
            node (Program): The node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "program: {")
        for define in node.defines:
            ASTPrinter.visit_node(define, tabs + 1)
        ASTPrinter.visit_node(node.statement, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(While, int)
    def visit_node(node: While, tabs: int) -> None:
        """
        Visits a node in the AST and prints its representation.

        Args:
            node (While): The node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "while:{")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(If, int)
    def visit_node(node: If, tabs: int):
        """
        Prints the representation of an If node in the abstract syntax tree.

        Args:
            node (If): The If node to be printed.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "if: {")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        for elif_expr in node.elif_clauses:
            ASTPrinter.visit_node(elif_expr, tabs + 1)
        print("   " * (tabs + 1), "else: {")
        ASTPrinter.visit_node(node.else_body, tabs + 1)
        print("   " * (tabs + 1), "}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Elif, int)
    def visit_node(node: Elif, tabs: int):
        """
        Visits an Elif node and prints its representation.

        Args:
            node (Elif): The Elif node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "elif: {")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "{")

    @staticmethod
    @dispatch(For, int)
    def visit_node(node: For, tabs: int):
        """
        Visits a For node in the AST and prints its contents.

        Args:
            node (For): The For node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "for {")
        print("   " * (tabs + 1), "index: ", node.index_identifier)
        ASTPrinter.visit_node(node.iterable, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LetVar, int)
    def visit_node(node: LetVar, tabs: int):
        """
        Visits a LetVar node and prints its contents.

        Args:
            node (LetVar): The LetVar node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "let: {")
        for var in node.declarations:
            ASTPrinter.visit_node(var, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ExpressionBlock, int)
    def visit_node(node: ExpressionBlock, tabs: int):
        print("   " * tabs, "expression_block: {")
        for exp in node.body:
            ASTPrinter.visit_node(exp, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeCall, int)
    def visit_node(node: AttributeCall, tabs: int):
        print("   " * tabs, "attribute_call: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionCall, int)
    def visit_node(node: FunctionCall, tabs: int):
        print("   " * tabs, "function_call: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        print("as")
        ASTPrinter.visit_node(node.invocation, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Invocation, int)
    def visit_node(node: Invocation, tabs: int):
        print("   " * tabs, "invocation: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Identifier, int)
    def visit_node(node: Identifier, tabs: int):
        print("   " * tabs, "identifier:", node.identifier)

    @staticmethod
    @dispatch(NegativeNode, int)
    def visit_node(node: NegativeNode, tabs: int):
        print("   " * tabs, "negative_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(PositiveNode, int)
    def visit_node(node: NegativeNode, tabs: int):
        print("   " * tabs, "positive_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(NotNode, int)
    def visit_node(node: NotNode, tabs: int):
        print("   " * tabs, "not_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(BinaryExpression, int)
    def visit_node(node: BinaryExpression, tabs: int):
        print("   " * tabs, "binary_node: {")
        print("   " * (tabs + 1), "operator: ", node.operator)
        ASTPrinter.visit_node(node.left, tabs + 1)
        ASTPrinter.visit_node(node.right, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LiteralNode, int)
    def visit_node(node: LiteralNode, tabs: int):
        print("   " * tabs, "literal: ", node.value)
        print("   " * tabs, "infered_type: ", node.inferred_type)

    @staticmethod
    @dispatch(Inherits, int)
    def visit_node(node: Inherits, tabs: int):
        print("   " * tabs, "inherits: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionDeclaration, int)
    def visit_node(node: FunctionDeclaration, tabs: int):
        print("   " * tabs, "function_declaration: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)

        for arg in node.params:
            ASTPrinter.visit_node(arg, tabs + 1)

        print("   " * (tabs + 1), "return_type: ", node.return_type)
        if node.body:
            ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeDeclaration, int)
    def visit_node(node: AttributeDeclaration, tabs: int):
        print("   " * tabs, "atribute: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * (tabs + 1), "type: ", node.static_type)

        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(IndexNode, int)
    def visit_node(node: IndexNode, tabs: int):
        print("   " * tabs, "index: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        ASTPrinter.visit_node(node.index, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Vector, int)
    def visit_node(node: Vector, tabs: int):
        print("   " * tabs, "vector: {")
        for literal in node.elements:
            ASTPrinter.visit_node(literal, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ComprehensionVector, int)
    def visit_node(node: ComprehensionVector, tabs: int):
        """
        Visits a ComprehensionVector node and prints its contents.

        Args:
            node (ComprehensionVector): The ComprehensionVector node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "ComprehensionVector: {")
        ASTPrinter.visit_node(node.generator, tabs + 1)
        print("   " * (tabs + 1), "item: ", node.identifier)
        ASTPrinter.visit_node(node.iterator, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Instanciate, int)
    def visit_node(node: Instanciate, tabs: int):
        """
        Visits an instance node in the AST and prints its information.

        Args:
            node (Instanciate): The instance node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "instanciate: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.params:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(DestructiveAssign, int)
    def visit_node(node: DestructiveAssign, tabs: int):
        """
        Visits a DestructiveAssign node and prints its contents.

        Args:
            node (DestructiveAssign): The DestructiveAssign node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "destructive_assigment: {")
        print("   " * (tabs + 1), "identifier", node.identifier.identifier)
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(VariableDeclaration, int)
    def visit_node(node: VariableDeclaration, tabs: int):
        """
        Visits a VariableDeclaration node and prints its information.

        Args:
            node (VariableDeclaration): The VariableDeclaration node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "variable_declaration: {")
        print("   " * (tabs + 1), "identifier:", node.identifier)
        print("   " * (tabs + 1), "static_type:", node.static_type)
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ProtocolDeclaration, int)
    def visit_node(node: ProtocolDeclaration, tabs: int):
        """
        Visits a ProtocolDeclaration node and prints its contents.

        Args:
            node (ProtocolDeclaration): The ProtocolDeclaration node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "protoco_declaration: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * (tabs + 1), "extend: ", node.extends)
        for func in node.functions:
            ASTPrinter.visit_node(func, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Parameter, int)
    def visit_node(node: Parameter, tabs: int):
        """
        Visits a Parameter node and prints its contents.

        Args:
            node (Parameter): The Parameter node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "parameter: {")
        print("   " * (tabs + 1), "identifier", node.identifier)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(TypeDeclaration, int)
    def visit_node(node: TypeDeclaration, tabs: int):
        """
        Visits a TypeDeclaration node and prints its information.

        Args:
            node (TypeDeclaration): The TypeDeclaration node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "type: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for param in node.params:
            ASTPrinter.visit_node(param, tabs + 1)
        if node.inherits:
            ASTPrinter.visit_node(node.inherits, tabs + 1)
        for attr in node.attributes:
            ASTPrinter.visit_node(attr, tabs + 1)
        for func in node.functions:
            ASTPrinter.visit_node(func, tabs + 1)
        print("   " * tabs, "}")
