# A sample of taking performance evaluation using Xcrypt and a parallel implementation of Fibonacci
from xcrypt_python.lib import Xcrypt

# Uncomment if your system does not support a batch scheduler.
@Xcrypt
def fib_eval():
    from qw import limit, core
    limit.initialize(5)

    job_lu = {
        'id': 'jobfibpar',
        'RANGE0': [1, 4],  # # of workers
        'RANGE1': [40, 43],  # fib's param (problem size)
        'RANGE2': list(range(1, 4)),  # # of trials
        'exe0': 'bin/fib-par/fib-par',
        'JS_cpu@': lambda VALUE: VALUE[0],  # # of cpus requested to a batch scheduler
        'JS_node': 1,  # # of nodes requested to a batch scheduler
        'arg0_0@': lambda VALUE: f"-n {VALUE[0]}",
        'arg0_1@': lambda VALUE: f"-i \"1 {VALUE[1]}\"",
        'JS_limit_time': 180  # Estimated job execution time sent to a batch scheduler
    }

    core.prepare_submit_sync(job_lu)
