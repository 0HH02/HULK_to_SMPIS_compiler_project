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


class LoadWord(Node):
    def __init__(self, destiny, address) -> None:
        self.destiny = destiny
        self.address = address

    def __str__(self) -> str:
        return f"lw {self.destiny}, {self.address}"

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


class PrintMips(Node):
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        instruccions = []
        instruccions.append(LoadConstant("$v0", 4))
        instruccions.append(LoadConstant("$a0", self.value))
        instruccions.append("Syscall()")
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
        instruccions.append(OperationInmediate(self.exp, self.exp, 1, "subi"))
        instruccions.append(BranchOnNotEqualZero(self.exp, "exp_loop"))
        return "\n".join(map(str, instruccions))

    def __repr__(self) -> str:
        return str(self)
