"""
This module contains the types used in the semantic analyzer.
"""


class Method:
    """
    Represents a method in a class.

    Attributes:
        name (str): The name of the method.
        params (list): The parameters of the method.
        return_type: The return type of the method.
    """

    def __init__(self, name: str, params: list["IdentifierVar"], return_type: "Type"):
        self.name: str = name
        self.params: list[IdentifierVar] = params
        self.return_type: Type = return_type
        self.line = -1

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Method)
            and self.name == value.name
            and self.params == value.params
            and self.return_type == value.return_type
        )

    def __str__(self) -> str:
        string = f"method -> {self.name}"
        string += "params :\n"
        for param in self.params:
            string += f"{param}\n"
        string += f"return type : {self.return_type.name}"
        return string

    def __repr__(self) -> str:
        return self.__str__()


class IdentifierVar:
    """
    Represents a param or an atributte in a class.

    Attributes:
        name (str): The name of the variable.
        type: The type of the variable.
    """

    def __init__(self, name: str, var_type: "Type") -> None:
        self.name = name
        self.type: Type = var_type

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, IdentifierVar)
            and self.name == value.name
            and self.type == value.type
        )

    def __str__(self) -> str:
        return f"var -> {self.name}:{self.type.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.name)


class Type:
    """
    Represents a base class for types in the semantic analyzer.
    """

    def __init__(
        self,
        name: str,
        parent: "Type" = None,
        params: list[IdentifierVar] = None,
        attributes: list[IdentifierVar] = None,
        methods: list[Method] = None,
    ) -> None:
        self.name = name
        self.parent: Type | None = parent
        self.params: list[IdentifierVar] = params if params is not None else []
        self.attributes: list[IdentifierVar] = (
            attributes if attributes is not None else []
        )
        self.methods: list[Method] = methods if methods is not None else []

    def __eq__(self, value: object) -> bool:
        return isinstance(value, type(self)) and self.name == value.name

    def get_attribute(self, name: str) -> IdentifierVar | None:
        """
        Retrieves the attribute with the given name.

        Args:
            name (str): The name of the attribute.

        Returns:
            The attribute with the given name.
        """
        if name in self.attributes:
            return self.attributes[name]

        if self.parent is not None:
            return self.parent.get_attribute(name)

        return None

    def get_method(self, name: str):
        """
        Retrieves the method with the given name.

        Args:
            name (str): The name of the method.

        Returns:
            The method with the given name.
        """
        if name in self.methods:
            return self.methods[name]

        if self.parent is not None:
            return self.parent.get_method(name)

        return None

    def conforms_to(self, other) -> bool:
        """
        This method checks if the current type conforms to the other type.
        """
        if isinstance(other, Protocol):
            return other.is_implemented_by(self)

        if self == other:
            return True

        if self.parent is not None:
            if self.parent == other:
                return True
            return self.parent.conforms_to(other)

        return False

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.name)


class Protocol:
    """
    Represents a protocol in the HULK compiler.

    A protocol defines a set of methods that a class can implement.
    """

    def __init__(self, name: str, methods: list[Method] | None = None) -> None:
        self.name: str = name
        self.methods: list[Method] = methods if methods is not None else []

    def get_method(self, name: str):
        """
        Retrieves a method from the protocol.

        Args:
            name (str): The name of the method to retrieve.

        Returns:
            bool: True if the method exists in the protocol, False otherwise.
        """
        return name in self.methods

    def set_method(self, method: "Method"):
        """
        This method sets a method to the protocol.
        """
        if method not in self.methods:
            self.methods.append(method)

    def is_implemented_by(self, type_t: "Type"):
        """
        This method checks if the protocol is implemented by the given type.
        """
        for method in self.methods:
            if not type_t.get_method(method):
                return False

        return True


class UnknownType(Type):
    """
    Represents an unknown type in the semantic analyzer.
    """

    def __init__(self) -> None:
        super().__init__("Unknown")
        self.parent = ObjectType()


class ObjectType(Type):
    """
    Represents an object type in the semantic analyzer.
    """

    def __init__(self, name: str = "Object") -> None:
        super().__init__(name)


class NumberType(ObjectType):
    """
    Represents a number type in the semantic analyzer.
    """

    def __init__(self) -> None:
        super().__init__("Number")
        self.parent = ObjectType()


class StringType(ObjectType):
    """
    Represents a string type in the semantic analyzer.
    """

    def __init__(self) -> None:
        super().__init__("String")
        self.parent = ObjectType()


class BooleanType(ObjectType):
    """
    Represents a boolean type in the semantic analyzer.
    """

    def __init__(self) -> None:
        super().__init__("Boolean")
        self.parent = ObjectType()


class RangeType(ObjectType):
    """
    Represents a range type.

    Attributes:
        parent (ObjectType): The parent object type.
        methods (dict): A dictionary of methods available for the range type.
        attributes (dict): A dictionary of attributes associated with the range type.
        params (dict): A dictionary of parameters required for the range type.

    Methods:
        __init__(self): Initializes a new instance of the RangeType class.
    """

    def __init__(self, items_type: Type = UnknownType()) -> None:
        super().__init__("Range")
        self.items_type: Type = items_type if items_type is not None else UnknownType()
        self.parent = ObjectType()
        self.methods = {
            "current": Method("current", [], NumberType()),
            "next": Method("next", [], NumberType()),
        }
        self.attributes = {
            "min": IdentifierVar("min", NumberType()),
            "max": IdentifierVar("max", NumberType()),
        }

        self.params = {
            "min": IdentifierVar("min", NumberType()),
            "max": IdentifierVar("max", NumberType()),
        }
