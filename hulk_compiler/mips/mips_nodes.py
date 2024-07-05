OPER_TO_CLASS = {}


class Node:
    pass


class Operation(Node):
    def __init__(self, destini, op1, op2, op) -> None:
        self.destini = destini
        self.op1 = op1
        self.op2 = op2
        self.op: str = op

        if not self.op in [
            "add",
            "sub",
            "mul",
            "div",
            "rem",
            "and",
            "or",
            "slt",
            "sle",
            "sgt",
            "sge",
            "seq",
            "sne",
        ]:
            raise ValueError("Invalid operation")

    def __str__(self) -> str:
        return f"{self.op} {self.destini}, {self.op1}, {self.op2}"

    def __repr__(self) -> str:
        return str(self)


class OperationInmediate(Node):
    def __init__(self, destini, op1, constant, op) -> None:
        self.destini = destini
        self.op1 = op1
        self.constant = constant
        self.op: str = op

        if not self.op in [
            "addi",
            "subi",
            "muli",
            "divi",
            "remi",
            "andi",
            "ori",
            "slti",
            "slei",
            "sgti",
            "sgei",
            "seqi",
            "snei",
        ]:
            raise ValueError("Invalid operation")

    def __str__(self) -> str:
        return f"{self.op} {self.destini}, {self.op1}, {self.constant}"

    def __repr__(self) -> str:
        return str(self)


class MipsProgram(Node):
    def __init__(self, data, text, functions) -> None:
        self.data: list[MipsData] = data
        # self.text: list[MipsFunction] = []
        self.functions: list[MipsFunction] = functions

    def __str__(self) -> str:
        data = "\n".join(map(str, self.data))
        functions = "\n".join(map(str, self.functions))
        return f".data\n{data}\n.text\n\n.globl main\n{functions}"

    def __repr__(self) -> str:
        return str(self)


class JumpAndLink(Node):
    def __init__(self, label) -> None:
        self.label = label

    def __str__(self) -> str:
        return f"jal {self.label}"

    def __repr__(self) -> str:
        return str(self)


class JumpRegister(Node):
    def __init__(self, reg) -> None:
        self.reg = reg

    def __str__(self) -> str:
        return f"jr {self.reg}"

    def __repr__(self) -> str:
        return str(self)


class JumpLabel(Node):
    def __init__(self, label) -> None:
        self.label = label

    def __str__(self) -> str:
        return f"j {self.label}"

    def __repr__(self) -> str:
        return str(self)


class BranchOnNotEqualZero(Node):
    def __init__(self, reg, label) -> None:
        self.reg = reg
        self.label = label

    def __str__(self) -> str:
        return f"bnez {self.reg}, {self.label}"

    def __repr__(self) -> str:
        return str(self)


class BranchOnEqualZero(Node):
    def __init__(self, reg, label) -> None:
        self.reg = reg
        self.label = label

    def __str__(self) -> str:
        return f"beqz {self.reg}, {self.label}"

    def __repr__(self) -> str:
        return str(self)


class Move(Node):
    def __init__(self, destini, source) -> None:
        self.destini = destini
        self.source = source

    def __str__(self) -> str:
        return f"move {self.destini}, {self.source}"

    def __repr__(self) -> str:
        return str(self)


class StoreWord(Node):
    def __init__(self, source, address) -> None:
        self.source = source
        self.address = address

    def __str__(self) -> str:
        return f"sw {self.source}, {self.address}"

    def __repr__(self) -> str:
        return str(self)


class StoreByte(Node):
    def __init__(self, source, address) -> None:
        self.source = source
        self.address = address

    def __str__(self) -> str:
        return f"sb {self.source}, {self.address}"

    def __repr__(self) -> str:
        return str(self)


class LoadWord(Node):
    def __init__(self, destiny, address) -> None:
        self.destiny = destiny
        self.address = address

    def __str__(self) -> str:
        return f"lw {self.destiny}, {self.address}"

    def __repr__(self) -> str:
        return str(self)


class LoadByte(Node):
    def __init__(self, destiny, address) -> None:
        self.destiny = destiny
        self.address = address

    def __str__(self) -> str:
        return f"lb {self.destiny}, {self.address}"

    def __repr__(self) -> str:
        return str(self)


