import pytest
from sample.xcryptpy.signal_handle import signal_handle
from xcrypt_python.formatter import format_perl_code

def test_signal_handle_conversion():
    xcr_code = signal_handle()
    expected_code = """
use base qw(core);
sub sigint_handler {
    print "User's SIGINT handler is called.\n";
}
my %template = (
    'id' => 'jobsig',
    'RANGE0' => [30, 40],
    'RANGE1' => [0..4],
    'exe0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$self->{id}"; },
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
