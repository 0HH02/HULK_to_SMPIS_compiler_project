"""
"""

from .context import Context
from .type_checker import TypeChecker
from .type_collector import TypeCollector
from .type_inferer import TypeInferer
from .error_stack import StackError, print_error
from ..parser.ast.ast import ASTNode


def check_semantic(program: ASTNode, code: str):
    """
    Performs semantic analysis on the given program.

    Args:
        program (ASTNode): The abstract syntax tree representing the program.

    Returns:
        bool: True if the program passes semantic analysis, False otherwise.
    """

    stack_error = StackError()

    program_context = Context()
    program_context.define_built_ins()

    TypeCollector.collect(program, program_context, stack_error)
    if not stack_error.ok:
        print_errors(stack_error, code)

    TypeInferer.infer_node(program, program_context, stack_error)
    if not stack_error.ok:
        print_errors(stack_error, code)

    valid_program = TypeChecker.check_node(program, program_context, stack_error)
    if not stack_error.ok:
        print_errors(stack_error, code)

    return valid_program


def print_errors(stack: StackError, code: str):
    for error in stack.get_errors():
        print_error(code, error)