class LoadConstant(Node):
    def __init__(self, destiny, constant) -> None:
        self.destiny = destiny
        self.constant = constant

    def __str__(self) -> str:
        return f"li {self.destiny}, {self.constant}"

    def __repr__(self) -> str:
        return str(self)


class LoadString(Node):
    def __init__(self, destiny, label) -> None:
        self.destiny = destiny
        self.label = label

    def __str__(self) -> str:
        return f"la {self.destiny}, {self.label}"

    def __repr__(self) -> str:
        return str(self)


class MipsFunction(Node):
    def __init__(self, name, instructions) -> None:
        self.name = name
        self.instructions = instructions

    def __str__(self) -> str:
        instruccions = []
        instruccions.append(f"{self.name}:")
        instruccions.extend(map(str, self.instructions))
        instruccions.append("jr $ra")
        return "\n".join(instruccions)

    def __repr__(self) -> str:
        return str(self)


class Label(Node):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}:"

    def __repr__(self) -> str:
        return str(self)


class PrintStringMips(Node):
    def __init__(self, label) -> None:
        self.label = label

    def __str__(self) -> str:
        instruccions = []
        instruccions.append(LoadConstant("$v0", 4))
        instruccions.append(LoadString("$a0", self.label))
        instruccions.append("syscall")
        return "\n".join(map(str, instruccions))

    def __repr__(self) -> str:
        return str(self)


class PrintIntMips(Node):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        instruccions = []
        instruccions.append(LoadConstant("$v0", 1))
        instruccions.append(Move("$a0", self.value))
        instruccions.append("syscall")
        return "\n".join(map(str, instruccions))

    def __repr__(self) -> str:
        return str(self)


class PowMips(Node):
    def __init__(self, destini, base, exp) -> None:
        self.destini: str = destini
        self.base: str = base
        self.exp: str = exp

    def __str__(self) -> str:
        instruccions = []
        instruccions.append(LoadConstant(self.destini, 1))
        instruccions.append(Label("exp_loop"))
        instruccions.append(Operation(self.destini, self.destini, self.base, "mul"))
        instruccions.append(OperationInmediate(self.exp, self.exp, -1, "addi"))
        instruccions.append(BranchOnNotEqualZero(self.exp, "exp_loop"))
        return "\n".join(map(str, instruccions))

    def __repr__(self) -> str:
        return str(self)


class MipsData(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: .asciiz {self.value}"

    def __repr__(self) -> str:
        return str(self)


class MipsConcat(Node):
    def __init__(self, t0, t1, t2, buffer, op1, op2) -> None:
        self.t0 = t0
        self.t1 = t1
        self.t2 = t2
        self.buffer = buffer
        self.op1 = op1
        self.op2 = op2

    def __str__(self) -> str:
        instructions = []
        instructions.append(LoadString(self.t0, self.op1))
        instructions.append(LoadString(self.t1, self.buffer))
        instructions.append(Label("copy_str1"))
        instructions.append(LoadByte(self.t2, f"0({self.t0})"))
        instructions.append(BranchOnEqualZero(self.t2, "find_end"))
        instructions.append(StoreByte(self.t2, f"0({self.t1})"))
        instructions.append(OperationInmediate(self.t0, self.t0, 1, "addi"))
        instructions.append(OperationInmediate(self.t1, self.t1, 1, "addi"))
        instructions.append(JumpLabel("copy_str1"))
        instructions.append(Label("find_end"))
        instructions.append(LoadString(self.t0, self.op2))
        instructions.append(Label("copy_str2"))
        instructions.append(LoadByte(self.t2, f"0({self.t0})"))
        instructions.append(BranchOnEqualZero(self.t2, "add_null"))
        instructions.append(StoreByte(self.t2, f"0({self.t1})"))
        instructions.append(OperationInmediate(self.t0, self.t0, 1, "addi"))
        instructions.append(OperationInmediate(self.t1, self.t1, 1, "addi"))
        instructions.append(JumpLabel("copy_str2"))
        instructions.append(Label("add_null"))
        instructions.append(StoreByte("$zero", f"0({self.t1})"))
        return "\n".join(map(str, instructions))

    def __repr__(self) -> str:
        return str(self)
