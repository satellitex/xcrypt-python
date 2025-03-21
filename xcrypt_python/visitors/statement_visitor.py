"""
文のAST訪問者クラス。
Python文をXcrypt（Perlベース）コードに変換するための機能を提供します。
"""

import ast
from typing import List, Dict, Any, Optional, Union
from xcrypt_python.visitors.expression_visitor import ExpressionVisitor


class StatementVisitor(ExpressionVisitor):
    """
    文のAST訪問者クラス。
    Python文をXcrypt（Perlベース）コードに変換するための機能を提供します。
    """

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
        self.xcrypt_code.append(f"my {targets[0]} = {value};")



    def visit_Call(self, node: ast.Call) -> None:
        """
        関数呼び出しを処理し、適切なPerl構文に変換します。
        ルールに従って値渡しと参照渡しを使い分けます:
        1. sample/ にある関数や Perl の標準関数へは値渡しを使う。
        2. スカラー値は値渡しを行う
        3. スカラー値以外は参照渡しを行う
        """
        # 特殊なパターンまたはデフォルト処理を使って関数呼び出しを変換
        call_str = self._process_function_call(node)
        self.xcrypt_code.append(call_str)
        
    def _process_function_call(self, node: ast.Call) -> str:
        """関数呼び出しをPerl形式に処理します"""
        # 特殊な呼び出しハンドラを順番に試す
        for handler in [self._visit_call_attribute, self._visit_call_list_range, self._visit_call_args_dict]:
            result = handler(node)
            if result:
                return result
                
        # どの特殊パターンにもマッチしない場合はデフォルト処理
        return self._process_standard_function_call(node)
        
    def _process_standard_function_call(self, node: ast.Call) -> str:
        """標準的な関数呼び出しを処理します"""
        func_name = self._expr_to_str(node.func, is_function=True)
        is_sample_func = self._is_sample_or_standard_func(node.func)
        
        args_list = []
        for arg in node.args:
            if isinstance(arg, ast.Name):
                args_list.append(self._format_name_arg(arg.id, is_sample_func))
            else:
                # リテラルや式の場合はそのまま渡す
                args_list.append(self._expr_to_str(arg))
        
        args = ", ".join(args_list)
        return f"{func_name}({args});"
    
    def _format_name_arg(self, arg_id: str, is_sample_func: bool) -> str:
        """関数引数の名前を適切なPerl形式にフォーマットします"""
        var_type = self.variable_types.get(arg_id, "scalar")
        
        if is_sample_func:
            # sample/関数やPerl標準関数: 値渡し
            if var_type == "dict":
                return f"%{arg_id}"
            elif var_type == "list":
                return f"@{arg_id}"
            else:
                return f"${arg_id}"
        else:
            # その他の関数:
            if var_type == "scalar":
                # スカラー値: 値渡し
                return f"${arg_id}"
            else:
                # 非スカラー値: 参照渡し
                if var_type == "dict":
                    return f"\\%{arg_id}"
                elif var_type == "list":
                    return f"\\@{arg_id}"
                else:
                    return f"\\${arg_id}"

    def visit_For(self, node: ast.For) -> None:
        """
        forループを処理し、Perlのforeachシンタックスに変換します。
        """
        target = self._expr_to_str(node.target)
        iter_expr = self._process_for_iterator(node.iter)
        
        self.xcrypt_code.append(f"foreach my {target} ({iter_expr}) {{")
        self.generic_visit(node)
        self.xcrypt_code.append("}")
        
    def _process_for_iterator(self, iter_node: ast.AST) -> str:
        """for文のイテレータを処理します"""
        # range関数を特別扱い
        if isinstance(iter_node, ast.Call) and isinstance(iter_node.func, ast.Name) and iter_node.func.id == 'range':
            return self._process_range_iterator(iter_node)
        else:
            return self._expr_to_str(iter_node)
            
    def _process_range_iterator(self, range_node: ast.Call) -> str:
        """range()呼び出しをPerl範囲構文に変換します"""
        args = range_node.args
        
        if len(args) == 1:
            # range(n) => [0..n-1]
            end = int(self._expr_to_str(args[0]))
            return f"[ 0..{end-1} ]"
        elif len(args) == 2:
            # range(start, end) => [start..end-1]
            start = self._expr_to_str(args[0])
            end = int(self._expr_to_str(args[1]))
            return f"[ {start}..{end-1} ]"
        elif len(args) == 3:
            # range(start, end, step) => [start..end-1]
            # (Perlではステップ指定は単純な範囲で近似)
            start = self._expr_to_str(args[0])
            end = int(self._expr_to_str(args[1]))
            return f"[ {start}..{end-1} ]"
        else:
            return self._expr_to_str(range_node)

    def visit_FormattedValue(self, node: ast.FormattedValue) -> None:
        """
        f文字列内のフォーマット値を処理します。
        """
        self.xcrypt_code.append(self._expr_to_str(node.value))
        self.generic_visit(node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> Any:
        self.xcrypt_code.append(self._visit_JoinedStr(node))
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        関数定義を処理し、Perlの`sub`関数宣言に変換します。
        Pythonでは変数が参照渡しとして扱われるため、Perlでもリファレンスとして扱います。
        テスト互換性のために、Perlでは参照を使用していますが、名前は元のままにしています。
        """
        # 関数の状態を設定
        func_name = node.name
        self.current_function = func_name
        self.function_defs[func_name] = node
        
        # 関数宣言を追加
        self.xcrypt_code.append(f"sub {func_name} {{")
        
        # 引数を処理
        self._process_function_parameters(node.args)
        
        # 関数本体を処理
        for stmt in node.body:
            self.visit(stmt)
            
        # 関数終了
        self.xcrypt_code.append("}")
        self.current_function = None
        
    def _process_function_parameters(self, args_info) -> None:
        """関数の引数を処理します"""
        # 引数がなければ何もしない
        if not args_info.args:
            return
            
        # 引数名のリスト (self引数を除く)
        arg_names = []
        for arg in args_info.args:
            if arg.arg != 'self':
                arg_names.append(f"${arg.arg}")
                
        if not arg_names:
            return
            
        # パラメータの宣言を追加
        self.xcrypt_code.append(f"    my ({', '.join(arg_names)}) = @_;")
        
        # デフォルト値を処理
        self._process_default_parameters(args_info.args, args_info.defaults)
    
    def _process_default_parameters(self, args, defaults) -> None:
        """デフォルト引数値を処理します"""
        if not defaults:
            return
            
        num_defaults = len(defaults)
        num_args = len(args)
        offset = num_args - num_defaults
        
        for i, default in enumerate(defaults):
            arg_idx = i + offset
            if arg_idx < num_args:
                arg_name = args[arg_idx].arg
                if arg_name != 'self':  # 'self'引数はスキップ
                    default_value = self._expr_to_str(default)
                    self.xcrypt_code.append(f"    ${arg_name} = {default_value} unless defined ${arg_name};")
        
    def visit_Return(self, node: ast.Return) -> None:
        """
        return文を処理し、Perlのreturn文に変換します。
        Python: return value
        Perl: return value;
        """
        if node.value:
            value = self._expr_to_str(node.value)
            self.xcrypt_code.append(f"    return {value};")
        else:
            self.xcrypt_code.append("    return;")
            
    def visit_If(self, node: ast.If) -> None:
        """
        if文を処理し、Perlのif文に変換します。
        Python: if condition: ... else: ...
        Perl: if (condition) { ... } else { ... }
        """
        condition = self._expr_to_str(node.test)
        self.xcrypt_code.append(f"if ({condition}) {{")
        
        # ifブロックの本体
        for stmt in node.body:
            self.visit(stmt)
        
        # elseブロックがある場合
        if node.orelse:
            self.xcrypt_code.append("} else {")
            for stmt in node.orelse:
                self.visit(stmt)
        
        self.xcrypt_code.append("}")
