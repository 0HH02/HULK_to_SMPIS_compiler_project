"""

"""

from multipledispatch import dispatch
from .semantic_exceptions import (
    InferTypeException,
    InvalidDeclarationException,
)
from .context import Context
from .types import (
    StringType,
    NumberType,
    BooleanType,
    RangeType,
    IdentifierVar,
    UnkownType,
)
from ..lexer.token import TokenType
from ..core.i_visitor import IVisitor
from ..parser.ast.ast import (
    LiteralNode,
    PositiveNode,
    NegativeNode,
    NotNode,
    Identifier,
    If,
    LetVar,
    Elif,
    While,
    For,
    Invocation,
    FunctionCall,
    AttributeCall,
    DestructiveAssign,
    BinaryExpression,
    VariableDeclaration,
    Operator,
)

# pylint: disable=function-redefined
# pylint: disable=line-too-long


class TypeCheckVisitor(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @staticmethod
    @dispatch(LiteralNode)
    def visit_node(node: LiteralNode, context: Context) -> bool:

        if node.token.token_type == TokenType.NUMBER_LITERAL:
            node.inferred_type = NumberType()
        elif node.token.token_type == TokenType.STRING_LITERAL:
            node.inferred_type = StringType()
        else:
            node.inferred_type = BooleanType()

        return True

    @staticmethod
    @dispatch(NegativeNode | PositiveNode)
    def visit_node(node: NegativeNode, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)
        return isinstance(node.expression.inferred_type, NumberType)

    @staticmethod
    @dispatch(NotNode)
    def visit_node(node: NotNode, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)
        return isinstance(node.expression.inferred_type, BooleanType)

    @staticmethod
    @dispatch(While | Elif)
    def visit_node(node: While, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.condition, context)
        if not isinstance(node.condition.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        return TypeCheckVisitor.visit_node(node.body, context)

    @staticmethod
    @dispatch(If)
    def visit_node(node: If, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.condition, context)

        if not isinstance(node.condition.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        valid_body: bool = TypeCheckVisitor.visit_node(node.body, context)

        if not valid_body:
            return False

        for elif_clause in node.elif_clauses:
            elif_valid = TypeCheckVisitor.visit_node(elif_clause, context)
            if not elif_valid:
                return False

        return TypeCheckVisitor.visit_node(node.else_body, context)

    @staticmethod
    @dispatch(For)
    def visit_node(node: For, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.iterable, context)

        if not isinstance(node.iterable.inferred_type, RangeType):
            print(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to iterable"
            )
            return False

        new_context = context.create_child_context()
        new_context.define_variable(IdentifierVar(node.index_identifier, NumberType()))

        return TypeCheckVisitor.visit_node(node.body, new_context)

    @staticmethod
    @dispatch(FunctionCall)
    def visit_node(node: FunctionCall, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type

        if isinstance(object_type, UnkownType):
            print("Can not infer type of expression")
            return False

        method = object_type.get_method(node.invocation.identifier)
        if method is None:
            print(
                f"Method {node.invocation.identifier} is not defined in {object_type.name}"
            )
            return False

        if len(node.invocation.arguments) != len(method.params):
            print(
                f"Method {node.invocation.identifier} expects {len(method.params)} arguments, but {len(node.arguments)} were given"
            )
            return False

        for i, arg in enumerate(node.invocation.arguments):
            if arg.inferred_type is not method.params[i]:
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].name}"
                )
                return False

        return True

    @staticmethod
    @dispatch(Invocation)
    def visit_node(node: Invocation, context: Context):

        if not context.check_method(node.identifier, node.arguments):
            print(f"Method {node.identifier} is not defined")
            return False

        method = context.get_method(node.identifier, len(node.arguments))

        for i, arg in enumerate(node.arguments):
            if arg.inferred_type is not method.params[i]:
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].name}"
                )
                return False

        return True

    @staticmethod
    @dispatch(AttributeCall)
    def visit_node(node: AttributeCall, context: Context):
        TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type
        if isinstance(object_type, UnkownType):
            print("Can not infer type of expression")
            return False
        atrribute = object_type.get_attribute(node.identifier)

        if atrribute is None:
            print(f"Attribute {node.identifier} is not defined in {object_type.name}")
            return False

        node.inferred_type = atrribute.type

        return True

    @staticmethod
    @dispatch(DestructiveAssign)
    def visit_node(node: DestructiveAssign, context: Context):
        if not isinstance(node.identifier, (AttributeCall, Identifier)):
            print(
                "Invalid Assignment , The left part of the assignment must be a variable or attribute"
            )
            return False

        TypeCheckVisitor.visit_node(node.identifier, context)
        TypeCheckVisitor.visit_node(node.expression, context)

        return node.identifier.inferred_type == node.expression.inferred_type

    @staticmethod
    @dispatch(Identifier)
    def visit_node(node: Identifier, context: Context) -> bool:

        if not context.check_var(node.identifier):
            print(f"Variable {node.identifier} is not defined")
            return False

        node.inferred_type = context.get_var_type(node.identifier)

        return True

    @staticmethod
    @dispatch(LetVar)
    def visit_node(node: LetVar, context: Context) -> bool:
        new_context = context.create_child_context()
        for var_declaration in node.declarations:
            valid_declaration: bool = TypeCheckVisitor.visit_node(
                var_declaration, context
            )
            if not valid_declaration:
                raise InvalidDeclarationException(var_declaration.identifier)

            new_context.define_variable(
                IdentifierVar(var_declaration.identifier, var_declaration.type)
            )

        TypeCheckVisitor.visit_node(node.body, new_context)

    @staticmethod
    @dispatch(VariableDeclaration)
    def visit_node(node: VariableDeclaration, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)

        if node.type is not None:
            if not context.check_type(node.type):
                raise InvalidDeclarationException(node.type)

            if not node.expression.inferred_type.conforms_to(node.type):
                print(
                    f"Can not implicitly convert from {node.expression.inferred_type.name} to {node.type}"
                )
                return False

            return True

        if node.expression.inferred_type is UnkownType:
            raise InferTypeException()

        node.type = node.expression.inferred_type
        return True

    @staticmethod
    @dispatch(BinaryExpression)
    def visit_node(node: BinaryExpression, context: Context) -> bool:
        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            return TypeCheckVisitor._visit_binary_aritmethic(node, context)

        if node.operator in [Operator.AND, Operator.OR]:
            return TypeCheckVisitor._visit_binary_logic(node, context)

        if node.operator in [
            Operator.EQ,
            Operator.NEQ,
            Operator.GT,
            Operator.LT,
            Operator.GE,
            Operator.LE,
        ]:
            return TypeCheckVisitor._visit_binary_comparison(node, context)

        if node.operator is Operator.IS:
            return TypeCheckVisitor._visit_binary_type_checker(node, context)

        if node.operator is Operator.AS:
            return TypeCheckVisitor._visit_binary_downcast(node, context)

        if node.operator in [Operator.CONCAT, Operator.DCONCAT]:
            return TypeCheckVisitor._visit_binary_concat(node, context)

        return False

    @staticmethod
    def _visit_binary_aritmethic(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if not isinstance(node.left.inferred_type, NumberType):
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to number"
            )
            return False

        if not isinstance(node.right.inferred_type, NumberType):
            print(
                f"Can not implicitly convert from {node.right.inferred_type.name} to number"
            )
            return False

        return True

    @staticmethod
    def _visit_binary_logic(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if not isinstance(node.left.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to boolean"
            )
            return False

        if not isinstance(node.right.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.right.inferred_type.name} to boolean"
            )
            return False

        return True

    @staticmethod
    def _visit_binary_comparison(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if node.left.inferred_type != node.right.inferred_type:
            print(
                f"Can not compare {node.left.inferred_type.name} with {node.right.inferred_type.name}"
            )
            return False

        return True

    @staticmethod
    def _visit_binary_downcast(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if isinstance(node.right, Identifier):
            if not context.check_type(node.right.identifier):
                print(f"Type {node.right.identifier} is not defined")
                return False

            return node.right.inferred_type.conforms_to(node.left.inferred_type)

        print("Invalid Expression")
        return False

    @staticmethod
    def _visit_binary_type_checker(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if isinstance(node.right, Identifier):
            if not context.check_type(node.right.identifier):
                print(f"Type {node.right.identifier} is not defined")
                return False

            return node.left.inferred_type is node.right.inferred_type

        print("Invalid Expression")
        return False

    @staticmethod
    def _visit_binary_concat(node: BinaryExpression, context: Context):
        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if (
            not isinstance(node.left.inferred_type, NumberType)
            and not isinstance(node.left.inferred_type, StringType)
        ) or (
            not isinstance(node.right.inferred_type, NumberType)
            and not isinstance(node.right.inferred_type, StringType)
        ):
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to string"
            )
            return False

        return True
