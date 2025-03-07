import ast
import inspect
import functools
from typing import List, Dict, Any, Optional, Union
from xcrypt_python.formatter import format_perl_code

class XcryptTransformer(ast.NodeVisitor):
    """
    AST Visitor クラス。PythonコードをXcrypt（Perlベース）コードに変換します。
    """
    def __init__(self):
        self.xcrypt_code: List[str] = []  # 生成されたXcryptコード
        self.imported_modules: List[str] = []  # インポートされたモジュール
        self.variable_types: Dict[str, str] = {}  # 変数の型情報
        self.standard_functions: List[str] = ["print", "sprintf", "printf"]  # 標準関数

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """
        型アノテーション付き代入（例：var_name: type = value）を処理します。
        変数の型を検出し、適切なPerlコードを生成します。
        """
        var_name = node.target.id
        var_type = self._expr_to_str(node.annotation, is_annotation=True)
        
        # アノテーションに基づいて変数の型を決定
        if var_type in ["dict", "Dict"]:
            self.variable_types[var_name] = "dict"
        elif var_type == "list" or "List" in var_type:
            self.variable_types[var_name] = "list"
        else:
            self.variable_types[var_name] = "scalar"
        
        value = self._expr_to_str(node.value)
        self.xcrypt_code.append(f"my {self._expr_to_str(node.target)} = {value};")


    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """
        インポート文を処理し、インポートされたモジュールを追跡します。
        """
        modules = [alias.name for alias in node.names]
        self.imported_modules.extend(modules)
        self.generic_visit(node)

    def finalize_imports(self) -> None:
        """
        インポートされたすべてのモジュールに対してPerlの'use base'文を生成します。
        """
        if self.imported_modules:
            self.xcrypt_code.insert(0, f"use base qw({' '.join(self.imported_modules)});")

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        通常の代入（例：var_name = value）を処理します。
        割り当てられた値に基づいて変数の型を決定します。
        """
        targets = [self._expr_to_str(target) for target in node.targets]
        value = self._expr_to_str(node.value)
        
        # 辞書には%プレフィックス、その他の型には$を使用
        if isinstance(node.value, ast.Dict):
            self.xcrypt_code.append(f"my %{targets[0]} = {value};")
        else:
            self.xcrypt_code.append(f"my ${targets[0]} = {value};")


    def _visit_call_attribute(self, node: ast.Call) -> Union[str, bool]:
        """
        オブジェクトのメソッド呼び出し（例：obj.method()）を処理します。
        オブジェクトがインポートされたモジュールかどうかに基づいて、適切なPerl構文に変換します。
        """
        if isinstance(node.func, ast.Attribute):
            obj = self._expr_to_str(node.func.value, is_function=True)
            method = node.func.attr
            args = ", ".join(self._expr_to_str(arg) for arg in node.args)
            
            # モジュールメソッドには::を、オブジェクトメソッドには->を使用
            if obj in self.imported_modules:
                return f"{obj}::{method}({args});"
            else:
                return f"{obj}->{method}({args});"
        return False
    
    def _visit_call_list_range(self, node: ast.Call) -> Union[str, bool]:
        """
        list(range(...))パターンを処理し、Perlの範囲構文に変換します。
        """
        func_name = self._expr_to_str(node.func, is_function=True)
        
        # list(range(...))パターンを検出
        if func_name == "list" and len(node.args) == 1 and isinstance(node.args[0], ast.Call):
            inner_func = self._expr_to_str(node.args[0].func, is_function=True)
            
            if inner_func == "range":
                range_args = [self._expr_to_str(arg) for arg in node.args[0].args]
                
                # range()の引数の数に基づいて変換
                if len(range_args) == 1:  # range(n) → [0..n-1]
                    return f"[ 0..{int(range_args[0])-1} ]"
                elif len(range_args) == 2:  # range(x, y) → [x..y-1]
                    return f"[ {range_args[0]}..{int(range_args[1])-1} ]"
                elif len(range_args) == 3:  # range(x, y, step) → [x, x+step, ...]
                    return f"[ {range_args[0]}..{int(range_args[1])-1} step {range_args[2]} ]"  # Perlではstepは明示的に書く必要あり
        return False

    def _visit_call_args_dict(self, node: ast.Call) -> Union[str, bool]:
        """
        最初の引数が辞書である関数呼び出しを処理します。
        PythonのdictをPerlのハッシュリスト形式に変換します。
        """
        if len(node.args) == 1 and isinstance(node.args[0], ast.Dict):
            func_name = self._expr_to_str(node.func, is_function=True)
            args = []
            
            # 各キーと値のペアを「key => value」形式に変換
            for key_node, value_node in zip(node.args[0].keys, node.args[0].values):
                key = self._expr_to_str(key_node)
                value = self._expr_to_str(value_node)
                args.append(f"{key} => {value}")

            # 読みやすさのために適切なインデントで整形
            return f"{func_name}(\n    " + ",\n    ".join(args) + "\n);"
        return False


    def visit_Call(self, node: ast.Call) -> None:
        """
        関数呼び出しを処理し、適切なPerl構文に変換します。
        特殊なパターンを順番に試します。
        """
        # 特殊な呼び出しハンドラを順番に試す
        append_str = self._visit_call_attribute(node)
        if not append_str:
            append_str = self._visit_call_list_range(node)
        if not append_str:
            append_str = self._visit_call_args_dict(node)
        if not append_str:
            # デフォルトの関数呼び出し処理
            func_name = self._expr_to_str(node.func, is_function=True)
            args = ", ".join(self._expr_to_str(arg) for arg in node.args)
            append_str = f"{func_name}({args});"
        
        self.xcrypt_code.append(append_str)

    def visit_For(self, node: ast.For) -> None:
        """
        forループを処理し、Perlのforeachシンタックスに変換します。
        """
        target = self._expr_to_str(node.target)
        iter_expr = self._expr_to_str(node.iter)
        self.xcrypt_code.append(f"foreach my {target} ({iter_expr}) {{")
        self.generic_visit(node)
        self.xcrypt_code.append("}")

    def visit_FormattedValue(self, node: ast.FormattedValue) -> None:
        """
        f文字列内のフォーマット値を処理します。
        """
        self.xcrypt_code.append(self._expr_to_str(node.value))
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> str:
        """
        f文字列を処理し、Perlのsprintf形式に変換します。
        """
        perl_fmt_string = ""
        values = []
        
        # f文字列の各部分を処理
        for part in node.values:
            if isinstance(part, ast.FormattedValue):
                values.append(self._expr_to_str(part.value))
                perl_fmt_string += "%s"
            else:
                # リテラル部分の%文字をエスケープ
                perl_fmt_string += part.s.replace("%", "%%")
                
        return f"sprintf(\"{perl_fmt_string}\", {', '.join(values)})"

    def _expr_to_str(self, expr: ast.AST, is_function: bool = False, is_annotation: bool = False) -> str:
        """
        Python ASTの式をPerlの文字列表現に変換します。
        
        引数:
            expr: 変換するAST式
            is_function: 式が関数名かどうか
            is_annotation: 式が型アノテーションかどうか
            
        戻り値:
            式のPerl文字列表現
        """
        # 異なるASTノードタイプを処理
        if isinstance(expr, ast.Name):
            # 名前式の処理
            if is_function or is_annotation:
                return f"{expr.id}"
                
            var_type = self.variable_types.get(expr.id, "scalar")
            if var_type == "dict":
                return f"%{expr.id}"
            elif var_type == "list":
                return f"@{expr.id}"
            else:
                return f"${expr.id}"
                
        elif isinstance(expr, ast.Constant):
            # 定数式の処理
            if isinstance(expr.value, str):
                if (expr.value[0] == '"' and expr.value[-1] == '"') or (expr.value[0] == "'" and expr.value[-1] == "'"):
                    return f'{expr.value}'
                return f"'{expr.value}'"
            return f'{expr.value}'
            
        elif isinstance(expr, ast.BinOp):
            # 二項演算式の処理
            return f"{self._expr_to_str(expr.left)} {self._op_to_str(expr.op)} {self._expr_to_str(expr.right)}"
            
        elif isinstance(expr, ast.UnaryOp):
            # 単項演算式の処理
            return f"{self._op_to_str(expr.op)}{self._expr_to_str(expr.operand)}"
            
        elif isinstance(expr, ast.BoolOp):
            # ブール演算式の処理
            return f"{' '.join(self._expr_to_str(v) for v in expr.values)}"
            
        elif isinstance(expr, ast.Lambda):
            # ラムダ式の処理
            return f"sub {{ {self._expr_to_str(expr.body)} }}"
            
        elif isinstance(expr, ast.IfExp):
            # 条件式の処理
            return f"({self._expr_to_str(expr.body)} if {self._expr_to_str(expr.test)} else {self._expr_to_str(expr.orelse)})"
            
        elif isinstance(expr, ast.Dict):
            # 辞書式の処理
            items = ", ".join(f"{self._expr_to_str(k)} => {self._expr_to_str(v)}" for k, v in zip(expr.keys, expr.values))
            return f"({items})"
            
        elif isinstance(expr, ast.List):
            # リスト式の処理
            return "[" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "]"
            
        elif isinstance(expr, ast.Set):
            # セット式の処理
            return "{" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "}"
            
        elif isinstance(expr, ast.Compare):
            # 比較式の処理
            return f" ({self._expr_to_str(expr.left)} {' '.join(self._op_to_str(op) + ' ' + self._expr_to_str(cmp) for op, cmp in zip(expr.ops, expr.comparators))}) "
            
        elif isinstance(expr, ast.Call):
            # 関数呼び出し式の処理
            res = self._visit_call_attribute(expr)
            if not res:
                res = self._visit_call_list_range(expr)
            if not res:
                res = self._visit_call_args_dict(expr)
            if not res:
                res = f"{self._expr_to_str(expr.func, is_function=True)}({', '.join(self._expr_to_str(arg) for arg in expr.args)})"
            return res
            
        elif isinstance(expr, ast.Attribute):
            # 属性アクセス式の処理
            if isinstance(expr.value, ast.Name) and expr.value.id == "self":
                return f"$self->{{{expr.attr}}}"  # Perlのハッシュアクセス形式
            return f"{self._expr_to_str(expr.value)}->{expr.attr}"
            
        elif isinstance(expr, ast.Subscript):
            # 添字アクセス式の処理
            value = self._expr_to_str(expr.value)
            index = self._expr_to_str(expr.slice)
            
            # 既知の変数型の特殊ケースを処理
            if hasattr(expr.value, 'id'):
                var_type = self.variable_types.get(expr.value.id, "scalar")
                if var_type == "dict" or var_type == "list":
                    return f"${value[1:]}[{index}]"
            
            return f"{value}[{index}]"
            
        elif isinstance(expr, ast.Slice):
            # スライス式の処理
            return f"{self._expr_to_str(expr.lower)}:{self._expr_to_str(expr.upper)}:{self._expr_to_str(expr.step)}"
            
        elif isinstance(expr, ast.Tuple):
            # タプル式の処理
            return "(" + ", ".join(self._expr_to_str(e) for e in expr.elts) + ")"
            
        elif isinstance(expr, ast.JoinedStr):
            # 結合文字列（f文字列）の処理
            return self.visit_JoinedStr(expr)
            
        elif isinstance(expr, ast.FormattedValue):
            # フォーマット値の処理
            return f"{self._expr_to_str(expr.value)}"
            
        elif isinstance(expr, ast.Str):
            # 文字列リテラルの処理
            return repr(expr.s).replace("'", "")
            
        elif isinstance(expr, ast.Starred):  # *argsの処理
            value = self._expr_to_str(expr.value)
            return f"@{value}"  # Perlのリスト展開
        
        return f"UNDERSTAND_ERROR: {expr}"

    def _op_to_str(self, op: ast.operator) -> str:
        """
        Python ASTの演算子をPerlの文字列表現に変換します。
        """
        # 演算子マッピング
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

    def transform(self, tree: ast.AST) -> str:
        """
        ASTをPerlコードに変換します。
        
        引数:
            tree: 変換するAST
            
        戻り値:
            生成されたPerlコード（文字列）
        """
        self.visit(tree)
        self.finalize_imports()
        return "\n".join(self.xcrypt_code)


def execute(tree: ast.AST) -> str:
    """
    ASTをXcryptコードに変換します。
    
    引数:
        tree: 変換するAST
        
    戻り値:
        生成されたXcryptコード（文字列）
    """
    transformer = XcryptTransformer()
    xcrypt_code = transformer.transform(tree)
    return xcrypt_code


def Xcrypt(func):
    """
    Python関数をXcrypt（Perl）コードに変換するデコレータ。
    
    引数:
        func: 変換する関数
        
    戻り値:
        変換されたコードを返すラッパー関数
    """
    source = inspect.getsource(func)
    tree = ast.parse(source)

    @functools.wraps(func)
    def wrapper():
        xcr = format_perl_code(execute(tree))
        print(xcr)
        return xcr
    
    return wrapper
