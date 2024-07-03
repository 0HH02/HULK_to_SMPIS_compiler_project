"""
This module contains the types used in the semantic analyzer.
"""


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
        return isinstance(value, IdentifierVar) and self.name == value.name

    def __str__(self) -> str:
        return f"var -> {self.name}: {self.type.name}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.name)


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

    def get_param(self, name: str) -> IdentifierVar | None:

        for param in self.params:
            if param.name == name:
                return param

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, Method)
            and self.name == value.name
            and self.params == value.params
            and self.return_type == value.return_type
        )

    def __str__(self) -> str:
        string = f"method -> {self.name}"
        string += "\nparams :\n" + "{"
        for param in self.params:
            string += f"\n  {param}"
        string += "\n}\n" f"return type : {self.return_type.name}\n"
        return string

    def __repr__(self) -> str:
        return self.__str__()


class Type:
    """
    Represents a base class for types in the semantic analyzer.
    """

    def __init__(
        self,
        name: str,
        parent: "Type" = None,
        params: list[IdentifierVar] = None,
        attributes: dict[str, IdentifierVar] = None,
        methods: dict[str, Method] = None,
    ) -> None:
        self.name: str = name
        self.parent: Type | None = parent
        self.params: list[IdentifierVar] = params if params else []
        self.attributes: dict[str, IdentifierVar] = attributes if attributes else {}
        self.methods: dict[str, Method] = methods if methods else {}

    @staticmethod
    def get_lower_ancestor(types: list["Type"]) -> "Type":
        """
        This method returns the lower ancestor of the given types.
        """
        lower_ancestor = types[0]

        for type_t in types[1:]:
            lower_ancestor = Type.__get_lower_ancestor(lower_ancestor, type_t)

        return lower_ancestor

    @staticmethod
    def __get_lower_ancestor(type_1: "Type", type_2: "Type"):
        """
        This method returns the lower ancestor of the two types.
        """
        if type_1 == type_2:
            return type_1

        if type_1.conforms_to(type_2):
            return type_2

        if type_2.conforms_to(type_1):
            return type_1

        if type_1.parent:
            return Type.__get_lower_ancestor(type_1.parent, type_2)

        if type_2.parent:
            return Type.__get_lower_ancestor(type_1, type_2.parent)

        return ObjectType()

    def __eq__(self, value: object) -> bool:
        return isinstance(value, type(self)) and self.name == value.name

    def get_param(self, name: str) -> IdentifierVar | None:

        for param in self.params:
            if param.name == name:
                return param

    def set_param(self, param: IdentifierVar):
        self.params.append(param)

    def set_parent(self, type_t: "Type"):
        self.parent = type_t

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

        if self.parent:
            return self.parent.get_attribute(name)

        return None

    def set_attribute(self, attr: IdentifierVar):
        self.attributes[attr.name] = attr

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

        if self.parent:
            return self.parent.get_method(name)

        return None

    def set_method(self, method: Method):
        self.methods[method.name] = method

    def conforms_to(self, other) -> bool:
        """
        This method checks if the current type conforms to the other type.
        """
        if other is UnknownType():
            return True

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
        self.methods: dict[str, Method] = (
            {method.name: method for method in methods} if methods is not None else {}
        )

    def get_method(self, name: str):
        """
        Retrieves a method from the protocol.

        Args:
            name (str): The name of the method to retrieve.

        Returns:
            bool: True if the method exists in the protocol, False otherwise.
        """
        try:
            return self.methods[name]
        except KeyError:
            return None

    def set_method(self, method: "Method"):
        """
        This method sets a method to the protocol.
        """
        if method.name not in self.methods:
            self.methods[method.name] = method

    def is_implemented_by(self, type_t: "Type"):
        """
        This method checks if the protocol is implemented by the given type.
        """
        for method in self.methods.values():
            type_method: Method | None = type_t.get_method(method.name)

            if not type_method:
                return False

            if not type_method.return_type.conforms_to(method.return_type):
                return False

            if len(method.params) != len(type_method.params):
                return False

            for i, param in enumerate(method.params):
                if not param.type.conforms_to(type_method.params[i]):
                    return False

        return True

    def __str__(self) -> str:
        return (
            f"Protocol {self.name}: "
            + "{\n  "
            + "\n".join([m.__str__() for m in self.methods.values()])
            + "\n}\n"
        )

    def __repr__(self) -> str:
        return self.__str__()


class UnknownType(Type):
    """
    Represents an unknown type in the semantic analyzer.
    """

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("Unknown")

        return cls._instance


class ObjectType(Type):
    """
    Represents an object type in the semantic analyzer.
    """

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("Object")

        return cls._instance


class NumberType(Type):
    """
    Represents a number type in the semantic analyzer.
    """

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("Number", ObjectType())

        return cls._instance


class StringType(Type):
    """
    Represents a string type in the semantic analyzer.
    """

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("String", ObjectType())

        return cls._instance


class BooleanType(Type):
    """
    Represents a boolean type in the semantic analyzer.
    """

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("Boolean", ObjectType())

        return cls._instance


class RangeType(Type):
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

    _instance = None

    def __new__(cls) -> Type:
        if not cls._instance:
            cls._instance = Type("Range", ObjectType())
            cls._instance.parent = ObjectType()
            cls._instance.methods = {
                "current": Method("current", [], NumberType()),
                "next": Method("next", [], BooleanType()),
            }
            cls._instance.attributes = {
                "min": IdentifierVar("min", NumberType()),
                "max": IdentifierVar("max", NumberType()),
                "current": IdentifierVar("current", NumberType()),
            }
            cls._instance._params = [
                IdentifierVar("min", NumberType()),
                IdentifierVar("max", NumberType()),
            ]
        return cls._instance


class VectorType(Type):
    """
    Represents a vector type.

    Args:
        items_type (Type): The type of the items in the vector.
    """

    def __init__(self, items_type: Type = UnknownType()) -> None:
        super().__init__("Vector", ObjectType())
        self.methods = {
            "current": Method("current", [], items_type),
            "next": Method("next", [], BooleanType()),
            "size": Method("size", [], NumberType()),
        }
