from multipledispatch import dispatch
from hulk_compiler.core.i_visitor import IVisitor

# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []


class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions


class ParamNode(Node):
    def __init__(self, name):
        self.name = name


class LocalNode(Node):
    def __init__(self, name):
        self.name = name


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class GetAttribNode(InstructionNode):
    pass


class SetAttribNode(InstructionNode):
    pass


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    pass


class GotoNode(InstructionNode):
    pass


class GotoIfNode(InstructionNode):
    pass


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    pass


class ConcatNode(InstructionNode):
    pass


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    pass


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class PrintVisitor(IVisitor):

    @dispatch(ProgramNode)
    def visit_node(self, node: ProgramNode):
        dottypes = "\n".join(self.visit_node(t) for t in node.dottypes)
        dotdata = "\n".join(self.visit_node(t) for t in node.dotdata)
        dotcode = "\n".join(self.visit_node(t) for t in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @dispatch(TypeNode)
    def visit_node(self, node: TypeNode):
        attributes = "\n\t".join(f"attribute {x}" for x in node.attributes)
        methods = "\n\t".join(f"method {x}: {y}" for x, y in node.methods)

        return f"type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}"

    @dispatch(FunctionNode)
    def visit_node(self, node: FunctionNode):
        params = "\n\t".join(self.visit_node(x) for x in node.params)
        localvars = "\n\t".join(self.visit_node(x) for x in node.localvars)
        instructions = "\n\t".join(self.visit_node(x) for x in node.instructions)

        return f"function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}"

    @dispatch(ParamNode)
    def visit_node(self, node: ParamNode):
        return f"PARAM {node.name}"

    @dispatch(LocalNode)
    def visit_node(self, node: LocalNode):
        return f"LOCAL {node.name}"

    @dispatch(AssignNode)
    def visit_node(self, node: AssignNode):
        return f"{node.dest} = {node.source}"

    @dispatch(PlusNode)
    def visit_node(self, node: PlusNode):
        return f"{node.dest} = {node.left} + {node.right}"

    @dispatch(MinusNode)
    def visit_node(self, node: MinusNode):
        return f"{node.dest} = {node.left} - {node.right}"

    @dispatch(StarNode)
    def visit_node(self, node: StarNode):
        return f"{node.dest} = {node.left} * {node.right}"

    @dispatch(DivNode)
    def visit_node(self, node: DivNode):
        return f"{node.dest} = {node.left} / {node.right}"

    @dispatch(AllocateNode)
    def visit_node(self, node: AllocateNode):
        return f"{node.dest} = ALLOCATE {node.type}"

    @dispatch(TypeOfNode)
    def visit_node(self, node: TypeOfNode):
        return f"{node.dest} = TYPEOF {node.type}"

    @dispatch(StaticCallNode)
    def visit_node(self, node: StaticCallNode):
        return f"{node.dest} = CALL {node.function}"

    @dispatch(DynamicCallNode)
    def visit_node(self, node: DynamicCallNode):
        return f"{node.dest} = VCALL {node.type} {node.method}"

    @dispatch(ArgNode)
    def visit_node(self, node: ArgNode):
        return f"ARG {node.name}"

    @dispatch(ReturnNode)
    def visit_node(self, node: ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'
