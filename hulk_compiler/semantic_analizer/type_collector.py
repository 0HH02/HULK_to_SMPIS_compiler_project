"""
    This Module Contains the Type Collector Visitor classes.
    Each one represent a tour for the AST with different tasks
"""

from multipledispatch import dispatch
from .types import (
    Method,
    IdentifierVar,
    UnknownType,
    Protocol,
    Type,
    ObjectType,
    StringType,
    BooleanType,
    NumberType,
)
from .context import Context
from ..parser.ast.ast import (
    Program,
    TypeDeclaration,
    ProtocolDeclaration,
    FunctionDeclaration,
)
from ..core.i_visitor import IVisitor

# pylint: disable=function-redefined
# pylint: disable=arguments-differ
# pylint: disable=line-too-long


def define_type(name: str | None, context: Context) -> Type | None:
    return context.get_type(name) if name else UnknownType()


class TypeCollector(IVisitor):
    """ """

    @staticmethod
    @dispatch(Program, Context)
    def collect(node: Program, context: Context):
        for class_def in node.defines:
            TypeCollector.collect(class_def, context)

        _TypeAttrCollector.collect_attr(node, context)
        _TypeParentCollector.collect_parent(node, context)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def collect(node: ProtocolDeclaration, context: Context):
        if context.get_protocol(node.identifier):
            print(f"protocol {node.identifier} is already defined")
        else:
            context.define_protocol(Protocol(node.identifier))

    @staticmethod
    @dispatch(FunctionDeclaration, Context)
    def collect(node: FunctionDeclaration, _: Context):
        """
        In this case the functions aren't a type
        """

    @staticmethod
    @dispatch(TypeDeclaration, Context)
    def collect(node: TypeDeclaration, context: Context):
        if context.get_type(node.identifier):
            print(f"type {node.identifier} is already defined")
        else:
            context.define_type(Type(node.identifier))


class _TypeAttrCollector:

    @staticmethod
    @dispatch(Program, Context)
    def collect_attr(node: Program, context: Context):
        for declaration in node.defines:
            _TypeAttrCollector.collect_attr(declaration, context)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def collect_attr(node: ProtocolDeclaration, context: Context):
        protocol = context.get_protocol(node.identifier)

        for method in node.functions:
            if protocol.get_method(method.identifier):
                print(
                    f"Method {method.identifier} is already defined in protocol {protocol.name}"
                )
                return

            return_type = define_type(method.static_return_type, context)
            if not return_type:
                print(f"{method.static_return_type} is not defined")
            if return_type is UnknownType():
                print(
                    f"return type not declared in method {method.identifier} in protocol {protocol.name}"
                )

            params = []

            for param in method.params:
                param_type = define_type(param.static_type, context)
                if not param_type:
                    print(f"{param.static_type} is not defined")
                else:
                    if param_type is UnknownType():
                        print(f"type of param {param.identifier} is not declared")
                    else:
                        if param in params:
                            print(f"duplicated param {param.identifier} in method")
                        else:
                            params.append(IdentifierVar(param.identifier, param_type))

            protocol.set_method(
                Method(
                    method.identifier,
                    params,
                    return_type,
                )
            )

    @staticmethod
    @dispatch(FunctionDeclaration, Context)
    def collect_attr(node: FunctionDeclaration, context: Context):

        if context.get_method(node.static_return_type, len(node.params)):
            print(f"The method  {node.static_return_type} is already defined")

        return_type = define_type(node.static_return_type, context)

        if not return_type:
            print(f"{return_type} is not defined")

        params = []

        for param in node.params:
            param_type = define_type(param.static_type, context)
            if not param_type:
                print(f"{param.static_type} is not defined")
            else:
                if param in params:
                    print(f"diplicated parameter {param.identifier} in method")
                else:
                    params.append(IdentifierVar(param.identifier, param_type))

        context.define_method(
            Method(
                node.identifier,
                params,
                return_type,
            )
        )

    @staticmethod
    @dispatch(TypeDeclaration, Context)
    def collect_attr(node: TypeDeclaration, context: Context):
        type_t = context.get_type(node.identifier)

        for param in node.params:
            param_type = define_type(param.static_type, context)
            if not param_type:
                print(f"{param.static_type} is not defined")
            else:
                if type_t.get_param(param.identifier):
                    print(f"duplicated param {param.identifier} in type {type_t.name}")
                else:
                    type_t.set_param(IdentifierVar(param.identifier, param_type))

        for attr in node.attributes:
            attr_type = define_type(attr.static_type, context)
            if not attr_type:
                print(f"{attr.static_type} is not defined")
            else:
                if type_t.get_attribute(attr.identifier):
                    print(
                        f"attribute {attr.identifier} already defined in type {type_t.name}"
                    )
                else:
                    type_t.set_attribute(IdentifierVar(attr.identifier, attr_type))

        for method in node.functions:
            if type_t.get_method(method.identifier):
                print(
                    f"method {method.identifier} is already defined in type {type_t.name}"
                )
            else:
                return_type = define_type(method.static_return_type, context)
                if not return_type:
                    print(f"{method.static_return_type} is not defined")

                params = []

                for param in method.params:
                    param_type = define_type(param.static_type, context)
                    if not param_type:
                        print(f"{param.static_type} is not defined")
                    else:
                        if param in params:
                            print(
                                f"duplicated param in method {method.identifier} in type {type_t.name}"
                            )
                        params.append(IdentifierVar(param.identifier, param_type))

                type_t.set_method(Method(method.identifier, params, return_type))


class _TypeParentCollector:

    @staticmethod
    @dispatch(Program, Context)
    def collect_parent(node: Program, context: Context):
        for definitions in node.defines:
            _TypeParentCollector.collect_parent(definitions, context)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context)
    def collect_parent(node: ProtocolDeclaration, context: Context):
        protocol = context.get_protocol(node.identifier)

        for extend in node.extends:
            ext_protocol = context.get_protocol(extend)
            if not ext_protocol:
                print(f"protocol {extend} is not defined")
            else:
                for method in ext_protocol.methods.values():
                    if protocol.get_method(method.name):
                        print(
                            f"protocol {protocol.name} declare the method {method.name} and extend from {ext_protocol.name} which already declare it"
                        )
                    else:
                        protocol.set_method(method)

    @staticmethod
    @dispatch(FunctionDeclaration, Context)
    def collect_parent(_: FunctionDeclaration, __: Context):
        """
        The function declaration node is an orphan, so he don't have parentns
        """

    @staticmethod
    @dispatch(TypeDeclaration, Context)
    def collect_parent(node: TypeDeclaration, context: Context):
        type_t = context.get_type(node.identifier)

        if node.inherits:
            parent = context.get_type(node.inherits.identifier)
            if not parent:
                print(f"type {node.inherits.identifier} is not defined")
            else:
                if parent in [NumberType(), StringType(), BooleanType()]:
                    print(f"type {parent} can't be inherited")
                else:
                    if len(node.params) > 0:
                        if len(node.inherits.arguments) == 0:
                            print(
                                f"missing initialization expression for the parent type type {type_t.name}. hint: when you want to override the arguments of a type which inherits from another type you must provide initialization for the parent type"
                            )
                    else:
                        for param in parent.params:
                            type_t.set_param(param)
                    type_t.set_parent(parent)
        else:
            type_t.set_parent(ObjectType())
