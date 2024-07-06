from multipledispatch import dispatch
from hulk_compiler.core.i_visitor import IVisitor
from hulk_compiler.parser.ast.ast import Operator

# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes: list[TypeNode] = dottypes
        self.dotdata: list[ArrayNode] = dotdata
        self.dotcode: list[FunctionNode] = dotcode


class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes: dict[str, str] = {}
        self.methods = []


class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params: list[ParamNode] = params
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


class MoveNode(InstructionNode):
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


class ModNode(ArithmeticNode):
    pass


class PowNode(ArithmeticNode):
    pass


class GTNode(ArithmeticNode):
    pass


class LTNode(ArithmeticNode):
    pass


class EQNode(ArithmeticNode):
    pass


class ANDNode(ArithmeticNode):
    pass


class ORNode(ArithmeticNode):
    pass


class NEQNode(ArithmeticNode):
    pass


class GENode(ArithmeticNode):
    pass


class LENode(ArithmeticNode):
    pass


class GetAttribNode(InstructionNode):
    pass


class SetAttribNode(InstructionNode):
    def __init__(self, source, dest, value):
        self.dest = dest
        self.source = source
        self.value = value


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest


class ArrayNode(InstructionNode):
    def __init__(self, list: list, dest: str):
        self.list = list
        self.dest = dest


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class GotoNode(InstructionNode):
    def __init__(self, label_name):
        self.label_name = label_name


class GotoIfNode(InstructionNode):
    def __init__(self, condicion, label_name):
        self.condicion = condicion
        self.label_name = label_name


class GotoIfNotNode(InstructionNode):
    def __init__(self, condicion, label_name):
        self.condicion = condicion
        self.label_name = label_name


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
    def __init__(self, dest, left, left_type, right, right_type):
        self.dest = dest
        self.left = left
        self.left_type = left_type
        self.right = right
        self.right_type = right_type


class IsNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class AsNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


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


OPER_TO_CLASS = {
    Operator.ADD: PlusNode,
    Operator.SUB: MinusNode,
    Operator.MUL: StarNode,
    Operator.DIV: DivNode,
    Operator.MOD: ModNode,
    Operator.POW: PowNode,
    Operator.AND: ANDNode,
    Operator.OR: ORNode,
    Operator.EQ: EQNode,
    Operator.NEQ: NEQNode,
    Operator.GT: GTNode,
    Operator.LT: LTNode,
    Operator.GE: GENode,
    Operator.LE: LENode,
    Operator.CONCAT: ConcatNode,
    Operator.DCONCAT: ConcatNode,
    Operator.IS: IsNode,
    Operator.AS: AsNode,
}


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
        return f"ASSIGN {node.dest} = {node.source}"

    @dispatch(MoveNode)
    def visit_node(self, node: MoveNode):
        return f"MOVE {node.dest} = {node.source}"

    @dispatch(SetAttribNode)
    def visit_node(self, node: SetAttribNode):
        return f"{node.source}.{node.dest} = {node.value}"

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

    @dispatch(ModNode)
    def visit_node(self, node: ModNode):
        return f"{node.dest} = {node.left} % {node.right}"

    @dispatch(GTNode)
    def visit_node(self, node: GTNode):
        return f"{node.dest} = {node.left} > {node.right}"

    @dispatch(LTNode)
    def visit_node(self, node: LTNode):
        return f"{node.dest} = {node.left} < {node.right}"

    @dispatch(PowNode)
    def visit_node(self, node: PowNode):
        return f"{node.dest} = {node.left} ** {node.right}"

    @dispatch(EQNode)
    def visit_node(self, node: EQNode):
        return f"{node.dest} = {node.left} == {node.right}"

    @dispatch(ANDNode)
    def visit_node(self, node: ANDNode):
        return f"{node.dest} = {node.left} and {node.right}"

    @dispatch(ORNode)
    def visit_node(self, node: ORNode):
        return f"{node.dest} = {node.left} or {node.right}"

    @dispatch(NEQNode)
    def visit_node(self, node: NEQNode):
        return f"{node.dest} = {node.left} != {node.right}"

    @dispatch(GENode)
    def visit_node(self, node: GENode):
        return f"{node.dest} = {node.left} >= {node.right}"

    @dispatch(LENode)
    def visit_node(self, node: LENode):
        return f"{node.dest} = {node.left} <= {node.right}"

    @dispatch(IsNode)
    def visit_node(self, node: IsNode):
        return f"{node.dest} = {node.left} is {node.right}"

    @dispatch(AsNode)
    def visit_node(self, node: AsNode):
        return f"{node.dest} = {node.left} as {node.right}"

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

    @dispatch(PrintNode)
    def visit_node(self, node: PrintNode):
        return f'PRINT {node.str_addr if node.str_addr is not None else ""}'

    @dispatch(ConcatNode)
    def visit_node(self, node: ConcatNode):
        return f"{node.dest} = CONCAT {node.left} {node.right}"

    @dispatch(LabelNode)
    def visit_node(self, node: LabelNode):
        return f"LABEL {node.name}"

    @dispatch(GotoNode)
    def visit_node(self, node: GotoNode):
        return f"GOTO {node.label_name}"

    @dispatch(GotoIfNode)
    def visit_node(self, node: GotoIfNode):
        return f"GOTO {node.label_name} if {node.condicion}"

    @dispatch(ArrayNode)
    def visit_node(self, node: ArrayNode):
        return f"ARRAY {node.dest} {[str(x) for x in node.list]}"
