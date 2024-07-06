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
    MoveNode,
    ConcatNode,
)

from multipledispatch import dispatch

# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class CilToMipsVisitor:

    def __init__(self) -> None:
        self.functions = []
        self.data = []
        self.text = []
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
        # Queue of (registers, variable_name) tuples
        self.registers_queue: Queue[(str, str)] = Queue()
        for register in self.registers:
            self.registers_queue.put((register, None))
        self.variables_in_registers: dict[str, str] = {}
        self.variables_in_ram: dict[str, int] = {}
        self.heap_pointer = 0

    @dispatch(ProgramNode)
    def visit(self, node: ProgramNode) -> None:

        for data in node.dotdata:
            self.data.append(str(MipsData(data.dest, data.list)))

        for function in node.dotcode:
            self.functions.append(str(self.visit(function)))

        program = MipsProgram(self.data, self.text, self.functions)
        print(str(program))

        return program

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
    def visit(self, node: PrintNode) -> PrintStringMips:
        if "data" in node.str_addr:
            return PrintStringMips(node.str_addr)
        reg, instruccion = self.get_variable(node.str_addr)
        return PrintIntMips(reg)

    @dispatch(PowNode)
    def visit(self, node: PowNode) -> PowMips:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return PowMips(dest, left, right)

    @dispatch(PlusNode)
    def visit(self, node: PlusNode) -> Operation:

        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "add")

    @dispatch(MinusNode)
    def visit(self, node: MinusNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "sub")

    @dispatch(StarNode)
    def visit(self, node: StarNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "mul")

    @dispatch(DivNode)
    def visit(self, node: DivNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "div")

    @dispatch(ModNode)
    def visit(self, node: ModNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "mod")

    @dispatch(ANDNode)
    def visit(self, node: ANDNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "and")

    @dispatch(ORNode)
    def visit(self, node: ORNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "or")

    @dispatch(EQNode)
    def visit(self, node: EQNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "seq")

    @dispatch(NEQNode)
    def visit(self, node: NEQNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "sne")

    @dispatch(GTNode)
    def visit(self, node: GTNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "sgt")

    @dispatch(LTNode)
    def visit(self, node: LTNode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "slt")

    @dispatch(GENode)
    def visit(self, node: GENode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "sge")

    @dispatch(LENode)
    def visit(self, node: LENode) -> Operation:
        dest, instructions = self.set_variable(node.dest)
        left, instructions = self.get_variable(node.left)
        right, instructions = self.get_variable(node.right)
        return Operation(dest, left, right, "sle")

    @dispatch(AssignNode)
    def visit(self, node: AssignNode) -> Operation:
        dest, instruction = self.set_variable(node.dest)
        return LoadConstant(dest, node.source)

    @dispatch(MoveNode)
    def visit(self, node: MoveNode) -> Operation:
        dest, instruction = self.set_variable(node.dest)
        source, instruction = self.get_variable(node.source)
        return Move(dest, source)

    def set_variable(self, variable: str) -> str:
        instruccions = []
        if (
            variable in self.variables_in_registers
            and self.variables_in_registers[variable] is not None
        ):
            return self.variables_in_registers[variable], instruccions

        (register, reg_var) = self.registers_queue.get()
        if reg_var is not None:
            self.variables_in_registers[reg_var] = None

            if not reg_var in self.variables_in_ram:
                self.variables_in_ram[reg_var] = self.heap_pointer
                self.heap_pointer += 4

            instruccions.append(StoreWord(register, self.variables_in_ram[reg_var]))

        self.variables_in_registers[variable] = register
        self.registers_queue.put((register, variable))

        return register, instruccions

    def get_variable(self, variable: str) -> str:
        instruccions = []

        if (
            variable in self.variables_in_registers
            and self.variables_in_registers[variable] is not None
        ):
            return self.variables_in_registers[variable], instruccions

        register, instruccions = self.set_variable(variable)

        instruccions.append(LoadWord(register, self.variables_in_ram[variable]))

        return self.variables_in_ram[variable], instruccions
