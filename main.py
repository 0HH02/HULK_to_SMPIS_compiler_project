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


PROGRAM = """
    let iterable= range(  0,10)in
        while(iterable.next ( ) )
            let x= iterable.current()in
                print( x ) ;
    """

lexer = Lexer(TOKEN_PATTERNS)

tokens: list[Token] = lexer.tokenize(PROGRAM)

start_time = time.time()

grammar, mapping = get_hulk_grammar()
parser = ParserLR1(grammar, mapping)

parser.parse(tokens)
end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")
