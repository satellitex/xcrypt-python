from xcrypt_python.lib import Xcrypt

@Xcrypt
def DC():
    # Sample of DC.pm module (Divide and Conquer)
    # Compute Fib(n) by dividing a job for Fib(n) into jobs for Fib(n-1) and Fib(n-2) recursively
    from qw import DC, core

    n = 13
    threshold = 10


    # Returns 1 (true) if the $job can be divided into equivalent multiple jobs.
    # Returns 0 (false) otherwise.
    def can_divde(job):
        print("User function")
        if job['arg0_0'] > threshold:
            return 1
        else:
            return 0

    # Divides $job into equivalent multiple jobs and returns an array of them.
    def divide(job):
        print("User Function divide")

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
        children = []
        children.append(prepare(j1))
        children.append(prepare(j2))
        print("parent: " + job['id'])
        print("child: " + children[0]['id'])
        print("child: " + children[1]['id'])
        return children

    # Merges the results of @children jobs as the result of the $parent job.
    def merge(parent, children):
        print("User Function merge")
        val = 0
        for child in children:
            ans = read_output_file(child['JS_stdout'])
            val += ans
            print("CHILD: " + child['id'] + " -> " + ans)
        OUT = open(">" + parent['JS_stdout'], "w")
        print("OUT", str(val))
        OUT.close()
        print("PARENT: " + parent['id'] + " -> " + str(val))

    def read_output_file(file):
        FH = open(file, 'r')
        line = FH.readline()
        line = line.strip()
        FH.close()
        return line

    template = {
        'id': 'jobDC',
        'exe0': "$ENV{'XCRYPT'}/sample/bin/fib-stdo",
        'arg0_0': n,
        'canDivideFunc': can_divde,
        'divideFunc': divide,
        'mergeFunc': merge,
    }

    jobs = core.prepare_submit_sync(template)
    result = read_output_file(jobs[0]['JS_stdout'])

    print("Fib(" + str(n) + ") = " + result)
