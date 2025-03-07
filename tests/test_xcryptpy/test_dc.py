import pytest
from sample.xcryptpy.DC import DC
from xcrypt_python.formatter import format_perl_code
from tests.util import normalize_whitespace

def test_dc_conversion():
    xcr_code = DC()
    expected_code = """use base qw(DC core);
my $n = 13;
my $threshold = 10;
sub can_divde {
    my $job = shift;
    print("User function");
    if($job->{arg0_0} > $threshold) {
        return 1;
    } else {
        return 0;
    }
}
sub divide {
    my $job = shift;
    print("User Function divide");
    my %j1 = (
        'id' => $job->{id}."_".($job->{arg0_0}-1),
        'exe0' => $job->{exe0},
        'arg0_0' => $job->{arg0_0}-1,
        'canDivideFunc' => $job->{canDivideFunc},
        'divideFunc' => $job->{divideFunc},
        'mergeFunc' => $job->{mergeFunc},
    );
    my %j2 = (
        'id' => $job->{id}."_".($job->{arg0_0}-2),
        'exe0' => $job->{exe0},
        'arg0_0' => $job->{arg0_0}-2,
        'canDivideFunc' => $job->{canDivideFunc},
        'divideFunc' => $job->{divideFunc},
        'mergeFunc' => $job->{mergeFunc},
    );
    my @children = ();
    push(@children, prepare(%j1));
    push(@children, prepare(%j2));
    print "parent: $job->{id}\n";
    print "child: $children[0]->{id}\n";
    print "child: $children[1]->{id}\n";
    return @children;
}
sub merge {
    my ($parent, @children) = @_;
    print "User Function merge"."\n";
    my $val = 0;
    foreach my $child (@children) {
        my $ans = read_output_file ($child->{JS_stdout});
        $val += $ans;
        print "CHILD: $child->{id} -> $ans\n";
    }
    open(OUT,">".$parent->{JS_stdout});
    print OUT "$val\n";
    close(OUT);
    print "PARENT: $parent->{id} -> $val\n";
}
sub read_output_file {
    my $file = shift;
    open(FH, '<', $file);
    my $line = <FH>;
    chomp ($line);
    close(FH);
    return $line;
}
my %template = (
    'id' => 'jobDC',
    'exe0' => "$ENV{'XCRYPT'}/sample/bin/fib-stdo",
    'arg0_0' => $n,
    'canDivideFunc' => \&can_divde,
    'divideFunc' => \&divide,
    'mergeFunc' => \&merge,
);
my @jobs = &prepare_submit_sync(%template);
my $result = read_output_file ($jobs[0]->{JS_stdout});
print "Fib($n) = $result\n";
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        normalize_line = normalize_whitespace(xcr_line)
        normalize_expected_line = normalize_whitespace(expected_line)
        assert normalize_line == normalize_expected_line, f"{normalize_line} != {normalize_expected_line}"
