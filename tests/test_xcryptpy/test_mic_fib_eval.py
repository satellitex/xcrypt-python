import pytest
from sample.xcryptpy.mic_fib_eval import mic_fib_eval
from xcrypt_python.formatter import format_perl_code

def test_mic_fib_eval_conversion():
    xcr_code = mic_fib_eval()
    expected_code = """
use base qw(limit core);
&limit::initialize(5);
my %template = (
    'id' => 'jobfibpar',
    'RANGE0' => [1,4,8,16,32,60],
    'RANGE1' => [43],
    'RANGE2' => [1..3],
    'exe0' => 'aprun -k -n $LSB_PROCS_MIC -d $LSB_CPUS_MIC -N $LSB_PPN_MIC ./bin/fib-par/fib-par-mic',
    'JS_mic_node' => 1,
    'JS_mic_cpu@' => sub { $VALUE[0]; },
    'JS_mic_thread@' => sub { $VALUE[0]; },
    'arg0_0@' => sub { "-n $VALUE[0]"; },
    'arg0_1@' => sub { '-i "1 $VALUE[1]"'; },
    'JS_limit_time' => 180
);
&prepare_submit_sync(%template);
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
