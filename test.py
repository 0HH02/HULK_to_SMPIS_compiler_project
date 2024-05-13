"""
This is the Tester File for the Project
"""

from testers.lexer_tester import LexerTester
from lexer.lexer import Lexer
from core.hulk_language.hulk_token_patterns import TOKEN_PATTERNS

tester = LexerTester(Lexer(TOKEN_PATTERNS))

tester.run_tests()
