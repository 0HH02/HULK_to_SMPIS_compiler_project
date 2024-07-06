"""

"""

from multipledispatch import dispatch

from hulk_compiler.semantic_analizer.types import Protocol, Type

from .error_stack import StackError

from .context import Context
from .types import (
    StringType,
    NumberType,
    BooleanType,
    IdentifierVar,
    UnknownType,
    Method,
    VectorType,
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
    ComprehensionVector,
    IndexNode,
    BinaryExpression,
    VariableDeclaration,
    Operator,
    Program,
    TypeDeclaration,
    FunctionDeclaration,
    ProtocolDeclaration,
    AttributeDeclaration,
)


# pylint: disable=function-redefined
# pylint: disable=line-too-long
# pylint: disable=arguments-differ


class TypeChecker(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @staticmethod
    @dispatch(Program, Context, StackError)
    def check_node(node: Program, context: Context, stack: StackError) -> bool:
        valid_node = True
        for define in node.defines:
            valid_node &= TypeChecker.check_node(define, context, stack)

        valid_node &= TypeChecker.check_node(node.statement, context, stack)

        return valid_node

    @staticmethod
    @dispatch(LiteralNode, Context, StackError)
    def check_node(_: LiteralNode, __: Context, ___: StackError) -> bool:
        return True

    @staticmethod
    @dispatch(NegativeNode, Context, StackError)
    def check_node(node: NegativeNode, context: Context, stack: StackError) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context, stack)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(PositiveNode, Context, StackError)
    def check_node(node: PositiveNode, context: Context, stack: StackError) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context, stack)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(NotNode, Context, StackError)
    def check_node(node: NotNode, context: Context, stack: StackError) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context, stack)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(ExpressionBlock, Context, StackError)
    def check_node(node: ExpressionBlock, context: Context, stack: StackError) -> bool:
        valid_node = True

        for expression in node.body:
            valid_node &= TypeChecker.check_node(expression, context, stack)

        return valid_node

    @staticmethod
    @dispatch(While, Context, StackError)
    def check_node(node: While, context: Context, stack: StackError) -> bool:

        valid_node: bool = TypeChecker.check_node(node.condition, context, stack)
        if node.condition.inferred_type is not BooleanType():
            stack.add_error(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean",
                (node.condition.line, node.condition.column),
            )
            return False

        valid_node &= TypeChecker.check_node(node.body, context, stack)

        return valid_node

    @staticmethod
    @dispatch(Elif, Context, StackError)
    def check_node(node: Elif, context: Context, stack: StackError) -> bool:

        valid_condition: bool = TypeChecker.check_node(node.condition, context, stack)
        if node.condition.inferred_type is not BooleanType():
            stack.add_error(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean",
                (node.condition.line, node.condition.column),
            )
            return False

        return valid_condition and TypeChecker.check_node(node.body, context, stack)

    @staticmethod
    @dispatch(If, Context, StackError)
    def check_node(node: If, context: Context, stack: StackError) -> bool:

        valid_node: bool = TypeChecker.check_node(node.condition, context, stack)

        if node.condition.inferred_type is not BooleanType():
            stack.add_error(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean",
                (node.condition.line, node.condition.column),
            )
            return False

        for elif_c in node.elif_clauses:
            valid_node &= TypeChecker.check_node(elif_c, context, stack)

        valid_node &= TypeChecker.check_node(node.else_body, context, stack)

        return valid_node

    @staticmethod
    @dispatch(For, Context, StackError)
    def check_node(node: For, context: Context, stack: StackError) -> bool:

        valid_iter: bool = TypeChecker.check_node(node.iterable, context, stack)

        if not context.iter_protocol.is_implemented_by(node.iterable.inferred_type):
            stack.add_error(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to Iterable"(
                    node.iterable.line, node.iterable.column
                )
            )
            return False

        new_context = context.create_child_context()
        new_context.define_variable(
            IdentifierVar(node.index_identifier, node.index_identifier_type)
        )

        return valid_iter and TypeChecker.check_node(node.body, new_context, stack)

    @staticmethod
    @dispatch(Vector, Context, StackError)
    def check_node(node: Vector, context: Context, stack: StackError):

        valid_node = True
        vector_type = node.elements_type

        for element in node.elements:
            valid_node &= TypeChecker.check_node(element, context, stack)
            if element.inferred_type != vector_type:
                stack.add_error(
                    f"Can not implicity convert from {element.inferred_type} to {vector_type}",
                    (element.line, element.column),
                )
                return False

        return valid_node

    @staticmethod
    @dispatch(ComprehensionVector, Context, StackError)
    def check_node(node: ComprehensionVector, context: Context, stack: StackError):

        iterator_expression_valid: bool = TypeChecker.check_node(
            node.iterator, context, stack
        )

        if not context.iter_protocol.is_implemented_by(node.iterator.inferred_type):
            stack.add_error(
                f"Can't implicity convert from {node.iterator.inferred_type} to Iterable",
                (node.iterator.line, node.iterator.column),
            )
            return False

        child_context: Context = context.create_child_context()

        child_context.define_variable(
            IdentifierVar(
                node.identifier,
                node.iterator.inferred_type.get_method("current").return_type,
            )
        )

        generator_expresion_valid: bool = TypeChecker.check_node(
            node.generator, child_context, stack
        )

        return generator_expresion_valid and iterator_expression_valid

    @staticmethod
    @dispatch(IndexNode, Context, StackError)
    def check_node(node: IndexNode, context: Context, stack: StackError):

        valid_node = True

        valid_node &= TypeChecker.check_node(node.obj, context, stack)
        valid_node &= TypeChecker.check_node(node.index, context, stack)

        if not isinstance(node.obj.inferred_type, VectorType):
            stack.add_error(
                f"object of type {node.obj.inferred_type.name} is not suscriptable",
                (node.obj.line, node.obj.column),
            )
            return False

        if node.index.inferred_type is not NumberType():
            stack.add_error(
                f"Can't implicity convert from {node.index.inferred_type.name} to Number",
                (node.index.line, node.index.column),
            )
            return False

        return valid_node

    @staticmethod
    @dispatch(FunctionCall, Context, StackError)
    def check_node(node: FunctionCall, context: Context, stack: StackError) -> bool:

        valid_node: bool = TypeChecker.check_node(node.obj, context, stack)

        object_type = node.obj.inferred_type

        method: Method | None = object_type.get_method(node.invocation.identifier)

        if not method:
            stack.add_error(
                f"Method {node.invocation.identifier} is not defined in {object_type.name}",
                (node.line, node.column),
            )
            return False

        if len(node.invocation.arguments) != len(method.params):
            stack.add_error(
                f"Method {node.invocation.identifier} expects {len(method.params)} arguments, but {len(node.arguments)} were given",
                (node.invocation.line, node.invocation.column),
            )
            return False

        for i, arg in enumerate(node.invocation.arguments):
            if not arg.inferred_type.conforms_to(method.params[i].type):
                stack.add_error(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].name}",
                    (arg.line, arg.column),
                )
                return False

        return valid_node

    @staticmethod
    @dispatch(Invocation, Context, StackError)
    def check_node(node: Invocation, context: Context, stack: StackError):

        method: Method | None = context.get_method(node.identifier, len(node.arguments))

        if not method:
            if context.check_method(node.identifier):
                stack.add_error(
                    f"There is no method {node.identifier} that receives {len(node.arguments)} arguments",
                    (node.line, node.column),
                )
            else:
                stack.add_error(
                    f"Method {node.identifier} is not defined", (node.line, node.column)
                )
            return False

        for i, arg in enumerate(node.arguments):

            TypeChecker.check_node(arg, context, stack)

            if not arg.inferred_type.conforms_to(method.params[i].type):
                stack.add_error(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].type}",
                    (arg.line, arg.column),
                )
                return False

        return True

    @staticmethod
    @dispatch(AttributeCall, Context, StackError)
    def check_node(node: AttributeCall, context: Context, stack: StackError):

        valid_node: bool = TypeChecker.check_node(node.obj, context, stack)

        object_type = node.obj.inferred_type

        atrribute: IdentifierVar | None = object_type.get_attribute(node.identifier)

        if not atrribute:
            stack.add_error(
                f"Attribute {node.identifier} is not defined in {object_type.name}",
                (node.line, node.column),
            )
            return False

        return valid_node

    @staticmethod
    @dispatch(DestructiveAssign, Context, StackError)
    def check_node(node: DestructiveAssign, context: Context, stack: StackError):

        valid_node = True
        valid_node &= TypeChecker.check_node(node.expression, context, stack)

        return valid_node and node.expression.inferred_type.conforms_to(
            node.identifier.inferred_type
        )

    @staticmethod
    @dispatch(Identifier, Context, StackError)
    def check_node(_: Identifier, __: Context, ___: StackError) -> bool:
        return True

    @staticmethod
    @dispatch(LetVar, Context, StackError)
    def check_node(node: LetVar, context: Context, stack: StackError) -> bool:

        new_context: Context = context.create_child_context()
        valid_node = True

        for i, var_declaration in enumerate(node.declarations):

            valid_node &= TypeChecker.check_node(var_declaration, context, stack)

            new_context.define_variable(
                IdentifierVar(
                    var_declaration.identifier, node.declarations[i].inferred_type
                )
            )

        valid_node &= TypeChecker.check_node(node.body, new_context, stack)

        return valid_node

    @staticmethod
    @dispatch(VariableDeclaration, Context, StackError)
    def check_node(
        node: VariableDeclaration, context: Context, stack: StackError
    ) -> bool:

        valid_node: bool = TypeChecker.check_node(node.expression, context, stack)

        if node.static_type:
            static_type: Type | None = context.get_type_or_protocol(node.static_type)

            if not static_type:
                stack.add_error(
                    f"Type {node.static_type} is not defined", (node.line, node.column)
                )
                return False

            if not node.expression.inferred_type.conforms_to(static_type):
                stack.add_error(
                    f"Can't impicity convert from  {node.expression.inferred_type.name} to {static_type.name}",
                    (node.line, node.column),
                )
                return False

        return valid_node

    @staticmethod
    @dispatch(Instanciate, Context, StackError)
    def check_node(node: Instanciate, context: Context, stack: StackError) -> bool:

        type_t: Type | None = context.get_type(node.identifier)

        if not type_t:
            stack.add_error(
                f"{node.identifier} is not defined", (node.line, node.column)
            )
            return False

        if len(type_t.params) != len(node.params):
            stack.add_error(
                f"Invalid constructor call {len(node.params)} arguments expected {len(type_t.params)} were given",
                (node.line, node.column),
            )
            return False

        for i, param in enumerate(node.params):
            if not param.inferred_type.conforms_to(type_t.params[i].type):
                stack.add_error(
                    f"Can't implicity convert from {param.inferred_type.name} to {type_t.params[i].name}"(
                        param.line, param.column
                    )
                )
                return False

        return True

    @staticmethod
    @dispatch(BinaryExpression, Context, StackError)
    def check_node(node: BinaryExpression, context: Context, stack: StackError) -> bool:

        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            return TypeChecker._visit_binary_aritmethic(node, context, stack)

        if node.operator in [Operator.AND, Operator.OR]:
            return TypeChecker._visit_binary_logic(node, context, stack)

        if node.operator in [
            Operator.EQ,
            Operator.NEQ,
            Operator.GT,
            Operator.LT,
            Operator.GE,
            Operator.LE,
        ]:
            return TypeChecker._visit_binary_comparison(node, context, stack)

        if node.operator is Operator.IS:
            return TypeChecker._visit_binary_type_checker(node, context, stack)

        if node.operator is Operator.AS:
            return TypeChecker._visit_binary_downcast(node, context, stack)

        if node.operator in [Operator.CONCAT, Operator.DCONCAT]:
            return TypeChecker._visit_binary_concat(node, context, stack)

        return False

    @staticmethod
    def _visit_binary_aritmethic(
        node: BinaryExpression, context: Context, stack: StackError
    ) -> bool:

        TypeChecker.check_node(node.left, context, stack)
        TypeChecker.check_node(node.right, context, stack)

        if node.left.inferred_type is not NumberType():
            stack.add_error(
                f"Can not implicitly convert from {node.left.inferred_type.name} to Number",
                (node.left.line, node.left.column),
            )
            return False

        if node.right.inferred_type is not NumberType():
            stack.add_error(
                f"Can not implicitly convert from {node.right.inferred_type.name} to Number",
                (node.right.line, node.right.column),
            )
            return False

        return True

    @staticmethod
    def _visit_binary_logic(
        node: BinaryExpression, context: Context, stack: StackError
    ) -> bool:

        valid_node = TypeChecker.check_node(node.left, context, stack)
        valid_node &= TypeChecker.check_node(node.right, context, stack)

        if node.left.inferred_type is not BooleanType():
            stack.add_error(
                f"Can not implicitly convert from {node.left.inferred_type.name} to boolean",
                (node.left.line, node.left.column),
            )
            return False

        if node.right.inferred_type is not BooleanType():
            stack.add_error(
                f"Can not implicitly convert from {node.right.inferred_type.name} to boolean",
                (node.left.line, node.left.column),
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_comparison(
        node: BinaryExpression, context: Context, stack: StackError
    ) -> bool:

        valid_node = TypeChecker.check_node(node.left, context, stack)
        valid_node &= TypeChecker.check_node(node.right, context, stack)

        if node.left.inferred_type != node.right.inferred_type:
            stack.add_error(
                f"Can not compare {node.left.inferred_type.name} with {node.right.inferred_type.name}",
                (node.line, node.column),
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_downcast(
        node: BinaryExpression, context: Context, stack: StackError
    ) -> bool:

        valid_node: bool = TypeChecker.check_node(node.left, context, stack)

        if not context.get_type(node.right.identifier):
            stack.add_error(
                f"Type {node.right.identifier} is not defined",
                node.right.line,
                node.right.column,
            )
            return False

        if not node.right.inferred_type.conforms_to(node.left.inferred_type):
            stack.add_error(
                f"Can't cast from {node.right.inferred_type} to {node.left.inferred_type}",
                (node.right.line, node.right.column),
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_type_checker(
        node: BinaryExpression, context: Context, stack: StackError
    ) -> bool:

        valid_node = TypeChecker.check_node(node.left, context, stack)
        valid_node &= TypeChecker.check_node(node.right, context, stack)

        if not context.get_type(node.right.identifier):
            stack.add_error(
                f"Type {node.right.identifier} is not defined",
                (node.right.line, node.right.column),
            )
            return False

        if not node.right.inferred_type.conforms_to(node.left.inferred_type):
            stack.add_error(
                f"Can't implicity convert from {node.right.inferred_type} to {node.left.inferred_type}",
                (node.right.line, node.right.column),
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_concat(
        node: BinaryExpression, context: Context, stack: StackError
    ):
        valid_node = TypeChecker.check_node(node.left, context, stack)
        valid_node &= TypeChecker.check_node(node.right, context, stack)

        if (
            node.left.inferred_type is not NumberType()
            and node.left.inferred_type is not StringType()
        ) or (
            node.right.inferred_type is not NumberType()
            and node.right.inferred_type is not StringType()
        ):
            stack.add_error(
                f"Can not implicitly convert from {node.left.inferred_type.name} to String",
                (node.line, node.column),
            )
            return False

        return valid_node

    @staticmethod
    @dispatch(TypeDeclaration, Context, StackError)
    def check_node(node: TypeDeclaration, context: Context, stack: StackError):

        type_t = context.get_type(node.identifier)
        constructor_context = context.create_child_context()
        type_context = context.create_child_context()

        valid_node = True

        for param in type_t.params:
            valid_node &= param is not UnknownType()
            constructor_context.define_variable(param)

        if node.inherits and len(node.inherits.arguments) > 0:
            valid_node &= TypeChecker.check_node(
                Instanciate(node.inherits.identifier, node.inherits.arguments),
                constructor_context,
                stack,
            )

        for attr in node.attributes:
            valid_node &= TypeChecker.check_node(attr, context, stack)
            type_context.define_variable(type_t.get_attribute(attr.identifier))

        for method in node.functions:
            if type_t.parent:
                parent_function = type_t.parent.get_method(method.identifier)
                if parent_function:
                    type_context.define_method(
                        Method(
                            "base", parent_function.params, parent_function.return_type
                        )
                    )
            type_context.define_method(type_t.get_method(method.identifier))
            valid_node &= TypeChecker.check_node(method, type_context, stack)

        return valid_node

    @staticmethod
    @dispatch(ProtocolDeclaration, Context, StackError)
    def check_node(node: ProtocolDeclaration, context: Context, stack: StackError):
        protocol: Protocol | None = context.get_protocol(node.identifier)

        for method in protocol.methods.values():
            for param in method.params:
                if param.type is UnknownType():
                    stack.add_error(
                        f"Missing type declaration of param: {param.name} in method: {method.name} in protocol: {protocol.name}",
                        (node.line, node.column),
                    )
                    return False

            if method.return_type is UnknownType():
                stack.add_error(
                    f"Missing return type declaration of method: {method.name} in protocol: {protocol.name}",
                    (node.line, node.column),
                )
                return False

        return True

    @staticmethod
    @dispatch(FunctionDeclaration, Context, StackError)
    def check_node(node: FunctionDeclaration, context: Context, stack: StackError):

        function_t: Method = context.get_method(node.identifier, len(node.params))
        function_context: Context = context.create_child_context()

        for param in function_t.params:
            if param.type is UnknownType():
                stack.add_error(
                    f"Can't infer type of param {param.name} in method {node.identifier}",
                    (node.line, node.column),
                )
                return False

            function_context.define_variable(param)

        valid_node = TypeChecker.check_node(node.body, function_context, stack)

        if function_t.return_type is UnknownType():
            stack.add_error(
                f"Can't infer return type of method {node.identifier}",
                (node.line, node.column),
            )

        if not function_t.return_type.conforms_to(
            context.get_type_or_protocol(node.static_return_type)
            if node.static_return_type
            else UnknownType()
        ):
            stack.add_error(
                f"Can't implicty convert from {function_t.return_type} to {node.static_return_type}",
                (node.line, node.column),
            )
            return False
        return valid_node

    @staticmethod
    @dispatch(AttributeDeclaration, Context, StackError)
    def check_node(node: AttributeDeclaration, context: Context, stack: StackError):
        if node.expression.inferred_type is UnknownType():
            stack.add_error(
                "Can't infer type of expression",
                (node.expression.line, node.expression.column),
            )
            return False

        if not node.expression.inferred_type.conforms_to(
            context.get_type_or_protocol(node.static_type)
            if node.static_type
            else UnknownType()
        ):
            stack.add_error(
                f"Can't implicity convert from {node.expression.inferred_type} to {node.static_type}",
                (node.line, node.column),
            )
            return False

        return True
