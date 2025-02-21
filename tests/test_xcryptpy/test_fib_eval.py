import pytest
from sample.xcryptpy.fib_eval import fib_eval
from xcrypt_python.formatter import format_perl_code

def test_fib_eval_conversion():
    xcr_code = fib_eval()
    expected_code = """
use base qw(limit core);
&limit::initialize(5);
my %job_lu = (
    'id' => 'jobfibpar',
    'RANGE0' => [1,4],
    'RANGE1' => [40,43],
    'RANGE2' => [1..3],
    'exe0' => 'bin/fib-par/fib-par',
    'JS_cpu@' => sub { $VALUE[0]; },
    'JS_node' => 1,
    'arg0_0@' => sub {"-n $VALUE[0]";},
    'arg0_1@' => sub {"-i \"1 $VALUE[1]\""},
    'JS_limit_time' => 180
);
&prepare_submit_sync(%job_lu);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
