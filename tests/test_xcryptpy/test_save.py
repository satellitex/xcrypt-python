import pytest
from sample.xcryptpy.save import save
from xcrypt_python.formatter import format_perl_code

def test_save_conversion():
    xcr_code = save()
    expected_code = """
use base qw(core);
use data_extractor;
my %template = (
    'id' => 'jobsave',
    'exe0' => 'bin/fib-file',
    'arg0_0' => "dat/num40",
    'arg0_1' => "jobsave_OUT",
);
my @jobs = &prepare_submit_sync(%template);
my $self = $jobs[0];
$self->restore();
if ($self->{result}) {
    print "restored: $self->{result}\n";
} else {
    my $ohandler = data_extractor->new($self->{arg0_1});
    $ohandler->extract_line_nn(1);
    $ohandler->extract_column_nn('end');
    my $output = $ohandler->execute();
    $self->{result} = $output->[0];
    print "calclated: $self->{result}\n";
    $self->save('result');
}
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
