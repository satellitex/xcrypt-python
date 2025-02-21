import pytest
from sample.xcryptpy.limit import limit
from xcrypt_python.formatter import format_perl_code

def test_limit_conversion():
    xcr_code = limit()
    expected_code = """
use base qw(limit core);
&limit::initialize(2);
my %template = (
    'id' => 'joblmt',
    'RANGE0' => [30, 40],
    'RANGE1' => [0..4],
    'exe0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$VALUE[0]_$VALUE[1]"; },
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
