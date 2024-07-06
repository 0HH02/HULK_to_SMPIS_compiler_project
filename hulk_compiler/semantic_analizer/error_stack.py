from collections import deque


class SemanticError:
    def __init__(self, message: str, position: tuple[int, int]) -> None:
        self.message: str = message
        self.position: tuple[int, int] = position

    @property
    def line_error(self):
        return self.position[0]

    @property
    def column_error(self):
        return self.position[1]


class StackError:
    def __init__(self) -> None:
        self.errors: deque[SemanticError] = deque()

    def add_error(self, message: str, position: tuple[int, int]):
        self.errors.append(SemanticError(message, position))

    def get_errors(self):
        while len(self.errors) > 0:
            yield self.errors.pop()

    @property
    def ok(self):
        return len(self.errors) == 0


def print_error(code: str, error: SemanticError):
    print(f"Error in line: {error.line_error} and column: {error.column_error}")
    print(error.message)
    show_code = ""

    line = 0
    for char in code:
        if char == "\n":
            line += 1
        if error.line_error < line:
            break
        if line == error.line_error:
            show_code += char

    print(show_code)
    print("^" * len(show_code))
