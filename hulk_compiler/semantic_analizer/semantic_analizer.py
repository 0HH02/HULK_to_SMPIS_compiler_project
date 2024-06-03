from .semantic_type import (
    ObjectType,
    BooleanType,
    NumberType,
    StringType,
    Type,
    Method,
    RangeType,
    OrderedDict,
    UndefinedType,
    UnknownType,
)

from .semantic_exceptions import RedefineException


class Context:
    def __init__(self, types, var, methods, father) -> None:
        self.types = (
            {
                "Object": ObjectType(),
                "Boolean": BooleanType(),
                "Number": NumberType(),
                "String": StringType(),
            }
            if types
            else types
        )
        self.var = [] if var else var
        self.methods = (
            [
                Method("sqrt", ["value"], [NumberType()], NumberType(), -1),
                Method("sin", ["angle"], [NumberType()], NumberType(), -1),
                Method("cos", ["angle"], [NumberType()], NumberType(), -1),
                Method(
                    "log",
                    ["base", "value"],
                    [NumberType(), NumberType()],
                    NumberType(),
                    -1,
                ),
                Method("exp", ["value"], [NumberType()], NumberType(), -1),
                Method("rand", [], [], NumberType(), -1),
                Method("print", ["message"], [StringType()], StringType(), -1),
                Method(
                    "range",
                    ["min", "max"],
                    [NumberType(), NumberType()],
                    RangeType(),
                    -1,
                ),
            ]
            if methods
            else methods
        )
        self.father: Context = None

    def define_type(self, name: str, is_protocol=False) -> bool:
        if name in self.types:
            raise RedefineException("Type", name)
        self.types[name] = Type(name, is_protocol)
        return True

    def define_var(self, name: str) -> bool:
        if name in self.var:
            raise RedefineException("Variable", name)
        self.var.append(name)
        return True

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type, line
    ):
        if name in (method.name for method in self.methods):
            raise RedefineException("Method", name)
        self.methods.append(Method(name, param_names, param_types, return_type, line))
        return True

    def check_type(self, name: str) -> bool:
        return name in self.types

    def check_var(self, name: str) -> bool:
        return name in self.var

    def check_method(self, name: str, params: int):
        for method in self.methods:
            if name in method.name and params == len(method.param_names):
                return True
        return False

    def create_child_context(self) -> "Context":
        return Context(self.types, self.var, self.methods, self)

    # def get_type(self, name: str):
    #     try:
    #         return True, self.types[name]
    #     except KeyError:
    #         return False, f'Type "{name}" is not defined.'

    # def get_method(self, name: str):
    #     try:
    #         return True, next(method for method in self.methods if method.name == name)
    #     except StopIteration:
    #         return False, f'Method "{name}" is not defined.'

    # def update_method(self, name: str, param_types: list, return_type):
    #     try:
    #         method = next(method for method in self.methods if method.name == name)
    #         method.param_types = param_types
    #         method.return_type = return_type
    #     except StopIteration:
    #         return False, f'Method "{name}" is not defined.'

    # def all_methods(self, clean=True):
    #     plain = OrderedDict()
    #     for method in self.methods:
    #         plain[method.name] = (method, self)
    #     return plain.values() if clean else plain

    # def get_lowest_ancestor(self, type_a, type_b):

    #     if type_a in [UnknownType(), UndefinedType()] or type_a.is_protocol:
    #         return type_b

    #     if type_b in [UnknownType(), UndefinedType()] or type_b.is_protocol:
    #         return type_a

    #     while type_a.depth > type_b.depth:
    #         type_a = type_a.parent

    #     while type_b.depth > type_a.depth:
    #         type_b = type_b.parent

    #     while type_b != type_a:
    #         type_a = type_a.parent
    #         type_b = type_b.parent

    #     return type_a

    # def check_inheritance(self, child: Type, parent: Type, args, line):

    #     errors = []

    #     if len(child.params) > 0:

    #         if len(args) != len(parent.params):
    #             errors.append(
    #                 (
    #                     f"{parent.name} expects {len(parent.params)} arguments, "
    #                     f"got {len(args)}",
    #                     line,
    #                 )
    #             )

    #         parent_args = list(parent.params.values())

    #         for i in range(len(parent_args)):
    #             if not parent_args[i] or parent_args[i] == UnknownType():
    #                 parent_args[i] = parent.params_inferred_type[i]

    #         for i in range(len(args)):
    #             if not args[i].conforms_to(parent_args[i]):
    #                 errors.append(
    #                     (
    #                         f"Argument type mismatch, on {parent.name} got {args[i]} "
    #                         f"expected {parent_args[i]}",
    #                         line,
    #                     )
    #                 )

    #     parent_methods = parent.all_methods(False)
    #     child_methods = child.all_methods(False)

    #     for name, (method, _) in child_methods.items():

    #         if name in parent_methods:

    #             base_method = parent_methods[name][0]

    #             if len(base_method.param_types) != len(method.param_types):
    #                 errors.append(
    #                     (
    #                         f"{name} expects {len(base_method.param_types)} parameters, "
    #                         f"got {len(method.param_types)}",
    #                         method.line,
    #                     )
    #                 )

    #             for i in range(len(base_method.param_types)):

    #                 if method.param_types[i] != base_method.param_types[i]:
    #                     errors.append(
    #                         (
    #                             f"Parameter type mismatch, on {method.param_names[i].name} got {method.param_types[i].name} "
    #                             f"expected {base_method.param_types[i].name}",
    #                             method.line,
    #                         )
    #                     )

    #             if method.return_type != base_method.return_type:
    #                 errors.append(
    #                     (
    #                         f"Return type mismatch, on {name} got {method.return_type} "
    #                         f"expected {base_method.return_type}",
    #                         method.line,
    #                     )
    #                 )

    #     return errors

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)
