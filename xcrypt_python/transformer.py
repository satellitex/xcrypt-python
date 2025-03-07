"""
AST変換モジュール。
PythonコードをXcrypt（Perlベース）コードに変換するためのメインロジックを提供します。
"""

import ast
from typing import Dict, Any
from xcrypt_python.visitors.statement_visitor import StatementVisitor


class XcryptTransformer:
    """
    AST変換クラス。
    PythonコードをXcrypt（Perlベース）コードに変換します。
    """
    def __init__(self):
        self.visitor = StatementVisitor()

    def transform(self, tree: ast.AST) -> str:
        """
        ASTをXcryptコードに変換します。
        
        引数:
            tree: 変換するAST
            
        戻り値:
            生成されたXcryptコード（文字列）
        """
        return self.visitor.transform(tree)


def execute(tree: ast.AST) -> str:
    """
    ASTをXcryptコードに変換します。
    
    引数:
        tree: 変換するAST
        
    戻り値:
        生成されたXcryptコード（文字列）
    """
    # デコレータ関数の場合、関数定義を取り除いて内容だけを返す
    if isinstance(tree, ast.Module) and len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef):
        func_def = tree.body[0]
        func_name = func_def.name
        
        # 関数本体だけを含む新しいASTを作成
        new_tree = ast.Module(body=func_def.body, type_ignores=[])
        transformer = XcryptTransformer()
        xcrypt_code = transformer.transform(new_tree)
        
        
        return xcrypt_code
    else:
        transformer = XcryptTransformer()
        xcrypt_code = transformer.transform(tree)
        return xcrypt_code
