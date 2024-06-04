"""
"""

from .types import (
    StringType,
    ObjectType,
    BooleanType,
    NumberType,
    Type,
    Method,
    RangeType,
    Identifier,
)
from .semantic_exceptions import RedefineException


class Context:
    def __init__(self, father: "Context" = None) -> None:
        self.types = {
            "Object": ObjectType(),
            "Boolean": BooleanType(),
            "Number": NumberType(),
            "String": StringType(),
        }
        self.var = []
        self.methods = [
            Method("sqrt", [Identifier("value", NumberType())], NumberType()),
            Method("sin", [Identifier("angle", NumberType())], NumberType()),
            Method("cos", [Identifier("angle", NumberType())], NumberType()),
            Method(
                "log",
                [
                    Identifier("value", NumberType()),
                    Identifier("base", NumberType()),
                ],
                NumberType(),
            ),
            Method("exp", [Identifier("value", NumberType())], NumberType()),
            Method("rand", [], NumberType()),
            Method("print", [Identifier("message", StringType)], StringType()),
            Method(
                "range",
                [
                    Identifier("start", NumberType()),
                    Identifier("end", NumberType()),
                ],
                RangeType(),
            ),
        ]
        self.father: Context = father

    def define_type(self, name: str):
        """
        Defines a new type in the context.

        Args:
            name (str): The name of the type to define.

        Raises:
            RedefineException: If the type with the given name already exists in the context.
        """
        if self.check_type(name):
            raise RedefineException("Type", name)
        self.types[name] = Type(name)

    def define_var(self, name: str) -> None:
        """
        Defines a variable in the context.

        Args:
            name (str): The name of the variable to define.

        Raises:
            RedefineException: If the variable is already defined in the context.
        """

        if self.check_var(name):
            raise RedefineException("Variable", name)
        self.var.append(name)

    def define_method(self, name: str, params: list[Identifier], return_type):
        """
        Defines a method in the context.

        Args:
            name (str): The name of the method.
            params (list[Identifier]): The list of method parameters.
            return_type: The return type of the method.

        Raises:
            RedefineException: If a method with the same name and number
            of parameters already exists.
        """

        if self.check_method(name, len(params)):
            raise RedefineException("Method", name)

        self.methods.append(Method(name, params, return_type))

    def check_type(self, name: str) -> bool:
        """
        Check if a type with the given name exists in the current context or any parent contexts.

        Args:
            name (str): The name of the type to check.

        Returns:
            bool: True if the type exists, False otherwise.
        """

        if name in self.types:
            return True

        if self.father:
            return self.father.check_type(name)

        return False

    def check_var(self, name: str) -> bool:
        """
        Check if a variable with the given name exists in the
        current context or any parent contexts.

        Args:
            name (str): The name of the variable to check.

        Returns:
            bool: True if the variable exists, False otherwise.
        """

        if name in self.var:
            return True

        if self.father:
            return self.father.check_var(name)

        return False

    def check_method(self, name: str, params: int):
        """
        Check if a method with the given name and number of parameters
        exists in the current context.

        Args:
            name (str): The name of the method to check.
            params (int): The number of parameters the method should have.

        Returns:
            bool: True if a method with the given name and number
            of parameters exists, False otherwise.
        """

        for method in self.methods:
            if method.name == name and len(method.params) == params:
                return True

        if self.father:
            return self.father.check_method(name, params)

        return False

    def create_child_context(self) -> "Context":
        """
        Creates a new child context based on the current context.

        Returns:
            A new instance of the Context class, representing the child context.
        """
        return Context(self)

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
