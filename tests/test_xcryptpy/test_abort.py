import pytest
from sample.xcryptpy.abort import abort
from xcrypt_python.formatter import format_perl_code

def test_abort_conversion():
    xcr_code = abort()
    expected_code = """
use base qw(core);
my $template = (
    'id@' => sub { "jobabrt_$VALUE[0]" },
    'exe0@' => sub { 'bin/fib ' . ($VALUE[0]) . " > out_$VALUE[0]" },
    'RANGE0' => [60,61,62,40,41,42],
    'initially' => sub {print ">initially> $self->{id}.\n"},
    'before' => sub {print ">>before>> $self->{id}.\n"},
    'after' => sub {print "<<after<< $self->{id}.\n"},
    'after_aborted' => sub {print "!after_aborted! $self->{id}.\n"},
    'finally' => sub {print "<finally< $self->{id}.\n"},
);
my @jobs = &prepare_submit(%template);
$jobs[0]->abort();
$jobs[1]->cancel();
$jobs[2]->invalidate();
&sync(@jobs);
$jobs[3]->abort();
$jobs[4]->cancel();
$jobs[5]->invalidate();
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
