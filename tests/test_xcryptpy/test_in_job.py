import pytest
from sample.xcryptpy.in_job import in_job
from xcrypt_python.formatter import format_perl_code

def test_in_job_conversion():
    xcr_code = in_job()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'job_injob',
    'exe0' => 'bin/fib-file',
    'arg0_0' => 'dat/num40',
    'arg0_1' => 'out_0',
    'before_in_job' => sub { print "$self->{arg0_0}\n"; },
    'after_in_job' => sub { print "$self->{exe0}\n"; },
);
my @jobs = &prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
