from multipledispatch import dispatch
from .cil_nodes import *
from .base_cil_generation import BaseHULKToCILVisitor
from hulk_compiler.semantic_analizer.context import Context
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


# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring


class HULKToCILVisitor(BaseHULKToCILVisitor):

    @dispatch(Program)
    def visit_node(self, node: Program):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################

        self.current_function = self.register_function("entry")
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name("main", "Main")
        self.register_instruction(AllocateNode("Main", instance))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(main_method_name, result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        for define in node.defines:
            self.visit_node(define)

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @dispatch(TypeDeclaration)
    def visit_node(self, node: TypeDeclaration):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################

        # self.current_type = self.context.get_type(node.id)

        for feature in zip(node.functions):
            self.visit_node(feature)

        self.current_type = None

    @dispatch(FunctionDeclaration)
    def visit_node(self, node: FunctionDeclaration):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################

        self.current_method = self.current_type.get_method(node.id)

        # Your code here!!! (Handle PARAMS)

        for instruction in zip(node.body):
            value = self.visit_node(instruction)
        # Your code here!!! (Handle RETURN)

        self.current_method = None

    @dispatch(VariableDeclaration)
    def visit_node(self, node):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################

        # Your code here!!!
        pass

    @dispatch(LetVar)
    def visit_node(self, node: LetVar):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################

        self.current_function = self.register_function(
            f"function_let_{len(self.dotcode)}"
        )
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name("main", "Main")
        self.register_instruction(AllocateNode("Main", instance))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(main_method_name, result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None

        for var in node.declarations:
            self.visit_node(var.expression)
            self.define_internal_local()

    @dispatch(FunctionCall)
    def visit_node(self, node):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################

        # Your code here!!!
        pass

    @dispatch(LiteralNode)
    def visit_node(self, node):
        ###############################
        # node.lex -> str
        ###############################

        # Your code here!!! (Pretty easy ;-))
        pass

    @dispatch(VariableDeclaration)
    def visit_node(self, node):
        ###############################
        # node.lex -> str
        ###############################

        # Your code here!!!
        pass

    @dispatch(Instanciate)
    def visit_node(self, node):
        ###############################
        # node.lex -> str
        ###############################

        # Your code here!!!
        pass

    @dispatch(PositiveNode)
    def visit_node(self, node):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################

        # Your code here!!!
        pass

    @dispatch(NegativeNode)
    def visit_node(self, node):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################

        # Your code here!!!
        pass

    @dispatch(NotNode)
    def visit_node(self, node):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################

        # Your code here!!!
        pass

    @dispatch(BinaryExpression)
    def visit_node(self, node):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################

        # Your code here!!!
        pass
