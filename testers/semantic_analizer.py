from hulk_compiler.parser.ast.ast import (
    Program,
    TypeDeclaration,
    Inherits,
    AttributeDeclaration,
    FunctionDeclaration,
    Parameter,
    ProtocolDeclaration,
    VariableDeclaration,
    DestructiveAssign,
    Call,
    Elif,
    If,
    For,
    While,
    LetVar,
    Instanciate,
    Vector,
    IndexNode,
    BinaryExpression,
    NotNode,
    PositiveNode,
    NegativeNode,
    LiteralNode,
    Operator,
    Identifier,
)

from hulk_compiler.lexer.token import Token, TokenType
from hulk_compiler.semantic_analizer.types import Type


AST1_PROGRAM = "let x = 8 in 2;"
AST1 = Program(
    [],
    [
        LetVar(
            VariableDeclaration(
                Token("x", TokenType.IDENTIFIER, 0, 5),
                LiteralNode(Token("8", TokenType.NUMBER_LITERAL, 0, 8)),
            ),
            LiteralNode(Token("2", TokenType.NUMBER_LITERAL, 0, 10)),
        )
    ],
)

AST2_PROGRAM = """
    let number = 42 in (
        let text = "The meaning of life is" in (
                print(text @ number)
            )
        );
    """

AST2 = Program(
    [],
    [
        LetVar(
            VariableDeclaration(
                Token("number", TokenType.IDENTIFIER, 0, 5),
                LiteralNode(Token("42", TokenType.NUMBER_LITERAL, 0, 14)),
            ),
            LetVar(
                VariableDeclaration(
                    Token("text", TokenType.IDENTIFIER, 1, 9),
                    LiteralNode(
                        Token("The meaning of life is", TokenType.STRING_LITERAL, 1, 16)
                    ),
                ),
                Call(
                    None,
                    Token(
                        "print",
                        TokenType.IDENTIFIER,
                        2,
                        12,
                    ),
                    BinaryExpression(
                        Operator.CONCAT,
                        Identifier(Token("text", TokenType.IDENTIFIER, 2, 18)),
                        Identifier(Token("number", TokenType.IDENTIFIER, 2, 25)),
                    ),
                ),
            ),
        )
    ],
)

AST3 = Program(
    [
        TypeDeclaration(
            "Carro",
            [],
            None,
            [
                AttributeDeclaration(
                    "ruedas", LiteralNode(Token("4", TokenType.NUMBER, 0, 0))
                ),
                AttributeDeclaration(
                    "color", LiteralNode(Token("rojo", TokenType.STRING, 0, 0))
                ),
            ],
            [],
        ),
        TypeDeclaration(
            "Persona",
            [],
            None,
            [
                AttributeDeclaration(
                    "fuerza", LiteralNode(Token("5", TokenType.NUMBER, 0, 0))
                ),
                AttributeDeclaration(
                    "ojos", LiteralNode(Token("café", TokenType.STRING, 0, 0))
                ),
            ],
            [
                FunctionDeclaration(
                    "suma",
                    [Parameter("a", None), Parameter("b", None)],
                    None,
                    Type("Sumando"),
                )
            ],
        ),
    ],
    [],
)
