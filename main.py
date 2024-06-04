"""
"""

import time
from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS


PROGRAM = """
    5*8;
    """
PROGRAM = """
    5*8;
    """

lexer = Lexer(TOKEN_PATTERNS)
lexer = Lexer(TOKEN_PATTERNS)

tokens: list[Token] = lexer.tokenize(PROGRAM)
tokens: list[Token] = lexer.tokenize(PROGRAM)

start_time = time.time()
start_time = time.time()

grammar, mapping = get_hulk_grammar()
parser = ParserLR1(grammar, mapping)
grammar, mapping = get_hulk_grammar()
parser = ParserLR1(grammar, mapping)

parser.parse(tokens)
end_time = time.time()
execution_time = end_time - start_time
parser.parse(tokens)
end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
print(f"Execution time: {execution_time} seconds")


# a = 5

# a = "jola"


# print(a)
