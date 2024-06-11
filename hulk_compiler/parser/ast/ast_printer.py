from multipledispatch import dispatch
from .ast import (
    Program,
    While,
    If,
    Elif,
    For,
    LetVar,
    ExpressionBlock,
    AttributeCall,
    FunctionCall,
    Invocation,
    Identifier,
    NegativeNode,
    PositiveNode,
    NotNode,
    BinaryExpression,
    AttributeDeclaration,
    FunctionDeclaration,
    Inherits,
    LiteralNode,
    ProtocolDeclaration,
    IndexNode,
    Vector,
    VariableDeclaration,
    TypeDeclaration,
    Parameter,
    DestructiveAssign,
    Instanciate,
    ComprehensionVector,
)

# pylint: disable=function-redefined


class ASTPrinter:

    @staticmethod
    @dispatch(Program, int)
    def visit_node(node: Program, tabs: int = 0):
        print("   " * tabs, "program: {")
        for define in node.defines:
            ASTPrinter.visit_node(define, tabs + 1)
        ASTPrinter.visit_node(node.statement, tabs + 1)
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
        ASTPrinter.visit_node(node.else_body, tabs + 1)
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
    @dispatch(ExpressionBlock, int)
    def visit_node(node: ExpressionBlock, tabs: int):
        print("   " * tabs, "expression_block: {")
        for exp in node.body:
            ASTPrinter.visit_node(exp, tabs + 1)
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
        print("   " * tabs, "literal: ", node.lex.lex)

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
        ASTPrinter.visit_node(node.body, tabs + 1)
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
