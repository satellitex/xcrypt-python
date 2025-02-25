import ast
import inspect
import functools
from xcrypt_python.formatter import format_perl_code

class XcryptTransformer(ast.NodeVisitor):
    def __init__(self):
        self.xcrypt_code = []
        self.imported_modules = []
        self.variable_types = {}
        self.standard_functions = ["print", "sprintf", "printf"]

    def visit_AnnAssign(self, node):
        var_name = node.target.id
        var_type = self._expr_to_str(node.annotation, is_annotation=True)
        
        if  var_type in ["dict" ,"Dict"]:
            self.variable_types[var_name] = "dict"
        elif var_type == "list" or "List" in var_type:
            self.variable_types[var_name] = "list"
        else:
            self.variable_types[var_name] = "scalar"
        
        value = self._expr_to_str(node.value)
        self.xcrypt_code.append(f"my {self._expr_to_str(node.target)} = {value};")


    def visit_ImportFrom(self, node):
        modules = [alias.name for alias in node.names]
        self.imported_modules.extend(modules)
        self.generic_visit(node)

    def finalize_imports(self):
        if self.imported_modules:
            self.xcrypt_code.insert(0, f"use base qw({' '.join(self.imported_modules)});")

    def visit_Assign(self, node):
        targets = [self._expr_to_str(target) for target in node.targets]
        value = self._expr_to_str(node.value)
        if isinstance(node.value, ast.Dict):
            self.xcrypt_code.append(f"my %{targets[0]} = {value};")
        else:
            self.xcrypt_code.append(f"my ${targets[0]} = {value};")        

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            obj = self._expr_to_str(node.func.value, is_function=True)
            method = node.func.attr
            args = ", ".join(self._expr_to_str(arg) for arg in node.args)
            if obj in self.imported_modules:
                append_str = f"{obj}::{method}({args});"
            else:
                append_str = f"{obj}->{method}({args});"
        else:
            func_name = self._expr_to_str(node.func,is_function=True)
            args = ", ".join(self._expr_to_str(arg) for arg in node.args)
            append_str = f"{func_name}({args});"
        self.xcrypt_code.append(append_str)

    def visit_For(self, node):
        target = self._expr_to_str(node.target)
        iter = self._expr_to_str(node.iter)
        self.xcrypt_code.append(f"foreach my ${target} (@{iter}) {{")
        self.generic_visit(node)
        self.xcrypt_code.append("}")

    def visit_FormattedValue(self, node):
        self.xcrypt_code.append(self._expr_to_str(node.value))
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        perl_fmt_string = ""
        values = []
        for part in node.values:
            if isinstance(part, ast.FormattedValue):
                values.append(self._expr_to_str(part.value))
                perl_fmt_string += "%s"
            else:
                perl_fmt_string += part.s.replace("%", "%%")
        return f"sprintf(\"{perl_fmt_string}\", {', '.join(values)})"

    def _expr_to_str(self, expr, is_function=False, is_annotation=False):
        if isinstance(expr, ast.Name):
            if is_function:
                return f"{expr.id}"
            if is_annotation:
                return f"{expr.id}"
            var_type = self.variable_types.get(expr.id, "scalar")
            if var_type == "dict":
                return f"%{expr.id}"
            elif var_type == "list":
                return f"@{expr.id}"
            else:
                return f"${expr.id}"
        elif isinstance(expr, ast.Constant):
            return repr(expr.value).replace("'", "")
        elif isinstance(expr, ast.BinOp):
            return f"({self._expr_to_str(expr.left)} {self._op_to_str(expr.op)} {self._expr_to_str(expr.right)})"
        elif isinstance(expr, ast.UnaryOp):
            return f"({self._op_to_str(expr.op)}{self._expr_to_str(expr.operand)})"
        elif isinstance(expr, ast.BoolOp):
            return f" ({' '.join(self._expr_to_str(v) for v in expr.values)}) "
        elif isinstance(expr, ast.Lambda):
            return f"sub {{ {self._expr_to_str(expr.body)} }}"
        elif isinstance(expr, ast.IfExp):
            return f"({self._expr_to_str(expr.body)} if {self._expr_to_str(expr.test)} else {self._expr_to_str(expr.orelse)})"
        elif isinstance(expr, ast.Dict):
            items = ", ".join(f"'{self._expr_to_str(k)}' => {self._expr_to_str(v)}" for k, v in zip(expr.keys, expr.values))
            return f"({items})"
        elif isinstance(expr, ast.List):
            return "[" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "]"
        elif isinstance(expr, ast.Set):
            return "{" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "}"
        elif isinstance(expr, ast.Compare):
            return f" ({self._expr_to_str(expr.left)} {' '.join(self._op_to_str(op) + ' ' + self._expr_to_str(cmp) for op, cmp in zip(expr.ops, expr.comparators))}) "
        elif isinstance(expr, ast.Call):
            return f"{self._expr_to_str(expr.func, is_function=True)}({', '.join(self._expr_to_str(arg) for arg in expr.args)})"
        elif isinstance(expr, ast.Attribute):
            if isinstance(expr.value, ast.Name) and expr.value.id == "self":
                return f"$self->{{{expr.attr}}}"  # Perl のハッシュアクセス形式
            return f"{self._expr_to_str(expr.value)}->{expr.attr}"
        elif isinstance(expr, ast.Subscript):
            value = self._expr_to_str(expr.value)
            index = self._expr_to_str(expr.slice)
            var_type = self.variable_types.get(expr.value.id, "scalar")
            if var_type == "dict" or var_type == "list":
                return f"${value[1:]}[{index}]"
            return f"{value}[{index}]"
        elif isinstance(expr, ast.Slice):
            return f"{self._expr_to_str(expr.lower)}:{self._expr_to_str(expr.upper)}:{self._expr_to_str(expr.step)}"
        elif isinstance(expr, ast.Tuple):
            return "(" + ", ".join(self._expr_to_str(e) for e in expr.elts) + ")"
        elif isinstance(expr, ast.JoinedStr):
            return self.visit_JoinedStr(expr)
        elif isinstance(expr, ast.FormattedValue):
            return f"{self._expr_to_str(expr.value)}"        
        
        return expr.value

    def _op_to_str(self, op):
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Mod):
            return "%"
        elif isinstance(op, ast.Pow):
            return "**"
        elif isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.GtE):
            return ">="
        elif isinstance(op, ast.And):
            return "&&"
        elif isinstance(op, ast.Or):
            return "||"
        return "UNKNOWN_OP"

    def transform(self, tree):
        self.visit(tree)
        self.finalize_imports()
        return "\n".join(self.xcrypt_code)


def execute(tree):
    transformer = XcryptTransformer()
    xcrypt_code = transformer.transform(tree)
    return xcrypt_code


def Xcrypt(func):
    source = inspect.getsource(func)
    tree = ast.parse(source)

    @functools.wraps(func)
    def dummy():
        xcr =  format_perl_code(execute(tree))
        print(xcr)
        return xcr
    
    return dummy
