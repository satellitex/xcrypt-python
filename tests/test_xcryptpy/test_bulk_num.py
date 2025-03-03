import pytest
from sample.xcryptpy.bulk_num import bulk_num
from xcrypt_python.formatter import format_perl_code
from tests.util import normalize_whitespace

def test_bulk_num_conversion():
    xcr_code = bulk_num()
    expected_code = """use base qw(bulk core);
bulk::initialize( 'max_num', '3' );
my %template = (
    'RANGE0'  => [ 30,40 ],
    'RANGE1'  => [ 0..4 ],
    'id'      => 'jobbulknum',
    'exe0'    => 'bin/fib',
    'arg0_0@' => sub {$VALUE[0] + $VALUE[1]}
);
my @jobs = prepare(%template);
my @bulked_jobs = bulk::bulk('bulknum', @jobs);
submit(@bulked_jobs);
sync(@bulked_jobs);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        normalize_line = normalize_whitespace(xcr_line)
        normalize_expected_line = normalize_whitespace(expected_line)
        assert normalize_line == normalize_expected_line, f"{normalize_line} != {normalize_expected_line}"
