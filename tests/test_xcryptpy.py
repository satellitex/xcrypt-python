import pytest
from xcrypt_python.lib import Xcrypt
from xcrypt_python.formatter import format_perl_code

def test_abort_conversion():
    from sample.xcryptpy.abort import abort
    xcr_code = abort()
    expected_code = """
use base qw(core);
my $template = (
    'id@' => sub { "jobabrt_$VALUE[0]" },
    'exe0@' => sub { 'bin/fib ' . ($VALUE[0]) . " > out_$VALUE[0]" },
    'RANGE0' => [60,61,62,40,41,42],
    'initially' => sub {print ">initially> $self->{id}.\n"},
    'before' => sub {print ">>before>> $self->{id}.\n"},
    'after' => sub {print "<<after<< $self->{id}.\n"},
    'after_aborted' => sub {print "!after_aborted! $self->{id}.\n"},
    'finally' => sub {print "<finally< $self->{id}.\n"},
);
my @jobs = &prepare_submit(%template);
$jobs[0]->abort();
$jobs[1]->cancel();
$jobs[2]->invalidate();
&sync(@jobs);
$jobs[3]->abort();
$jobs[4]->cancel();
$jobs[5]->invalidate();
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_bulk_num_conversion():
    from sample.xcryptpy.bulk_num import bulk_num
    xcr_code = bulk_num()
    expected_code = """
use base qw(bulk core);
&bulk::initialize(
    'max_num' => "3",
 );
my $template = (
    'RANGE0'  => [30,40],
    'RANGE1'  => [0..4],
    'id'      => 'jobbulknum',
    'exe0'    => 'bin/fib',
    'arg0_0@' => sub {$VALUE[0] + $VALUE[1];},
);
my @jobs = &prepare(%template);
my @bulkedjobs = &bulk::bulk('bulknum', @jobs);
&submit(@bulkedjobs);
&sync(@bulkedjobs);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_customize_conversion():
    from sample.xcryptpy.customize import customize
    xcr_code = customize()
    expected_code = """
use base qw(core);
&nocheck_separator();
&set_separator('-');
&add_key('added0', 'added1');
&add_prefix_of_key('prefix');
my @jobs = &prepare(
    'id' => 'jobcustom',
    'exe0' => 'echo',
    'arg0_0' => sub { $VALUE[0]; },
    'RANGE0' => [0..3],
    'added0' => 100,
    'added1@' => sub { $VALUE[0] + 10; },
    'prefix0' => 300,
    'prefix1@' => sub { $VALUE[0] + 30; },
    ':auto0' => 0,
    ':auto1@' => sub { $VALUE[0]; },
    'unadd0' => 200,
    'unadd1@' => sub { $VALUE[0] + 20; }
);
foreach my $j (@jobs) {
    print $j->{id}."\n";
    foreach my $p (':auto0', ':auto1', 'added0', 'added1',
                   'prefix0', 'prefix1', 'unadd0', 'unadd1') {
        print "$p:\t" . $j->{"$p"} . "\n";
    }
}
&submit(@jobs);
&sync(@jobs);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_dc_conversion():
    from sample.xcryptpy.DC import DC
    xcr_code = DC()
    expected_code = """
