"""
This module contains the classes for the Abstract Syntax Tree (AST) 
and the differents types of Nodes of the tree
"""


class AstNode:
    """
    Represents a abstract node in the Abstract Syntax Tree (AST)

    Attributes:
        children (list[AstNode]): The list of child nodes.
    """

    def __init__(self):
        self.children: list[AstNode] = []


class AST:
    """
    Represents the Abstract Syntax Tree (AST).

    Attributes:
        root (AstNode): The root node of the AST.
    """

    def __init__(self, root: AstNode):
        self.root = root
