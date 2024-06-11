"""
    This module contains the AST visitor class.
"""

from multipledispatch import dispatch
from dataclasses import dataclass
from ..parser.ast.ast import Program, TypeDeclaration
from .types import Method, IdentifierVar, Type
from .context import Context

# pylint: disable=function-redefined


@dataclass
class TypeCollector:
    context: Context

    @dispatch(Program)
    def visit(self, node: Program):
        for class_def in node.defines:
            if isinstance(class_def, TypeDeclaration):
                self.visit(class_def)

    @dispatch(TypeDeclaration)
    def visit(self, node: TypeDeclaration):
        current_type: Type = self.context.define_type(node.identifier)
        for attr_def in node.attributes:
            current_type.attributes[attr_def.identifier] = IdentifierVar(
                attr_def.identifier, None
            )

        for func_def in node.functions:
            params: list[IdentifierVar] = []
            for param in func_def.params:
                params.append(IdentifierVar(param.identifier, None))
            current_type.methods[func_def.identifier] = Method(
                func_def.identifier, params, func_def.return_type
            )
