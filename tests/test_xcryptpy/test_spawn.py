import pytest
from sample.xcryptpy.spawn import spawn
from xcrypt_python.formatter import format_perl_code

def test_spawn_conversion():
    xcr_code = spawn()
    expected_code = """
use base qw(sandbox core);
use return_transmission;
our %TEMPLATE = ();
$TEMPLATE{transfer_variable} = ['$i'];
for (my $i = 10; $i <= 20; $i++) {
    my $j = spawn {
        'id' => "jobspn$i",
        'exe0' => "../bin/fib $i > out",
        'before' => sub { print "(spawn) Submitting $self->{id}\n"; },
        'after' => sub { print "(spawn) The job $self->{id} is finished\n"; },
    };
    print "Spawned $j->{id}\n";
}
&sync();
my @jobs = ();
for (my $i = 10; $i <= 20; $i++) {
    my $j = spawn_prepare {
        'id' => "jobspn$i",
        'exe0' => "../bin/fib $i > out",
        'before' => sub { print "(spawn_prepare) Submitting $self->{id}\n"; },
        'after' => sub { print "(spawn_prepare) The job $self->{id} is finished\n"; },
    };
    print "Prepared $j->{id}\n";
    push(@jobs, $j);
}
&submit_sync(@jobs);
for (my $i = 10; $i <= 20; $i++) {
    my $j = spawn_sync {
        'id' => "jobspn$i",
        'exe0' => "../bin/fib $i > out",
        'before' => sub { print "(spawn_sync) Submitting $self->{id}\n"; },
        'after' => sub { print "(spawn_sync) The job $self->{id} is finished\n"; },
    };
    print "Completed $j->{id}\n";
    push(@jobs, $j);
}
"""
    formatted_xcr_code = format_perl_code(xcr_code).split('\n')
    formatted_expected_code = format_perl_code(expected_code).split('\n')
    for xcr_line, expected_line in zip(formatted_xcr_code, formatted_expected_code):
        assert xcr_line == expected_line
