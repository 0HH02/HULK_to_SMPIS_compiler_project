from typing import Any
from multipledispatch import dispatch

from .cil_nodes import (
    FunctionNode,
)
from .cil_nodes import *
from .base_cil_generation import BaseHULKToCILVisitor
from .cil_context import Context
from ...semantic_analizer.types import IdentifierVar
from ...semantic_analizer.transpiler.hulk_transpiler import HulkTranspiler


from hulk_compiler.parser.ast.ast import (
    Program,
    While,
    If,
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
    LiteralNode,
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
    def generate_cil(self, node: Program, context: Context = Context()):
        # self.buildin_types(node)
    def visit_node(self, node: Program, context: Context = Context()):
        self.buildin_types(node)
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################

        main = Type("main")
        self.current_function = None

        self.current_type = main
        for define in node.defines:
            if isinstance(define, FunctionDeclaration):
                self.current_type = main
                self.generate_cil(define, context.create_child_context())

        orden: list[TypeDeclaration] = self.topological_sort(node)
        for n in orden:
            self.generate_cil(n, context.create_child_context())

        self.current_function = self.register_function("main")
        self.generate_cil(node.statement, context.create_child_context())
        # self.register_instruction(ReturnNode(0))

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    def buildin_types(self, node):
        node.defines.append(
            TypeDeclaration(
                "range",
                [Parameter("min"), Parameter("max")],
                None,
                [
                    AttributeDeclaration("min", Identifier("min")),
                    AttributeDeclaration("max", Identifier("max")),
                    AttributeDeclaration(
                        "current",
                        BinaryExpression(
                            Operator.SUB,
                            Identifier("min"),
                            LiteralNode("1", NumberType()),
                        ),
                    ),
                ],
                [
                    FunctionDeclaration(
                        "current", [], AttributeCall(Identifier("self"), "current")
                    ),
                    FunctionDeclaration(
                        "next",
                        [],
                        BinaryExpression(
                            Operator.LT,
                            DestructiveAssign(
                                AttributeCall(Identifier("self"), "current"),
                                BinaryExpression(
                                    Operator.ADD,
                                    AttributeCall(Identifier("self"), "current"),
                                    LiteralNode("1", NumberType()),
                                ),
                            ),
                            AttributeCall(Identifier("self"), "max"),
                        ),
                    ),
                ],
            )
        )
        node.defines.append(
            TypeDeclaration(
                "vector",
                [Parameter("elements"), Parameter("length")],
                None,
                [
                    AttributeDeclaration("elements", Identifier("elements")),
                    AttributeDeclaration("length", Identifier("length")),
                    AttributeDeclaration("current", LiteralNode("0", NumberType())),
                ],
                [
                    FunctionDeclaration("current", [], LiteralNode("1", None)),
                    FunctionDeclaration("next", [], LiteralNode("2", None)),
                    FunctionDeclaration("get_item", [], LiteralNode("2", None)),
                ],
            )
        )

    def topological_sort(self, node) -> list[TypeDeclaration]:
        type_list: list[TypeDeclaration] = [
            tp for tp in node.defines if isinstance(tp, TypeDeclaration)
        ]

        adyacents: list[list[int]] = [[] for _ in range(len(type_list))]

        for i, tp in enumerate(type_list):
            if tp.inherits:
                for j, tp2 in enumerate(type_list):
                    if tp2.identifier == tp.inherits.identifier:
                        adyacents[j].append(i)
                        break

        # Topological sort
        indegrees: list[int] = [0] * len(type_list)

        for i in range(len(type_list)):
            for j in adyacents[i]:
                indegrees[j] += 1

        cola: list[int] = [i for i, indegree in enumerate(indegrees) if indegree == 0]

        # Paso 3: Orden topológico
        orden = []
        while cola:
            nodo = cola.pop(0)
            orden.append(type_list[nodo])
            for vecino in adyacents[nodo]:
                indegrees[vecino] -= 1
                if indegrees[vecino] == 0:
                    cola.append(vecino)
        return orden

    @dispatch(TypeDeclaration, Context)
    def generate_cil(self, node: TypeDeclaration, context: Context):
        self.current_type = self.register_type(node.identifier)

        if node.inherits:
            father = TypeNode("None")
            for t in self.dottypes:
                if t.name == node.inherits.identifier:
                    father = t
                    break
            for attr in father.attributes:
                self.current_type.attributes[attr] = father.attributes[attr]
            for method in father.methods:
                self.current_type.methods.append([method[0], method[1]])

        self.current_function = self.register_function(
            f"function_{node.identifier}_constructor"
        )
        self.current_type.methods.append(
            ["constructor", f"function_{node.identifier}_constructor"]
        )
        context.define_method(
            "contructor", f"function_{node.identifier}_constructor", len(node.params)
        )
        if node.inherits:
            if node.inherits.arguments:
                for attr in node.params:
                    param_name = f"{self.current_function.name[9:]}_{attr.identifier}_{len(self.localvars)}"
                    context.define_variable(attr.identifier, param_name)
                    self.current_function.params.append(ParamNode(param_name))
                args = []
                for attr in node.inherits.arguments:
                    result = self.generate_cil(attr, context.create_child_context())
                    args.append(result)
                for arg in args:
                    self.register_instruction(ArgNode(arg))
                result = self.register_local(IdentifierVar("constructor_result", None))
                self.register_instruction(
                    DynamicCallNode(
                        self.current_type.name,
                        f"function_{node.inherits.identifier}_constructor",
                        result,
                    )
                )
            else:
                result = self.register_local(IdentifierVar("constructor_result", None))
                self.register_instruction(
                    DynamicCallNode(
                        self.current_type.name,
                        f"function_{node.inherits.identifier}_constructor",
                        result,
                    )
                )
        elif node.params:
            for attr in node.params:
                param_name = f"{self.current_function.name[9:]}_{attr.identifier}_{len(self.localvars)}"
                context.define_variable(attr.identifier, param_name)
                self.current_function.params.append(ParamNode(param_name))
            for attr in node.attributes:
                self.generate_cil(attr, context.create_child_context())
        else:
            for attr in node.attributes:
                self.generate_cil(attr, context.create_child_context())
        for method in node.functions:
            method_reference = self.generate_cil(method, context.create_child_context())
            for method_declared in self.current_type.methods:
                if method_declared[0] == method.identifier:
                    method_declared[1] = method_reference
                    break
            else:
                self.current_type.methods.append([method.identifier, method_reference])
                context.define_method(
                    method.identifier, method_reference, len(method.params)
                )

    @dispatch(AttributeDeclaration, Context)
    def generate_cil(self, node: AttributeDeclaration, context: Context):
        attr_name = (
            self.current_type.name
            + "_"
            + node.identifier
            + "_"
            + str(len(self.current_type.attributes))
        )
        self.current_type.attributes[node.identifier] = attr_name
        attr_value = self.generate_cil(node.expression, context.create_child_context())
        self.current_function.instructions.append(
            SetAttribNode(self.current_type.name, attr_name, attr_value)
        )
        return node.identifier

    @dispatch(AttributeCall, Context)
    def generate_cil(self, node: AttributeCall, context: Context):
        obj = self.generate_cil(node.obj, context)
        if "self" in obj:
            value = self.current_type.attributes[node.identifier]
            return value

    @dispatch(FunctionDeclaration, Context)
    def generate_cil(self, node: FunctionDeclaration, context: Context):
        function_name: str = self.to_function_name(
            node.identifier, self.current_type.name
        )
        self.current_function: FunctionNode = self.register_function(function_name)
        context.define_method(node.identifier, self.current_function, len(node.params))

        param_name = f"{self.current_function.name[9:]}_self_{len(self.localvars)}"
        param_node = ParamNode(param_name)
        context.define_variable("self", param_name)
        self.current_function.params.append(param_node)
        for param in node.params:
            param_name = f"{self.current_function.name[9:]}_{param.identifier}_{len(self.localvars)}"
            param_node = ParamNode(param_name)
            context.define_variable(param.identifier, param_name)
            self.current_function.params.append(param_node)

        result = self.generate_cil(node.body, context.create_child_context())
        self.register_instruction(ReturnNode(result))

        self.current_function = None
        return function_name

    @dispatch(VariableDeclaration, Context)
    def generate_cil(self, node: VariableDeclaration, context: Context):

        var_info = IdentifierVar(node.identifier, node.inferred_type)

        var_name = self.register_local(var_info)

        context.define_variable(node.identifier, var_name)

        expr_value = self.generate_cil(node.expression, context.create_child_context())

        self.register_instruction(MoveNode(var_name, expr_value))
        return var_name

    @dispatch(LetVar, Context)
    def generate_cil(self, node: LetVar, context: Context):

        # Procesar las declaraciones de variables
        for var_decl in node.declarations:
            # Visitar la expresión de la declaración de la variable
            var_name: str = self.generate_cil(var_decl, context.create_child_context())
            # Registrar la variable local
            context.define_variable(var_decl.identifier, var_name)

        # Procesar el cuerpo del letvar
        body_result: str = self.generate_cil(node.body, context.create_child_context())
        return body_result

    @dispatch(FunctionCall, Context)
    def generate_cil(self, node: FunctionCall, context: Context):
        result = self.register_local(IdentifierVar(node.invocation.identifier, None))
        variable = context.get_var(node.obj.identifier)
        self.register_instruction(ArgNode(variable))
        for param in node.invocation.arguments:
            value = self.generate_cil(param, context)
            self.register_instruction(ArgNode(value))
        self.register_instruction(
            DynamicCallNode(variable, node.invocation.identifier, result)
        )
        return result

    @dispatch(LiteralNode, Context)
    def generate_cil(self, node: LiteralNode, context: Context):
        if node.inferred_type is StringType():
            return self.register_data(node.value).dest

        reference = self.register_local(
            IdentifierVar(
                f"value_{node.value}_{len(self.current_function.localvars)}", None
            )
        )
        self.register_instruction(AssignNode(reference, node.value))
        return reference

    @dispatch(Instanciate, Context)
    def generate_cil(self, node: Instanciate, context: Context):
        for param in node.params:
            param_value = self.generate_cil(param, context)
            self.register_instruction(ArgNode(param_value))
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode(node.identifier, instance))
        self.register_instruction(
            StaticCallNode(f"{node.identifier}_constructor", result)
        )
        return instance

    @dispatch(Invocation, Context)
    def generate_cil(self, node: Invocation, context: Context):

        if node.identifier == "print":
            result = self.generate_cil(
                node.arguments[0], context.create_child_context()
            )
            self.register_instruction(PrintNode(result))
            return result
        if node.identifier == "range":
            min_value = self.visit_node(
                node.arguments[0], context.create_child_context()
            )
            max_value = self.visit_node(
                node.arguments[1], context.create_child_context()
            )
            instance = self.register_local(IdentifierVar("range", None))
            self.register_instruction(AllocateNode("range", instance))
            self.register_instruction(ArgNode(min_value))
            self.register_instruction(ArgNode(max_value))
            result = self.register_local(IdentifierVar("cache", None))
            self.register_instruction(
                DynamicCallNode("range", "range_constructor", result)
            )
            return instance

        # Falta por implementar: Guardar en el contexto las funciones a medida que las voy declarando y aquí solamente devuelvo la referencia a la función
        args = [
            self.generate_cil(arg, context.create_child_context())
            for arg in node.arguments
        ]
        for arg in args:
            self.register_instruction(ArgNode(arg))

        result = self.define_internal_local()
        self.register_instruction(StaticCallNode(node.identifier, result))
        return result

    @dispatch(PositiveNode, Context)
    def generate_cil(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(NegativeNode, Context)
    def generate_cil(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(NotNode, Context)
    def generate_cil(self, node, context: Context):

        # Your code here!!!
        pass

    @dispatch(ExpressionBlock, Context)
    def generate_cil(self, node: ExpressionBlock, context: Context):
        for i, expression in enumerate(node.body):
            result = self.generate_cil(expression, context.create_child_context())
            if i == len(node.body) - 1:
                return result

    @dispatch(BinaryExpression, Context)
    def generate_cil(self, node: BinaryExpression, context: Context):

        left = self.generate_cil(node.left, context.create_child_context())
        right = self.generate_cil(node.right, context.create_child_context())
        result = self.register_local(
            IdentifierVar(f"value_{len(self.current_function.localvars)}", None)
        )
        if OPER_TO_CLASS[node.operator] is ConcatNode:
            self.register_instruction(
                OPER_TO_CLASS[node.operator](
                    result,
                    left,
                    node.left.inferred_type,
                    right,
                    node.right.inferred_type,
                )
            )
            return result
        self.register_instruction(OPER_TO_CLASS[node.operator](result, left, right))
        return result

    @dispatch(Identifier, Context)
    def generate_cil(self, node: Identifier, context: Context):

        return context.get_var(node.identifier)
        # return self.register_instruction(LoadNode(node.name))

    @dispatch(PlusNode, Context)
    def generate_cil(self, node: PlusNode, context: Context):
        pass

    @dispatch(MinusNode, Context)
    def generate_cil(self, node: MinusNode, context: Context):
        pass

    @dispatch(StarNode, Context)
    def generate_cil(self, node: StarNode, context: Context):
        pass

    @dispatch(While, Context)
    def generate_cil(self, node: While, context: Context):
        self.register_instruction(LabelNode("while_condition"))
        condition = self.generate_cil(node.condition, context.create_child_context())
        self.register_instruction(GotoIfNode(condition, "while_start"))
        self.register_instruction(GotoNode("while_end"))
        self.register_instruction(LabelNode("while_start"))
        result = self.generate_cil(node.body, context.create_child_context())
        self.register_instruction(GotoNode("while_condition"))
        self.register_instruction(LabelNode("while_end"))
        return result

    @dispatch(DestructiveAssign, Context)
    def generate_cil(self, node: DestructiveAssign, context: Context):
        result = self.generate_cil(node.identifier, context.create_child_context())
        value = self.generate_cil(node.expression, context.create_child_context())
        self.register_instruction(MoveNode(result, value))
        return result

    @dispatch(If, Context)
    def generate_cil(self, node: If, context: Context):
        result = self.define_internal_local()
        # conditions
        condition = self.generate_cil(node.condition, context.create_child_context())
        self.register_instruction(GotoIfNode(condition, "if_true"))
        for i, elif_node in enumerate(node.elif_clauses):
            condition = self.generate_cil(
                elif_node.condition, context.create_child_context()
            )
            self.register_instruction(GotoIfNode(condition, "if_true_" + str(i)))
        if_result = self.visit_node(node.else_body, context.create_child_context())
        self.register_instruction(MoveNode(result, if_result))
        self.register_instruction(GotoNode("if_end"))

        # body
        self.register_instruction(LabelNode("if_true"))
        if_result = self.visit_node(node.body, context.create_child_context())
        self.register_instruction(MoveNode(result, if_result))
        self.register_instruction(GotoNode("if_end"))
        for i, elif_node in enumerate(node.elif_clauses):
            self.register_instruction(LabelNode("if_true_" + str(i)))
            if_result = self.visit_node(elif_node.body, context.create_child_context())
            self.register_instruction(MoveNode(result, if_result))
            self.register_instruction(LabelNode("if_end"))

        self.register_instruction(LabelNode("if_end"))
        return result

    @dispatch(Identifier, Context)
    def generate_cil(self, node: Identifier, context: Context):
        value = context.get_var(node.identifier)
        if value is None:
            value = context.get_type(node.identifier)
        return value

    @dispatch(For, Context)
    def generate_cil(self, node: For, context: Context):
        node = HulkTranspiler.transpile_node(node)
        return self.generate_cil(node, context.create_child_context())

    @dispatch(Vector, Context)
    def generate_cil(self, node: Vector, context: Context):
        # Crear un nuevo vector
        vector: ArrayNode = self.register_data(
            [element.value for element in node.elements]
        )

        instance = self.define_internal_local()
        self.register_instruction(AllocateNode("array", instance))

        self.register_instruction(ArgNode(vector.dest))
        self.register_instruction(ArgNode(len(node.elements)))

        result = self.define_internal_local()
        self.register_instruction(
            StaticCallNode(f"function_vector_constructor", result)
        )
        return instance

    @dispatch(IndexNode, Context)
    def generate_cil(self, node: IndexNode, context: Context):
        if isinstance(node.index, LiteralNode):
            index = self.generate_cil(node.index, context)
        else:
            index = context.get_var(node.index.identifier)
        vector = context.get_var(node.obj.identifier)
        result = self.register_local(IdentifierVar("indexed_value", None))
        self.register_instruction(ArgNode(index))
        self.register_instruction(DynamicCallNode(vector, "get_item", result))
        return result

    @dispatch(ComprehensionVector, Context)
    def generate_cil(self, node: ComprehensionVector, context: Context):
        node = HulkTranspiler.transpile_node(node)
        return self.generate_cil(node, context.create_child_context())
