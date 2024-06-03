"""
    This module contains the AST visitor class.
"""

from abc import ABC, abstractmethod
from multipledispatch import dispatch
from .types import BooleanType
from ..parser.ast.ast import (
    ASTNode,
    While,
    If,
    LetVar,
    For,
)

# pylint: disable=function-redefined


class IVisitor(ABC):
    """
    Interface for visitor classes that implement the visitor pattern.
    """

    @abstractmethod
    def visit_node(self, node: ASTNode, context) -> bool:
        """
        Abstract method for visiting a node in the AST.

        Args:
            node: The node to be visited.
            context: The context object for the visitor.

        Returns:
            None
        """


class ASTVisitor(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @dispatch(While)
    def visit_node(self, node: While, context) -> bool:
        valid = node.validate(self, context)

        if node.infered_type is BooleanType:
            return node.body.validate(self, context) and valid

        print(f"Error: {node.infered_type} is not a boolean type.")
        return False

    @dispatch(If)
    def visit_node(self, node: If, context) -> bool:
        valid = node.condition.validate(self, context)

        if node.infered_type is BooleanType:
            return node.body.validate(self, context) and valid

        print(f"Error: {node.infered_type} is not a boolean type.")
        return False

    @dispatch(For)
    def visit_node(self, node: For, context) -> bool:
        pass

    @dispatch(LetVar)
    def visit_node(self, node: LetVar, context) -> bool:
        pass
