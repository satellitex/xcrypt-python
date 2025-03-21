"""
Xcryptライブラリのメインモジュール。
PythonコードをXcrypt（Perlベース）コードに変換するための機能を提供します。
"""

import ast
import inspect
import functools
from typing import Callable, Any
from xcrypt_python.transformer import execute
from xcrypt_python.formatter import format_perl_code


def Xcrypt(func: Callable) -> Callable:
    """
    Python関数をXcrypt（Perlベース）コードに変換するデコレータ。
    
    引数:
        func: 変換する関数
        
    戻り値:
        変換されたコードを返すラッパー関数
    """
    source = inspect.getsource(func)
    tree = ast.parse(source)

    @functools.wraps(func)
    def wrapper() -> str:
        xcr = format_perl_code(execute(tree))
        print(xcr)
        return xcr
    
    return wrapper
