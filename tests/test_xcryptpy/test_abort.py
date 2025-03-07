import pytest
from sample.xcryptpy.abort import abort
from xcrypt_python.formatter import format_perl_code
from tests.util import normalize_whitespace

def test_abort_conversion():
    xcr_code = abort()
    expected_code = """use base qw(core);
my %template1 = (
    'id@' => sub { sprintf( "jobabrt_%s", $VALUE[0] ) },
    'exe0@' => sub { sprintf( "bin/fib %s > out_%s", $VALUE[0], $VALUE[0] ) },
    'RANGE0' => [ 60, 61, 62, 40, 41, 42 ],
    'initially' => sub { print( sprintf( ">initially> %s.", $self->{id} ) ) },
    'before' => sub { print( sprintf( ">>before>> %s.", $self->{id} ) ) },
    'after' => sub { print( sprintf( "<<after<< %s.", $self->{id} ) ) },
    'after_aborted' => sub { print( sprintf("!after_aborted! %s.", $self->{id} ) ) },
    'finally' => sub { print( sprintf("<finally< %s.", $self->{id} ) ) }
);
my @jobs = prepare_submit(%template1);
$jobs[0]->abort();
$jobs[1]->cancel();
$jobs[2]->invalidate();
sync(@jobs);
$jobs[3]->abort();
$jobs[4]->cancel();
$jobs[5]->invalidate();
"""

    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        normalize_line = normalize_whitespace(xcr_line)
        normalize_expected_line = normalize_whitespace(expected_line)
        assert normalize_line == normalize_expected_line, f"{normalize_line} != {normalize_expected_line}"

