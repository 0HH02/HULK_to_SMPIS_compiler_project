from ...parser.grammar.grammar import Grammar
from ..token import RegexTokenType
from .regex_ast import (
    LiteralCharNode,
    GroupNode,
    AnyCharNode,
    OrNode,
    EpsilonNode,
    ConcatNode,
    PlusNode,
    RepeatNode,
)

# pylint: disable=expression-not-assigned
# pylint:disable=pointless-statement


def get_regex_grammar():

    regex_grammar = Grammar()

    (
        plus,
        optional,
        caret,
        pipe,
        dot,
        minus,
        lbrace,
        lbracket,
        lpar,
        rpar,
        rbracket,
        rbrace,
        letter,
        number,
        symbol,
    ) = regex_grammar.set_terminals(
        [
            "+",
            "?",
            "^",
            "|",
            "dot",
            "-",
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            "letter",
            "num",
            "symbol",
        ]
    )

    (
        character,
        char_group,
        group,
        expression,
        gen_expression,
        list_expression,
        regex,
        s,
    ) = regex_grammar.set_non_terminals(
        [
            "character",
            "char_group",
            "group",
            "expression",
            "gen_expression",
            "list_expression",
            "regex",
            "s",
        ]
    )

    regex_grammar.set_seed(s)

    s <= (
        regex,
        lambda x: OrNode(x[0]),
    )

    regex <= (
        regex + pipe + list_expression,
        lambda x: x[0] + [ConcatNode(x[2])],
    )
    regex <= (
        list_expression,
        lambda x: [ConcatNode(x[0])],
    )

    list_expression <= (
        ~list_expression + gen_expression,
        (
            lambda x: x[0] + [x[1]],
            lambda x: [x[0]],
        ),
    )

    gen_expression <= (
        expression + plus,
        lambda x: PlusNode(x[0]),
    )
    gen_expression <= (
        expression + optional,
        lambda x: OrNode([x[0], EpsilonNode()]),
    )
    gen_expression <= (
        expression + lbrace + number + rbrace,
        lambda x: RepeatNode(x[0], int(x[2].lex)),
    )
    gen_expression <= (
        expression,
        lambda x: x[0],
    )

    expression <= (
        lpar + regex + rpar,
        lambda x: OrNode(x[1]),
    )
    expression <= (
        lbracket + ~caret + group + rbracket,
        (
            lambda x: GroupNode(x[2], True),
            lambda x: GroupNode(x[1], False),
        ),
    )
    expression <= (
        character,
        lambda x: x[0],
    )
    # expression <= (
    #     dot,
    #     lambda x: AnyCharNode(),
    # )

    group <= (
        ~group + char_group,
        (
            lambda x: x[0] + x[1],
            lambda x: x[0],
        ),
    )

    char_group <= (
        character + minus + character,
        lambda x: [chr(c) for c in range(ord(x[0].value), ord(x[2].value) + 1)],
    )

    char_group <= (
        character,
        lambda x: [x[0].value],
    )

    character <= (
        letter | number | symbol,
        (lambda x: LiteralCharNode(x[0].lex)),
    )

    mapping: dict = {
        RegexTokenType.PLUS: plus,
        RegexTokenType.OR: pipe,
        RegexTokenType.OPTIONAL: optional,
        RegexTokenType.RANGE: minus,
        RegexTokenType.NOT: caret,
        RegexTokenType.LPAREN: lpar,
        RegexTokenType.RPAREN: rpar,
        RegexTokenType.LBRACE: lbrace,
        RegexTokenType.RBRACE: rbrace,
        RegexTokenType.LBRACKET: lbracket,
        RegexTokenType.RBRACKET: rbracket,
        RegexTokenType.LETTER: letter,
        RegexTokenType.SYMBOL: symbol,
        RegexTokenType.NUMBER: number,
        # RegexTokenType.DOT: dot,
        RegexTokenType.EOF: regex_grammar.eof,
    }

    return regex_grammar, mapping
