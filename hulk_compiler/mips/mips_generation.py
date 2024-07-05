from .mips_nodes import *
from queue import Queue


from hulk_compiler.code_generation.cil_generation.cil_nodes import (
    ProgramNode,
    FunctionNode,
    GotoIfNode,
    GotoNode,
    PrintNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    ModNode,
    PowNode,
    ANDNode,
    ORNode,
    EQNode,
    NEQNode,
    GTNode,
    LTNode,
    GENode,
    LENode,
    AssignNode,
)

from multipledispatch import dispatch

# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class CilToMipsVisitor:

    def __init__(self) -> None:
        self.mips = []
        self.registers: list[str] = [
            "$t0",
            "$t1",
            "$t2",
            "$t3",
            "$t4",
            "$t5",
            "$t6",
            "$t7",
            "$t8",
            "$t9",
        ]

        self.registers_queue: Queue[(str, str)] = Queue()
        for register in self.registers:
            self.registers_queue.put((register, None))
        self.variables_in_registers: dict[str, str] = {}
        self.variables_in_ram: dict[str, int] = {}
        self.heap_pointer = 0

    @dispatch(ProgramNode)
    def visit(self, node: ProgramNode) -> None:
        self.mips = []
        self.mips.append(".data")
        self.mips.append(".text")
        self.mips.append(".globl main")

        for function in node.dotcode:
            self.mips.append(str(self.visit(function)))

        print("\n".join(self.mips))

    @dispatch(FunctionNode)
    def visit(self, node: FunctionNode) -> MipsFunction:

        instruccions: list = []

        for instruccion in node.instructions:
            instruccions.append(self.visit(instruccion))

        return MipsFunction(node.name, instruccions)

    @dispatch(GotoIfNode)
    def visit(self, node: GotoIfNode) -> BranchOnNotEqualZero:
        return BranchOnNotEqualZero(node.condicion, node.label)

    @dispatch(GotoNode)
    def visit(self, node: GotoNode) -> JumpLabel:
        return JumpLabel(node.label)

    @dispatch(PrintNode)
    def visit(self, node: PrintNode) -> PrintMips:
        return PrintMips(node.str_addr)

    @dispatch(PowNode)
    def visit(self, node: PowNode) -> PowMips:
        return PowMips(node.dest, node.left, node.right)

    @dispatch(PlusNode)
    def visit(self, node: PlusNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "add")

    @dispatch(MinusNode)
    def visit(self, node: MinusNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "sub")

    @dispatch(StarNode)
    def visit(self, node: StarNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "mul")

    @dispatch(DivNode)
    def visit(self, node: DivNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "div")

    @dispatch(ModNode)
    def visit(self, node: ModNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "mod")

    @dispatch(ANDNode)
    def visit(self, node: ANDNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "and")

    @dispatch(ORNode)
    def visit(self, node: ORNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "or")

    @dispatch(EQNode)
    def visit(self, node: EQNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "seq")

    @dispatch(NEQNode)
    def visit(self, node: NEQNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "sne")

    @dispatch(GTNode)
    def visit(self, node: GTNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "sgt")

    @dispatch(LTNode)
    def visit(self, node: LTNode) -> Operation:
        return Operation(node.dest, node.left, node.right, "slt")

    @dispatch(GENode)
    def visit(self, node: GENode) -> Operation:
        return Operation(node.dest, node.left, node.right, "sge")

    @dispatch(LENode)
    def visit(self, node: LENode) -> Operation:
        return Operation(node.dest, node.left, node.right, "sle")

    @dispatch(AssignNode)
    def visit(self, node: AssignNode) -> Operation:
        dest = self.handle_variable(node.dest)
        return LoadConstant(dest, node.source)

    def handle_variable(self, variable: str) -> str:
        instruccions = []
        if variable in self.variables_in_registers:
            return self.variables_in_registers[variable]

        (register, reg_var) = self.registers_queue.get()
        if reg_var is not None:
            if not reg_var in self.variables_in_ram:
                self.variables_in_ram[reg_var] = self.heap_pointer
                self.heap_pointer += 4

            instruccions.append(StoreWord(register, self.variables_in_ram[reg_var]))

        return register
