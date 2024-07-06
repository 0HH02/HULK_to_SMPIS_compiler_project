"""

"""

from multipledispatch import dispatch

from hulk_compiler.semantic_analizer.types import Type

from .error_stack import StackError
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
    Inherits,
    ASTNode,
)

# pylint: disable=too-many-function-args
# pylint: disable=function-redefined
# pylint: disable=line-too-long
# pylint: disable=arguments-differ


class TypeInferer(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @staticmethod
    @dispatch(Program, Context, StackError)
    def infer_node(node: Program, context: Context, stack: StackError):
        for _ in range(2):
            for definition in node.defines:
                TypeInferer.infer_node(definition, context, stack)

        TypeInferer.infer_node(node.statement, context, stack)

    @staticmethod
    @dispatch(LiteralNode, Context, StackError)
    def infer_node(_: LiteralNode, __: Context, ___: StackError):
        """
        The Type of a LiteralNode is assigned in the grammar
        """

    @staticmethod
    @dispatch(NegativeNode, Context, StackError)
    def infer_node(node: NegativeNode, context: Context, _: StackError):
        node.inferred_type = NumberType()

        infer_top_bottom(node.expression, NumberType(), context)

    @staticmethod
    @dispatch(PositiveNode, Context, StackError)
    def infer_node(node: PositiveNode, context: Context, _: StackError):
        node.inferred_type = NumberType()

        infer_top_bottom(node.expression, NumberType(), context)

    @staticmethod
    @dispatch(NotNode, Context, StackError)
    def infer_node(node: NotNode, context: Context, _: StackError) -> bool:
        node.inferred_type = BooleanType()

        infer_top_bottom(node.expression, BooleanType(), context)

    @staticmethod
    @dispatch(ExpressionBlock, Context, StackError)
    def infer_node(node: ExpressionBlock, context: Context, stack: StackError):

        for expression in node.body:
            TypeInferer.infer_node(expression, context, stack)

        node.inferred_type = node.body[-1].inferred_type

    @staticmethod
    @dispatch(While, Context, StackError)
    def infer_node(node: While, context: Context, stack: StackError):

        TypeInferer.infer_node(node.condition, context, stack)
        infer_top_bottom(node.condition, BooleanType(), context)

        TypeInferer.infer_node(node.body, context, stack)
        node.inferred_type = node.body.inferred_type

    @staticmethod
    @dispatch(Elif, Context, StackError)
    def infer_node(node: Elif, context: Context, stack: StackError):

        TypeInferer.infer_node(node.condition, context, stack)
        infer_top_bottom(node.condition, BooleanType(), context)

        TypeInferer.infer_node(node.body, context, stack)
        node.inferred_type = node.body.inferred_type

    @staticmethod
    @dispatch(If, Context, StackError)
    def infer_node(node: If, context: Context, stack: StackError):

        TypeInferer.infer_node(node.condition, context, stack)
        infer_top_bottom(node.condition, BooleanType(), context)

        for elif_c in node.elif_clauses:
            TypeInferer.infer_node(elif_c, context, stack)

        TypeInferer.infer_node(node.else_body, context, stack)
        TypeInferer.infer_node(node.body, context, stack)

        node.inferred_type = Type.get_lower_ancestor(
            [
                node.body.inferred_type,
                node.else_body.inferred_type,
                *[elif_c.inferred_type for elif_c in node.elif_clauses],
            ]
        )

    @staticmethod
    @dispatch(For, Context, StackError)
    def infer_node(node: For, context: Context, stack: StackError):

        TypeInferer.infer_node(node.iterable, context, stack)

        if context.iter_protocol.is_implemented_by(node.iterable.inferred_type):
            node.index_identifier_type = node.iterable.inferred_type.get_method(
                "current"
            ).return_type

        new_context = context.create_child_context()
        new_context.define_variable(
            IdentifierVar(node.index_identifier, node.index_identifier_type)
        )

        TypeInferer.infer_node(node.body, new_context, stack)

        node.inferred_type = node.body.inferred_type

    @staticmethod
    @dispatch(Vector, Context, StackError)
    def infer_node(node: Vector, context: Context, stack: StackError):

        for element in node.elements:
            TypeInferer.infer_node(element, context, stack)

        node.inferred_type = VectorType(node.elements[0].inferred_type)
        node.elements_type = node.elements[0].inferred_type

    @staticmethod
    @dispatch(ComprehensionVector, Context, StackError)
    def infer_node(node: ComprehensionVector, context: Context, stack: StackError):

        TypeInferer.infer_node(node.iterator, context, stack)

        if context.iter_protocol.is_implemented_by(node.iterator.inferred_type):

            child_context: Context = context.create_child_context()

            current_method = node.iterator.inferred_type.get_method("current")

            child_context.define_variable(
                IdentifierVar(
                    node.identifier,
                    current_method.return_type if current_method else UnknownType(),
                )
            )

            TypeInferer.infer_node(node.generator, child_context, stack)

            node.inferred_type = VectorType(node.generator.inferred_type)

    @staticmethod
    @dispatch(IndexNode, Context, StackError)
    def infer_node(node: IndexNode, context: Context, stack: StackError):

        TypeInferer.infer_node(node.obj, context, stack)
        TypeInferer.infer_node(node.index, context, stack)

        if isinstance(node.obj.inferred_type, VectorType):
            node.inferred_type = node.obj.inferred_type.get_method(
                "current"
            ).return_type

    @staticmethod
    @dispatch(FunctionCall, Context, StackError)
    def infer_node(node: FunctionCall, context: Context, stack: StackError):

        TypeInferer.infer_node(node.obj, context, stack)

        method: Method | None = node.obj.inferred_type.get_method(
            node.invocation.identifier
        )

        for i, arg in enumerate(node.invocation.arguments):
            TypeInferer.infer_node(arg, context, stack)
            infer_top_bottom(arg, method.params[i].type, context)

        if method:
            node.inferred_type = method.return_type

    @staticmethod
    @dispatch(Invocation, Context, StackError)
    def infer_node(node: Invocation, context: Context, stack: StackError):
        method: Method | None = context.get_method(node.identifier, len(node.arguments))

        for i, arg in enumerate(node.arguments):
            TypeInferer.infer_node(arg, context, stack)
            infer_top_bottom(arg, method.params[i].type, context)

        if method:
            node.inferred_type = method.return_type

    @staticmethod
    @dispatch(AttributeCall, Context, StackError)
    def infer_node(node: AttributeCall, context: Context, stack: StackError):

        TypeInferer.infer_node(node.obj, context, stack)

        atrribute: IdentifierVar | None = node.obj.inferred_type.get_attribute(
            node.identifier
        )

        if atrribute:
            node.inferred_type = atrribute.type

    @staticmethod
    @dispatch(DestructiveAssign, Context, StackError)
    def infer_node(node: DestructiveAssign, context: Context, stack: StackError):

        TypeInferer.infer_node(node.identifier, context, stack)
        TypeInferer.infer_node(node.expression, context, stack)

        infer_top_bottom(node.identifier, node.expression.inferred_type, context)

        node.inferred_type = node.expression.inferred_type

    @staticmethod
    @dispatch(Identifier, Context, StackError)
    def infer_node(node: Identifier, context: Context, stack: StackError):

        var_type: Type | None = context.get_var_type(node.identifier)

        if not var_type:
            stack.add_error(
                f"Variable {node.identifier} is not defined", (node.line, node.column)
            )
            return False

        node.inferred_type = var_type

    @staticmethod
    @dispatch(LetVar, Context, StackError)
    def infer_node(node: LetVar, context: Context, stack: StackError) -> bool:

        HulkTranspiler.transpile_node(node)
        new_context: Context = context.create_child_context()

        for var_declaration in node.declarations:

            TypeInferer.infer_node(var_declaration, context, stack)
            new_context.define_variable(
                IdentifierVar(var_declaration.identifier, var_declaration.inferred_type)
            )

        TypeInferer.infer_node(node.body, new_context, stack)
        node.inferred_type = node.body.inferred_type

    @staticmethod
    @dispatch(VariableDeclaration, Context, StackError)
    def infer_node(node: VariableDeclaration, context: Context, stack: StackError):

        TypeInferer.infer_node(node.expression, context, stack)
        node.inferred_type = node.expression.inferred_type

    @staticmethod
    @dispatch(Instanciate, Context, StackError)
    def infer_node(node: Instanciate, context: Context, stack: StackError) -> bool:

        type_t: Type | None = context.get_type(node.identifier)

        if type_t:
            node.inferred_type = type_t
        else:
            stack.add_error(
                f"type {node.identifier} is not defined", (node.line, node.column)
            )

        for i, param in enumerate(node.params):
            TypeInferer.infer_node(param, context, stack)
            infer_top_bottom(param, type_t.params[i].type, context)

    @staticmethod
    @dispatch(BinaryExpression, Context, StackError)
    def infer_node(node: BinaryExpression, context: Context, stack: StackError):

        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            TypeInferer._visit_binary_aritmethic(node, context, stack)

        if node.operator in [Operator.AND, Operator.OR]:
            TypeInferer._visit_binary_logic(node, context, stack)

        if node.operator in [
            Operator.EQ,
            Operator.NEQ,
            Operator.GT,
            Operator.LT,
            Operator.GE,
            Operator.LE,
        ]:
            TypeInferer._visit_binary_comparison(node, context, stack)

        if node.operator is Operator.IS:
            TypeInferer._visit_binary_type_checker(node, context, stack)

        if node.operator is Operator.AS:
            TypeInferer._visit_binary_downcast(node, context, stack)

        if node.operator in [Operator.CONCAT, Operator.DCONCAT]:
            TypeInferer._visit_binary_concat(node, context, stack)

    @staticmethod
    def _visit_binary_aritmethic(
        node: BinaryExpression, context: Context, stack: StackError
    ):

        TypeInferer.infer_node(node.left, context, stack)
        TypeInferer.infer_node(node.right, context, stack)

        infer_top_bottom(node.left, NumberType(), context)
        infer_top_bottom(node.right, NumberType(), context)

        node.inferred_type = NumberType()

    @staticmethod
    def _visit_binary_logic(
        node: BinaryExpression, context: Context, stack: StackError
    ):

        TypeInferer.infer_node(node.left, context, stack)
        TypeInferer.infer_node(node.right, context, stack)

        infer_top_bottom(node.left, BooleanType(), context)
        infer_top_bottom(node.right, BooleanType(), context)

        node.inferred_type = BooleanType()

    @staticmethod
    def _visit_binary_comparison(
        node: BinaryExpression, context: Context, stack: StackError
    ):

        TypeInferer.infer_node(node.left, context, stack)
        TypeInferer.infer_node(node.right, context, stack)

        node.inferred_type = BooleanType()

    @staticmethod
    def _visit_binary_downcast(
        node: BinaryExpression, context: Context, stack: StackError
    ):

        TypeInferer.infer_node(node.left, context, stack)

        type_t = context.get_type(node.right.identifier)
        if not type_t:
            stack.add_error(
                f"Type {node.right.identifier} is not defined",
                (node.right.line, node.right.column),
            )
        else:
            node.right.inferred_type = type_t

        node.inferred_type = type_t

    @staticmethod
    def _visit_binary_type_checker(
        node: BinaryExpression, context: Context, stack: StackError
    ):

        TypeInferer.infer_node(node.left, context, stack)

        type_t = context.get_type(node.right.identifier)
        if not type_t:
            stack.add_error(
                f"Type {node.right.identifier} is not defined",
                (node.right.line, node.right.column),
            )
        else:
            node.right.inferred_type = type_t

        node.inferred_type = BooleanType()

    @staticmethod
    def _visit_binary_concat(
        node: BinaryExpression, context: Context, stack: StackError
    ):
        TypeInferer.infer_node(node.left, context, stack)
        TypeInferer.infer_node(node.right, context, stack)

        infer_top_bottom(node.left, StringType(), context)
        infer_top_bottom(node.right, StringType(), context)

        node.inferred_type = StringType()

    @staticmethod
    @dispatch(ProtocolDeclaration, Context, StackError)
    def infer_node(_: ProtocolDeclaration, __: Context, ___: StackError):
        """
        The Protocol node is statically tiped and his types can't be inferred
        """

    @staticmethod
    @dispatch(FunctionDeclaration, Context, StackError)
    def infer_node(node: FunctionDeclaration, context: Context, stack: StackError):

        fun_context = context.create_child_context()

        method: Method = context.get_method(node.identifier, len(node.params))

        for param in method.params:
            fun_context.define_variable(param)

        TypeInferer.infer_node(node.body, fun_context, stack)

        if node.body.inferred_type.conforms_to(method.return_type):
            method.return_type = node.body.inferred_type
            node.inferred_return_type = node.body.inferred_type
        # Update the AST node inferred type
        for param in node.params:
            param.inferred_type = fun_context.get_var(param.identifier).type

    @staticmethod
    @dispatch(TypeDeclaration, Context, StackError)
    def infer_node(node: TypeDeclaration, context: Context, stack: StackError):

        type_t: Type | None = context.get_type(node.identifier)
        constructor_context = context.create_child_context()
        type_context = context.create_child_context()

        for param in type_t.params:
            constructor_context.define_variable(param)

        if node.inherits:
            TypeInferer.infer_node(node.inherits, constructor_context, stack)

        for function in node.functions:
            type_context.define_method(type_t.get_method(function.identifier))

        for attr in node.attributes:
            TypeInferer.infer_node(attr, constructor_context, stack)
            update_type_attr(type_t, attr.identifier, attr.expression.inferred_type)
            infer_top_bottom(
                attr.expression,
                type_t.get_attribute(attr.identifier).type,
                constructor_context,
            )

        type_context.define_variable(IdentifierVar("self", type_t))

        for function in node.functions:
            funtion_context = type_context.create_child_context()
            if node.inherits:
                parent_function = type_t.parent.get_method(function.identifier)
                if parent_function:
                    funtion_context.define_method(
                        Method(
                            "base",
                            parent_function.params,
                            parent_function.return_type,
                        )
                    )
            TypeInferer.infer_node(function, funtion_context, stack)

        for attr in node.attributes:
            infer_top_bottom(
                attr.expression,
                type_t.get_attribute(attr.identifier).type,
                constructor_context,
            )
            attr.expression.inferred_type = type_t.get_attribute(attr.identifier).type

        for param in node.params:
            param.inferred_type = type_t.get_param(param.identifier)

    @staticmethod
    @dispatch(AttributeDeclaration, Context, StackError)
    def infer_node(node: AttributeDeclaration, context: Context, stack: StackError):
        TypeInferer.infer_node(node.expression, context, stack)

    @staticmethod
    @dispatch(Inherits, Context, StackError)
    def infer_node(node: Inherits, context: Context, stack: StackError):
        for arg in node.arguments:
            TypeInferer.infer_node(arg, context, stack)


def infer_top_bottom(node: ASTNode, inferred_type: Type, context: Context):
    if isinstance(node, Identifier):
        update_variable_type(node.identifier, inferred_type, context)
    if isinstance(node, AttributeCall):
        update_type_attr(node.obj.inferred_type, node.identifier, inferred_type)
    if isinstance(node, Invocation):
        update_fun_return_type(
            node.identifier, len(node.arguments), inferred_type, context
        )


def update_variable_type(var_name: str, var_infered_type: Type, context: Context):
    var = context.get_var(var_name)
    if var and var_infered_type.conforms_to(var.type):
        var.type = var_infered_type


def update_type_attr(type_t: Type, attr_name: str, attr_infered_type: Type):
    attr = type_t.get_attribute(attr_name)
    if attr and attr_infered_type.conforms_to(attr.type):
        attr.type = attr_infered_type


def update_fun_return_type(
    fun_name: str, fun_params: int, inferred_type: Type, context: Context
):
    method: Method = context.get_method(fun_name, fun_params)
    if method and inferred_type.conforms_to(method.return_type):
        method.return_type = inferred_type


def update_type_method_return_type(type_t: Type, method_name: str, inferred_type: Type):
    method = type_t.get_method(method_name)
    if method and inferred_type.conforms_to(method.return_type):
        method.return_type = inferred_type
