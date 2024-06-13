"""
This module contains the interface for visitor classes that implement the visitor pattern.
"""

from abc import ABC, abstractmethod


class IVisitor(ABC):
    """
    Interface for visitor classes that implement the visitor pattern.
    """

    @staticmethod
    @abstractmethod
    def visit_node(node):
        """
        Abstract method for visiting a node in the AST.

        Args:
            node: The node to be visited.
            context: The context object for the visitor.

        Returns:
            None
        """
