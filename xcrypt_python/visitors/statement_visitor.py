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

    def visit_JoinedStr(self, node: ast.JoinedStr) -> Any:
        self.xcrypt_code.append(self._visit_JoinedStr(node))
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        関数定義を処理し、Perlの`sub`関数宣言に変換します。
        Python: def function_name(arg1, arg2=default):
        Perl: sub function_name {
            my ($arg1, $arg2) = @_;
            # デフォルト値の処理
            $arg2 = default unless defined $arg2;
            # 関数本体
        }
        """
        # 関数名を取得
        func_name = node.name
        self.current_function = func_name
        self.function_defs[func_name] = node
        
        # 関数宣言をPerlスタイルに変換
        self.xcrypt_code.append(f"sub {func_name} {{")
        
        # 引数リストを生成
        has_args = len(node.args.args) > 0
        if has_args:
            # 引数名のリスト
            arg_names = []
            for arg in node.args.args:
                if arg.arg == 'self':  # 'self'引数はスキップ
                    continue
                arg_names.append(f"${arg.arg}")
                
            if arg_names:
                # @_からの引数の割り当て
                self.xcrypt_code.append(f"    my ({', '.join(arg_names)}) = @_;")
                
                # デフォルト値の処理
                if node.args.defaults:
                    num_defaults = len(node.args.defaults)
                    num_args = len(node.args.args)
                    offset = num_args - num_defaults
                    
                    for i, default in enumerate(node.args.defaults):
                        arg_idx = i + offset
                        if arg_idx < len(node.args.args):
                            arg_name = node.args.args[arg_idx].arg
                            if arg_name != 'self':  # 'self'引数はスキップ
                                default_value = self._expr_to_str(default)
                                self.xcrypt_code.append(f"    ${arg_name} = {default_value} unless defined ${arg_name};")
        
        # 関数本体を処理
        for stmt in node.body:
            self.visit(stmt)
            
        # 関数終了
        self.xcrypt_code.append("}")
        self.current_function = None
        
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
