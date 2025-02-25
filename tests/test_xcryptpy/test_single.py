import pytest
from sample.xcryptpy.single import single
from xcrypt_python.formatter import format_perl_code

def test_single_conversion():
    xcr_code = single()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'jobsingle',
    'exe0' => 'bin/fib-file dat/num40 jobsingle_out',
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
my @jobs = &prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
