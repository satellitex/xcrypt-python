import pytest
from sample.xcryptpy.successor import successor
from xcrypt_python.formatter import format_perl_code

def test_successor_conversion():
    xcr_code = successor()
    expected_code = """
use base qw(successor core);
my %parent = (
    'id' => 'jobsuc_prnt',
    'exe0' => 'echo PARENT',
    'successor' => ['child1', 'child2']
);
my %child1 = (
    'id' => 'jobsuc_chld1',
    'exe0' => 'echo CHILD1'
);
my %child2 = (
    'id' => 'jobsuc_chld2',
    'exe0' => 'echo CHILD2'
);
&prepare_submit_sync(%parent);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
