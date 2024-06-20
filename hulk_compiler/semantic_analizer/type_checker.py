"""

"""

from multipledispatch import dispatch

from hulk_compiler.semantic_analizer.types import Protocol, Type

from .hulk_transpiler import HulkTranspiler

from .context import Context
from .types import (
    StringType,
    NumberType,
    BooleanType,
    IdentifierVar,
    UnknownType,
    Method,
    VectorType,
    ObjectType,
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
        valid_expression: bool = TypeCheckVisitor.visit_node(node.expression, context)
        return node.expression.inferred_type is NumberType() and valid_expression

    @staticmethod
    @dispatch(PositiveNode, Context)
    def visit_node(node: PositiveNode, context: Context) -> bool:
        valid_expression: bool = TypeCheckVisitor.visit_node(node.expression, context)
        return node.expression.inferred_type is NumberType() and valid_expression

    @staticmethod
    @dispatch(NotNode, Context)
    def visit_node(node: NotNode, context: Context) -> bool:
        valid_expression: bool = TypeCheckVisitor.visit_node(node.expression, context)
        return node.expression.inferred_type is NumberType() and valid_expression

    @staticmethod
    @dispatch(ExpressionBlock, Context)
    def visit_node(node: ExpressionBlock, context: Context) -> bool:
        valid_node = True

        for expression in node.body:
            valid_node &= TypeCheckVisitor.visit_node(expression, context)
            if not valid_node:
                return False

        node.inferred_type = node.body[-1].inferred_type

        return True

    @staticmethod
    @dispatch(While, Context)
    def visit_node(node: While, context: Context) -> bool:

        valid_node: bool = TypeCheckVisitor.visit_node(node.condition, context)
        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        valid_node &= TypeCheckVisitor.visit_node(node.body, context)
        node.inferred_type = node.body.inferred_type

        return valid_node

    @staticmethod
    @dispatch(Elif, Context)
    def visit_node(node: Elif, context: Context) -> bool:

        valid_condition: bool = TypeCheckVisitor.visit_node(node.condition, context)
        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        return valid_condition and TypeCheckVisitor.visit_node(node.body, context)

    @staticmethod
    @dispatch(If, Context)
    def visit_node(node: If, context: Context) -> bool:

        valid_node: bool = TypeCheckVisitor.visit_node(node.condition, context)

        if node.condition.inferred_type is not BooleanType():
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to Boolean"
            )
            return False

        valid_node &= TypeCheckVisitor.visit_node(node.body, context)

        expr_type: Type = node.body.inferred_type

        for elif_clause in node.elif_clauses:
            elif_valid = TypeCheckVisitor.visit_node(elif_clause, context)
            if expr_type != elif_clause.body.inferred_type:
                print(
                    f"All conditional expression block must return the same type. Can not implicitly convert from {elif_clause.body.inferred_type.name} to {expr_type.name}"
                )
                return False
            if not elif_valid:
                return False

        valid_node &= TypeCheckVisitor.visit_node(node.else_body, context)

        if expr_type != node.else_body.inferred_type:
            print(
                f"All conditional expression block must return the same type. Can not implicitly convert from {node.else_body.inferred_type.name} to {expr_type.name}"
            )
            return False

        node.inferred_type = expr_type
        return valid_node

    @staticmethod
    @dispatch(For, Context)
    def visit_node(node: For, context: Context) -> bool:

        valid_iter: bool = TypeCheckVisitor.visit_node(node.iterable, context)

        if not context.iter_protocol.is_implemented_by(node.iterable.inferred_type):
            print(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to Iterable"
            )
            return False

        node.index_identifier_type = node.iterable.inferred_type.get_method(
            "current"
        ).return_type

        new_context = context.create_child_context()
        new_context.define_variable(
            IdentifierVar(node.index_identifier, node.index_identifier_type)
        )

        return valid_iter and TypeCheckVisitor.visit_node(node.body, new_context)

    @staticmethod
    @dispatch(Vector, Context)
    def visit_node(node: Vector, context: Context):

        vector_type = None

        for i, element in enumerate(node.elements):
            TypeCheckVisitor.visit_node(element, context)
            if vector_type is None:
                vector_type = node.elements[i].inferred_type
            else:
                if vector_type != node.elements[i].inferred_type:
                    print(
                        f"Can not implicitly convert from {node.elements[i].inferred_type.name} to {vector_type.name}"
                    )
                    return False

        node.inferred_type = VectorType(vector_type)

        return True

    @staticmethod
    @dispatch(ComprehensionVector, Context)
    def visit_node(node: ComprehensionVector, context: Context):

        iterator_expression_valid: bool = TypeCheckVisitor.visit_node(
            node.iterator, context
        )

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

        generator_expresion_valid: bool = TypeCheckVisitor.visit_node(
            node.generator, child_context
        )

        node.inferred_type = VectorType(node.generator.inferred_type)

        return generator_expresion_valid and iterator_expression_valid

    @staticmethod
    @dispatch(IndexNode, Context)
    def visit_node(node: IndexNode, context: Context):

        valid_node = True

        valid_node &= TypeCheckVisitor.visit_node(node.obj, context)
        valid_node &= TypeCheckVisitor.visit_node(node.index, context)

        if not isinstance(node.obj.inferred_type, VectorType):
            print(f"object of type {node.obj.inferred_type.name} is not suscriptable")
            return False

        if node.index.inferred_type is not NumberType():
            print(
                f"Can't implicity convert from {node.index.inferred_type.name} to Number"
            )
            return False

        node.inferred_type = node.obj.inferred_type.get_method("current").return_type

        return valid_node

    @staticmethod
    @dispatch(FunctionCall, Context)
    def visit_node(node: FunctionCall, context: Context) -> bool:

        valid_node: bool = TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type

        if object_type is UnknownType():
            print("Can not infer type of expression")
            return False

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
    def visit_node(node: Invocation, context: Context):

        method: Method | None = context.get_method(node.identifier, len(node.arguments))

        if not method:
            print(f"Method {node.identifier} is not defined")
            return False

        for i, arg in enumerate(node.arguments):

            TypeCheckVisitor.visit_node(arg, context)

            if not arg.inferred_type.conforms_to(method.params[i].type):
                print(
                    f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].type}"
                )
                return False

        node.inferred_type = method.return_type

        return True

    @staticmethod
    @dispatch(AttributeCall, Context)
    def visit_node(node: AttributeCall, context: Context):

        valid_node: bool = TypeCheckVisitor.visit_node(node.obj, context)

        object_type = node.obj.inferred_type

        if object_type is UnknownType():
            print("Can not infer type of expression")
            return False

        atrribute: IdentifierVar | None = object_type.get_attribute(node.identifier)

        if not atrribute:
            print(f"Attribute {node.identifier} is not defined in {object_type.name}")
            return False

        node.inferred_type = atrribute.type

        return valid_node

    @staticmethod
    @dispatch(DestructiveAssign, Context)
    def visit_node(node: DestructiveAssign, context: Context):

        if not isinstance(node.identifier, (AttributeCall, Identifier)):
            print(
                "Invalid Assignment , The left part of the assignment must be a variable or attribute"
            )
            return False

        valid_node: bool = TypeCheckVisitor.visit_node(node.identifier, context)
        valid_node &= TypeCheckVisitor.visit_node(node.expression, context)

        node.inferred_type = node.expression.inferred_type

        return valid_node and node.expression.inferred_type.conforms_to(
            node.identifier.inferred_type
        )

    @staticmethod
    @dispatch(Identifier, Context)
    def visit_node(node: Identifier, context: Context) -> bool:

        var_type: Type | None = context.get_var_type(node.identifier)

        if not var_type:
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

        for i, var_declaration in enumerate(node.declarations):

            valid_declaration: bool = TypeCheckVisitor.visit_node(
                var_declaration, context
            )
            valid_node &= valid_declaration
            new_context.define_variable(
                IdentifierVar(
                    var_declaration.identifier, node.declarations[i].inferred_type
                )
            )

        valid_node &= TypeCheckVisitor.visit_node(node.body, new_context)
        node.inferred_type = node.body.inferred_type

        return valid_node

    @staticmethod
    @dispatch(VariableDeclaration, Context)
    def visit_node(node: VariableDeclaration, context: Context) -> bool:

        valid_node: bool = TypeCheckVisitor.visit_node(node.expression, context)

        static_type: Type | None = context.get_type(node.static_type)

        if not static_type:
            print(f"Type {node.static_type} is not defined")
            return False

        if static_type is not UnknownType():
            if not static_type.conforms_to(node.expression.inferred_type):
                print(
                    f"Can't impicity convert from  {node.expression.inferred_type.name} to {static_type.name}"
                )
                return False
        else:
            if node.expression.inferred_type is UnknownType():
                print("Can't infer type of expression")

        node.inferred_type = node.expression.inferred_type

        return valid_node

    @staticmethod
    @dispatch(Instanciate, Context)
    def visit_node(node: Instanciate, context: Context) -> bool:

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
                    f"Can't implicity convert from {param.inferred_type.name} to {type_t.params[i].name}"
                )
                return False

        node.inferred_type = type_t

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

        node.inferred_type = NumberType()
        return True

    @staticmethod
    def _visit_binary_logic(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

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
            if not context.get_type(node.right.identifier):
                print(f"Type {node.right.identifier} is not defined")
                return False

            return node.right.inferred_type.conforms_to(node.left.inferred_type)

        print("Invalid Expression, Right part of the expression must be a type")
        return False

    @staticmethod
    def _visit_binary_type_checker(node: BinaryExpression, context: Context) -> bool:

        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

        if isinstance(node.right, Identifier):
            if not context.get_type(node.right.identifier):
                print(f"Type {node.right.identifier} is not defined")
                return False

            return node.left.inferred_type is node.right.inferred_type

        print("Invalid Expression, Right part of the expression must be a type")
        return False

    @staticmethod
    def _visit_binary_concat(node: BinaryExpression, context: Context):
        TypeCheckVisitor.visit_node(node.left, context)
        TypeCheckVisitor.visit_node(node.right, context)

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

        node.inferred_type = StringType()
        return True

    @staticmethod
    @dispatch(TypeDeclaration)
    def visit_node(node: TypeDeclaration, context: Context):
        type_context = context.create_child_context()

        type_t: Type | None = context.get_type(node.identifier)

        valid_node: bool = True

        if not type_t:
            print(f"Type {node.identifier} is somehow not defined")
            return False

        type_context.define_variable(IdentifierVar("self", type_t))

        for method in type_t.methods.values():
            type_context.define_method(method)

        for param in type_t.params:
            if param.type is UnknownType():
                print(f"Can not infer param {param.name} in Type {type_t.name}")
                return False

        for attr in type_t.attributes.values():
            if attr.type is UnknownType():
                attr.type = ObjectType()
                type_t.get_attribute(attr.name).type = ObjectType()

            type_context.define_variable(IdentifierVar(attr.name, attr.type))

        for method in node.functions:
            valid_node &= TypeCheckVisitor(method)

        return valid_node

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def visit_node(node: ProtocolDeclaration, context: Context):
        protocol: Protocol | None = context.get_protocol(node.identifier)

        for method in protocol.methods:
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
    @dispatch(FunctionDeclaration, Context, bool)
    def visit_node(node: FunctionDeclaration, context: Context):
        function_context: Context = context.create_child_context()

        function_t: Method | None = context.get_method(
            node.identifier, len(node.params)
        )

        for param in function_t.params:
            if param.type is UnknownType():
                param.type = ObjectType()
                function_t.get_param(param.name).type = ObjectType()

        valid_node = TypeCheckVisitor.visit_node(node.body, function_context)

        fun_return_type: Type = node.body.inferred_type

        if fun_return_type is UnknownType():
            print(f"Can not infer return type of the function {function_t.name}")
            return False

        function_t.return_type = fun_return_type

        return valid_node

    @staticmethod
    @dispatch(AttributeDeclaration, Context)
    def visit_node(node: AttributeDeclaration, _: Context):
        return node.expression.inferred_type.conforms_to(node.static_type)
