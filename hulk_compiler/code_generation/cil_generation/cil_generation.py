from typing import Any
from multipledispatch import dispatch

from hulk_compiler.code_generation.cil_generation.cil_nodes import FunctionNode
from .cil_nodes import *
from .base_cil_generation import BaseHULKToCILVisitor
from .cil_context import Context
from hulk_compiler.semantic_analizer.types import IdentifierVar
from hulk_compiler.parser.ast.ast import (
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
from hulk_compiler.semantic_analizer.types import NumberType, StringType, Type


# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring


class HULKToCILVisitor(BaseHULKToCILVisitor):

    @dispatch(Program)
    def visit_node(self, node: Program, context: Context = Context()):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################

        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name("main", "Main")
        self.register_instruction(ArgNode(instance))
        self.register_instruction(AllocateNode("Main", instance))
        self.register_instruction(StaticCallNode(main_method_name, result))
        self.register_instruction(ReturnNode(0))

        self.visit_node(node.statement, context.create_child_context())
        main = Type("main")
        self.current_function = None

        self.current_type = main
        for define in node.defines:
            if isinstance(define, FunctionDeclaration):
                self.current_type = main
            self.visit_node(define, context.create_child_context())

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @dispatch(TypeDeclaration, Context)
    def visit_node(self, node: TypeDeclaration, context: Context):
        self.current_type = self.register_type(node.identifier)

        self.current_function = self.register_function(f"{node.identifier}_constructor")
        for attr in node.attributes:
            self.visit_node(attr, context.create_child_context())
        for method in node.functions:
            method_reference = self.visit_node(method, context.create_child_context())
            self.current_type.methods.append((method.identifier, method_reference))
            context.define_method(
                method.identifier, method_reference, len(method.params)
            )

    @dispatch(AttributeDeclaration, Context)
    def visit_node(self, node: AttributeDeclaration, context: Context):
        attr_name = (
            self.current_type.name
            + "_"
            + node.identifier
            + "_"
            + str(len(self.current_type.attributes))
        )
        self.current_type.attributes[node.identifier] = attr_name
        attr_value = self.visit_node(node.expression, context.create_child_context())
        self.current_function.instructions.append(
            SetAttribNode(self.current_type.name, attr_name, attr_value)
        )
        return node.identifier

    @dispatch(AttributeCall, Context)
    def visit_node(self, node: AttributeCall, context: Context):
        object = self.visit_node(node.obj, context)
        if "self" in object:
            value = self.current_type.attributes[node.identifier]
            return value

    @dispatch(FunctionDeclaration, Context)
    def visit_node(self, node: FunctionDeclaration, context: Context):
        function_name: str = self.to_function_name(
            node.identifier, self.current_type.name
        )
        self.current_function: FunctionNode = self.register_function(function_name)
        context.define_method(node.identifier, self.current_function, len(node.params))

        param_name = self.register_local(IdentifierVar("self", self.current_type.name))
        param_node = ParamNode(param_name)
        context.define_variable("self", param_name)
        self.current_function.params.append(param_node)
        for param in node.params:
            param_name = self.register_local(
                IdentifierVar(param.identifier, self.current_type.name)
            )
            param_node = ParamNode(param_name)
            context.define_variable(param.identifier, param_name)
            self.current_function.params.append(param_node)

        result = self.visit_node(node.body, context.create_child_context())
        self.register_instruction(ReturnNode(result))

        self.current_function = None
        return function_name

    @dispatch(VariableDeclaration, Context)
    def visit_node(self, node: VariableDeclaration, context: Context):

        var_info = IdentifierVar(node.identifier, node.inferred_type)

        var_name = self.register_local(var_info)

        context.define_variable(node.identifier, var_name)

        expr_value = self.visit_node(node.expression, context.create_child_context())
        self.register_instruction(AssignNode(var_name, expr_value))
        return var_name

    @dispatch(LetVar, Context)
    def visit_node(self, node: LetVar, context: Context):

        # Procesar las declaraciones de variables
        for var_decl in node.declarations:
            # Visitar la expresión de la declaración de la variable
            var_name: str = self.visit_node(var_decl, context.create_child_context())
            # Registrar la variable local
            context.define_variable(var_decl.identifier, var_name)

        # Procesar el cuerpo del letvar
        body_result: str = self.visit_node(node.body, context.create_child_context())
        return body_result

    @dispatch(FunctionCall, Context)
    def visit_node(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(LiteralNode, Context)
    def visit_node(self, node: LiteralNode, context: Context):
        if isinstance(node.inferred_type, StringType):
            return self.register_data(node.value)
        # if node.inferred_type is NumberType:
        #     return int(node.value)
        return node.value

    @dispatch(Instanciate, Context)
    def visit_node(self, node: Instanciate, context: Context):
        for param in node.params:
            param_value = self.visit_node(param, context)
            self.register_instruction(ArgNode(param_value))
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(self.current_type.name, instance))
        self.register_instruction(
            StaticCallNode(f"{self.current_type.name}_constructor", result)
        )

    @dispatch(Invocation, Context)
    def visit_node(self, node: Invocation, context: Context):

        if node.identifier == "print":
            result = self.visit_node(node.arguments[0], context.create_child_context())
            self.register_instruction(PrintNode(result))
            return result

        # Falta por implementar: Guardar en el contexto las funciones a medida que las voy declarando y aquí solamente devuelvo la referencia a la función
        args = [
            self.visit_node(arg, context.create_child_context())
            for arg in node.arguments
        ]
        for arg in args:
            self.register_instruction(ArgNode(arg))

        result = self.define_internal_local()
        self.register_instruction(StaticCallNode(node.identifier, result))
        return result

    @dispatch(PositiveNode, Context)
    def visit_node(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(NegativeNode, Context)
    def visit_node(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(NotNode, Context)
    def visit_node(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(ExpressionBlock, Context)
    def visit_node(self, node: ExpressionBlock, context: Context):
        for i, expression in enumerate(node.body):
            result = self.visit_node(expression, context.create_child_context())
            if i == len(node.body) - 1:
                return result

    @dispatch(BinaryExpression, Context)
    def visit_node(self, node: BinaryExpression, context: Context):

        left = self.visit_node(node.left, context.create_child_context())
        right = self.visit_node(node.right, context.create_child_context())
        result = self.define_internal_local()
        self.register_instruction(OPER_TO_CLASS[node.operator](result, left, right))
        return result

    @dispatch(Identifier, Context)
    def visit_node(self, node: Identifier, context: Context):

        return context.get_var(node.identifier)
        # return self.register_instruction(LoadNode(node.name))

    @dispatch(PlusNode, Context)
    def visit_node(self, node: PlusNode, context: Context):
        pass

    @dispatch(MinusNode, Context)
    def visit_node(self, node: MinusNode, context: Context):
        pass

    @dispatch(StarNode, Context)
    def visit_node(self, node: StarNode, context: Context):
        pass

    @dispatch(While, Context)
    def visit_node(self, node: While, context: Context):
        self.register_instruction(LabelNode("while_condition"))
        condition = self.visit_node(node.condition, context.create_child_context())
        self.register_instruction(GotoIfNode(condition, "while_start"))
        self.register_instruction(GotoIfNode(condition, "while_end"))
        self.register_instruction(LabelNode("while_start"))
        result = self.visit_node(node.body, context.create_child_context())
        self.register_instruction(GotoNode("while_condition"))
        self.register_instruction(LabelNode("while_end"))
        return result

    @dispatch(DestructiveAssign, Context)
    def visit_node(self, node: DestructiveAssign, context: Context):
        result = self.visit_node(node.identifier, context.create_child_context())
        value = self.visit_node(node.expression, context.create_child_context())
        self.register_instruction(AssignNode(result, value))
        return result

    @dispatch(If, Context)
    def visit_node(self, node: If, context: Context):
        result = self.define_internal_local()
        # conditions
        condition = self.visit_node(node.condition, context.create_child_context())
        self.register_instruction(GotoIfNode(condition, "if_true"))
        for i, elif_node in enumerate(node.elif_clauses):
            condition = self.visit_node(
                elif_node.condition, context.create_child_context()
            )
            self.register_instruction(GotoIfNode(condition, "if_true_" + str(i)))
        if_result = self.visit_node(node.else_body, context.create_child_context())
        self.register_instruction(AssignNode(result, if_result))

        # body
        self.register_instruction(LabelNode("if_true"))
        if_result = self.visit_node(node.body, context.create_child_context())
        self.register_instruction(AssignNode(result, if_result))
        self.register_instruction(GotoNode("if_end"))
        for i, elif_node in enumerate(node.elif_clauses):
            self.register_instruction(LabelNode("if_true_" + str(i)))
            if_result = self.visit_node(elif_node.body, context.create_child_context())
            self.register_instruction(AssignNode(result, if_result))
            self.register_instruction(LabelNode("if_end"))

        self.register_instruction(LabelNode("if_end"))
        return result

    @dispatch(Identifier, Context)
    def visit_node(self, node: Identifier, context: Context):
        value = context.get_var(node.identifier)
        return value
