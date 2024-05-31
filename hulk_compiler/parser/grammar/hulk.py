"""
    This module contains the grammar for the HULK programming language.
"""

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
)
from .grammar import Grammar, Symbol
from ...lexer.token import TokenType

# pylint: disable=expression-not-assigned
# pylint: disable=pointless-statement


def get_hulk_grammar() -> Grammar:
    """
    Returns the grammar for the HULK programming language.

    The grammar consists of non-terminals and terminals that define the syntax
    and structure of the HULK language. It includes definitions for statements,
    expressions, control flow, function definitions, type definitions, and more.

    Returns:
        Grammar: The grammar object representing the HULK programming language.
    """

    grammar = Grammar()

    program = grammar.set_non_terminals(["program"])
    grammar.set_seed(program)

    (
        define_statement,
        statement,
        type_definition,
        function_definition,
        protocol_definition,
        expression_block,
        statement_list,
        if_expression,
        invocation_expression,
        expression,
        aritmetic_expression,
        mult_expression,
        exponential_expression,
        unary_expression,
        primary_expression,
        literal,
        vector,
        indexed_value,
        argument_list,
        destructive_assignment,
        member_access,
        multiple_declaration,
        argument_list_definition,
        or_expression,
        and_expression,
        equality_expression,
        relational_expression,
        if_statement,
        elif_statement,
        attribute_definition,
        type_inherits,
        inherits_declaration,
        type_body,
        type_arguments,
        instantiation,
        extends_definition,
        protocol_body,
        protocol_arguments_definition,
        extends_multiple_identifier,
        protocol_multiple_arguments_definition,
        vector_element,
        head_program,
        elif_expression,
        concat_expression,
        control_statement,
        while_header,
        for_header,
        let_header,
        control_expression,
        inline_function,
        block_function,
        type_declaration,
    ) = grammar.set_non_terminals(
        [
            "define_statement",
            "statement",
            "type_definition",
            "function_definition",
            "protocol_definition",
            "expression_block",
            "statement_list",
            "if_expression",
            "invocation_expression",
            "expression",
            "aritmetic_expression",
            "mult_expression",
            "exponential_expression",
            "unary_expression",
            "primary_expression",
            "literal",
            "vector",
            "indexed_value",
            "argument_list",
            "destructive_assignment",
            "member_access",
            "multiple_declaration",
            "argument_list_definition",
            "or_expression",
            "and_expression",
            "equality_expression",
            "relational_expression",
            "if_statement",
            "elif_statement",
            "attribute_definition",
            "type_inherits",
            "inherits_declaration",
            "type_body",
            "type_arguments",
            "instantiation",
            "extends_definition",
            "protocol_body",
            "protocol_arguments_definition",
            "extends_multiple_identifier",
            "protocol_multiple_arguments_definition",
            "vector_element",
            "head_program",
            "elif_expression",
            "concat_expression",
            "control_statement",
            "while_header",
            "for_header",
            "let_header",
            "control_expression",
            "inline_function",
            "block_function",
            "type_declaration",
        ]
    )

    (
        open_brace,
        close_brace,
        semicolon,
        plus,
        minus,
        multiply,
        divide,
        power,
        mod,
        open_parenthesis,
        close_parenthesis,
        comma,
        concat,
        double_concat,
        dot,
        assignment_terminal,
        destructive_assignment_terminal,
        inline,
        colon,
        not_operator,
        or_terminal,
        and_terminal,
        equal,
        different,
        less,
        less_equal,
        greater,
        greater_equal,
        open_bracket,
        close_bracket,
        double_pipe,
    ) = grammar.set_terminals(
        [
            "{",
            "}",
            ";",
            "+",
            "-",
            "*",
            "/",
            "^",
            "%",
            "(",
            ")",
            ",",
            "@",
            "@@",
            ".",
            "=",
            ":=",
            "=>",
            ":",
            "!",
            "|",
            "&",
            "==",
            "!=",
            "<",
            "<=",
            ">",
            ">=",
            "[",
            "]",
            "||",
        ]
    )

    (
        identifier,
        let_terminal,
        in_terminal,
        function_terminal,
        number,
        string,
        true,
        false,
        is_terminal,
        as_terminal,
        if_terminal,
        elif_terminal,
        else_terminal,
        while_terminal,
        for_terminal,
        type_terminal,
        inherits,
        new,
        protocol,
        extends,
        number_type,
        string_type,
        boolean_type,
    ) = grammar.set_terminals(
        [
            "identifier",
            "let",
            "in",
            "function",
            "number",
            "string",
            "true",
            "false",
            "is",
            "as",
            "if",
            "elif",
            "else",
            "while",
            "for",
            "type",
            "inherits",
            "new",
            "protocol",
            "extends",
            "number_type",
            "string_type",
            "boolean_type",
        ]
    )

    program <= ~head_program + statement, (
        lambda h, s: Program(s[1], s[2]),
        lambda h, s: Program([], s[2]),
    )

    head_program <= ~head_program + define_statement, (
        lambda h, s: s[1] + [s[2]],
        lambda h, s: [s[1]],
    )

    define_statement <= (
        function_terminal + function_definition | type_definition | protocol_definition
    ), (lambda h, s: s[2], lambda h, s: s[1], lambda h, s: s[1])

    type_definition <= (
        type_terminal
        + identifier
        + type_arguments
        + ~type_inherits
        + open_brace
        + ~type_body
        + close_brace
    ), (
        lambda h, s: TypeDeclaration(
            identifier=s[2],
            params=s[3],
            inherits=s[4],
            attributes=[
                definition
                for definition in s[6]
                if isinstance(definition, AttributeDeclaration)
            ],
            functions=[
                definition
                for definition in s[6]
                if isinstance(definition, FunctionDeclaration)
            ],
        ),
        lambda h, s: TypeDeclaration(
            identifier=s[2],
            params=s[3],
            inherits=s[4],
            attributes=[],
            functions=[],
        ),
        lambda h, s: TypeDeclaration(
            identifier=s[2],
            params=s[3],
            inherits=None,
            attributes=[
                definition
                for definition in s[5]
                if isinstance(definition, AttributeDeclaration)
            ],
            functions=[
                definition
                for definition in s[5]
                if isinstance(definition, FunctionDeclaration)
            ],
        ),
        lambda h, s: TypeDeclaration(
            identifier=s[2],
            params=s[3],
            inherits=None,
            attributes=[],
            functions=[],
        ),
    )

    type_body <= (
        ~type_body + attribute_definition | ~type_body + function_definition,
        lambda h, s: s[1] + [s[2]],
        lambda h, s: [s[2]],
        lambda h, s: s[1] + [s[2]],
        lambda h, s: [s[1]],
    )

    attribute_definition <= identifier + ~type_declaration + assignment_terminal + expression + semicolon, (
        lambda h, s: AttributeDeclaration(s[1], s[4], s[2]),
        lambda h, s: AttributeDeclaration(s[1], s[3]),
    )

    type_arguments <= (
        open_parenthesis + ~argument_list_definition + close_parenthesis
    ), (
        lambda h, s: s[2],
        lambda h, s: [],
    )

    type_inherits <= inherits + identifier + ~inherits_declaration, (
        lambda h, s: Inherits(s[2], s[3]),
        lambda h, s: Inherits(s[2], []),
    )

    type_declaration <= (
        colon + identifier
        | colon + number_type
        | colon + string_type
        | colon + boolean_type
    ), (lambda h, s: s[2])

    inherits_declaration <= open_parenthesis + ~argument_list + close_parenthesis, (
        lambda h, s: s[2],
        lambda h, s: [],
    )

    function_definition <= inline_function | block_function, (lambda h, s: s[1])

    inline_function <= (
        identifier
        + open_parenthesis
        + ~argument_list_definition
        + close_parenthesis
        + ~type_declaration
        + inline
        + statement
    ), (
        lambda h, s: FunctionDeclaration(s[1], s[3], s[7], s[5]),
        lambda h, s: FunctionDeclaration(s[1], s[3], s[6]),
        lambda h, s: FunctionDeclaration(s[1], [], s[6], s[4]),
        lambda h, s: FunctionDeclaration(s[1], [], s[5]),
    )

    block_function <= (
        identifier
        + open_parenthesis
        + ~argument_list_definition
        + close_parenthesis
        + ~type_declaration
        + expression_block
    ), (
        lambda h, s: FunctionDeclaration(s[1], s[3], s[6], s[5]),
        lambda h, s: FunctionDeclaration(s[1], s[3], s[5]),
        lambda h, s: FunctionDeclaration(s[1], [], s[5], s[4]),
        lambda h, s: FunctionDeclaration(s[1], [], s[4], []),
    )

    argument_list_definition <= (
        ~(argument_list_definition + comma) + identifier + ~type_declaration
    ), (
        lambda h, s: s[1] + [Parameter(s[3], s[4])],
        lambda h, s: s[1] + [Parameter(s[3])],
        lambda h, s: [Parameter(s[2], s[3])],
        lambda h, s: [Parameter(s[1])],
    )

    protocol_definition <= (
        protocol
        + identifier
        + ~extends_definition
        + open_brace
        + ~protocol_body
        + close_brace
    ), (
        lambda h, s: ProtocolDeclaration(s[2], s[3], s[5]),
        lambda h, s: ProtocolDeclaration(s[2], s[3], []),
        lambda h, s: ProtocolDeclaration(s[2], [], s[4]),
        lambda h, s: ProtocolDeclaration(s[2], [], []),
    )

    extends_definition <= (extends + identifier + ~extends_multiple_identifier), (
        lambda h, s: [s[2]] + s[3],
        lambda h, s: [s[2]],
    )

    extends_multiple_identifier <= (
        comma + identifier + ~extends_multiple_identifier
    ), (lambda h, s: [s[2]] + s[3], lambda h, s: [s[2]])

    protocol_body <= (
        ~protocol_body
        + identifier
        + open_parenthesis
        + ~protocol_arguments_definition
        + close_parenthesis
        + type_declaration
        + semicolon
    ), (
        lambda h, s: s[1] + [FunctionDeclaration(s[2], s[4], None, s[6])],
        lambda h, s: s[1] + [FunctionDeclaration(s[2], None, None, s[5])],
        lambda h, s: [FunctionDeclaration(s[1], s[3], None, s[5])],
        lambda h, s: [FunctionDeclaration(s[1], None, None, s[4])],
    )

    protocol_arguments_definition <= (
        identifier + type_declaration + ~protocol_multiple_arguments_definition
    ), (
        lambda h, s: [Parameter(s[1], s[2])] + s[3],
        lambda h, s: [Parameter(s[1], s[2])],
    )

    protocol_multiple_arguments_definition <= (
        comma + identifier + type_declaration + ~protocol_multiple_arguments_definition
    ), (
        lambda h, s: [Parameter(s[2], s[3])] + s[4],
        lambda h, s: [Parameter(s[2], s[3])],
    )

    statement <= (
        expression_block + ~semicolon
        | or_expression + semicolon
        | destructive_assignment + semicolon
        | control_statement
    ), (lambda h, s: s[1])

    control_statement <= (
        if_statement
        | while_header + statement
        | for_header + statement
        | let_header + statement
    ), (
        lambda h, s: s[1],
        lambda h, s: While(s[1], s[2]),
        lambda h, s: For(s[1][0], s[1][1], s[1][2], s[2]),
    )

    if_statement <= (
        if_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
        + ~elif_statement
        + else_terminal
        + statement
    ), (
        lambda h, s: If(s[3], s[5], s[6], s[8]),
        lambda h, s: If(s[3], s[5], None, s[7]),
    )

    elif_statement <= (
        ~elif_statement
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + statement
    ), (lambda h, s: s[1] + [Elif(s[4], s[6])], lambda h, s: [Elif(s[3], s[5])])

    while_header <= (
        while_terminal + open_parenthesis + expression + close_parenthesis
    ), (lambda h, s: s[3])

    for_header <= (
        for_terminal
        + open_parenthesis
        + identifier
        + ~type_declaration
        + in_terminal
        + expression
        + close_parenthesis
    ), (lambda h, s: [s[3], s[4], s[6]], lambda h, s: [s[3], None, s[5]])

    let_header <= (
        let_terminal
        + identifier
        + ~type_declaration
        + assignment_terminal
        + expression
        + ~multiple_declaration
        + in_terminal
    ), (
        lambda h, s: [VariableDeclaration(s[2], s[5], s[3])] + s[6],
        lambda h, s: [VariableDeclaration(s[2], s[5], s[3])],
        lambda h, s: [VariableDeclaration(s[2], s[4])] + s[5],
        lambda h, s: [VariableDeclaration(s[2], s[4])],
    )

    multiple_declaration <= (
        comma
        + identifier
        + ~type_declaration
        + assignment_terminal
        + expression
        + ~multiple_declaration
    ), (
        lambda h, s: [VariableDeclaration(s[2], s[5], s[3])] + s[6],
        lambda h, s: [VariableDeclaration(s[2], s[5], s[3])],
        lambda h, s: [VariableDeclaration(s[2], s[4])] + s[5],
        lambda h, s: [VariableDeclaration(s[2], s[4])],
    )

    expression <= (
        expression_block | destructive_assignment | or_expression | control_expression
    ), (lambda h, s: s[1])

    control_expression <= (
        if_expression
        | while_header + expression
        | for_header + expression
        | let_header + expression
    ), (
        lambda h, s: s[1],
        lambda h, s: While(s[1], s[2]),
        lambda h, s: For(s[1][0], s[1][1], s[1][2], s[2]),
        lambda h, s: LetVar(s[1], s[2]),
    )

    if_expression <= (
        if_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
        + ~elif_expression
        + else_terminal
        + expression
    ), (lambda h, s: If(s[3], s[5], s[6], s[8]), lambda h, s: If(s[3], s[5], [], s[7]))

    elif_expression <= (
        ~elif_expression
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
    ), (lambda h, s: s[1] + [Elif(s[4], s[6])], lambda h, s: [Elif(s[3], s[5])])

    expression_block <= open_brace + statement_list + close_brace, (lambda h, s: s[2])

    statement_list <= ~statement_list + statement, (
        lambda h, s: s[1] + [s[2]],
        lambda h, s: [s[1]],
    )

    destructive_assignment <= (
        identifier + destructive_assignment_terminal + expression
        | member_access + destructive_assignment_terminal + expression
    ), (
        lambda h, s: DestructiveAssign(s[1], s[3]),
    )

    or_expression <= ~(or_expression + or_terminal) + and_expression, (
        lambda h, s: BinaryExpression(Operator.OR, s[1], s[3]),
        lambda h, s: s[1],
    )

    and_expression <= ~(and_expression + and_terminal) + equality_expression, (
        lambda h, s: BinaryExpression(Operator.AND, s[1], s[3]),
        lambda h, s: s[1],
    )

    equality_expression <= (
        ~(equality_expression + equal) + relational_expression
        | equality_expression + different + relational_expression
    ), (
        lambda h, s: BinaryExpression(Operator.EQ, s[1], s[3]),
        lambda h, s: s[1],
        lambda h, s: BinaryExpression(Operator.NEQ, s[1], s[3]),
    )

    relational_expression <= (
        ~(relational_expression + less) + concat_expression
        | relational_expression + less_equal + concat_expression
        | relational_expression + greater + concat_expression
        | relational_expression + greater_equal + concat_expression
        | relational_expression + is_terminal + identifier
        | relational_expression + as_terminal + identifier
    ), (
        lambda h, s: BinaryExpression(Operator.LT, s[1], s[3]),
        lambda h, s: s[1],
        lambda h, s: BinaryExpression(Operator.LE, s[1], s[3]),
        lambda h, s: BinaryExpression(Operator.GT, s[1], s[3]),
        lambda h, s: BinaryExpression(Operator.GE, s[1], s[3]),
        lambda h, s: BinaryExpression(Operator.IS, s[1], s[3]),
        lambda h, s: BinaryExpression(Operator.AS, s[1], s[3]),
    )

    concat_expression <= (
        ~(concat_expression + concat) + aritmetic_expression
        | concat_expression + double_concat + aritmetic_expression
    ), (
        lambda h, s: BinaryExpression(Operator.CONCAT, s[1], s[3]),
        lambda h, s: s[1],
        lambda h, s: BinaryExpression(Operator.DCONCAT, s[1], s[3]),
    )

    aritmetic_expression <= (
        ~(aritmetic_expression + plus) + mult_expression
        | aritmetic_expression + minus + mult_expression
    ), (
        lambda h, s: BinaryExpression(Operator.ADD, s[1], s[3]),
        lambda h, s: s[1],
        lambda h, s: BinaryExpression(Operator.SUB, s[1], s[3]),
    )

    mult_expression <= (
        ~(mult_expression + multiply) + exponential_expression
        | mult_expression + divide + exponential_expression
        | mult_expression + mod + exponential_expression
    ), (
        lambda h, s: BinaryExpression(Operator.MUL, s[1], s[3]),
        lambda h, s: s[1],
        lambda h, s: BinaryExpression(Operator.DIV, s[1], s[3]),
        lambda h, s: BinaryExpression(Operator.MOD, s[1], s[3]),
    )

    exponential_expression <= (unary_expression + ~(power + exponential_expression)), (
        lambda h, s: BinaryExpression(Operator.POW, s[1], s[3]),
        lambda h, s: s[1],
    )

    unary_expression <= (
        ~plus + primary_expression
        | minus + primary_expression
        | not_operator + primary_expression
    ), (
        lambda h, s: PositiveNode(s[2]),
        lambda h, s: s[1],
        lambda h, s: NegativeNode(s[2]),
        lambda h, s: NotNode(s[2]),
    )

    primary_expression <= (
        literal
        | invocation_expression
        | identifier
        | vector
        | indexed_value
        | member_access
        | open_parenthesis + expression + close_parenthesis
        | instantiation
    ), (
        *[lambda h, s: s[1]] * 6,
        lambda h, s: s[2],
        lambda h, s: s[1],
    )

    invocation_expression <= (
        identifier + open_parenthesis + ~argument_list + close_parenthesis
    ), (lambda h, s: s[1] + s[3], lambda h, s: s[1])

    argument_list <= ~(argument_list + comma) + expression, (
        lambda h, s: s[1] + [s[3]],
        lambda h, s: [s[1]],
    )

    vector <= (
        open_bracket + vector_element + close_bracket
        | open_bracket
        + expression
        + double_pipe
        + identifier
        + in_terminal
        + expression
        + close_bracket
    ), (
        lambda h, s: Vector(s[2], None, None, None),
        lambda h, s: Vector([], s[2], s[4], s[6]),
    )

    vector_element <= ~(vector_element + comma) + expression, (
        lambda h, s: s[1] + [s[3]],
        lambda h, s: [s[1]],
    )

    indexed_value <= (
        primary_expression + open_bracket + primary_expression + close_bracket
    ), (lambda h, s: IndexNode(s[1], s[3]))

    member_access <= (
        primary_expression + dot + identifier
        | primary_expression + dot + invocation_expression
    ), (
        lambda h, s: Call(s[1], s[3], []),
        lambda h, s: Call(s[1], s[3][0], s[3][1]),
    )

    instantiation <= new + invocation_expression, (
        lambda h, s: Instanciate(s[2][0], s[2][1])
    )

    literal <= (number | string | true | false), (lambda h, s: LiteralNode(s[1]),)

    mapping: dict[TokenType, Symbol] = {
        TokenType.NUMBER_LITERAL: number,
        TokenType.NUMBER: number_type,
        TokenType.STRING: string_type,
        TokenType.BOOLEAN: boolean_type,
        TokenType.PI: number,
        TokenType.STRING_LITERAL: string,
        TokenType.IDENTIFIER: identifier,
        TokenType.PLUS: plus,
        TokenType.MINUS: minus,
        TokenType.TIMES: multiply,
        TokenType.DIVIDE: divide,
        TokenType.POWER: power,
        TokenType.MOD: mod,
        TokenType.LEFT_BRACE: open_brace,
        TokenType.RIGHT_BRACE: close_brace,
        TokenType.SEMI_COLON: semicolon,
        TokenType.LEFT_PARENTHESIS: open_parenthesis,
        TokenType.RIGHT_PARENTHESIS: close_parenthesis,
        TokenType.ARROW_OPERATOR: inline,
        TokenType.COMMA: comma,
        TokenType.ASSIGNMENT: assignment_terminal,
        TokenType.DESTRUCTIVE_ASSIGNMENT: destructive_assignment_terminal,
        TokenType.DOT: dot,
        TokenType.COLON: colon,
        TokenType.LEFT_BRACKET: open_bracket,
        TokenType.RIGHT_BRACKET: close_bracket,
        TokenType.DOUBLE_PIPE: double_pipe,
        TokenType.CONCAT_OPERATOR: concat,
        TokenType.DOUBLE_CONCAT_OPERATOR: double_concat,
        TokenType.FUNCTION: function_terminal,
        TokenType.LET: let_terminal,
        TokenType.IN: in_terminal,
        TokenType.IF: if_terminal,
        TokenType.ELIF: elif_terminal,
        TokenType.ELSE: else_terminal,
        TokenType.TRUE_LITERAL: true,
        TokenType.FALSE_LITERAL: false,
        TokenType.WHILE: while_terminal,
        TokenType.FOR: for_terminal,
        TokenType.TYPE: type_terminal,
        TokenType.NEW: new,
        TokenType.INHERITS: inherits,
        TokenType.IS: is_terminal,
        TokenType.AS: as_terminal,
        TokenType.PROTOCOL: protocol,
        TokenType.EXTENDS: extends,
        TokenType.GREATER_THAN: greater,
        TokenType.LESS_THAN: less,
        TokenType.GREATER_THAN_EQUAL: greater_equal,
        TokenType.LESS_THAN_EQUAL: less_equal,
        TokenType.EQUAL: equal,
        TokenType.NOT_EQUAL: different,
        TokenType.AND: and_terminal,
        TokenType.OR: or_terminal,
        TokenType.NOT: not_operator,
        TokenType.EOF: grammar.eof,
    }

    return grammar, mapping
