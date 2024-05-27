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
    IS = 15
    AS = 16


@dataclass
class Node(ABC):
    """
    Abstract base class for all AST nodes.
    """
    pass

@dataclass
class Program(Node):
    """
    Represents a program node in the AST.
    """
    defines: list[DefineStatement]
    statements: list[]

@dataclass
class DefineStatement(Node):
    """
    Represents a define statement node in the AST.
    """
    pass

@dataclass
class TypeDeclaration(DefineStatement):
    """
    Represents a type declaration node in the AST.
    """
    identifier: Token
    params: list
    inherits: any
    attributes: list
    functions: list

@dataclass
class Inherits(Node):
    """
    Represents an inherits node in the AST.
    """
    identifier: Token
    arguments: list

@dataclass
class AttributeDeclaration(Node):
    """
    Represents an attribute declaration node in the AST.
    """
    identifier: Token
    type = None
    expression: any

@dataclass
class FunctionDeclaration(DefineStatement):
    """
    Represents a function declaration node in the AST.
    """
    identifier: Token
    params: list
    body: any
    return_type: any = None

@dataclass
class Parameter(Node):
    """
    Represents a parameter node in the AST.
    """
    identifier: Token
    type = None

@dataclass
class ProtocolDeclaration(DefineStatement):
    """
    Represents a protocol declaration node in the AST.
    """
    identifier: Token
    extends: list
    functions: list[FunctionDeclaration]

@dataclass
class Expression(Node):
    """
    Represents an expression node in the AST.
    """
    pass

@dataclass
class VariableDeclaration(Expression):
    """
    Represents a variable declaration node in the AST.
    """
    identifier: Token
    type = None
    expression: any

@dataclass
class Variable(Expression):
    """
    Represents a variable node in the AST.
    """
    identifier: Token
    type = None
    expression: any

@dataclass
class DestructiveAssign(Expression):
    """
    Represents a destructive assignment node in the AST.
    """
    identifier: Token
    expression: any

@dataclass
class Call(Expression):
    """
    Represents a function call node in the AST.
    """
    identifier: Token
    params: list

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
    elifclauses: list
    elseBody: Expression

@dataclass
class For(Expression):
    """
    Represents a for loop node in the AST.
    """
    indexIdentifier: Token
    indexIdentifierTyppe: Token
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
    body: list

@dataclass
class LetVar(Expression):
    """
    Represents a let variable node in the AST.
    """
    declarations: list
    body: Expression

@dataclass
class Instanciate(Expression):
    """
    Represents an instantiation node in the AST.
    """
    identifier: Token
    params: list

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
class LiteralNode(Expression):
    """
    Represents a literal node in the AST.
    """
    lex: Token
