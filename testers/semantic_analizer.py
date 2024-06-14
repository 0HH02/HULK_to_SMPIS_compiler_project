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

from hulk_compiler.semantic_analizer.types import NumberType, StringType
from hulk_compiler.semantic_analizer.types import Type


AST1_PROGRAM = "let x = 8 in 2;"
AST1 = Program(
    [],
    [
        LetVar(
            [
                VariableDeclaration("x", LiteralNode("8", NumberType())),
            ],
            LiteralNode("2", NumberType()),
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

# AST2 = Program(
#     [],
#     [
#         LetVar(
#             [
#                 VariableDeclaration(
#                     Token("number", TokenType.IDENTIFIER, 0, 5),
#                     LiteralNode(Token("42", TokenType.NUMBER_LITERAL, 0, 14)),
#                 )
#             ],
#             LetVar(
#                 [
#                     VariableDeclaration(
#                         Token("text", TokenType.IDENTIFIER, 1, 9),
#                         LiteralNode(
#                             Token(
#                                 "The meaning of life is",
#                                 TokenType.STRING_LITERAL,
#                                 1,
#                                 16,
#                             )
#                         ),
#                     ),
#                 ],
#                 Call(
#                     Identifier("fulanito"),
#                     Token(
#                         "print",
#                         TokenType.IDENTIFIER,
#                         2,
#                         12,
#                     ),
#                     [
#                         BinaryExpression(
#                             Operator.CONCAT,
#                             Identifier(Token("text", TokenType.IDENTIFIER, 2, 18)),
#                             Identifier(Token("number", TokenType.IDENTIFIER, 2, 25)),
#                         )
#                     ],
#                 ),
#             ),
#         )
#     ],
# )

AST3 = Program(
    [
        TypeDeclaration(
            "Carro",
            [],
            None,
            [
                AttributeDeclaration("ruedas", LiteralNode("4", NumberType())),
                AttributeDeclaration("color", LiteralNode("rojo", NumberType())),
            ],
            [],
        ),
        TypeDeclaration(
            "Persona",
            [],
            None,
            [
                AttributeDeclaration("fuerza", LiteralNode("5", NumberType())),
                AttributeDeclaration("ojos", LiteralNode("café", StringType())),
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
