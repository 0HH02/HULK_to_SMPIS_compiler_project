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
    FunctionCall,
    Invocation,
    ExpressionBlock,
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

AST2 = Program(
    [],
    [
        LetVar(
            [
                VariableDeclaration(
                    "number",
                    LiteralNode("42", NumberType()),
                )
            ],
            LetVar(
                [
                    VariableDeclaration(
                        "text", LiteralNode("The meaning of life is", StringType())
                    ),
                ],
                Invocation(
                    "print",
                    [
                        BinaryExpression(
                            Operator.CONCAT,
                            Identifier("text"),
                            Identifier("number"),
                        )
                    ],
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


AST4 = Program(
    [],
    [
        LetVar(
            [VariableDeclaration("a", LiteralNode("20", NumberType()))],
            ExpressionBlock(
                [
                    LetVar(
                        [VariableDeclaration("a", LiteralNode("42", NumberType()))],
                        Invocation("print", [Identifier("a")]),
                    ),
                    Invocation("print", [Identifier("a")]),
                ]
            ),
        ),
    ],
)


AST5_PROGRAM = """program: {
    invocation: {
       identifier:  print
       let: {
          variable_declaration: {
             identifier: b
             static_type: Unknown
             literal:  6
             infered_type:  Number
          }
          binary_node: {
             operator:  Operator.MUL
             identifier: b
             literal:  7
             infered_type:  Number
          }
       }
    }
 }"""

AST5 = Program(
    [],
    [
        Invocation(
            "print",
            [
                LetVar(
                    [
                        VariableDeclaration("b", LiteralNode("6", NumberType())),
                    ],
                    BinaryExpression(
                        Operator.MUL,
                        Identifier("b"),
                        LiteralNode("7", NumberType()),
                    ),
                )
            ],
        )
    ],
)


AST6_PROGRAM = """ program: {
    let: {
       variable_declaration: {
          identifier: a
          static_type: Unknown
          let: {
             variable_declaration: {
                identifier: b
                static_type: Unknown
                literal:  6
                infered_type:  Number
             }
             binary_node: {
                operator:  Operator.MUL
                identifier: b
                literal:  7
                infered_type:  Number
             }
          }
       }
       invocation: {
          identifier:  print
          identifier: a
       }
    }
 }"""

AST6 = Program(
    [],
    [
        LetVar(
            [
                VariableDeclaration(
                    "a",
                    LetVar(
                        [
                            VariableDeclaration("b", LiteralNode("6", NumberType())),
                        ],
                        BinaryExpression(
                            Operator.MUL,
                            Identifier("b"),
                            LiteralNode("7", NumberType()),
                        ),
                    ),
                )
            ],
            Invocation("print", [Identifier("a")]),
        )
    ],
)

AST7_PROGRAM = """ program: {
    let: {
       variable_declaration: {
          identifier: a
          static_type: Unknown
          literal:  5
          infered_type:  Number
       }
       variable_declaration: {
          identifier: b
          static_type: Unknown
          literal:  10
          infered_type:  Number
       }
       variable_declaration: {
          identifier: c
          static_type: Unknown
          literal:  20
          infered_type:  Number
       }
       expression_block: {
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.ADD
                identifier: a
                identifier: b
             }
          }
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.MUL
                identifier: b
                identifier: c
             }
          }
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.DIV
                identifier: c
                identifier: a
             }
          }
       }
    }
 }"""
AST7 = Program(
    [],
    [
        LetVar(
            [
                VariableDeclaration("a", LiteralNode("5", NumberType())),
                VariableDeclaration("b", LiteralNode("10", NumberType())),
                VariableDeclaration("c", LiteralNode("20", NumberType())),
            ],
            ExpressionBlock(
                [
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.ADD,
                                Identifier("a"),
                                Identifier("b"),
                            )
                        ],
                    ),
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.MUL,
                                Identifier("b"),
                                Identifier("c"),
                            )
                        ],
                    ),
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.DIV,
                                Identifier("c"),
                                Identifier("a"),
                            )
                        ],
                    ),
                ]
            ),
        )
    ],
)


AST8_PROGRAM = """program: {
    function_declaration: {
       identifier:  operate
       parameter: {
          identifier x
       }
       parameter: {
          identifier y
       }
       return_type:  Unknown
       expression_block: {
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.ADD
                identifier: x
                identifier: y
             }
          }
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.SUB
                identifier: x
                identifier: y
             }
          }
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.MUL
                identifier: x
                identifier: y
             }
          }
          invocation: {
             identifier:  print
             binary_node: {
                operator:  Operator.DIV
                identifier: x
                identifier: y
             }
          }
       }
    }
    invocation: {
       identifier:  operate
       literal:  2
       infered_type:  Number
       literal:  4
       infered_type:  Number
    }
 }"""

AST8 = Program(
    [
        FunctionDeclaration(
            "operate",
            [Parameter("x", None), Parameter("y", None)],
            ExpressionBlock(
                [
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.ADD,
                                Identifier("x"),
                                Identifier("y"),
                            )
                        ],
                    ),
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.SUB,
                                Identifier("x"),
                                Identifier("y"),
                            )
                        ],
                    ),
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.MUL,
                                Identifier("x"),
                                Identifier("y"),
                            )
                        ],
                    ),
                    Invocation(
                        "print",
                        [
                            BinaryExpression(
                                Operator.DIV,
                                Identifier("x"),
                                Identifier("y"),
                            )
                        ],
                    ),
                ]
            ),
            None,
        ),
    ],
    [
        Invocation(
            "operate", [LiteralNode("2", NumberType()), LiteralNode("4", NumberType())]
        ),
    ],
)

AST9_PROGRAM = """ program: {
    function_declaration: {
       identifier:  gcd
       parameter: {
          identifier a
       }
       parameter: {
          identifier b
       }
       return_type:  Unknown
       while:{
          binary_node: {
             operator:  Operator.GT
             identifier: a
             literal:  0
             infered_type:  Number
          }
          let: {
             variable_declaration: {
                identifier: m
                static_type: Unknown
                binary_node: {
                   operator:  Operator.MOD
                   identifier: a
                   identifier: b
                }
             }
             expression_block: {
                destructive_assigment: {
                   identifier b
                   identifier: a
                }
                destructive_assigment: {
                   identifier a
                   identifier: m
                }
             }
          }
       }
    }
    invocation: {
       identifier:  print
       invocation: {
          identifier:  gcd
          literal:  200
          infered_type:  Number
          literal:  2
          infered_type:  Number
       }
    }
 }"""
AST9 = Program(
    [
        FunctionDeclaration(
            "gcd",
            [Parameter("a", None), Parameter("b", None)],
            While(
                BinaryExpression(
                    Operator.GT,
                    Identifier("a"),
                    LiteralNode("0", NumberType()),
                ),
                LetVar(
                    [
                        VariableDeclaration(
                            "m",
                            BinaryExpression(
                                Operator.MOD,
                                Identifier("a"),
                                Identifier("b"),
                            ),
                        )
                    ],
                    ExpressionBlock(
                        [
                            DestructiveAssign(Identifier("b"), Identifier("a")),
                            DestructiveAssign(Identifier("a"), Identifier("m")),
                        ]
                    ),
                ),
            ),
            None,
        )
    ],
    [
        Invocation(
            "print",
            [
                Invocation(
                    "gcd",
                    [LiteralNode("200", NumberType()), LiteralNode("2", NumberType())],
                )
            ],
        )
    ],
)
