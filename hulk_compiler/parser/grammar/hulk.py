from grammar.grammar import Grammar, Epsilon
from core.classes.token import TokenType


def get_hulk_grammar() -> Grammar:
    grammar = Grammar()

    program = grammar.non_terminal("program", True)
    eof = grammar.terminal("$")

    # epsilon = grammar.terminal("epsilon")

    grammar.Epsilon = Epsilon(grammar)
    epsilon = grammar.Epsilon
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
        arguments,
        argument_list,
        destructive_assignment,
        member_access,
        optional_type_declaration,
        multiple_declaration,
        arguments_definition,
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
        type_element,
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
    ) = grammar.non_terminals(
        """define_statement statement type_definition function_definition protocol_definition expression_block
        statement_list if_expression invocation_expression expression aritmetic_expression 
        mult_expression exponential_expression unary_expression primary_expression literal vector indexed_value arguments 
        argument_list destructive_assignment member_access optional_type_declaration multiple_declaration 
        arguments_definition argument_list_definition or_expression and_expression equality_expression 
        relational_expression if_statement elif_statement attribute_definition type_inherits 
        inherits_declaration type_body type_element type_arguments instantiation extends_definition 
        protocol_body protocol_arguments_definition extends_multiple_identifier protocol_multiple_arguments_definition 
        vector_element head_program elif_expression concat_expression control_statement 
        while_header for_header let_header control_expression inline_function block_function type_declaration"""
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
        "{ } ; + - * / ^ % ( ) , @ @@ . = := => : ! | & == != < <= > >= [ ] ||"
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
        "identifier let in function number string true false is as if elif else while for type inherits new protocol extends number_type string_type boolean_type"
    )

    program %= head_program + statement
    program %= statement

    head_program %= define_statement
    head_program %= head_program + define_statement

    define_statement %= function_terminal + function_definition
    define_statement %= type_definition
    define_statement %= protocol_definition

    type_definition %= (
        type_terminal
        + identifier
        + type_arguments
        + type_inherits
        + open_brace
        + type_body
        + close_brace
    )

    type_body %= type_body + attribute_definition
    type_body %= type_body + function_definition
    type_body %= epsilon

    attribute_definition %= (
        identifier
        + optional_type_declaration
        + assignment_terminal
        + expression
        + semicolon
    )

    type_arguments %= open_parenthesis + arguments_definition + close_parenthesis
    type_arguments %= epsilon

    type_inherits %= inherits + identifier + inherits_declaration
    type_inherits %= epsilon

    type_declaration %= colon + identifier
    type_declaration %= colon + number_type
    type_declaration %= colon + string_type
    type_declaration %= colon + boolean_type

    optional_type_declaration %= type_declaration
    optional_type_declaration %= epsilon

    inherits_declaration %= open_parenthesis + arguments + close_parenthesis
    inherits_declaration %= epsilon

    function_definition %= inline_function
    function_definition %= block_function

    inline_function %= (
        identifier
        + open_parenthesis
        + arguments_definition
        + close_parenthesis
        + optional_type_declaration
        + inline
        + statement
    )
    block_function %= (
        identifier
        + open_parenthesis
        + arguments_definition
        + close_parenthesis
        + optional_type_declaration
        + expression_block
    )

    arguments_definition %= argument_list_definition
    arguments_definition %= epsilon

    argument_list_definition %= identifier + optional_type_declaration
    argument_list_definition %= (
        argument_list_definition + comma + identifier + optional_type_declaration
    )

    protocol_definition %= (
        protocol
        + identifier
        + extends_definition
        + open_brace
        + protocol_body
        + close_brace
    )

    extends_definition %= extends + identifier + extends_multiple_identifier
    extends_definition %= epsilon

    extends_multiple_identifier %= comma + identifier + extends_multiple_identifier
    extends_multiple_identifier %= epsilon

    protocol_body %= (
        protocol_body
        + identifier
        + open_parenthesis
        + protocol_arguments_definition
        + close_parenthesis
        + type_declaration
        + semicolon
    )
    protocol_body %= epsilon

    protocol_arguments_definition %= (
        identifier + type_declaration + protocol_multiple_arguments_definition
    )
    protocol_arguments_definition %= epsilon

    protocol_multiple_arguments_definition %= (
        comma + identifier + type_declaration + protocol_multiple_arguments_definition
    )
    protocol_multiple_arguments_definition %= epsilon

    statement %= expression_block
    statement %= expression_block + semicolon
    statement %= or_expression + semicolon
    statement %= destructive_assignment + semicolon
    statement %= control_statement

    control_statement %= if_statement
    control_statement %= while_header + statement
    control_statement %= for_header + statement
    control_statement %= let_header + statement

    if_statement %= (
        if_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
        + elif_statement
        + else_terminal
        + statement
    )
    elif_statement %= (
        elif_statement
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + statement
    )
    elif_statement %= epsilon

    while_header %= while_terminal + open_parenthesis + expression + close_parenthesis

    for_header %= (
        for_terminal
        + open_parenthesis
        + identifier
        + optional_type_declaration
        + in_terminal
        + expression
        + close_parenthesis
    )

    let_header %= (
        let_terminal
        + identifier
        + optional_type_declaration
        + assignment_terminal
        + expression
        + multiple_declaration
        + in_terminal
    )

    multiple_declaration %= (
        comma
        + identifier
        + optional_type_declaration
        + assignment_terminal
        + expression
        + multiple_declaration
    )
    multiple_declaration %= epsilon

    expression %= expression_block
    expression %= destructive_assignment
    expression %= or_expression
    expression %= control_expression

    control_expression %= if_expression
    control_expression %= while_header + expression
    control_expression %= for_header + expression
    control_expression %= let_header + expression

    if_expression %= (
        if_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
        + elif_expression
        + else_terminal
        + expression
    )
    elif_expression %= (
        elif_expression
        + elif_terminal
        + open_parenthesis
        + expression
        + close_parenthesis
        + expression
    )
    elif_expression %= epsilon

    expression_block %= open_brace + statement_list + close_brace
    statement_list %= statement
    statement_list %= statement_list + statement

    destructive_assignment %= identifier + destructive_assignment_terminal + expression
    destructive_assignment %= (
        member_access + destructive_assignment_terminal + expression
    )

    or_expression %= or_expression + or_terminal + and_expression
    or_expression %= and_expression

    and_expression %= and_expression + and_terminal + equality_expression
    and_expression %= equality_expression

    equality_expression %= equality_expression + equal + relational_expression
    equality_expression %= equality_expression + different + relational_expression

    equality_expression %= relational_expression

    relational_expression %= concat_expression
    relational_expression %= relational_expression + less + concat_expression
    relational_expression %= relational_expression + less_equal + concat_expression
    relational_expression %= relational_expression + greater + concat_expression
    relational_expression %= relational_expression + greater_equal + concat_expression

    relational_expression %= relational_expression + is_terminal + identifier
    relational_expression %= relational_expression + as_terminal + identifier

    concat_expression %= concat_expression + concat + aritmetic_expression
    concat_expression %= concat_expression + double_concat + aritmetic_expression
    concat_expression %= aritmetic_expression

    aritmetic_expression %= aritmetic_expression + plus + mult_expression
    aritmetic_expression %= aritmetic_expression + minus + mult_expression
    aritmetic_expression %= mult_expression

    mult_expression %= mult_expression + multiply + exponential_expression
    mult_expression %= mult_expression + divide + exponential_expression
    mult_expression %= mult_expression + mod + exponential_expression
    mult_expression %= exponential_expression

    exponential_expression %= unary_expression + power + exponential_expression
    exponential_expression %= unary_expression

    unary_expression %= plus + primary_expression
    unary_expression %= minus + primary_expression
    unary_expression %= not_operator + primary_expression
    unary_expression %= primary_expression

    primary_expression %= literal
    primary_expression %= invocation_expression
    primary_expression %= identifier
    primary_expression %= vector
    primary_expression %= indexed_value
    primary_expression %= member_access
    primary_expression %= open_parenthesis + expression + close_parenthesis
    primary_expression %= instantiation

    invocation_expression %= (
        identifier + open_parenthesis + arguments + close_parenthesis
    )
    arguments %= argument_list
    arguments %= epsilon
    argument_list %= argument_list + comma + expression
    argument_list %= expression

    vector %= open_bracket + vector_element + close_bracket
    vector %= (
        open_bracket
        + expression
        + double_pipe
        + identifier
        + in_terminal
        + expression
        + close_bracket
    )

    vector_element %= expression
    vector_element %= vector_element + comma + expression

    indexed_value %= (
        primary_expression + open_bracket + primary_expression + close_bracket
    )

    member_access %= primary_expression + dot + identifier
    member_access %= primary_expression + dot + invocation_expression

    instantiation %= new + invocation_expression

    literal %= number
    literal %= string
    literal %= true
    literal %= false

    mapping = {
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
        TokenType.EOF: eof,
    }

    return grammar, mapping
