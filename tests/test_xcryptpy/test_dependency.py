import pytest
from sample.xcryptpy.dependency import dependency
from xcrypt_python.formatter import format_perl_code

def test_dependency_conversion():
    xcr_code = dependency()
    expected_code = """
use base qw (dependency limit core);
&limit::initialize (1);
my %template = (
    'id' => 'jobdep',
    'RANGE0' => [1..5],
    'exe0' => 'bin/fib',
    'arg0_0@' => sub {44-$VALUE[0]},
);
my @jobs = prepare(%template);
$jobs[0]->{depend_on} = $jobs[4];
$jobs[2]->{depend_on} = 'jobdep_2';
$jobs[3]->{depend_on} = ['jobdep_1', 'jobdep_3'];
submit_sync (@jobs);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
