"""
"""

from hulk_compiler.semantic_analizer.hulk_built_in import (
    ITERABLE_PROTOCOL,
    SIN_FUNCTION,
    SQRT_FUNCTION,
    COS_FUNCTION,
    LOG_FUNCTION,
    EXP_FUNCTION,
    RAND_FUNCTION,
    PRINT_FUNCTION,
    RANGE_FUNCTION,
)

from hulk_compiler.semantic_analizer.types import (
    StringType,
    ObjectType,
    BooleanType,
    NumberType,
    RangeType,
    VectorType,
    UnknownType,
    Type,
    Method,
    IdentifierVar,
    Protocol,
)
from hulk_compiler.semantic_analizer.semantic_exceptions import RedefineException


class Context:
    """
    Represents the context of an Abstract Syntax Tree (AST) and is used to store
    the methods, variables, and types declared in the program.
    """

    def __init__(self, father: "Context" = None) -> None:
        """
        Initializes a new instance of the Context class.
        This class represents the context of a AST and it is use to store
        the methods, variables and types declared in the program.

        Args:
            father (Context, optional): The parent context. Defaults to None.
        """
        self._types: dict[str, Type] = {}
        self._protocols: dict[str, Protocol] = {}
        self._variables: dict[str, str] = {}
        # self._variablesInt: dict[str, int] = {}
        self._methods: dict[str, str] = {}
        self._father: Context = father

    def define_built_ins(self):
        """
        Defines the built-in types, protocols, and methods in the context.
        """
        self.define_type(StringType())
        self.define_type(ObjectType())
        self.define_type(BooleanType())
        self.define_type(NumberType())
        self.define_type(UnknownType())
        self.define_type(RangeType())
        self.define_type(VectorType())

        self.define_protocol(ITERABLE_PROTOCOL)

        # self.define_method(SIN_FUNCTION)
        # self.define_method(SQRT_FUNCTION)
        # self.define_method(COS_FUNCTION)
        # self.define_method(LOG_FUNCTION)
        # self.define_method(EXP_FUNCTION)
        # self.define_method(RAND_FUNCTION)
        # self.define_method(PRINT_FUNCTION)
        # self.define_method(RANGE_FUNCTION)

    @property
    def iter_protocol(self) -> Protocol:
        """
        Returns the protocol for iterating over elements in the context.

        Returns:
            Protocol: The protocol for iterating over elements.
        """
        return self.get_protocol(ITERABLE_PROTOCOL.name)

    def define_type(self, type_t: Type):
        """
        Defines a new type in the context.

        Args:
            name (str): The name of the type to define.

        Raises:
            RedefineException: If the type with the given name already exists in the context.
        """
        self._types[type_t.name] = type_t

    def define_protocol(self, protocol: Protocol):
        """
        Defines a new protocol in the context.

        Args:
            name (str): The name of the protocol to define.
            methods (list[Method]): The list of methods the protocol should have.

        Raises:
            RedefineException: If the protocol with the given name already exists in the context.
        """
        if self.get_protocol(protocol.name):
            raise RedefineException("Protocol", protocol.name)

        self._protocols[protocol.name] = protocol

    def define_variable(self, var: str, reference_name: str) -> None:
        """
        Defines a variable in the context.

        Args:
            name (str): The name of the variable to define.

        Raises:
            RedefineException: If the variable is already defined in the context.
        """

        self._variables[var] = reference_name

    def define_method(self, function_name: str, function_reference: str, params: int):
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

        self._methods[(function_name, params)] = function_reference

    def get_var_type(self, name: str) -> Type | None:
        """
        Retrieves a type from the context.

        Args:
            name (str): The name of the type to retrieve.

        Returns:
            The type with the given name.
        """
        try:
            return self._variables[name].type

        except KeyError:
            if self._father:
                return self._father.get_var_type(name)

            return None

    def get_var(self, name: str) -> str | None:
        """
        Retrieves a variable from the context.

        Args:
            name (str): The name of the variable to retrieve.

        Returns:
            The variable with the given name.
        """
        try:
            return self._variables[name]

        except KeyError:
            if self._father:
                return self._father.get_var(name)

            return None

    def get_method(self, name: str, params: int) -> str:
        """
        Retrieves a method from the context.

        Args:
            name (str): The name of the method to retrieve.
            params (int): The number of parameters the method should have.

        Returns:
            The method with the given name and number of parameters.
        """
        try:
            return self._methods[(name, params)]
        except KeyError:
            if self._father:
                return self._father.get_method(name, params)

    def get_type(self, name: str) -> Type | None:
        """
        Retrieves a type from the context.

        Args:
            name (str): The name of the type to retrieve.

        Returns:
            The type with the given name.
        """
        try:
            return self._types[name]
        except KeyError:
            if self._father:
                return self._father.get_type(name)
            return None

    def get_protocol(self, name: str) -> Protocol | None:
        """
        Retrieves a protocol from the context.
        Args:
            name (str): The name of the protocol to retrieve.
        Returns:
            The protocol with the given name.
        """
        try:
            return self._protocols[name]
        except KeyError:
            if self._father:
                return self._father.get_protocol(name)
            return None

    def create_child_context(self) -> "Context":
        """
        Creates a new child context based on the current context.

        Returns:
            A new instance of the Context class, representing the child context and this context
            as his father.
        """
        return Context(self)

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self._types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)