use base qw(DC core);
use strict;
my $n = 13;
my $threshold = 10;
sub can_divde {
    my $job = shift;
    print "User function"."\n";
    if($job->{arg0_0} > $threshold) {
        return 1;
    } else {
        return 0;
    }
}
sub divide {
    my $job = shift;
    print "User Function divide"."\n";
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_dependency_conversion():
    from sample.xcryptpy.dependency import dependency
    xcr_code = dependency()
    expected_code = """
use base qw (dependency limit core);
&limit::initialize (1);
my %template = (
    'id' => 'jobdep',
    'RANGE0' => [1..5],
    'exe0' => 'bin/fib',
    'arg0_0@' => sub {44-$VALUE[0]},
);
my @jobs = prepare(%template);
$jobs[0]->{depend_on} = $jobs[4];
$jobs[2]->{depend_on} = 'jobdep_2';
$jobs[3]->{depend_on} = ['jobdep_1', 'jobdep_3'];
submit_sync (@jobs);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_fib_eval_conversion():
    from sample.xcryptpy.fib_eval import fib_eval
    xcr_code = fib_eval()
    expected_code = """
use base qw(limit core);
&limit::initialize(5);
my %job_lu = (
    'id' => 'jobfibpar',
    'RANGE0' => [1,4],
    'RANGE1' => [40,43],
    'RANGE2' => [1..3],
    'exe0' => 'bin/fib-par/fib-par',
    'JS_cpu@' => sub { $VALUE[0]; },
    'JS_node' => 1,
    'arg0_0@' => sub {"-n $VALUE[0]";},
    'arg0_1@' => sub {"-i \"1 $VALUE[1]\""},
    'JS_limit_time' => 180
);
&prepare_submit_sync(%job_lu);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_in_job_conversion():
    from sample.xcryptpy.in_job import in_job
    xcr_code = in_job()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'job_injob',
    'exe0' => 'bin/fib-file',
    'arg0_0' => 'dat/num40',
    'arg0_1' => 'out_0',
    'before_in_job' => sub { print "$self->{arg0_0}\n"; },
    'after_in_job' => sub { print "$self->{exe0}\n"; },
);
my @jobs = &prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_invalidate_conversion():
    from sample.xcryptpy.invalidate import invalidate
    xcr_code = invalidate()
    expected_code = """
use base qw(invalidate core);
my %template = (
    'RANGE0' => [3, 7, 40],
    'id@' => sub { "jobinval_$VALUE[0]" },
    'exe0' => 'bin/fib 44 > out_44',
    'allotted_time@' => sub { $VALUE[0] },
);
&prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_limit_conversion():
    from sample.xcryptpy.limit import limit
    xcr_code = limit()
    expected_code = """
use base qw(limit core);
&limit::initialize(2);
my %template = (
    'id' => 'joblmt',
    'RANGE0' => [30, 40],
    'RANGE1' => [0..4],
    'exe0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$VALUE[0]_$VALUE[1]"; },
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_mic_fib_eval_conversion():
    from sample.xcryptpy.mic_fib_eval import mic_fib_eval
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_n_section_method_conversion():
    from sample.xcryptpy.n_section_method import n_section_method
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_range_conversion():
    from sample.xcryptpy.range import range
    xcr_code = range()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'jobrng',
    'RANGE0' => [30,40],
    'RANGE1' => [0..4],
    'exe0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$VALUE[0]_$VALUE[1]"; },
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_remote_conversion():
    from sample.xcryptpy.remote import remote
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_repeat_conversion():
    from sample.xcryptpy.repeat import repeat
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_sandbox_conversion():
    from sample.xcryptpy.sandbox import sandbox
    xcr_code = sandbox()
    expected_code = """
use base qw(sandbox core);
my %template = (
    'id' => 'jobsndbox',
    'RANGE0' => [30, 40],
    'RANGE1' => [0..4],
    'exe0' => './fib',
    'linkedfile0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$VALUE[0]_$VALUE[1]"; },
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_save_conversion():
    from sample.xcryptpy.save import save
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_signal_handle_conversion():
    from sample.xcryptpy.signal_handle import signal_handle
    xcr_code = signal_handle()
    expected_code = """
use base qw(core);
sub sigint_handler {
    print "User's SIGINT handler is called.\n";
}
my %template = (
    'id' => 'jobsig',
    'RANGE0' => [30, 40],
    'RANGE1' => [0..4],
    'exe0' => './bin/fib',
    'arg0_0@' => sub { $VALUE[0] + $VALUE[1]; },
    'arg0_1@' => sub { "> out_$self->{id}"; },
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
&prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_single_conversion():
    from sample.xcryptpy.single import single
    xcr_code = single()
    expected_code = """
use base qw(core);
my %template = (
    'id' => 'jobsingle',
    'exe0' => 'bin/fib-file dat/num40 jobsingle_out',
    'JS_cpu' => 1,
    'JS_node' => 1,
    'JS_limit_time' => 300,
    'before' => sub { print "Submitting $self->{id}\n"; },
    'after' => sub { print "$self->{id} finished\n"; },
);
my @jobs = &prepare_submit_sync(%template);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_spawn_conversion():
    from sample.xcryptpy.spawn import spawn
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
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)

def test_successor_conversion():
    from sample.xcryptpy.successor import successor
    xcr_code = successor()
    expected_code = """
use base qw(successor core);
my %parent = (
    'id' => 'jobsuc_prnt',
    'exe0' => 'echo PARENT',
    'successor' => ['child1', 'child2']
);
my %child1 = (
    'id' => 'jobsuc_chld1',
    'exe0' => 'echo CHILD1'
);
my %child2 = (
    'id' => 'jobsuc_chld2',
    'exe0' => 'echo CHILD2'
);
&prepare_submit_sync(%parent);
"""
    assert format_perl_code(xcr_code) == format_perl_code(expected_code)
