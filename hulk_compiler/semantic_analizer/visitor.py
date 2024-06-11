"""
    This module contains the AST visitor class.
"""

from dataclasses import dataclass
from multipledispatch import dispatch
from .types import (
    BooleanType,
    RangeType,
    UnkownType,
    NumberType,
    StringType,
    Variable,
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
    AttributeCall,
    FunctionCall,
    Identifier,
    NegativeNode,
    PositiveNode,
    NotNode,
    BinaryExpression,
    Program,
    TypeDeclaration,
    Inherits,
    FunctionDeclaration,
    AttributeDeclaration,
    LiteralNode,
    IndexNode,
    Vector,
    ComprehensionVector,
    Instanciate,
    ExpressionBlock,
    DestructiveAssign,
    VariableDeclaration,
    ProtocolDeclaration,
    Parameter,
    Invocation,
)
from ..core.i_visitor import IVisitor
from .types import Type

# pylint: disable=function-redefined


@dataclass
class TypeCollector:
    context: Context

    @dispatch(Program)
    def visit(self, node: Program):
        for class_def in node.defines:
            if isinstance(class_def, TypeDeclaration):
                self.visit(class_def)

    @dispatch(TypeDeclaration)
    def visit(self, node: TypeDeclaration):
        current_type: Type = self.context.define_type(node.identifier)
        for attr_def in node.attributes:
            current_type.attributes[attr_def.identifier] = Variable(
                attr_def.identifier, None
            )

        for func_def in node.functions:
            params: list[Variable] = []
            for param in func_def.params:
                params.append(Variable(param.identifier, None))
            current_type.methods[func_def.identifier] = Method(
                func_def.identifier, params, func_def.return_type
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

    # @dispatch(Call)
    # def visit_node(self, node: Call, context) -> bool:
    #     expresion_type = node.obj.inferred_type

    #     if expresion_type is UnkownType:
    #         print("Can not infer type of expression")
    #         return False

    #     method = expresion_type.get_method(node.identifier)
    #     if method is None:
    #         print(f"Method {node.identifier} is not defined in {expresion_type.name}")
    #         return False

    #     if len(node.arguments) != len(method.params):
    #         print(
    #             f"Method {node.identifier} expects {len(method.params)} arguments, but {len(node.arguments)} were given"
    #         )
    #         return False

    #     for i, arg in enumerate(node.arguments):
    #         if not arg.inferred_type is method.params[i]:
    #             print(
    #                 f"Can not implicitly convert from {arg.inferred_type.name} to {method.params[i].name}"
    #             )
    #             return False

    #     return True

    @dispatch(Identifier)
    def visit_node(self, node: Identifier, context) -> bool:

        if not context.check_var(node.identifier):
            print(f"Variable {node.identifier} is not defined")
            return False

        return True

    @dispatch(NegativeNode)
    def visit_node(self, node: NegativeNode, context) -> bool:
        return node.expression.inferred_type is NumberType

    @dispatch(PositiveNode)
    def visit_node(self, node: NegativeNode, context) -> bool:
        return node.expression.inferred_type is NumberType

    @dispatch(NotNode)
    def visit_node(self, node: NotNode, context) -> bool:
        return node.expression.inferred_type is BooleanType

    @dispatch(BinaryExpression)
    def visit_node(self, node: BinaryExpression, context: Context) -> bool:
        if node.operator in [
            Operator.ADD,
            Operator.SUB,
            Operator.MUL,
            Operator.DIV,
            Operator.MOD,
            Operator.POW,
        ]:
            return (
                node.left.inferred_type is NumberType
                and node.right.inferred_type is NumberType
            )

        if node.operator in [Operator.AND, Operator.OR]:
            return (
                node.left.inferred_type is BooleanType
                and node.right.inferred_type is BooleanType
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

        if node.operator is Operator.IS:
            if node.right is Identifier:
                if not context.check_type(node.right.identifier):
                    print(f"Type {node.right.identifier} is not defined")
                    return False
                return node.left.inferred_type is node.right.inferred_type

            print("Invalid Expression")
            return False

        if node.operator is Operator.AS:
            if node.right is Identifier:
                if not context.check_type(node.right.identifier):
                    print(f"Type {node.right.identifier} is not defined")
                    return False

                return node.right.inferred_type.conforms_to(node.left.inferred_type)

            print("Invalid Expression")
            return False

        if node.operator in [Operator.CONCAT, Operator.DCONCAT]:
            return (
                node.left.inferred_type is NumberType
                or node.left.inferred_type is StringType
            ) and (
                node.right.inferred_type is NumberType
                or node.right.inferred_type is StringType
            )


class ASTPrinter:

    @staticmethod
    @dispatch(Program, int)
    def visit_node(node: Program, tabs: int = 0):
        print("   " * tabs, "program: {")
        for define in node.defines:
            ASTPrinter.visit_node(define, tabs + 1)
        for statement in node.statements:
            ASTPrinter.visit_node(statement, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(While, int)
    def visit_node(node: While, tabs: int):
        print("   " * tabs, "while:{")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(If, int)
    def visit_node(node: If, tabs: int):
        print("   " * tabs, "if: {")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        for elif_expr in node.elif_clauses:
            ASTPrinter.visit_node(elif_expr, tabs + 1)
        print("   " * (tabs + 1), "else: {")
        ASTPrinter.visit_node(node.else_body)
        print("   " * (tabs + 1), "}")
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Elif, int)
    def visit_node(node: Elif, tabs: int):
        print("   " * tabs, "elif: {")
        ASTPrinter.visit_node(node.condition, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "{")

    @staticmethod
    @dispatch(For, int)
    def visit_node(node: For, tabs: int):
        print("   " * tabs, "for {")
        print("   " * (tabs + 1), "index: ", node.index_identifier)
        ASTPrinter.visit_node(node.iterable, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LetVar, int)
    def visit_node(node: LetVar, tabs: int):
        print("   " * tabs, "let: {")
        for var in node.declarations:
            ASTPrinter.visit_node(var, tabs + 1)
        ASTPrinter.visit_node(node.body, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeCall, int)
    def visit_node(node: AttributeCall, tabs: int):
        print("   " * tabs, "attribute_call: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionCall, int)
    def visit_node(node: FunctionCall, tabs: int):
        print("   " * tabs, "function_call: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        ASTPrinter.visit_node(node.invocation, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Invocation, int)
    def visit_node(node: Invocation, tabs: int):
        print("   " * tabs, "invocation: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Identifier, int)
    def visit_node(node: Identifier, tabs: int):
        print("   " * tabs, "identifier:", node.identifier)

    @staticmethod
    @dispatch(NegativeNode, int)
    def visit_node(node: NegativeNode, tabs: int):
        print("   " * tabs, "negative_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(PositiveNode, int)
    def visit_node(node: NegativeNode, tabs: int):
        print("   " * tabs, "positive_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(NotNode, int)
    def visit_node(node: NotNode, tabs: int):
        print("   " * tabs, "not_node: {")
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(BinaryExpression, int)
    def visit_node(node: BinaryExpression, tabs: int):
        print("   " * tabs, "binary_node: {")
        print("   " * (tabs + 1), "operator: ", node.operator)
        ASTPrinter.visit_node(node.left, tabs + 1)
        ASTPrinter.visit_node(node.right, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(LiteralNode, int)
    def visit_node(node: LiteralNode, tabs: int):
        print("   " * tabs, "literal: ", node.lex)

    @staticmethod
    @dispatch(Inherits, int)
    def visit_node(node: Inherits, tabs: int):
        print("   " * tabs, "inherits: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.arguments:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(FunctionDeclaration, int)
    def visit_node(node: FunctionDeclaration, tabs: int):
        print("   " * tabs, "function_declaration: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.params:
            ASTPrinter.visit_node(arg, tabs + 1)
        if node.return_type:
            print("   " * (tabs + 1), "return_type: ", node.return_type)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(AttributeDeclaration, int)
    def visit_node(node: AttributeDeclaration, tabs: int):
        print("   " * tabs, "atribute: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(IndexNode, int)
    def visit_node(node: IndexNode, tabs: int):
        print("   " * tabs, "index: {")
        ASTPrinter.visit_node(node.obj, tabs + 1)
        ASTPrinter.visit_node(node.index, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Vector, int)
    def visit_node(node: Vector, tabs: int):
        print("   " * tabs, "vector: {")
        for literal in node.elements:
            ASTPrinter.visit_node(literal, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ComprehensionVector, int)
    def visit_node(node: ComprehensionVector, tabs: int):
        print("   " * tabs, "ComprehensionVector: {")
        ASTPrinter.visit_node(node.generator, tabs + 1)
        print("   " * (tabs + 1), "item: ", node.item.lex)
        node.iterator()
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Instanciate, int)
    def visit_node(node: Instanciate, tabs: int):
        print("   " * tabs, "instanciate: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for arg in node.params:
            ASTPrinter.visit_node(arg, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(DestructiveAssign, int)
    def visit_node(node: DestructiveAssign, tabs: int):
        print("   " * tabs, "destructive_assigment: {")
        print("   " * (tabs + 1), "identifier", node.identifier)
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(VariableDeclaration, int)
    def visit_node(node: VariableDeclaration, tabs: int):
        print("   " * tabs, "variable_declaration: {")
        print("   " * (tabs + 1), "identifier", node.identifier)
        ASTPrinter.visit_node(node.expression, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(ProtocolDeclaration, int)
    def visit_node(node: ProtocolDeclaration, tabs: int):
        print("   " * tabs, "protoco_declaration: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for ext in node.extends:
            ASTPrinter.visit_node(ext, tabs + 1)
        for func in node.functions:
            ASTPrinter.visit_node(func, tabs + 1)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(Parameter, int)
    def visit_node(node: Parameter, tabs: int):
        print("   " * tabs, "parameter: {")
        print("   " * (tabs + 1), "identifier", node.identifier)
        print("   " * tabs, "}")

    @staticmethod
    @dispatch(TypeDeclaration, int)
    def visit_node(node: TypeDeclaration, tabs: int):
        print("   " * tabs, "type: {")
        print("   " * (tabs + 1), "identifier: ", node.identifier)
        for param in node.params:
            ASTPrinter.visit_node(param, tabs + 1)
        if node.inherits:
            ASTPrinter.visit_node(node.inherits, tabs + 1)
        for attr in node.attributes:
            ASTPrinter.visit_node(attr, tabs + 1)
        for func in node.functions:
            ASTPrinter.visit_node(func, tabs + 1)
        print("   " * tabs, "}")
