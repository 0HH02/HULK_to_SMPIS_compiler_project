import time
from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.ast.ast import ASTNode
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS
from hulk_compiler.parser.ast.ast_printer import ASTPrinter
from testers.ast_tester import test_all
from testers.ast_tester import hulk_to_CIL_test


# test_all()

hulk_to_CIL_test()
