from abc import ABC


class AST(ABC):
    pass


class LiteralCharNode(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"LiteralNode : {self.value} "

    def __repr__(self) -> str:
        return self.__str__()


class AnyCharNode(AST):
    def __str__(self):
        return "AnyCharNode"

    def __repr__(self) -> str:
        return self.__str__()


class GroupNode(AST):
    def __init__(self, values: list[str], negative: bool):
        self.values: list[str] = values
        self.negative = negative

    def __str__(self) -> str:
        return (
            "GroupNode :"
            + ("not" if self.negative else "")
            + "{"
            + f"{self.values}"
            + "}"
        )

    def __repr__(self) -> str:
        return self.__str__()


class OrNode(AST):
    def __init__(self, nodes: list[AST]) -> None:
        self.nodes: list[AST] = nodes

    def __str__(self) -> str:
        return (
            "OrNode : " + "{" + " | ".join([str(node) for node in self.nodes]) + "}"
            if len(self.nodes) > 1
            else str(self.nodes[0])
        )

    def __repr__(self) -> str:
        return self.__str__()


class ConcatNode(AST):
    def __init__(self, expressions: list[AST]) -> None:
        self.expressions: list[AST] = expressions

    def __str__(self) -> str:
        return str(self.expressions)

    def __repr__(self) -> str:
        return self.__str__()


class EpsilonNode(AST):
    def __str__(self) -> str:
        return "EpsilonNode"

    def __repr__(self) -> str:
        return self.__str__()


class PlusNode(AST):
    def __init__(self, node: AST) -> None:
        self.child: AST = node

    def __str__(self) -> str:
        return f"PlusNode : {self.child}"

    def __repr__(self) -> str:
        return self.__str__()


class RepeatNode(AST):
    def __init__(self, node: AST, repeat: int) -> None:
        self.child: AST = node
        self.repeat: int = repeat

    def __str__(self) -> str:
        return f"RepeatNode x{self.repeat} : {self.child}"

    def __repr__(self) -> str:
        return self.__str__()
