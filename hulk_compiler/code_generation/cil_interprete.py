import math
from multipledispatch import dispatch
from hulk_compiler.code_generation.cil_generation.cil_nodes import *
from hulk_compiler.code_generation.cil_generation.cil_nodes import FunctionNode

# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class cil_interpreter:

    def __init__(self) -> None:
        self.data = {}
        self.locals = {}
        self.args = []
        self.functions = []
        self.return_var = None
        self.program_counter = {}
        self.current_function = None
        self.function_labels: dict[str, dict[str, int]] = {}

    @dispatch(ProgramNode)
    def visit(self, node: ProgramNode):
        for data in node.dotdata:
            self.visit(data)

        self.functions: list[FunctionNode] = node.dotcode
        self.visit(node.dotcode[-1])

    @dispatch(FunctionNode)
    def visit(self, node: FunctionNode):
        self.current_function: str = node.name
        self.program_counter[node.name] = 0
        self.function_labels[node.name] = {}
        for i, param in enumerate(node.params[1:]):
            self.locals[param.name] = self.locals[self.args[i]]
        self.args = []

        for i, instr in enumerate(node.instructions):
            if isinstance(instr, LabelNode):
                self.function_labels[node.name][instr.name] = i

        while self.program_counter[node.name] < len(node.instructions):
            self.visit(node.instructions[self.program_counter[node.name]])
            self.program_counter[node.name] += 1

    @dispatch(AssignNode)
    def visit(self, node: AssignNode):
        self.locals[node.dest] = float(node.source)

    @dispatch(PlusNode)
    def visit(self, node: PlusNode):
        self.locals[node.dest] = self.locals[node.left] + self.locals[node.right]

    @dispatch(MinusNode)
    def visit(self, node: MinusNode):
        self.locals[node.dest] = self.locals[node.left] - self.locals[node.right]

    @dispatch(StarNode)
    def visit(self, node: StarNode):
        self.locals[node.dest] = self.locals[node.left] * self.locals[node.right]

    @dispatch(DivNode)
    def visit(self, node: DivNode):
        self.locals[node.dest] = self.locals[node.left] / self.locals[node.right]

    @dispatch(ModNode)
    def visit(self, node: ModNode):
        self.locals[node.dest] = self.locals[node.left] % self.locals[node.right]

    @dispatch(ANDNode)
    def visit(self, node: ANDNode):
        self.locals[node.dest] = self.locals[node.left] & self.locals[node.right]

    @dispatch(ORNode)
    def visit(self, node: ORNode):
        self.locals[node.dest] = self.locals[node.left] | self.locals[node.right]

    @dispatch(EQNode)
    def visit(self, node: EQNode):
        self.locals[node.dest] = self.locals[node.left] == self.locals[node.right]

    @dispatch(NEQNode)
    def visit(self, node: NEQNode):
        self.locals[node.dest] = self.locals[node.left] != self.locals[node.right]

    @dispatch(GTNode)
    def visit(self, node: GTNode):
        self.locals[node.dest] = self.locals[node.left] > self.locals[node.right]

    @dispatch(GENode)
    def visit(self, node: GENode):
        self.locals[node.dest] = self.locals[node.left] >= self.locals[node.right]

    @dispatch(LTNode)
    def visit(self, node: LTNode):
        self.locals[node.dest] = self.locals[node.left] < self.locals[node.right]

    @dispatch(LENode)
    def visit(self, node: LENode):
        self.locals[node.dest] = self.locals[node.left] <= self.locals[node.right]

    @dispatch(PowNode)
    def visit(self, node: PowNode):
        self.locals[node.dest] = self.locals[node.left] ** self.locals[node.right]

    @dispatch(PrintNode)
    def visit(self, node: PrintNode):
        if "data" in node.str_addr:
            print(self.data[node.str_addr])
        else:
            print(self.locals[node.str_addr])

    @dispatch(ArrayNode)
    def visit(self, node: ArrayNode):
        self.data[node.dest] = node.list

    @dispatch(ConcatNode)
    def visit(self, node: ConcatNode):
        if "data" in node.left:
            left = self.data[node.left][1:-1]
        else:
            left = self.locals[node.left]

        if "data" in node.right:
            right = self.data[node.right][1:-1]
        else:
            right = self.locals[node.right]

        self.locals[node.dest] = str(left) + str(right)

    @dispatch(ArgNode)
    def visit(self, node: ArgNode):
        self.args.append(node.name)

    @dispatch(StaticCallNode)
    def visit(self, node: StaticCallNode):
        if node.function == "sin":
            self.locals[node.dest] = math.sin(self.locals[self.args[0]])
            self.args = []

        elif node.function == "cos":
            self.locals[node.dest] = math.cos(self.locals[self.args[0]])
            self.args = []

        elif node.function == "sqrt":
            self.locals[node.dest] = math.sqrt(self.locals[self.args[0]])
            self.args = []

        elif node.function == "log":
            self.locals[node.dest] = math.log(
                self.locals[self.args[0]], self.locals[self.args[1]]
            )
            self.args = []
        else:
            funct: FunctionNode = [
                f for f in self.functions if node.function in f.name
            ][0]
            self.visit(funct)
            self.locals[node.dest] = self.locals[self.return_var]

    @dispatch(ReturnNode)
    def visit(self, node: ReturnNode):
        self.return_var: str = node.value

    @dispatch(MoveNode)
    def visit(self, node: MoveNode):
        if "data" in node.source:
            source = self.data[node.source]
        else:
            source = self.locals[node.source]
        self.locals[node.dest] = source

    @dispatch(GotoIfNode)
    def visit(self, node: GotoIfNode):
        if self.locals[node.condicion]:
            self.program_counter[self.current_function] = self.function_labels[
                self.current_function
            ][node.label_name]

    @dispatch(GotoNode)
    def visit(self, node: GotoNode):
        self.program_counter[self.current_function] = self.function_labels[
            self.current_function
        ][node.label_name]

    @dispatch(LabelNode)
    def visit(self, node: LabelNode):
        pass
