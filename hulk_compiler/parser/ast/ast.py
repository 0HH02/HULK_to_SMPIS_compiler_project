from dataclasses import dataclass
from abc import ABC
from enum import Enum
from hulk_compiler.lexer.token import Token


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


@dataclass
class Node(ABC):
    """
    Abstract base class for all AST nodes.
    """


@dataclass
class Program(Node):
    """
    Represents a program node in the AST.
    """

    defines: list["DefineStatement"]
    statements: list["Expression"]


@dataclass
class DefineStatement(Node):
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
class Inherits(Node):
    """
    Represents an inherits node in the AST.
    """

    identifier: str
    arguments: list["Expression"]


@dataclass
class AttributeDeclaration(Node):
    """
    Represents an attribute declaration node in the AST.
    """

    identifier: str
    expression: "Expression"
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
class Parameter(Node):
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


@dataclass
class Expression(Node, ABC):
    """
    Represents an expression node in the AST.
    """


@dataclass
class VariableDeclaration(Expression):
    """
    Represents a variable declaration node in the AST.
    """

    identifier: Token
    expression: Expression
    type: any = None


@dataclass
class Variable(Expression):
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
    indexIdentifierTyppe: str
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
class BinaryExpression(Node):
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
    Represents a not node in the AST.
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
