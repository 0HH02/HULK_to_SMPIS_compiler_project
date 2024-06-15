"""

"""

from multipledispatch import dispatch

from hulk_compiler.semantic_analizer.types import Type

from .hulk_transpiler import HulkTranspiler

from .context import Context
from .types import (
    StringType,
    NumberType,
    BooleanType,
    RangeType,
    IdentifierVar,
    UnknownType,
    Method,
)
from ..core.i_visitor import IVisitor
from ..parser.ast.ast import (
    LiteralNode,
    PositiveNode,
    NegativeNode,
    NotNode,
    Identifier,
    ExpressionBlock,
    If,
    LetVar,
    Instanciate,
    Elif,
    While,
    For,
    Invocation,
    FunctionCall,
    AttributeCall,
    DestructiveAssign,
    Vector,
    IndexNode,
    BinaryExpression,
    VariableDeclaration,
    Operator,
    Program,
)


# pylint: disable=function-redefined
# pylint: disable=line-too-long
# pylint: disable=arguments-differ


class TypeCheckVisitor(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @staticmethod
    @dispatch(Program, Context)
    def visit_node(node: Program, context: Context) -> bool:
        return TypeCheckVisitor.visit_node(node.statement, context)

    @staticmethod
    @dispatch(LiteralNode, Context)
    def visit_node(node: LiteralNode, _: Context) -> bool:
        return True

    @staticmethod
    @dispatch(NegativeNode, Context)
    def visit_node(node: NegativeNode | PositiveNode, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)
        return isinstance(node.expression.inferred_type, NumberType)

    @staticmethod
    @dispatch(PositiveNode, Context)
    def visit_node(node: PositiveNode, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)
        return isinstance(node.expression.inferred_type, NumberType)

    @staticmethod
    @dispatch(NotNode, Context)
    def visit_node(node: NotNode, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)
        return isinstance(node.expression.inferred_type, BooleanType)

    @staticmethod
    @dispatch(ExpressionBlock, Context)
    def visit_node(node: ExpressionBlock, context: Context) -> bool:

        for expression in node.body:
            valid_expression: bool = TypeCheckVisitor.visit_node(expression, context)
            if not valid_expression:
                return False

        node.inferred_type = node.body[-1].inferred_type

        return True

    @staticmethod
    @dispatch(While, Context)
    def visit_node(node: While, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.condition, context)
        if not isinstance(node.condition.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        return TypeCheckVisitor.visit_node(node.body, context)

    @staticmethod
    @dispatch(Elif, Context)
    def visit_node(node: Elif, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.condition, context)
        if not isinstance(node.condition.inferred_type, BooleanType):
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        return TypeCheckVisitor.visit_node(node.body, context)

    @staticmethod
    @dispatch(If, Context)
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
    @dispatch(For, Context)
    def visit_node(node: For, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.iterable, context)

        if not isinstance(node.iterable.inferred_type, RangeType):
            print(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to iterable"
            )
            return False

        node.index_identifier_type = node.iterable.items_type

        new_context = context.create_child_context()
        new_context.define_variable(
            IdentifierVar(node.index_identifier, node.index_identifier_type)
        )

        return TypeCheckVisitor.visit_node(node.body, new_context)

    @staticmethod
    @dispatch(Vector, Context)
    def visit_node(node: Vector, context: Context):

        vector_type = None

        for element in node.elements:
            TypeCheckVisitor.visit_node(element, context)
            if vector_type is None:
                vector_type = element.inferred_type
            else:
                if vector_type != element.inferred_type:
                    print(
                        f"Can not implicitly convert from {element.inferred_type.name} to {vector_type.name}"
                    )
                    return False

        node.inferred_type = RangeType(vector_type)
        return True

    @staticmethod
    @dispatch(IndexNode, Context)
    def visit_node(node: IndexNode, context: Context):
        TypeCheckVisitor.visit_node(node.obj, context)
        TypeCheckVisitor.visit_node(node.index, context)

        if not isinstance(node.obj.inferred_type, Vector):
            print(f"Object of type {node.obj.inferred_type.name} is not suscriptable")
            return False

        if not isinstance(node.index.inferred_type, NumberType):
            print(
                f"Can't implicity convert from {node.index.inferred_type.name} to Number"
            )
            return False

        node.inferred_type = node.obj.items_type

        return True

    @staticmethod
    @dispatch(FunctionCall, Context)
    def visit_node(node: FunctionCall, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type

        if isinstance(object_type, UnknownType):
            print("Can not infer type of expression")
            return False

        method: Method | None = object_type.get_method(node.invocation.identifier)
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
            if not arg.inferred_type.conforms_to(method.params[i].type):
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].name}"
                )
                return False

        return True

    @staticmethod
    @dispatch(Invocation, Context)
    def visit_node(node: Invocation, context: Context):

        method: Method | None = context.get_method(node.identifier, len(node.arguments))

        if method is None:
            print(f"Method {node.identifier} is not defined")
            return False

        for i, arg in enumerate(node.arguments):

            TypeCheckVisitor.visit_node(arg, context)

            if not arg.inferred_type.conforms_to(method.params[i].type):
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].type}"
                )
                return False

        return True

    @staticmethod
    @dispatch(AttributeCall, Context)
    def visit_node(node: AttributeCall, context: Context):
        TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type
        if isinstance(object_type, UnknownType):
            print("Can not infer type of expression")
            return False
        atrribute: IdentifierVar | None = object_type.get_attribute(node.identifier)

        if atrribute is None:
            print(f"Attribute {node.identifier} is not defined in {object_type.name}")
            return False

        node.inferred_type = atrribute.type

        return True

    @staticmethod
    @dispatch(DestructiveAssign, Context)
    def visit_node(node: DestructiveAssign, context: Context):

        if not isinstance(node.identifier, (AttributeCall, Identifier)):
            print(
                "Invalid Assignment , The left part of the assignment must be a variable or attribute"
            )
            return False

        TypeCheckVisitor.visit_node(node.identifier, context)
        TypeCheckVisitor.visit_node(node.expression, context)

        return node.expression.inferred_type.conforms_to(node.identifier.inferred_type)

    @staticmethod
    @dispatch(Identifier, Context)
    def visit_node(node: Identifier, context: Context) -> bool:

        var_type = context.get_var_type(node.identifier)

        if var_type is None:
            print(f"Variable {node.identifier} is not defined")
            return False

        node.inferred_type = var_type
        return True

    @staticmethod
    @dispatch(LetVar, Context)
    def visit_node(node: LetVar, context: Context) -> bool:

        HulkTranspiler.visit_node(node)
        new_context: Context = context.create_child_context()
        valid_node = True

        for var_declaration in node.declarations:
            valid_declaration: bool = TypeCheckVisitor.visit_node(
                var_declaration, context
            )
            valid_node &= valid_declaration

            new_context.define_variable(
                IdentifierVar(var_declaration.identifier, var_declaration.inferred_type)
            )

        return valid_node and TypeCheckVisitor.visit_node(node.body, new_context)

    @staticmethod
    @dispatch(VariableDeclaration, Context)
    def visit_node(node: VariableDeclaration, context: Context) -> bool:
        TypeCheckVisitor.visit_node(node.expression, context)

        if not isinstance(node.static_type, UnknownType):
            if context.get_type(node.static_type.name) is None:
                print(f"Type {node.static_type.name} is not defined")

            if not node.expression.inferred_type.conforms_to(node.static_type):
                print(
                    f"Can not implicitly convert from {node.expression.inferred_type.name} to {node.static_type}"
                )
                return False

            return True

        if isinstance(node.expression.inferred_type, UnknownType):
            print("Can't infer type of expression")

        node.inferred_type = node.expression.inferred_type
        return True

    @staticmethod
    @dispatch(Instanciate, Context)
    def visit_node(node: Instanciate, context: Context) -> bool:

        type_t: Type | None = context.get_type(node.identifier)

        if type_t is None:
            print(f"{node.identifier} is not defined")
            return False

        if len(type_t.params) != len(node.params):
            print(
                f"Invalid constructor call {len(node.params)} arguments expected {len(type_t.params)} were given"
            )
            return False

        for i, param in enumerate(node.params):
            if not param.inferred_type.conforms_to(type_t.params[i]):
                print(
                    f"Can't implicity convert from {param.inferred_type.name} to {type_t.params[i].name}"
                )
                return False

        return True

    @staticmethod
    @dispatch(BinaryExpression, Context)
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

        node.inferred_type = NumberType()
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

        node.inferred_type = BooleanType()
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

        node.inferred_type = BooleanType()
        return True

    @staticmethod
    def _visit_binary_downcast(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if isinstance(node.right, Identifier):
            if not context.check_type_or_protocol(node.right.identifier):
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
            if not context.check_type_or_protocol(node.right.identifier):
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
