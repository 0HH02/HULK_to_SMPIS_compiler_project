from .types import (
    Protocol,
    Method,
    IdentifierVar,
    BooleanType,
    ObjectType,
    NumberType,
    RangeType,
)


ITERABLE_PROTOCOL = Protocol(
    "Iterable",
    [
        Method("next", [], BooleanType()),
        Method("current", [], ObjectType()),
    ],
)

SQRT_FUNCTION = Method("sqrt", [IdentifierVar("value", NumberType())], NumberType())
SIN_FUNCTION = Method("sin", [IdentifierVar("angle", NumberType())], NumberType())
COS_FUNCTION = Method("cos", [IdentifierVar("angle", NumberType())], NumberType())
LOG_FUNCTION = Method(
    "log",
    [
        IdentifierVar("value", NumberType()),
        IdentifierVar("base", NumberType()),
    ],
    NumberType(),
)
EXP_FUNCTION = Method("exp", [IdentifierVar("value", NumberType())], NumberType())
RAND_FUNCTION = Method("rand", [], NumberType())
PRINT_FUNCTION = Method("print", [IdentifierVar("message", ObjectType())], ObjectType())
RANGE_FUNCTION = Method(
    "range",
    [
        IdentifierVar("start", NumberType()),
        IdentifierVar("end", NumberType()),
    ],
    RangeType(),
)
