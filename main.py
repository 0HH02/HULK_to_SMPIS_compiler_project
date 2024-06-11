"""
"""

import time
from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.ast.ast import ASTNode
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS
from .hulk_compiler.parser.ast.ast_printer import ASTPrinter

PROGRAM = """
    function tan(x) => sin(x) / cos(x);

print(tan(4));
    """

lexer = Lexer(TOKEN_PATTERNS)

tokens: list[Token] = lexer.tokenize(PROGRAM)

start_time = time.time()

grammar, mapping = get_hulk_grammar()
parser = ParserLR1(grammar, mapping)

ast: ASTNode = parser.parse(tokens)
ASTPrinter.visit_node(ast, 0)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
