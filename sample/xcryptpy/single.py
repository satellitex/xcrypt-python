from xcrypt_python.lib import Xcrypt

template = {
    'id': 'jobsingle',
    'exe0': 'bin/fib-file dat/num40 jobsingle_out',
    'JS_cpu': 1,
    'JS_node': 1,
    'JS_limit_time': 300,
    'before': lambda self: print(f"Submitting {self['id']}"),
    'after': lambda self: print(f"{self['id']} finished")
}

@Xcrypt
def prepare_submit_sync(template):
    jobs = []
    jobs = core.prepare_submit_sync(template)
    return jobs

jobs = prepare_submit_sync(template)
