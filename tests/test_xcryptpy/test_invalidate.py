import pytest
from sample.xcryptpy.invalidate import invalidate
from xcrypt_python.formatter import format_perl_code

def test_invalidate_conversion():
    xcr_code = invalidate()
    expected_code = """
use base qw(invalidate core);
my %template = (
    'RANGE0' => [3, 7, 40],
    'id@' => sub { "jobinval_$VALUE[0]" },
    'exe0' => 'bin/fib 44 > out_44',
    'allotted_time@' => sub { $VALUE[0] },
);
&prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
