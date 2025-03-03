import pytest
from sample.xcryptpy.customize import customize
from xcrypt_python.formatter import format_perl_code
from tests.util import normalize_whitespace

def test_customize_conversion():
    xcr_code = customize()
    expected_code = """use base qw(core);
nocheck_separator();
set_separator('-');
add_key('added0', 'added1');
add_prefix_of_key('prefix');
my @jobs = prepare(
    'id' => 'jobcustom',
    'exe0' => 'echo',
    'arg0_0@' => sub { $VALUE[0] },
    'RANGE0' => [0..3],
    'added0' => 100,
    'added1@' => sub { $VALUE[0] + 10 },
    'prefix0' => 300,
    'prefix1@' => sub { $VALUE[0] + 30 },
    ':auto0' => 0,
    ':auto1@' => sub { $VALUE[0] },
    'unadd0' => 200,
    'unadd1@' => sub { $VALUE[0] + 20 }
);
foreach my $job (@jobs) {
    print ( $job['id'] );
    foreach my $p (
    [
    ':auto0', ':auto1', 'added0', 'added1',
                   'prefix0', 'prefix1', 'unadd0', 'unadd1'
                   ]
                   )
                     {
        print( sprintf( "%s:\t%s", $p, $job[$p] ) );
    }
}
submit(@jobs);
sync(@jobs);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        normalize_line = xcr_line.strip()
        normaluze_expected_line = expected_line.strip()
        assert normalize_line == normaluze_expected_line, f"{normalize_line} != {normaluze_expected_line}"
