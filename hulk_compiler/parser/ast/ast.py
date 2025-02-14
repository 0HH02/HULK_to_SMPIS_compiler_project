"""
This module contains the AST nodes for the Hulk programming language.
"""

from enum import Enum

from ...semantic_analizer.types import Type, UnknownType


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


class Program(ASTNode):
    """
    Represents a program node in the AST.
    """

    def __init__(self, defines: list["DefineStatement"], statement: "Expression"):
        self.defines: list["DefineStatement"] = defines
        self.statement: "Expression" = statement


class DefineStatement(ASTNode):
    """
    Represents a define statement node in the AST.
    """


class TypeDeclaration(DefineStatement):
    """
    Represents a type declaration node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        params: list["Parameter"],
        inherits: "Inherits",
        attributes: list["AttributeDeclaration"],
        functions: list["FunctionDeclaration"],
        line=None,
        column=None,
    ) -> None:
        self.identifier: str = identifier
        self.params: list["Parameter"] = params
        self.inherits: "Inherits" = inherits
        self.attributes: list["AttributeDeclaration"] = attributes
        self.functions: list["FunctionDeclaration"] = functions
        self.line: int = line
        self.column: int = column


class Inherits(ASTNode):
    """
    Represents an inherits node in the AST.
    """

    def __init__(
        self, identifier: str, arguments: list["Expression"], line=None, column=None
    ) -> None:
        self.identifier: str = identifier
        self.arguments: list["Expression"] = arguments
        self.line: int = line
        self.column: int = column


class AttributeDeclaration(ASTNode):
    """
    Represents an attribute declaration node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        expression: "Expression",
        static_type: str | None = None,
        line=None,
        column=None,
    ):
        self.identifier: str = identifier
        self.expression: "Expression" = expression
        self.static_type: str | None = static_type
        self.line: int = line
        self.column: int = column


class FunctionDeclaration(DefineStatement):
    """
    Represents a function declaration node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        params: list["Parameter"],
        body: "Expression",
        declared_return_type: str | None = None,
        line=None,
        column=None,
    ) -> None:
        self.identifier: str = identifier
        self.params: list["Parameter"] = params
        self.body: "Expression" = body
        self.static_return_type: str | None = declared_return_type
        self.inferred_return_type: Type = UnknownType()
        self.line: int = line
        self.column: int = column


class Parameter(ASTNode):
    """
    Represents a parameter node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        static_type: str | None = None,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ) -> None:

        self.identifier: str = identifier
        self.static_type: str | None = static_type
        self.inferred_type: Type = inferred_type
        self.line: int = line
        self.column: int = column


class ProtocolDeclaration(DefineStatement):
    """
    Represents a protocol declaration node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        extends: list[str],
        functions: list[FunctionDeclaration],
        line=None,
        column=None,
    ):
        self.identifier: str = identifier
        self.extends: list[str] = extends
        self.functions: list[FunctionDeclaration] = functions
        self.line: int = line
        self.column: int = column


class Expression(ASTNode):
    """
    Represents an expression node in the AST.
    """

    def __init__(self, inferred_type: Type) -> None:
        self.inferred_type = inferred_type


class VariableDeclaration(Expression):
    """
    Represents a variable declaration node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        expression: Expression,
        static_type: str | None = None,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):

        self.identifier: str = identifier
        self.expression: Expression = expression
        self.static_type: str | None = static_type
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class Identifier(Expression):
    """
    Represents a variable node in the AST.
    """

    def __init__(
        self, identifier, inferred_type: Type = UnknownType(), line=None, column=None
    ):
        self.identifier: str = identifier
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class AttributeCall(Expression):
    """
    Represents a function call node in the AST.
    """

    def __init__(
        self,
        obj: Expression,
        identifier: str,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ) -> None:
        self.obj: Expression = obj
        self.identifier: str = identifier
        self.line = line
        self.column = column
        super().__init__(inferred_type)


class DestructiveAssign(Expression):
    """
    Represents a destructive assignment node in the AST.
    """

    def __init__(
        self,
        identifier: Identifier | AttributeCall,
        expression: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ) -> None:
        self.identifier: Identifier | AttributeCall = identifier
        self.expression: Expression = expression
        self.line = line
        self.column = column
        super().__init__(inferred_type)


