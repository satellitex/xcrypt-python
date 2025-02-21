import pytest
from sample.xcryptpy.remote import remote
from xcrypt_python.formatter import format_perl_code

def test_remote_conversion():
    xcr_code = remote()
    expected_code = """
use base qw(core);
my $default = &get_local_env();
my $env0 = &add_host(
    'host' => 'foo@bar1',
    'sched' => 'sh',
    'wd' => '/home/foo/xcrypt/sample',
    'xd' => '/home/foo/xcrypt'
);
my $env1 = &add_host(
    'host' => 'foo@bar2',
    'sched' => 't2k_tsukuba'
);
my $env2 = &add_host(
    'host' => 'foo@bar3',
    'sched' => 't2k_tokyo'
);
my $env3 = &add_host(
    'host' => 'foo@bar3',
    'sched' => 't2k_kyoto'
);
my %template = (
    'id' => 'jobremote',
    'JS_cpu' => 1,
    'JS_memory' => '1GB',
    'JS_queue@' => [' ', 'ESCIENCE', 'debug', 'gh', ' '],
    'JS_group' => 'gh',
    'JS_limit_time' => 300,
    'exe0@' => sub { "echo $VALUE[0] > job4_$VALUE[0]"; },
    'RANGE0' => [0, 1, 2, 3, 4],
    'env@' => [$env0, $env1, $env2, $env3, $default],
);
&prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
