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
    def print(node: Program, tabs: int = 0) -> None:
        """
        Visits a node in the AST and prints its representation.

        Args:
            node (Program): The node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "program: {")
        for define in node.defines:
            ASTPrinter.print(define, tabs + 1)
        ASTPrinter.print(node.statement, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(While, int)
    def print(node: While, tabs: int) -> None:
        """
        Visits a node in the AST and prints its representation.

        Args:
            node (While): The node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "while:{")
        ASTPrinter.print(node.condition, tabs + 1)
        ASTPrinter.print(node.body, tabs + 1)
        print("  " * (tabs + 1), f"while inferred type: {node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(If, int)
    def print(node: If, tabs: int):
        """
        Prints the representation of an If node in the abstract syntax tree.

        Args:
            node (If): The If node to be printed.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "if: {")
        ASTPrinter.print(node.condition, tabs + 1)
        ASTPrinter.print(node.body, tabs + 1)
        for elif_expr in node.elif_clauses:
            ASTPrinter.print(elif_expr, tabs + 1)
        print("   " * (tabs + 1), "else: {")
        ASTPrinter.print(node.else_body, tabs + 1)
        print("   " * (tabs + 1), f"if inferred type: {node.inferred_type}")
        print("   " * (tabs + 1), "}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Elif, int)
    def print(node: Elif, tabs: int):
        """
        Visits an Elif node and prints its representation.

        Args:
            node (Elif): The Elif node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "elif: {")
        ASTPrinter.print(node.condition, tabs + 1)
        ASTPrinter.print(node.body, tabs + 1)
        print("   " * (tabs + 1), f"elif inferred type: {node.inferred_type}")
        print("   " * tabs, "{")

    @staticmethod
    @dispatch(For, int)
    def print(node: For, tabs: int):
        """
        Visits a For node in the AST and prints its contents.

        Args:
            node (For): The For node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "for {")
        print("   " * (tabs + 1), "index: ", node.index_identifier)
        ASTPrinter.print(node.iterable, tabs + 1)
        ASTPrinter.print(node.body, tabs + 1)
        print("   " * (tabs + 1), f"for inferred type: {node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LetVar, int)
    def print(node: LetVar, tabs: int):
        """
        Visits a LetVar node and prints its contents.

        Args:
            node (LetVar): The LetVar node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "let: {")
        for var in node.declarations:
            ASTPrinter.print(var, tabs + 1)
        ASTPrinter.print(node.body, tabs + 1)
        print("   " * (tabs + 1), f"let inferred type:{node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ExpressionBlock, int)
    def print(node: ExpressionBlock, tabs: int):
        print("   " * tabs, "expression_block: {")
        for exp in node.body:
            ASTPrinter.print(exp, tabs + 1)
        print("   " * (tabs + 1), f"block inferred type: {node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeCall, int)
    def print(node: AttributeCall, tabs: int):
        print("   " * tabs, "attribute_call: {")
        ASTPrinter.print(node.obj, tabs + 1)
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * (tabs + 1), f"attr call inferred type: {node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionCall, int)
    def print(node: FunctionCall, tabs: int):
        print("   " * tabs, "function_call: {")
        ASTPrinter.print(node.obj, tabs + 1)
        print("as")
        ASTPrinter.print(node.invocation, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Invocation, int)
    def print(node: Invocation, tabs: int):
        print("   " * tabs, "invocation: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.print(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Identifier, int)
    def print(node: Identifier, tabs: int):
        print("   " * tabs, "identifier:", node.identifier)
        print("   " * tabs, "inferred_type:", node.inferred_type)

    @staticmethod
    @dispatch(NegativeNode, int)
    def print(node: NegativeNode, tabs: int):
        print("   " * tabs, "negative_node: {")
        ASTPrinter.print(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(PositiveNode, int)
    def print(node: NegativeNode, tabs: int):
        print("   " * tabs, "positive_node: {")
        ASTPrinter.print(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(NotNode, int)
    def print(node: NotNode, tabs: int):
        print("   " * tabs, "not_node: {")
        ASTPrinter.print(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(BinaryExpression, int)
    def print(node: BinaryExpression, tabs: int):
        print("   " * tabs, "binary_node: {")
        print("   " * (tabs + 1), "operator: ", node.operator)
        ASTPrinter.print(node.left, tabs + 1)
        ASTPrinter.print(node.right, tabs + 1)
        print("   " * (tabs + 1), f"binary expr inferred type: {node.inferred_type}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LiteralNode, int)
    def print(node: LiteralNode, tabs: int):
        print("   " * tabs, "literal: ", node.value)
        print("   " * tabs, "infered_type: ", node.inferred_type)

    @staticmethod
    @dispatch(Inherits, int)
    def print(node: Inherits, tabs: int):
        print("   " * tabs, "inherits: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.print(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionDeclaration, int)
    def print(node: FunctionDeclaration, tabs: int):
        print("   " * tabs, "function_declaration: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)

        for arg in node.params:
            ASTPrinter.print(arg, tabs + 1)

        print("   " * (tabs + 1), "static_return_type: ", node.static_return_type)
        print("   " * (tabs + 1), "inferred_return_type: ", node.inferred_return_type)
        if node.body:
            ASTPrinter.print(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeDeclaration, int)
    def print(node: AttributeDeclaration, tabs: int):
        print("   " * tabs, "atribute: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * (tabs + 1), "static_type: ", node.static_type)
        print("   " * (tabs + 1), "inferred_type: ", node.expression.inferred_type)

        ASTPrinter.print(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(IndexNode, int)
    def print(node: IndexNode, tabs: int):
        print("   " * tabs, "index: {")
        ASTPrinter.print(node.obj, tabs + 1)
        ASTPrinter.print(node.index, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Vector, int)
    def print(node: Vector, tabs: int):
        print("   " * tabs, "vector: {")
        for literal in node.elements:
            ASTPrinter.print(literal, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ComprehensionVector, int)
    def print(node: ComprehensionVector, tabs: int):
        """
        Visits a ComprehensionVector node and prints its contents.

        Args:
            node (ComprehensionVector): The ComprehensionVector node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "ComprehensionVector: {")
        ASTPrinter.print(node.generator, tabs + 1)
        print("   " * (tabs + 1), "item: ", node.identifier)
        ASTPrinter.print(node.iterator, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Instanciate, int)
    def print(node: Instanciate, tabs: int):
        """
        Visits an instance node in the AST and prints its information.

        Args:
            node (Instanciate): The instance node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "instanciate: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.params:
            ASTPrinter.print(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(DestructiveAssign, int)
    def print(node: DestructiveAssign, tabs: int):
        """
        Visits a DestructiveAssign node and prints its contents.

        Args:
            node (DestructiveAssign): The DestructiveAssign node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "destructive_assigment: {")
        print("   " * (tabs + 1), "identifier: ")
        ASTPrinter.print(node.identifier, tabs + 2)
        print("   " * (tabs + 1), "expression: ")
        ASTPrinter.print(node.expression, tabs + 2)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(VariableDeclaration, int)
    def print(node: VariableDeclaration, tabs: int):
        """
        Visits a VariableDeclaration node and prints its information.

        Args:
            node (VariableDeclaration): The VariableDeclaration node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "variable_declaration: {")
        print("   " * (tabs + 1), "identifier:", node.identifier)
        print("   " * (tabs + 1), "static_type:", node.static_type)
        ASTPrinter.print(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ProtocolDeclaration, int)
    def print(node: ProtocolDeclaration, tabs: int):
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
            ASTPrinter.print(func, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Parameter, int)
    def print(node: Parameter, tabs: int):
        """
        Visits a Parameter node and prints its contents.

        Args:
            node (Parameter): The Parameter node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "parameter: {")
        print("   " * (tabs + 1), "identifier", node.identifier)
        print("   " * (tabs + 1), "inferred_type", node.inferred_type)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(TypeDeclaration, int)
    def print(node: TypeDeclaration, tabs: int):
        """
        Visits a TypeDeclaration node and prints its information.

        Args:
            node (TypeDeclaration): The TypeDeclaration node to visit.
            tabs (int): The number of tabs for indentation.
        """
        print("   " * tabs, "type: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for param in node.params:
            ASTPrinter.print(param, tabs + 1)
        if node.inherits:
            ASTPrinter.print(node.inherits, tabs + 1)
        for attr in node.attributes:
            ASTPrinter.print(attr, tabs + 1)
        for func in node.functions:
            ASTPrinter.print(func, tabs + 1)
        print("   " * tabs, "}")