class FunctionCall(Expression):
    """
    Represents a function call node in the AST.
    """

    def __init__(
        self,
        obj: Expression,
        invocation: "Invocation",
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.obj: Expression = obj
        self.invocation: "Invocation" = invocation
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class Invocation(Expression):
    """
    Represents an invocation of a function or method.

    Attributes:
        identifier (str): The name of the function or method being invoked.
        arguments (list[Expression]): The list of arguments passed to the function or method.
    """

    def __init__(
        self,
        identifier: str,
        arguments: list["Expression"],
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.identifier: str = identifier
        self.arguments: list["Expression"] = arguments
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class Elif(Expression):
    """
    Represents an elif clause node in the AST.
    """

    def __init__(
        self,
        condition: "Expression",
        body: "Expression",
        inferred_type: Type = UnknownType(),
    ):
        self.condition: Expression = condition
        self.body: Expression = body
        super().__init__(inferred_type)


class If(Expression):
    """
    Represents an if statement node in the AST.
    """

    def __init__(
        self,
        condition: Expression,
        body: Expression,
        elif_clauses: list[Elif],
        else_body: Expression,
        inferred_type: Type = UnknownType(),
    ):
        self.condition: Expression = condition
        self.body: Expression = body
        self.elif_clauses: list[Elif] = elif_clauses
        self.else_body: Expression = else_body
        super().__init__(inferred_type)


class For(Expression):
    """
    Represents a for loop node in the AST.
    """

    def __init__(
        self,
        index_identifier: str,
        index_identifier_type: Type,
        iterable: Expression,
        body: Expression,
        inferred_type: Type = UnknownType(),
    ):
        self.index_identifier: str = index_identifier
        self.index_identifier_type: Type = (
            index_identifier_type if not index_identifier_type else UnknownType()
        )
        self.iterable: Expression = iterable
        self.body: Expression = body
        super().__init__(inferred_type)


class While(Expression):
    """
    Represents a while loop node in the AST.
    """

    def __init__(
        self,
        condition: Expression,
        body: Expression,
        inferred_type: Type = UnknownType(),
    ):
        self.condition: Expression = condition
        self.body: Expression = body
        super().__init__(inferred_type)


class ExpressionBlock(Expression):
    """
    Represents an expression block node in the AST.
    """

    def __init__(self, body: list[Expression], inferred_type: Type = UnknownType()):
        self.body: list[Expression] = body
        super().__init__(inferred_type)


class LetVar(Expression):
    """
    Represents a let variable node in the AST.
    """

    def __init__(
        self,
        declartions: list[VariableDeclaration],
        body: Expression,
        inferred_type: Type = UnknownType(),
    ):
        self.declarations: list[VariableDeclaration] = declartions
        self.body: Expression = body
        super().__init__(inferred_type)


class Instanciate(Expression):
    """
    Represents an instantiation node in the AST.
    """

    def __init__(
        self,
        identifier: str,
        params: list[Expression],
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.identifier: str = identifier
        self.params: list[Expression] = params
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class Vector(Expression):
    """
    Represents a vector node in the AST.
    """

    def __init__(
        self,
        elements: list["LiteralNode"],
        elements_type: Type = UnknownType(),
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.elements: list["LiteralNode"] = elements
        self.elements_type: Type = elements_type
        self.lin = line
        self.column = column
        super().__init__(inferred_type)


class ComprehensionVector(Expression):
    """
    Represents a vector node in the AST.
    """

    def __init__(
        self,
        generator: Expression,
        identifier: str,
        iterator: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.generator: Expression = generator
        self.identifier: str = identifier
        self.iterator: Expression = iterator
        self.line = line
        self.column = column
        super().__init__(inferred_type)


class IndexNode(Expression):
    """
    Represents an index node in the AST.
    """

    def __init__(
        self,
        obj: Expression,
        index: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ) -> None:
        self.obj: Expression = obj
        self.index: Expression = index
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class BinaryExpression(Expression):
    """
    Represents a binary expression node in the AST.
    """

    def __init__(
        self,
        operator: Operator,
        left: Expression,
        right: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.operator: Operator = operator
        self.left: Expression = left
        self.right: Expression = right
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class NotNode(Expression):
    """
    Represents a not node in the AST.
    """

    def __init__(
        self,
        expression: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.expression: Expression = expression
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class PositiveNode(Expression):
    """
    Represents a positive node in the AST.
    """

    def __init__(
        self,
        expression: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.expression: Expression = expression
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class NegativeNode(Expression):
    """
    Represents a not node in the AST.
    """

    def __init__(
        self,
        expression: Expression,
        inferred_type: Type = UnknownType(),
        line=None,
        column=None,
    ):
        self.expression: Expression = expression
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)


class LiteralNode(Expression):
    """
    Represents a literal node in the AST.
    """

    def __init__(
        self,
        value: str,
        inferred_type: Type,
        line=None,
        column=None,
    ) -> None:
        self.value: str = value
        self.line: int = line
        self.column: int = column
        super().__init__(inferred_type)
