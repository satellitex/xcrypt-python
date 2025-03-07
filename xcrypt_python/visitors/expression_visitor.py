"""
式のAST訪問者クラス。
Python式をXcrypt（Perlベース）コードに変換するための機能を提供します。
"""

import ast
from typing import Union
from xcrypt_python.visitors.base_visitor import BaseVisitor


class ExpressionVisitor(BaseVisitor):
    """
    式のAST訪問者クラス。
    Python式をXcrypt（Perlベース）コードに変換するための機能を提供します。
    """

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
                # 特殊なメソッド処理
                if method == "append" and isinstance(node.func.value, ast.Name):
                    var_name = node.func.value.id
                    return f"push(@{var_name}, {args});"
                elif method == "readline":
                    return f"my $line = <{obj}>;"
                elif method == "strip":
                    return f"chomp({obj});"
                elif method == "close":
                    return f"close({obj});"
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
                # 実際のASTノードを使用して引数を取得
                range_args = node.args[0].args
                
                # range()の引数の数に基づいて変換
                if len(range_args) == 1:  # range(n) → [0..n-1]
                    end = int(self._expr_to_str(range_args[0]))
                    return f"[ 0..{end-1} ]"
                elif len(range_args) == 2:  # range(x, y) → [x..y-1]
                    start = self._expr_to_str(range_args[0])
                    end = int(self._expr_to_str(range_args[1]))                    
                    return f"[ {start}..{end-1} ]"
                elif len(range_args) == 3:  # range(x, y, step) → [x, x+step, ...]
                    start = self._expr_to_str(range_args[0])
                    end = int(self._expr_to_str(range_args[1]))
                    step = self._expr_to_str(range_args[2])
                    return f"[ {start}..{end-1} step {step} ]"  # Perlではstepは明示的に書く必要あり
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
                # キーが文字列でない場合、文字列に変換
                if not (key.startswith("'") or key.startswith('"')):
                    key = f"'{key}'"
                args.append(f"{key} => {value}")

            # 読みやすさのために適切なインデントで整形
            if func_name == "prepare":
                return f"{func_name}(\n        " + ",\n        ".join(args) + "\n    );"
            else:
                return f"{func_name}(\n        " + ",\n        ".join(args) + "\n    );"
        return False

    def _visit_JoinedStr(self, node: ast.JoinedStr) -> str:
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
            return self._visit_JoinedStr(expr)
            
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
