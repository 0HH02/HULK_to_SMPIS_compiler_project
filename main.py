from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.semantic_analizer.semantic_analizer import check_semantic
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS
from hulk_compiler.lexer.hulk_constants import HULK_CONSTANTS
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.code_generation.cil_generation.cil_generation import HULKToCILVisitor
from hulk_compiler.code_generation.cil_interprete import cil_interpreter
from testers.ast_tester import test_all


def main(path: str):
    test_all()
    # with open(path, "r", encoding="utf-8") as file:
    #     code: str = file.read()
    #     lexer = Lexer(TOKEN_PATTERNS, HULK_CONSTANTS)
    #     tokens: list[Token] = lexer.tokenize(code)
    #     grammar, mapping = get_hulk_grammar()
    #     parser = ParserLR1(grammar, mapping)
    #     ast = parser.parse(tokens)
    #     valid_program: bool = check_semantic(ast, code)
    #     if valid_program:
    #         cil_ast = HULKToCILVisitor().generate_cil(ast)
    #         cil_interpreter().visit(cil_ast)


if __name__ == "__main__":
    path = "tests/test_files/program.hulk"
    main(path)
