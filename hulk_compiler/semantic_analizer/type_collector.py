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
from .error_stack import StackError
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
    @dispatch(Program, Context, StackError)
    def collect(node: Program, context: Context, stack: StackError):
        for class_def in node.defines:
            TypeCollector.collect(class_def, context, stack)

        _TypeAttrCollector.collect_attr(node, context, stack)
        _TypeParentCollector.collect_parent(node, context, stack)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context, StackError)
    def collect(node: ProtocolDeclaration, context: Context, stack: StackError):
        if context.get_protocol(node.identifier):
            stack.add_error(
                f"protocol {node.identifier} is already defined",
                (node.line, node.column),
            )
        else:
            context.define_protocol(Protocol(node.identifier))

    @staticmethod
    @dispatch(FunctionDeclaration, Context, StackError)
    def collect(_: FunctionDeclaration, __: Context, ___: StackError):
        """
        In this case the functions aren't a type
        """

    @staticmethod
    @dispatch(TypeDeclaration, Context, StackError)
    def collect(node: TypeDeclaration, context: Context, stack: StackError):
        if context.get_type(node.identifier):
            stack.add_error(
                f"type {node.identifier} is already defined", (node.line, node.column)
            )
        else:
            context.define_type(Type(node.identifier))


class _TypeAttrCollector:

    @staticmethod
    @dispatch(Program, Context, StackError)
    def collect_attr(node: Program, context: Context, stack: StackError):
        for declaration in node.defines:
            _TypeAttrCollector.collect_attr(declaration, context, stack)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context, StackError)
    def collect_attr(node: ProtocolDeclaration, context: Context, stack: StackError):
        protocol = context.get_protocol(node.identifier)

        for method in node.functions:
            if protocol.get_method(method.identifier):
                stack.add_error(
                    f"Method {method.identifier} is already defined in protocol {protocol.name}",
                    (method.line, method.column),
                )
                return

            return_type = define_type(method.static_return_type, context)
            if not return_type:
                stack.add_error(
                    f"{method.static_return_type} is not defined",
                    (method.line, method.column),
                )
            if return_type is UnknownType():
                stack.add_error(
                    f"return type not declared in method {method.identifier} in protocol {protocol.name}",
                    (method.line, method.column),
                )

            params = []

            for param in method.params:
                param_type = define_type(param.static_type, context)
                if not param_type:
                    stack.add_error(
                        f"{param.static_type} is not defined", param.line, param.column
                    )
                else:
                    if param_type is UnknownType():
                        stack.add_error(
                            f"type of param {param.identifier} is not declared",
                            (param.line, param.column),
                        )
                    else:
                        if param in params:
                            stack.add_error(
                                f"duplicated param {param.identifier} in method",
                                (param.line, param.column),
                            )
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
    @dispatch(FunctionDeclaration, Context, StackError)
    def collect_attr(node: FunctionDeclaration, context: Context, stack: StackError):

        if context.get_method(node.static_return_type, len(node.params)):
            stack.add_error(
                f"The method  {node.static_return_type} is already defined",
                (node.line, node.column),
            )

        return_type = define_type(node.static_return_type, context)

        if not return_type:
            stack.add_error(f"{return_type} is not defined", (node.line, node.column))

        params = []

        for param in node.params:
            param_type = define_type(param.static_type, context)
            if not param_type:
                stack.add_error(
                    f"{param.static_type} is not defined", (param.line, param.column)
                )
            else:
                if param in params:
                    stack.add_error(
                        f"diplicated parameter {param.identifier} in method",
                        (param.line, param.column),
                    )
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
    @dispatch(TypeDeclaration, Context, StackError)
    def collect_attr(node: TypeDeclaration, context: Context, stack: StackError):
        type_t = context.get_type(node.identifier)

        for param in node.params:
            param_type = define_type(param.static_type, context)
            if not param_type:
                stack.add_error(
                    f"{param.static_type} is not defined", (param.line, param.column)
                )
            else:
                if type_t.get_param(param.identifier):
                    stack.add_error(
                        f"duplicated param {param.identifier} in type {type_t.name}",
                        (param.line, param.column),
                    )
                else:
                    type_t.set_param(IdentifierVar(param.identifier, param_type))

        for attr in node.attributes:
            attr_type = define_type(attr.static_type, context)
            if not attr_type:
                stack.add_error(
                    f"{attr.static_type} is not defined", (attr.line, attr.column)
                )
            else:
                if type_t.get_attribute(attr.identifier):
                    stack.add_error(
                        f"attribute {attr.identifier} already defined in type {type_t.name}",
                        (attr.line, attr.column),
                    )
                else:
                    type_t.set_attribute(IdentifierVar(attr.identifier, attr_type))

        for method in node.functions:
            if type_t.get_method(method.identifier):
                stack.add_error(
                    f"method {method.identifier} is already defined in type {type_t.name}",
                    (method.line, method.column),
                )
            else:
                return_type = define_type(method.static_return_type, context)
                if not return_type:
                    stack.add_error(
                        f"{method.static_return_type} is not defined",
                        (method.line, method.column),
                    )

                params = []

                for param in method.params:
                    param_type = define_type(param.static_type, context)
                    if not param_type:
                        stack.add_error(
                            f"{param.static_type} is not defined",
                            (param.line, param.column),
                        )
                    else:
                        if param in params:
                            stack.add_error(
                                f"duplicated param in method {method.identifier} in type {type_t.name}",
                                (param.line, param.column),
                            )
                        params.append(IdentifierVar(param.identifier, param_type))

                type_t.set_method(Method(method.identifier, params, return_type))


