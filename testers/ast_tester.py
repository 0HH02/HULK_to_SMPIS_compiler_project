from hulk_compiler.lexer.token import Token
from hulk_compiler.parser.ast.ast import ASTNode
from hulk_compiler.parser.grammar.hulk import get_hulk_grammar
from hulk_compiler.parser.parser_lr1 import ParserLR1
from hulk_compiler.lexer.lexer import Lexer
from hulk_compiler.lexer.hulk_token_patterns import TOKEN_PATTERNS
from hulk_compiler.parser.ast.ast_printer import ASTPrinter
from hulk_compiler.semantic_analizer.semantic_analizer import check_semantic
import os
from testers.semantic_analizer import AST1
from hulk_compiler.code_generation.cil_generation.cil_generation import HULKToCILVisitor
from hulk_compiler.code_generation.cil_generation.cil_nodes import PrintVisitor


def test_all() -> None:

    lexer = Lexer(TOKEN_PATTERNS)

    grammar, mapping = get_hulk_grammar()

    parser = ParserLR1(grammar, mapping)

    # Get the path to the test folder
    TEST_FOLDER = "testers/test"

    # Iterate over all files in the test folder
    for filename in os.listdir(TEST_FOLDER):
        # Get the full path to the file
        file_path: str = os.path.join(TEST_FOLDER, filename)
        # Open the file and read its contents
        with open(file_path, "r", encoding="utf-8") as file:
            program: str = file.read()
            try:
                tokens: list[Token] = lexer.tokenize(program)
                ast: ASTNode = parser.parse(tokens)
                print(f"AST for file: {file_path}")
                ASTPrinter.visit_node(ast)
                # check_semantic(ast)
            except:
                print(f"Error in file: {file_path}")
                raise


def hulk_to_CIL_test():
    cil_ast = HULKToCILVisitor().visit_node(AST1)
    PrintVisitor().visit_node(cil_ast)
