"""
式のAST訪問者クラス。
Python式をXcrypt（Perlベース）コードに変換するための機能を提供します。
"""

import ast
from typing import Union, Optional
from xcrypt_python.visitors.base_visitor import BaseVisitor


class ExpressionVisitor(BaseVisitor):
    """
    式のAST訪問者クラス。
    Python式をXcrypt（Perlベース）コードに変換するための機能を提供します。
    """

    
    # 最初の _visit_call_list_range と _visit_call_args_dict メソッドは重複しているため削除


    def _visit_call_attribute(self, node: ast.Call) -> Optional[str]:
        """
        オブジェクトのメソッド呼び出し（例：obj.method()）を処理します。
        オブジェクトがインポートされたモジュールかどうかに基づいて、適切なPerl構文に変換します。
        引数は値渡し/参照渡しのルールに従って渡します。
        """
        if not isinstance(node.func, ast.Attribute):
            return None
            
        obj = self._expr_to_str(node.func.value, is_function=True)
        method = node.func.attr
        
        # sample/ モジュールかどうかをチェック
        is_sample_module = obj in self.imported_modules
        
        # 引数を適切に処理（値渡し/参照渡しルールに従って）
        args_list = []
        for arg in node.args:
            if isinstance(arg, ast.Name):
                # 変数の型を取得
                var_type = self.variable_types.get(arg.id, "scalar")
                
                if is_sample_module:
                    # sample/モジュールのメソッド: 値渡し
                    args_list.append(self._expr_to_str(arg))
                else:
                    # その他のメソッド:
                    if var_type == "scalar":
                        # スカラー値: 値渡し
                        args_list.append(self._expr_to_str(arg))
                    else:
                        # 非スカラー値: 参照渡し
                        args_list.append(self._expr_to_str(arg, as_ref=True))
            else:
                # リテラルや式の場合はそのまま
                args_list.append(self._expr_to_str(arg))
        
        args = ", ".join(args_list)
        
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
        
    def _is_sample_or_standard_func(self, func_expr: ast.AST) -> bool:
        """
        sample/ディレクトリにある関数やPerlの標準関数かどうかを判定します。
        """
        if isinstance(func_expr, ast.Name):
            # 直接的に標準関数かどうか確認
            if func_expr.id in self.standard_functions:
                return True
            # Xcrypt固有の関数かどうか確認
            if func_expr.id in self.xcrypt_functions:
                return True
            # ここでsample/ディレクトリのモジュールチェックを追加可能
            if func_expr.id in self.imported_modules:
                # 簡易的なチェック - より詳細なチェックを実装することも可能
                return True
        return False

    def _expr_to_str(self, expr: ast.AST, is_function: bool = False, is_annotation: bool = False, 
                    is_in_str: bool = False, as_ref: bool = False) -> str:
        """
        Python ASTの式をPerlの文字列表現に変換します。
        
        引数:
            expr: 変換するAST式
            is_function: 式が関数名かどうか
            is_annotation: 式が型アノテーションかどうか
            is_in_str: 文字列内の式かどうか
            as_ref: 参照として返すかどうか
            
        戻り値:
            式のPerl文字列表現
        """
        # Handle None case
        if expr is None:
            return "undef"
            
        # Dispatch to appropriate handler method based on expression type
        handlers = {
            ast.Name: self._handle_name_expr,
            ast.Constant: self._handle_constant_expr,
            ast.BinOp: self._handle_binop_expr,
            ast.UnaryOp: self._handle_unaryop_expr,
            ast.BoolOp: self._handle_boolop_expr,
            ast.Lambda: self._handle_lambda_expr,
            ast.IfExp: self._handle_ifexp_expr,
            ast.Dict: self._handle_dict_expr,
            ast.List: self._handle_list_expr,
            ast.Set: self._handle_set_expr,
            ast.Compare: self._handle_compare_expr,
            ast.Call: self._handle_call_expr,
            ast.Attribute: self._handle_attribute_expr,
            ast.Subscript: self._handle_subscript_expr,
            ast.Slice: self._handle_slice_expr,
            ast.Tuple: self._handle_tuple_expr,
            ast.JoinedStr: self._handle_joined_str,
            ast.FormattedValue: self._handle_formatted_value_expr,
            ast.Str: self._handle_str_expr,
            ast.Starred: self._handle_starred_expr
        }
        
        handler = handlers.get(type(expr))
        if handler:
            return handler(expr, is_function, is_annotation, is_in_str, as_ref)
        
        return f"UNDERSTAND_ERROR: {expr}"
        
    def _handle_name_expr(self, expr: ast.Name, is_function: bool = False, is_annotation: bool = False,
                         is_in_str: bool = False, as_ref: bool = False) -> str:
        """名前式の処理"""
        if is_function or is_annotation:
            return f"{expr.id}"
        
        # 現在の関数内での変数アクセスを確認
        is_param = self._is_function_parameter(expr.id)
        var_type = self.variable_types.get(expr.id, "scalar")
        
        # 参照として渡す場合
        if as_ref:
            if var_type == "dict":
                return f"\\%{expr.id}"
            elif var_type == "list":
                return f"\\@{expr.id}"
            else:
                return f"\\${expr.id}"
        
        # 変数アクセスの形式を決定
        if var_type == "dict":
            return f"%{expr.id}"
        elif var_type == "list":
            return f"@{expr.id}"
        else:
            return f"${expr.id}"
    
    def _is_function_parameter(self, name: str) -> bool:
        """指定された名前が現在の関数のパラメータかどうかを判断"""
        if not self.current_function or name == 'self':
            return False
            
        func_def = self.function_defs.get(self.current_function)
        if not func_def:
            return False
            
        return any(arg.arg == name for arg in func_def.args.args)
    
    def _handle_constant_expr(self, expr: ast.Constant, *args) -> str:
        """定数式の処理"""
        if isinstance(expr.value, str):
            if (expr.value[0] == '"' and expr.value[-1] == '"') or (expr.value[0] == "'" and expr.value[-1] == "'"):
                return f'{expr.value}'
            if "'" in expr.value:
                return f'"{expr.value}"'
            else:
                return f"'{expr.value}'"
        return f'{expr.value}'
    
    def _handle_binop_expr(self, expr: ast.BinOp, *args) -> str:
        """二項演算式の処理"""
        return f"{self._expr_to_str(expr.left)} {self._op_to_str(expr.op)} {self._expr_to_str(expr.right)}"
    
    def _handle_unaryop_expr(self, expr: ast.UnaryOp, *args) -> str:
        """単項演算式の処理"""
        return f"{self._op_to_str(expr.op)}{self._expr_to_str(expr.operand)}"
    
    def _handle_boolop_expr(self, expr: ast.BoolOp, *args) -> str:
        """ブール演算式の処理"""
        return f"{' '.join(self._expr_to_str(v) for v in expr.values)}"
    
    def _handle_lambda_expr(self, expr: ast.Lambda, *args) -> str:
        """ラムダ式の処理"""
        return f"sub {{ {self._expr_to_str(expr.body)} }}"
    
    def _handle_ifexp_expr(self, expr: ast.IfExp, *args) -> str:
        """条件式の処理"""
        return f"({self._expr_to_str(expr.body)} if {self._expr_to_str(expr.test)} else {self._expr_to_str(expr.orelse)})"
    
    def _handle_dict_expr(self, expr: ast.Dict, *args) -> str:
        """辞書式の処理"""
        items = ", ".join(f"{self._expr_to_str(k)} => {self._expr_to_str(v)}" 
                         for k, v in zip(expr.keys, expr.values))
        return f"({items})"
    
    def _handle_list_expr(self, expr: ast.List, *args) -> str:
        """リスト式の処理"""
        return "[" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "]"
    
    def _handle_set_expr(self, expr: ast.Set, *args) -> str:
        """セット式の処理"""
        return "{" + ", ".join(self._expr_to_str(e) for e in expr.elts) + "}"
    
    def _handle_compare_expr(self, expr: ast.Compare, *args) -> str:
        """比較式の処理"""
        comparisons = []
        for op, comparator in zip(expr.ops, expr.comparators):
            op_str = self._op_to_str(op)
            comparator_str = self._expr_to_str(comparator)
            comparisons.append(f"{op_str} {comparator_str}")
            
        return f" ({self._expr_to_str(expr.left)} {' '.join(comparisons)}) "
    
    def _handle_call_expr(self, expr: ast.Call, *args) -> str:
        """関数呼び出し式の処理"""
        # 特殊なパターンを試す
        res = self._visit_call_attribute(expr)
        if res:
            return res
            
        res = self._visit_call_list_range(expr)
        if res:
            return res
            
        res = self._visit_call_args_dict(expr)
        if res:
            return res
        
        # 通常の関数呼び出し
        func_name = self._expr_to_str(expr.func, is_function=True)
        is_sample_func = self._is_sample_or_standard_func(expr.func)
        
        # 引数の処理
        args_list = []
        for arg in expr.args:
            if isinstance(arg, ast.Name):
                var_type = self.variable_types.get(arg.id, "scalar")
                
                if is_sample_func or var_type == "scalar":
                    # 値渡し
                    args_list.append(self._expr_to_str(arg))
                else:
                    # 参照渡し（非スカラー値）
                    args_list.append(self._expr_to_str(arg, as_ref=True))
            else:
                # リテラルや式はそのまま
                args_list.append(self._expr_to_str(arg))
        
        return f"{func_name}({', '.join(args_list)})"
    
    def _handle_attribute_expr(self, expr: ast.Attribute, *args) -> str:
        """属性アクセス式の処理"""
        if isinstance(expr.value, ast.Name) and expr.value.id == "self":
            return f"$self->{{{expr.attr}}}"  # Perlのハッシュアクセス形式
        return f"{self._expr_to_str(expr.value)}->{expr.attr}"
    
    def _handle_subscript_expr(self, expr: ast.Subscript, *args) -> str:
        """添字アクセス式の処理"""
        # インデックス値の取得
        if isinstance(expr.slice, ast.Index):
            index_value = expr.slice.value
        else:
            index_value = expr.slice
            
        index = self._expr_to_str(index_value)
        is_string_key = isinstance(index_value, ast.Constant) and isinstance(index_value.value, str)
        
        # 変数が関数パラメータかチェック
        param_name = None
        is_param = False
        
        if isinstance(expr.value, ast.Name):
            param_name = expr.value.id
            is_param = self._is_function_parameter(param_name)
        
        # 関数パラメータの場合の特別処理
        if is_param and param_name:
            var_type = self.variable_types.get(param_name, "scalar")
            if var_type == "dict" and is_string_key:
                return f"${param_name}->{{{index}}}"
            else:
                return f"${param_name}[{index}]"
        
        # 通常の変数
        value = self._expr_to_str(expr.value)
        if hasattr(expr.value, 'id'):
            var_type = self.variable_types.get(expr.value.id, "scalar")
            if var_type == "dict" and is_string_key:
                return f"${value[1:]}->{{{index}}}"
            elif var_type == "dict" or var_type == "list":
                return f"${value[1:]}[{index}]"
        
        return f"{value}[{index}]"
    
    def _handle_slice_expr(self, expr: ast.Slice, *args) -> str:
        """スライス式の処理"""
        return f"{self._expr_to_str(expr.lower)}:{self._expr_to_str(expr.upper)}:{self._expr_to_str(expr.step)}"
    
    def _handle_tuple_expr(self, expr: ast.Tuple, *args) -> str:
        """タプル式の処理"""
        return "(" + ", ".join(self._expr_to_str(e) for e in expr.elts) + ")"
        
    def _handle_joined_str(self, expr: ast.JoinedStr, *args) -> str:
        """f文字列の処理（ディスパッチャー）"""
        return self._visit_JoinedStr(expr)
    
    def _handle_formatted_value_expr(self, expr: ast.FormattedValue, *args) -> str:
        """フォーマット値の処理"""
        return f"{self._expr_to_str(expr.value)}"
    
    def _handle_str_expr(self, expr: ast.Str, *args) -> str:
        """文字列リテラルの処理"""
        return repr(expr.s).replace("'", "")
    
    def _handle_starred_expr(self, expr: ast.Starred, *args) -> str:
        """*args式の処理"""
        value = self._expr_to_str(expr.value)
        return f"@{value}"  # Perlのリスト展開
