import pytest
from sample.xcryptpy.n_section_method import n_section_method
from xcrypt_python.formatter import format_perl_code

def test_n_section_method_conversion():
    xcr_code = n_section_method()
    expected_code = """
use base qw(sandbox n_section_method core);
use data_generator;
use data_extractor;
&n_section_method::del_extra_job();
my %job = (
    'id' => 'jobnsec',
    'exe0' => './minushalf.pl template.dat',
    'linkedfile0' => 'bin/minushalf.pl',
    'before' => sub { data_generator('dat/template.dat', "$self->{id}/template.dat")->replace_key_value("param", $self->{x})->execute(); },
    'after' => sub { data_extractor("$self->{id}/output.dat")->extract_line_nn('end')->execute()->[0]; },
);
my ($x, $y) = &n_section_method::n_section_method(\%job, 12, 0.01, -1, 10, 0.5, -5);
print "The value is $y when x = $x.\n";
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
