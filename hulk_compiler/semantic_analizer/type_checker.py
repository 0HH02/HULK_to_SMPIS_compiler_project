"""

"""

from multipledispatch import dispatch

from hulk_compiler.semantic_analizer.types import Protocol, Type

from .transpiler.hulk_transpiler import HulkTranspiler

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
    @dispatch(Program, Context)
    def check_node(node: Program, context: Context) -> bool:
        valid_node = True
        for define in node.defines:
            valid_node &= TypeChecker.check_node(define, context)

        valid_node &= TypeChecker.check_node(node.statement, context)

        return valid_node

    @staticmethod
    @dispatch(LiteralNode, Context)
    def check_node(node: LiteralNode, _: Context) -> bool:
        return True

    @staticmethod
    @dispatch(NegativeNode, Context)
    def check_node(node: NegativeNode | PositiveNode, context: Context) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(PositiveNode, Context)
    def check_node(node: PositiveNode, context: Context) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(NotNode, Context)
    def check_node(node: NotNode, context: Context) -> bool:
        valid_node = TypeChecker.check_node(node.expression, context)
        return valid_node and node.expression.inferred_type is NumberType()

    @staticmethod
    @dispatch(ExpressionBlock, Context)
    def check_node(node: ExpressionBlock, context: Context) -> bool:
        valid_node = True

        for expression in node.body:
            valid_node &= TypeChecker.check_node(expression, context)

        return valid_node

    @staticmethod
    @dispatch(While, Context)
    def check_node(node: While, context: Context) -> bool:

        valid_node: bool = TypeChecker.check_node(node.condition, context)
        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        valid_node &= TypeChecker.check_node(node.body, context)

        return valid_node

    @staticmethod
    @dispatch(Elif, Context)
    def check_node(node: Elif, context: Context) -> bool:

        valid_condition: bool = TypeChecker.check_node(node.condition, context)
        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        return valid_condition and TypeChecker.check_node(node.body, context)

    @staticmethod
    @dispatch(If, Context)
    def check_node(node: If, context: Context) -> bool:

        valid_node: bool = TypeChecker.check_node(node.condition, context)

        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        for elif_c in node.elif_clauses:
            valid_node &= TypeChecker.check_node(elif_c, context)

        valid_node &= TypeChecker.check_node(node.else_body, context)

        return valid_node

    @staticmethod
    @dispatch(For, Context)
    def check_node(node: For, context: Context) -> bool:

        valid_iter: bool = TypeChecker.check_node(node.iterable, context)

        if not context.iter_protocol.is_implemented_by(node.iterable.inferred_type):
            print(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to Iterable"
            )
            return False

        new_context = context.create_child_context()
        new_context.define_variable(
            IdentifierVar(node.index_identifier, node.index_identifier_type)
        )

        return valid_iter and TypeChecker.check_node(node.body, new_context)

    @staticmethod
    @dispatch(Vector, Context)
    def check_node(node: Vector, context: Context):

        valid_node = True
        vector_type = node.elements_type

        for element in node.elements:
            valid_node &= TypeChecker.check_node(element, context)
            if element.inferred_type != vector_type:
                print(
                    f"Can not implicity convert from {element.inferred_type} to {vector_type} 1"
                )
                return False

        return valid_node

    @staticmethod
    @dispatch(ComprehensionVector, Context)
    def check_node(node: ComprehensionVector, context: Context):

        iterator_expression_valid: bool = TypeChecker.check_node(node.iterator, context)

        if not context.iter_protocol.is_implemented_by(node.iterator.inferred_type):
            print(
                f"Can't implicity convert from {node.iterator.inferred_type} to Iterable"
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
            node.generator, child_context
        )

        return generator_expresion_valid and iterator_expression_valid

    @staticmethod
    @dispatch(IndexNode, Context)
    def check_node(node: IndexNode, context: Context):

        valid_node = True

        valid_node &= TypeChecker.check_node(node.obj, context)
        valid_node &= TypeChecker.check_node(node.index, context)

        if not isinstance(node.obj.inferred_type, VectorType):
            print(f"object of type {node.obj.inferred_type.name} is not suscriptable")
            return False

        if node.index.inferred_type is not NumberType():
            print(
                f"Can't implicity convert from {node.index.inferred_type.name} to Number"
            )
            return False

        return valid_node

    @staticmethod
    @dispatch(FunctionCall, Context)
    def check_node(node: FunctionCall, context: Context) -> bool:

        valid_node: bool = TypeChecker.check_node(node.obj, context)

        object_type = node.obj.inferred_type

        method: Method | None = object_type.get_method(node.invocation.identifier)

        if not method:
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

        return valid_node

    @staticmethod
    @dispatch(Invocation, Context)
    def check_node(node: Invocation, context: Context):

        method: Method | None = context.get_method(node.identifier, len(node.arguments))

        if not method:
            if context.check_method(node.identifier):
                print(
                    f"There is no method {node.identifier} that receives {len(node.arguments)} arguments"
                )
            else:
                print(f"Method {node.identifier} is not defined")
            return False

        for i, arg in enumerate(node.arguments):

            TypeChecker.check_node(arg, context)

            if not arg.inferred_type.conforms_to(method.params[i].type):
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].type}"
                )
                return False

        return True

    @staticmethod
    @dispatch(AttributeCall, Context)
    def check_node(node: AttributeCall, context: Context):

        valid_node: bool = TypeChecker.check_node(node.obj, context)

        object_type = node.obj.inferred_type

        atrribute: IdentifierVar | None = object_type.get_attribute(node.identifier)

        if not atrribute:
            print(f"Attribute {node.identifier} is not defined in {object_type.name}")
            return False

        return valid_node

    @staticmethod
    @dispatch(DestructiveAssign, Context)
    def check_node(node: DestructiveAssign, context: Context):

        valid_node = True
        valid_node &= TypeChecker.check_node(node.expression, context)

        return valid_node and node.expression.inferred_type.conforms_to(
            node.identifier.inferred_type
        )

    @staticmethod
    @dispatch(Identifier, Context)
    def check_node(_: Identifier, __: Context) -> bool:
        return True

    @staticmethod
    @dispatch(LetVar, Context)
    def check_node(node: LetVar, context: Context) -> bool:

        new_context: Context = context.create_child_context()
        valid_node = True

        for i, var_declaration in enumerate(node.declarations):

            valid_node &= TypeChecker.check_node(var_declaration, context)

            new_context.define_variable(
                IdentifierVar(
                    var_declaration.identifier, node.declarations[i].inferred_type
                )
            )

        valid_node &= TypeChecker.check_node(node.body, new_context)

        return valid_node

    @staticmethod
    @dispatch(VariableDeclaration, Context)
    def check_node(node: VariableDeclaration, context: Context) -> bool:

        valid_node: bool = TypeChecker.check_node(node.expression, context)

        if node.static_type:
            static_type: Type | None = context.get_type_or_protocol(node.static_type)

            if not static_type:
                print(f"Type {node.static_type} is not defined")
                return False

            if not node.expression.inferred_type.conforms_to(static_type):
                print(
                    f"Can't impicity convert from  {node.expression.inferred_type.name} to {static_type.name}"
                )
                return False

        return valid_node

    @staticmethod
    @dispatch(Instanciate, Context)
    def check_node(node: Instanciate, context: Context) -> bool:

        type_t: Type | None = context.get_type(node.identifier)

        if not type_t:
            print(f"{node.identifier} is not defined")
            return False

        if len(type_t.params) != len(node.params):
            print(
                f"Invalid constructor call {len(node.params)} arguments expected {len(type_t.params)} were given"
            )
            return False

        for i, param in enumerate(node.params):
            if not param.inferred_type.conforms_to(type_t.params[i].type):
                print(
                    f"Can't implicity convert from {param.inferred_type.name} to {type_t.params[i].name} 2"
                )
                return False

        return True

    @staticmethod
    @dispatch(BinaryExpression, Context)
    def check_node(node: BinaryExpression, context: Context) -> bool:

        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            return TypeChecker._visit_binary_aritmethic(node, context)

        if node.operator in [Operator.AND, Operator.OR]:
            return TypeChecker._visit_binary_logic(node, context)

        if node.operator in [
            Operator.EQ,
            Operator.NEQ,
            Operator.GT,
            Operator.LT,
            Operator.GE,
            Operator.LE,
        ]:
            return TypeChecker._visit_binary_comparison(node, context)

        if node.operator is Operator.IS:
            return TypeChecker._visit_binary_type_checker(node, context)

        if node.operator is Operator.AS:
            return TypeChecker._visit_binary_downcast(node, context)

        if node.operator in [Operator.CONCAT, Operator.DCONCAT]:
            return TypeChecker._visit_binary_concat(node, context)

        return False

    @staticmethod
    def _visit_binary_aritmethic(node: BinaryExpression, context: Context) -> bool:

        TypeChecker.check_node(node.left, context)
        TypeChecker.check_node(node.right, context)

        if node.left.inferred_type is not NumberType():
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to Number"
            )
            return False

        if node.right.inferred_type is not NumberType():
            print(
                f"Can not implicitly convert from {node.right.inferred_type.name} to Number"
            )
            return False

        return True

    @staticmethod
    def _visit_binary_logic(node: BinaryExpression, context: Context) -> bool:

        valid_node = TypeChecker.check_node(node.left, context)
        valid_node &= TypeChecker.check_node(node.right, context)

        if node.left.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to boolean"
            )
            return False

        if node.right.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.right.inferred_type.name} to boolean"
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_comparison(node: BinaryExpression, context: Context) -> bool:

        valid_node = TypeChecker.check_node(node.left, context)
        valid_node &= TypeChecker.check_node(node.right, context)

        if node.left.inferred_type != node.right.inferred_type:
            print(
                f"Can not compare {node.left.inferred_type.name} with {node.right.inferred_type.name}"
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_downcast(node: BinaryExpression, context: Context) -> bool:

        valid_node: bool = TypeChecker.check_node(node.left, context)

        if not context.get_type(node.right.identifier):
            print(f"Type {node.right.identifier} is not defined")
            return False

        if not node.right.inferred_type.conforms_to(node.left.inferred_type):
            print(
                f"Can't cast from {node.right.inferred_type} to {node.left.inferred_type}"
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_type_checker(node: BinaryExpression, context: Context) -> bool:

        valid_node = TypeChecker.check_node(node.left, context)
        valid_node &= TypeChecker.check_node(node.right, context)

        if not context.get_type(node.right.identifier):
            print(f"Type {node.right.identifier} is not defined")
            return False

        if not node.right.inferred_type.conforms_to(node.left.inferred_type):
            print(
                f"Can't implicity convert from {node.right.inferred_type} to {node.left.inferred_type}"
            )
            return False

        return valid_node

    @staticmethod
    def _visit_binary_concat(node: BinaryExpression, context: Context):
        valid_node = TypeChecker.check_node(node.left, context)
        valid_node &= TypeChecker.check_node(node.right, context)

        if (
            node.left.inferred_type is not NumberType()
            and node.left.inferred_type is not StringType()
        ) or (
            node.right.inferred_type is not NumberType()
            and node.right.inferred_type is not StringType()
        ):
            print(
                f"Can not implicitly convert from {node.left.inferred_type.name} to String"
            )
            return False

        return valid_node

    @staticmethod
    @dispatch(TypeDeclaration, Context)
    def check_node(node: TypeDeclaration, context: Context):

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
            )

        for attr in node.attributes:
            valid_node &= TypeChecker.check_node(attr, context)
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
            valid_node &= TypeChecker.check_node(method, type_context)

        return valid_node

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def check_node(node: ProtocolDeclaration, context: Context):
        protocol: Protocol | None = context.get_protocol(node.identifier)

        for method in protocol.methods.values():
            for param in method.params:
                if param.type is UnknownType():
                    print(
                        f"Missing type declaration of param: {param.name} in method: {method.name} in protocol: {protocol.name}"
                    )
                    return False

            if method.return_type is UnknownType():
                print(
                    f"Missing return type declaration of method: {method.name} in protocol: {protocol.name}"
                )
                return False

        return True

    @staticmethod
    @dispatch(FunctionDeclaration, Context)
    def check_node(node: FunctionDeclaration, context: Context):

        function_t: Method = context.get_method(node.identifier, len(node.params))
        function_context: Context = context.create_child_context()

        for param in function_t.params:
            if param.type is UnknownType():
                print(
                    f"Can't infer type of param {param.name} in method {node.identifier}"
                )
                return False

            function_context.define_variable(param)

        valid_node = TypeChecker.check_node(node.body, function_context)

        if function_t.return_type is UnknownType():
            print(f"Can't infer return type of method {node.identifier}")

        if not function_t.return_type.conforms_to(
            context.get_type_or_protocol(node.static_return_type)
            if node.static_return_type
            else UnknownType()
        ):
            print(
                f"Can't implicty convert from {function_t.return_type} to {node.static_return_type}"
            )
            return False
        return valid_node

    @staticmethod
    @dispatch(AttributeDeclaration, Context)
    def check_node(node: AttributeDeclaration, context: Context):
        if node.expression.inferred_type is UnknownType():
            print("Can't infer type of expression")
            return False

        if not node.expression.inferred_type.conforms_to(
            context.get_type_or_protocol(node.static_type)
            if node.static_type
            else UnknownType()
        ):
            print(
                f"Can't implicity convert from {node.expression.inferred_type} to {node.static_type} 3"
            )
            return False

        return True
