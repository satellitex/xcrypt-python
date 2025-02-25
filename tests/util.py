import pytest
import re
from xcrypt_python.formatter import format_perl_code

def normalize_whitespace(text):
    """
    スペース、タブ、改行を単一のスペースに正規化し、前後の空白を削除。
    """
    # すべての連続する空白（スペース、タブ、改行など）を1つのスペースに置換
    return re.sub(r'\s+', ' ', text).strip()

def assert_code_equal(xcr_code, expected_code):
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        normalize_line = normalize_whitespace(xcr_line)
        normalize_expected_line = normalize_whitespace(expected_line)
        assert normalize_line == normalize_expected_line
