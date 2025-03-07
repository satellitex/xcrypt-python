# Submit just a single job.
from xcrypt_python.lib import Xcrypt

@Xcrypt
def single():
    from qw import core

    template = {
        'id': 'jobsingle',
        'exe0': 'bin/fib-file dat/num40 jobsingle_out',
        'JS_cpu': 1,
        'JS_node': 1,
        'JS_limit_time': 300,
        'before': lambda: print(f"Submitting {self['id']}"),
        'after': lambda: print(f"{self['id']} finished")
    }

    # Execute the job
    jobs = core.prepare_submit_sync(template)