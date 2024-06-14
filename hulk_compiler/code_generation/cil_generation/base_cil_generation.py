import cil_nodes as cil
from hulk_compiler.semantic_analizer.types import IdentifierVar


class BaseHULKToCILVisitor:
    def __init__(self):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        # self.context = context

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_local(self, vinfo: IdentifierVar):
        vinfo.name = (
            f"local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}"
        )
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = IdentifierVar("internal", None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name: str, type_name: str):
        return f"function_{method_name}_at_{type_name}"

    def register_function(self, function_name: str):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name: str):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f"data_{len(self.dotdata)}"
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node
