import inspect
import ast
import functools

class XcryptTransformer(ast.NodeVisitor):
    def __init__(self):
        self.xcrypt_code = []

    def visit_Import(self, node):
        for alias in node.names:
            self.xcrypt_code.append(f"use {alias.name};")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.xcrypt_code.append(f"use base qw({alias.name});")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = [self._expr_to_str(target) for target in node.targets]
        value = self._expr_to_str(node.value)
        self.xcrypt_code.append(f"my ${targets[0]} = {value};")
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = self._expr_to_str(node.func)
        args = ", ".join(self._expr_to_str(arg) for arg in node.args)
        self.xcrypt_code.append(f"&{func_name}({args});")
        self.generic_visit(node)

    def _expr_to_str(self, expr):
        if isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Constant):
            return repr(expr.value)
        elif isinstance(expr, ast.BinOp):
            return f"({self._expr_to_str(expr.left)} {self._op_to_str(expr.op)} {self._expr_to_str(expr.right)})"
        elif isinstance(expr, ast.UnaryOp):
            return f"({self._op_to_str(expr.op)}{self._expr_to_str(expr.operand)})"
        elif isinstance(expr, ast.BoolOp):
            return f" ({' '.join(self._op_to_str(expr.op).join(self._expr_to_str(v) for v in expr.values))}) "
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
            return f"&{self._expr_to_str(expr.func)}({', '.join(self._expr_to_str(arg) for arg in expr.args)})"
        elif isinstance(expr, ast.Attribute):
            return f"{self._expr_to_str(expr.value)}->{expr.attr}"
        elif isinstance(expr, ast.Subscript):
            return f"{self._expr_to_str(expr.value)}[{self._expr_to_str(expr.slice)}]"
        elif isinstance(expr, ast.ListComp) or isinstance(expr, ast.SetComp) or isinstance(expr, ast.DictComp) or isinstance(expr, ast.GeneratorExp):
            return "LIST_COMPREHENSION_UNSUPPORTED"
        return "UNKNOWN_EXPR"


    def _op_to_str(self, op):
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        return "UNKNOWN_OP"

    def transform(self, tree):
        self.visit(tree)
        return "\n".join(self.xcrypt_code)


def execute(tree):
    transformer = XcryptTransformer()
    xcrypt_code = transformer.transform(tree)
    print(xcrypt_code)


def Xcrypt(func):
    source = inspect.getsource(func)
    tree = ast.parse(source)

    @functools.wraps(func)
    def dummy():
        return execute(tree)
    
    return dummy
