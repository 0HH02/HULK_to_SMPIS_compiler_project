"""
    This module contains the grammar for the HULK programming language.
"""

from .grammar import Grammar

# pylint: disable=pointless-statement


# Rest of the code...
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
            "{ }",
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

    program <= ~head_program + statement

    head_program <= ~head_program + define_statement

    define_statement <= (
        function_terminal + function_definition | type_definition | protocol_definition
    )

    type_definition <= (
        type_terminal
        + identifier
        + type_arguments
        + ~type_inherits
        + open_brace
        + ~type_body
        + close_brace
    )

    type_body <= ~type_body + attribute_definition | ~type_body + function_definition

    attribute_definition <= (
        identifier + ~type_declaration + assignment_terminal + expression + semicolon
    )

    type_arguments <= open_parenthesis + ~argument_list_definition + close_parenthesis

    type_inherits <= inherits + identifier + ~inherits_declaration

    type_declaration <= (
        colon + identifier
        | colon + number_type
        | colon + string_type
        | colon + boolean_type
    )

    inherits_declaration <= open_parenthesis + ~argument_list + close_parenthesis

    function_definition <= inline_function | block_function

    inline_function <= (
        identifier
        + open_parenthesis
        + ~argument_list_definition
        + close_parenthesis
        + ~type_declaration
        + inline
        + statement
    )

    block_function <= (
        identifier
        + open_parenthesis
        + ~argument_list_definition
        + close_parenthesis
        + ~type_declaration
        + expression_block
    )

    argument_list_definition <= (
        ~(argument_list_definition + comma) + identifier + ~type_declaration
    )

    protocol_definition <= (
        protocol
        + identifier
        + ~extends_definition
        + open_brace
        + ~protocol_body
        + close_brace
    )

    extends_definition <= extends + identifier + ~extends_multiple_identifier

    extends_multiple_identifier <= comma + identifier + ~extends_multiple_identifier

    protocol_body <= (
        ~protocol_body
        + identifier
        + open_parenthesis
        + ~protocol_arguments_definition
        + close_parenthesis
        + type_declaration
        + semicolon
    )

    protocol_arguments_definition <= (
        identifier + type_declaration + ~protocol_multiple_arguments_definition
    )

    protocol_multiple_arguments_definition <= (
        comma + identifier + type_declaration + ~protocol_multiple_arguments_definition
    )

    statement <= (
        expression_block + ~semicolon
        | or_expression + semicolon
        | destructive_assignment + semicolon
        | control_statement
    )

    control_statement <= (
        if_statement
        | while_header + statement
        | for_header + statement
        | let_header + statement
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
    )
    elif_statement <= (
        ~elif_statement
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + statement
    )

    while_header <= while_terminal + open_parenthesis + expression + close_parenthesis

    for_header <= (
        for_terminal
        + open_parenthesis
        + identifier
        + ~type_declaration
        + in_terminal
        + expression
        + close_parenthesis
    )

    let_header <= (
        let_terminal
        + identifier
        + ~type_declaration
        + assignment_terminal
        + expression
        + ~multiple_declaration
        + in_terminal
    )

    multiple_declaration <= (
        comma
        + identifier
        + ~type_declaration
        + assignment_terminal
        + expression
        + ~multiple_declaration
    )

    expression <= (
        expression_block | destructive_assignment | or_expression | control_expression
    )

    control_expression <= (
        if_expression
        | while_header + expression
        | for_header + expression
        | let_header + expression
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
    )

    elif_expression <= (
        ~elif_expression
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
    )

    expression_block <= open_brace + statement_list + close_brace

    statement_list <= ~statement_list + statement

    destructive_assignment <= (
        identifier + destructive_assignment_terminal + expression
        | member_access + destructive_assignment_terminal + expression
    )

    or_expression <= ~(or_expression + or_terminal) + and_expression

    and_expression <= ~(and_expression + and_terminal) + equality_expression

    equality_expression <= (
        ~(equality_expression + equal) + relational_expression
        | equality_expression + different + relational_expression
    )

    relational_expression <= (
        ~(relational_expression + less) + concat_expression
        | relational_expression + less_equal + concat_expression
        | relational_expression + greater + concat_expression
        | relational_expression + greater_equal + concat_expression
        | relational_expression + is_terminal + identifier
        | relational_expression + as_terminal + identifier
    )

    concat_expression <= (
        ~(concat_expression + concat) + aritmetic_expression
        | concat_expression + double_concat + aritmetic_expression
    )

    aritmetic_expression <= (
        ~(aritmetic_expression + plus) + mult_expression
        | aritmetic_expression + minus + mult_expression
    )

    mult_expression <= (
        ~(mult_expression + multiply) + exponential_expression
        | mult_expression + divide + exponential_expression
        | mult_expression + mod + exponential_expression
    )

    exponential_expression <= unary_expression + ~(power + exponential_expression)

    unary_expression <= (
        ~plus + primary_expression
        | minus + primary_expression
        | not_operator + primary_expression
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
    )

    invocation_expression <= (
        identifier + open_parenthesis + ~argument_list + close_parenthesis
    )

    argument_list <= ~(argument_list + comma) + expression

    vector <= (
        open_bracket + vector_element + close_bracket
        | open_bracket
        + expression
        + double_pipe
        + identifier
        + in_terminal
        + expression
        + close_bracket
    )

    vector_element <= ~(vector_element + comma) + expression

    indexed_value <= (
        primary_expression + open_bracket + primary_expression + close_bracket
    )

    member_access <= (
        primary_expression + dot + identifier
        | primary_expression + dot + invocation_expression
    )

    instantiation <= new + invocation_expression

    literal <= number | string | true | false

    return grammar
