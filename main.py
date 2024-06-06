"""
"""

# pylint: disable=pointless-statement

from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.grammar.grammar import Grammar
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS
import time


lexer = Lexer(TOKEN_PATTERNS)


start_time = time.time()

grammar, mapping = get_hulk_grammar()
parser = ParserLR1(grammar, mapping)


end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")


# for p in grammar.productions.values():
#     for s in p:
#         print(p)
#         print(s.attributation)
PROGRAM = """
    if (4==4)
       2
    else
        4; 
    """

tokens: list[Token] = lexer.tokenize(PROGRAM)

print(parser.parse(tokens))
