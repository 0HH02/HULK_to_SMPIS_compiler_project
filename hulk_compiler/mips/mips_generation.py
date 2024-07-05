from hulk_compiler.code_generation.cil_generation.cil_nodes import ProgramNode

from multipledispatch import dispatch


class CilToMipsVisitor:

    @dispatch(ProgramNode)
    def visit(self, node: ProgramNode) -> None:
        self.mips = []
        self.mips.append(".data")
        self.mips.append('newline: .asciiz "\\n"')
        self.mips.append('space: .asciiz " "')
        self.mips.append(".text")
        self.mips.append("main:")

        for instruccion in node.dotcode:
            self.mips.append(str(self.visit(instruccion)))
