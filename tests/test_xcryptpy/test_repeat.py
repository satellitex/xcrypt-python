import pytest
from sample.xcryptpy.repeat import repeat
from xcrypt_python.formatter import format_perl_code

def test_repeat_conversion():
    xcr_code = repeat()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'jobrep',
    'exe0' => 'sleep 10'
);
my @jobs = &prepare_submit(%template);
&repeat('print "foo\n";');
my $bar = 'baz';
&repeat(sub { print "$bar\n"; }, 3);
&sync(@jobs);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
