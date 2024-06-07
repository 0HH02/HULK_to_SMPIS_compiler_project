"""
    This module contains the AST visitor class.
"""

from multipledispatch import dispatch
from dataclasses import dataclass
from hulk_compiler.semantic_analizer.types import (
    BooleanType,
    RangeType,
    UnkownType,
    NumberType,
    Identifier,
    Method,
)
from .context import Context
from ..parser.ast.ast import (
    Operator,
    While,
    If,
    LetVar,
    For,
    Elif,
    Call,
    Variable,
    NegativeNode,
    PositiveNode,
    NotNode,
    BinaryExpression,
    Program,
    TypeDeclaration,
    FunctionDeclaration,
    AttributeDeclaration,
)
from ..core.i_visitor import IVisitor
from .types import Type

# pylint: disable=function-redefined


@dataclass
class TypeCollector:
    context: Context

    @dispatch(Program)
    def visit(self, node: Program, current_type: Type = None):
        for class_def in node.defines:
            if isinstance(class_def, TypeDeclaration):
                self.visit(class_def)

    @dispatch(TypeDeclaration)
    def visit(self, node: TypeDeclaration, current_type: Type = None):
        current_type = self.context.define_type(node.identifier)
        for attr_def in node.attributes:
            current_type.attributes[attr_def.identifier] = Identifier(
                attr_def.identifier, None
            )
        for func_def in node.functions:
            params: list[Identifier] = []
            for param in func_def.params:
                params.append(Identifier(param.identifier, param.type))
            current_type.methods[func_def.identifier] = Method(
                func_def.identifier, params, func_def.return_type
            )


class TypeBuilder(IVisitor):
    context: Context
    current_type: Type

    @dispatch
    def visit(self, node: TypeDeclaration):
        self.currentType = self.context.get_type(node.identifier)

    @dispatch
    def visit(self, node: FunctionDeclaration):
        return_type = self.context.get_type(node.return_type)

        arg_types = [self.context.get_type(t) for t in node.arg_types]

        self.current_type.defone_method(
            node.name, return_type, node.arg_names, arg_types
        )


class TypeCheckVisitor(IVisitor):
    """
    This class represents an abstract syntax tree (AST) visitor.
    It provides methods to visit different nodes in the AST.
    """

    @dispatch(While)
    def visit_node(self, node: While, context) -> bool:

        if not node.condition.inferred_type is BooleanType:
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        return node.body.validate(self, context)

    @dispatch(If)
    def visit_node(self, node: If, context) -> bool:

        if not node.condition.inferred_type is BooleanType:
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        if not node.body.validate(self, context):
            return False

        for elif_clause in node.elif_clauses:
            elif_valid = elif_clause.condition.validate(self, context)
            if not elif_valid:
                return False

        return node.else_body.validate(self, context)

    @dispatch(Elif)
    def visit_node(self, node: Elif, context) -> bool:

        if not node.condition.inferred_type is BooleanType:
            print(
                f"Can not implicitly convert from {node.condition.inferred_type.name} to boolean"
            )
            return False

        return node.body.validate(self, context)

    @dispatch(For)
    def visit_node(self, node: For, context: Context) -> bool:

        if not node.iterable.inferred_type is RangeType:
            print(
                f"Can not implicitly convert from {node.iterable.inferred_type.name} to iterable"
            )
            return False

        return node.body.validate(self, context.create_child_context())

    @dispatch(LetVar)
    def visit_node(self, node: LetVar, context) -> bool:
        pass

    @dispatch(Call)
    def visit_node(self, node: Call, context) -> bool:
        expresion_type = node.obj.inferred_type

        if expresion_type is UnkownType:
            print("Can not infer type of expression")
            return False

        if not expresion_type.get_method(node.identifier):
            print(f"Method {node.identifier} is not defined in {expresion_type.name}")
            return False

        return True

    @dispatch(Variable)
    def visit_node(self, node: Variable, context) -> bool:

        if not context.check_var(node.identifier):
            print(f"Variable {node.identifier} is not defined")
            return False

        return True

    @dispatch(NegativeNode)
    def visit_node(self, node: NegativeNode, context) -> bool:
        return node.expression.inferred_type is NumberType()

    @dispatch(PositiveNode)
    def visit_node(self, node: NegativeNode, context) -> bool:
        return node.expression.inferred_type is NumberType()

    @dispatch(NotNode)
    def visit_node(self, node: NotNode, context) -> bool:
        return node.expression.inferred_type is BooleanType()

    @dispatch(BinaryExpression)
    def visit_node(self, node: BinaryExpression, context) -> bool:
        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            return (
                node.left.inferred_type is NumberType()
                and node.right.inferred_type is NumberType()
            )

        if node.operator in [Operator.AND, Operator.OR]:
            return (
                node.left.inferred_type is BooleanType()
                and node.right.inferred_type is BooleanType()
            )

        if node.operator in [
            Operator.EQ,
            Operator.NEQ,
            Operator.GT,
            Operator.LT,
            Operator.GE,
            Operator.LE,
        ]:
            return node.left.inferred_type == node.right.inferred_type
