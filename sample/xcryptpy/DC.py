from xcrypt_python.lib import Xcrypt

@Xcrypt
def DC():
    # Sample of DC.pm module (Divide and Conquer)
    # Compute Fib(n) by dividing a job for Fib(n) into jobs for Fib(n-1) and Fib(n-2) recursively
    from qw import DC, core

    n = 13;
    threshold = 10;


    # Returns 1 (true) if the $job can be divided into equivalent multiple jobs.
    # Returns 0 (false) otherwise.
    def can_divde(job):
        print("User function"+"\n");
        if job['arg0_0'] > threshold:
            return 1
        else:
            return 0

    # Divides $job into equivalent multiple jobs and returns an array of them.
    def divide(job):
        print("User Function divide"+"\n");

        j1 = {
            'id': job['id']+"_"+str(job['arg0_0']-1),
            'exe0': job['exe0'],
            'arg0_0': job['arg0_0']-1,
            'canDivideFunc': job['canDivideFunc'],
            'divideFunc': job['divideFunc'],
            'mergeFunc': job['mergeFunc'],
        }
        j2 = {
            'id': job['id']+"_"+str(job['arg0_0']-2),
            'exe0': job['exe0'],
            'arg0_0': job['arg0_0']-2,
            'canDivideFunc': job['canDivideFunc'],
            'divideFunc': job['divideFunc'],
            'mergeFunc': job['mergeFunc'],
        }
        children = [];
        children.append(core.prepare(j1));
        children.append(core.prepare(j2));
        print("parent: "+job['id']+"\n");
        print("child: "+children[0]['id']+"\n");
        print("child: "+children[1]['id']+"\n");
        return children

    # Merges the results of @children jobs as the result of the $parent job.
    def merge(parent, children):
        print("User Function merge"+"\n");
        val = 0;
        for child in children:
            ans = read_output_file(child['JS_stdout']);
            val += ans;
            print("CHILD: "+child['id']+" -> "+ans+"\n");
        with open(parent['JS_stdout'], 'w') as OUT:
            OUT.write(str(val)+"\n");
        print("PARENT: "+parent['id']+" -> "+val+"\n");

    def read_output_file(file):
        with open(file, 'r') as FH:
            line = FH.readline();
            return line.strip();


    template = {
        'id': 'jobDC',
        'exe0': "$ENV{'XCRYPT'}/sample/bin/fib-stdo",
        'arg0_0': n,
        'canDivideFunc': can_divde,
        'divideFunc': divide,
        'mergeFunc': merge,
    }

    # my @jobs = &prepare_submit_sync(%template);
    jobs = core.prepare_submit_sync(template);
    # my $result = read_output_file ($jobs[0]->{JS_stdout});
    result = read_output_file(jobs[0]['JS_stdout']);

    # print "Fib($n) = $result\n";
    print("Fib("+str(n)+") = "+result+"\n");

