"""
This module contains the AST nodes for the Hulk programming language.
"""

from dataclasses import dataclass
from enum import Enum
from hulk_compiler.lexer.token import Token
from ...semantic_analizer.types import Type, UnkownType
from ...core.i_visitor import IVisitor


class Operator(Enum):
    """
    Enum representing different operators.
    """

    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    MOD = 4
    POW = 5
    AND = 6
    OR = 7
    EQ = 8
    NEQ = 9
    GT = 10
    LT = 11
    GE = 12
    LE = 13
    CONCAT = 14
    DCONCAT = 15
    IS = 16
    AS = 17


class ASTNode:
    """
    Base class for all AST nodes.
    """

    def validate(self, visitor: IVisitor, context):
        """
        Validates the current node by invoking the corresponding
        visit method on the provided visitor.

        Args:
            visitor (IVisitor): The visitor object used to perform the validation.
            context: Additional context information that can be passed to the visitor.

        Returns:
            The result of the visit method called on the visitor.

        """
        return visitor.visit_node(self, context)


@dataclass
class Program(ASTNode):
    """
    Represents a program node in the AST.
    """

    defines: list["DefineStatement"]
    statements: list["Expression"]


@dataclass
class DefineStatement(ASTNode):
    """
    Represents a define statement node in the AST.
    """


@dataclass
class TypeDeclaration(DefineStatement):
    """
    Represents a type declaration node in the AST.
    """

    identifier: str
    params: list["Parameter"]
    inherits: "Inherits"
    attributes: list["AttributeDeclaration"]
    functions: list["FunctionDeclaration"]


@dataclass
class Inherits(ASTNode):
    """
    Represents an inherits node in the AST.
    """

    identifier: str
    arguments: list["Expression"]


@dataclass
class AttributeDeclaration(ASTNode):
    """
    Represents an attribute declaration node in the AST.
    """

    identifier: str
    expression: "Expression"
    type: any = None

    type: any = None


@dataclass
class FunctionDeclaration(DefineStatement):
    """
    Represents a function declaration node in the AST.
    """

    identifier: Token
    params: list[list["Parameter"]]
    body: any
    return_type: any = None


@dataclass
class Parameter(ASTNode):
    """
    Represents a parameter node in the AST.
    """

    identifier: str
    type: any = None


@dataclass
class ProtocolDeclaration(DefineStatement):
    """
    Represents a protocol declaration node in the AST.
    """

    identifier: str
    extends: list
    functions: list[FunctionDeclaration]


class Expression(ASTNode):
    """
    Represents an expression node in the AST.
    """

    def __init__(self) -> None:
        self.inferred_type: Type = UnkownType()


@dataclass
class VariableDeclaration(Expression):
    """
    Represents a variable declaration node in the AST.
    """

    identifier: Token
    expression: Expression
    type: any = None


@dataclass
class Identifier(Expression):
    """
    Represents a variable node in the AST.
    """

    identifier: str


@dataclass
class DestructiveAssign(Expression):
    """
    Represents a destructive assignment node in the AST.
    """

    identifier: str
    expression: Expression


@dataclass
class Call(Expression):
    """
    Represents a function call node in the AST.
    """

    obj: Expression
    identifier: str
    arguments: list["Expression"]


@dataclass
class Elif(Expression):
    """
    Represents an elif clause node in the AST.
    """

    condition: Expression
    body: Expression


@dataclass
class If(Expression):
    """
    Represents an if statement node in the AST.
    """

    condition: Expression
    body: Expression
    elif_clauses: list[Elif]
    else_body: Expression


@dataclass
class For(Expression):
    """
    Represents a for loop node in the AST.
    """

    index_identifier: str
    index_identifier_type: str
    iterable: Expression
    body: Expression


@dataclass
class While(Expression):
    """
    Represents a while loop node in the AST.
    """

    condition: Expression
    body: Expression


@dataclass
class ExpressionBlock:
    """
    Represents an expression block node in the AST.
    """

    body: list[Expression]


@dataclass
class LetVar(Expression):
    """
    Represents a let variable node in the AST.
    """

    declarations: list[Expression]
    body: Expression


@dataclass
class Instanciate(Expression):
    """
    Represents an instantiation node in the AST.
    """

    identifier: str
    params: list[Expression]


@dataclass
class Vector(Expression):
    """
    Represents a vector node in the AST.
    """

    elements: list
    generator: Expression
    item: Token
    iterator: Expression


@dataclass
class IndexNode(Expression):
    """
    Represents an index node in the AST.
    """

    obj: Expression
    index: Expression


@dataclass
class BinaryExpression(Expression):
    """
    Represents a binary expression node in the AST.
    """

    operator: Operator
    left: Expression
    right: Expression


@dataclass
class NotNode(Expression):
    """
    Represents a not node in the AST.
    """

    expression: Expression


@dataclass
class PositiveNode(Expression):
    """
    Represents a positive node in the AST.
    """

    expression: Expression


@dataclass
class NegativeNode(Expression):
    """
    Represents a not node in the AST.
    """

    expression: Expression


@dataclass
class LiteralNode(Expression):
    """
    Represents a literal node in the AST.
    """

    lex: Token
