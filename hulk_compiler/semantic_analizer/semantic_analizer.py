"""
"""

from .context import Context
from .type_checker import TypeCheckVisitor
from ..parser.ast.ast import ASTNode


def check_semantic(program: ASTNode):
    """
    Performs semantic analysis on the given program.

    Args:
        program (ASTNode): The abstract syntax tree representing the program.

    Returns:
        bool: True if the program passes semantic analysis, False otherwise.
    """
    program_context = Context()
    program_context.define_built_ins()

    return TypeCheckVisitor.visit_node(program, program_context)