class _TypeParentCollector:

    @staticmethod
    @dispatch(Program, Context, StackError)
    def collect_parent(node: Program, context: Context, stack: StackError):
        for definitions in node.defines:
            _TypeParentCollector.collect_parent(definitions, context, stack)

    @staticmethod
    @dispatch(ProtocolDeclaration, Context, StackError)
    def collect_parent(node: ProtocolDeclaration, context: Context, stack: StackError):
        protocol = context.get_protocol(node.identifier)

        for extend in node.extends:
            ext_protocol = context.get_protocol(extend)
            if not ext_protocol:
                stack.add_error(
                    f"protocol {extend} is not defined", (node.line, node.column)
                )
            else:
                for method in ext_protocol.methods.values():
                    if protocol.get_method(method.name):
                        stack.add_error(
                            f"protocol {protocol.name} declare the method {method.name} and extend from {ext_protocol.name} which already declare it",
                            (node.line, node.column),
                        )
                    else:
                        protocol.set_method(method)

    @staticmethod
    @dispatch(FunctionDeclaration, Context, StackError)
    def collect_parent(_: FunctionDeclaration, __: Context, ___: StackError):
        """
        The function declaration node is an orphan, so he don't have parentns
        """

    @staticmethod
    @dispatch(TypeDeclaration, Context, StackError)
    def collect_parent(node: TypeDeclaration, context: Context, stack: StackError):
        type_t = context.get_type(node.identifier)

        if node.inherits:
            parent = context.get_type(node.inherits.identifier)
            if not parent:
                stack.add_error(
                    f"type {node.inherits.identifier} is not defined",
                    (node.inherits.line, node.inherits.column),
                )
            else:
                if parent in [NumberType(), StringType(), BooleanType()]:
                    stack.add_error(
                        f"type {parent} can't be inherited",
                        (node.inherits.line, node.inherits.column),
                    )
                else:
                    if len(node.params) > 0:
                        if len(node.inherits.arguments) == 0:
                            stack.add_error(
                                f"missing initialization expression for the parent type type {type_t.name}. hint: when you want to override the arguments of a type which inherits from another type you must provide initialization for the parent type",
                                (node.inherits.line, node.inherits.column),
                            )
                    else:
                        for param in parent.params:
                            type_t.set_param(param)
                    type_t.set_parent(parent)
        else:
            type_t.set_parent(ObjectType())
