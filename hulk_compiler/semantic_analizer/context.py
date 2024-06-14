"""
"""

from .types import (
    StringType,
    ObjectType,
    BooleanType,
    NumberType,
    UnknownType,
    Type,
    Method,
    RangeType,
    IdentifierVar,
    Protocol,
)
from .semantic_exceptions import RedefineException, NotDeclaredVariableException


class Context:
    def __init__(self, father: "Context" = None) -> None:
        """
        Initializes a new instance of the Context class.
        This class represents the context of a AST and it is use to store
        the methods, variables and types declared in the program.

        Args:
            father (Context, optional): The parent context. Defaults to None.
        """
        self.types: dict[str, Type] = {
            "Unknown": UnknownType(),
            "Object": ObjectType(),
            "Boolean": BooleanType(),
            "Number": NumberType(),
            "String": StringType(),
            "Range": RangeType(),
        }
        self.protocols: list[Protocol] = [
            Protocol(
                "Iterable",
                [
                    Method("next", [], BooleanType()),
                    Method(
                        "current",
                        [],
                        ObjectType(),
                    ),
                ],
            ),
        ]
        self.variables: list[IdentifierVar] = []
        self.methods: list[Method] = [
            Method("sqrt", [IdentifierVar("value", NumberType())], NumberType()),
            Method("sin", [IdentifierVar("angle", NumberType())], NumberType()),
            Method("cos", [IdentifierVar("angle", NumberType())], NumberType()),
            Method(
                "log",
                [
                    IdentifierVar("value", NumberType()),
                    IdentifierVar("base", NumberType()),
                ],
                NumberType(),
            ),
            Method("exp", [IdentifierVar("value", NumberType())], NumberType()),
            Method("rand", [], NumberType()),
            Method("print", [IdentifierVar("message", ObjectType())], StringType()),
            Method(
                "range",
                [
                    IdentifierVar("start", NumberType()),
                    IdentifierVar("end", NumberType()),
                ],
                RangeType(),
            ),
        ]
        self.father: Context = father

    def define_type(self, type_t: Type):
        """
        Defines a new type in the context.

        Args:
            name (str): The name of the type to define.

        Raises:
            RedefineException: If the type with the given name already exists in the context.
        """
        if self.check_type(type_t.name):
            raise RedefineException("Type", type_t.name)
        self.types[type_t.name] = type_t

    def define_protocol(self, name: str, methods: list[Method]):
        """
        Defines a new protocol in the context.

        Args:
            name (str): The name of the protocol to define.
            methods (list[Method]): The list of methods the protocol should have.

        Raises:
            RedefineException: If the protocol with the given name already exists in the context.
        """
        if self.check_type(name):
            raise RedefineException("Protocol", name)

        new_protocol = Protocol(name)
        for method in methods:
            new_protocol.set_method(method)

        self.protocols.append(new_protocol)

    def define_variable(self, identifier: IdentifierVar) -> None:
        """
        Defines a variable in the context.

        Args:
            name (str): The name of the variable to define.

        Raises:
            RedefineException: If the variable is already defined in the context.
        """

        if self.check_var(identifier.name):
            raise RedefineException("Variable", identifier.name)

        self.variables.append(identifier)

    def define_method(self, name: str, params: list[IdentifierVar], return_type):
        """
        Defines a method in the context.

        Args:
            name (str): The name of the method.
            params (list[Variable]): The list of method parameters.
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

        if name in self.types or name in self.protocols:
            return True

        if self.father:
            return self.father.check_type(name)

        return False

    def check_var(self, var_name: str) -> bool:
        """
        Check if a variable with the given name exists in the
        current context or any parent contexts.

        Args:
            name (str): The name of the variable to check.

        Returns:
            bool: True if the variable exists, False otherwise.
        """

        if var_name in [var.name for var in self.variables]:
            return True

        if self.father:
            return self.father.check_var(var_name)

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

    def get_var_type(self, name: str) -> Type:
        """
        Retrieves a type from the context.

        Args:
            name (str): The name of the type to retrieve.

        Returns:
            The type with the given name.
        """
        try:
            return next(var.type for var in self.variables if var.name == name)
        except StopIteration as e:
            raise NotDeclaredVariableException(name) from e

    def get_method(self, name: str, params: int):
        """
        Retrieves a method from the context.

        Args:
            name (str): The name of the method to retrieve.
            params (int): The number of parameters the method should have.

        Returns:
            The method with the given name and number of parameters.
        """
        for method in self.methods:
            if method.name == name and len(method.params) == params:
                return method

        if self.father:
            return self.father.get_method(name, params)

        raise NotDeclaredVariableException(name)

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)
