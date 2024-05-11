"""
This is the Tester File for the Project
"""

from testers.lexer_tester import LexerTester
from lexer.lexer import Lexer
from lexer.hulk_token_patterns import TOKEN_PATTERNS

# from Lexer.HulkTokenize import hulk_tokenize

# with open("Test1.txt", "r", encoding="utf-8") as file:
#     text = file.read()

# tokens = []
# tokens = hulk_tokenize(text)
# print(tokens, sep="\n")

tester = LexerTester(Lexer(TOKEN_PATTERNS))

tester.run_tests()
