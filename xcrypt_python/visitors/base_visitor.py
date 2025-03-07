"""
基本的なAST訪問者クラス。
PythonコードをXcrypt（Perlベース）コードに変換するための基本機能を提供します。
"""

import ast
from typing import List, Dict, Any, Optional, Union


class BaseVisitor(ast.NodeVisitor):
    """
    AST Visitor の基本クラス。
    PythonコードをXcrypt（Perlベース）コードに変換するための基本機能を提供します。
    """
    def __init__(self):
        self.xcrypt_code: List[str] = []  # 生成されたXcryptコード
        self.imported_modules: List[str] = []  # インポートされたモジュール
        self.variable_types: Dict[str, str] = {}  # 変数の型情報
        self.standard_functions: List[str] = ["print", "sprintf", "printf"]  # 標準関数
        self.function_defs: Dict[str, ast.FunctionDef] = {}  # 関数定義を保存
        self.current_function: Optional[str] = None  # 現在処理中の関数名

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
