from xcrypt_python.lib import Xcrypt

@Xcrypt
def job_sandbox():
    template = {
        'id': 'jobsndbox',
        'RANGE0': [30, 40],
        'RANGE1': list(range(0, 5)),
        'exe0': './fib',
        'linkedfile0': './bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'arg0_1@': lambda self: f"> out_{self['id']}",
        'JS_cpu': 1,
        'JS_node': 1,
        'JS_limit_time': 300,
        'before': lambda self: print(f"Submitting {self['id']}"),
        'after': lambda self: print(f"{self['id']} finished")
    }
    prepare_submit_sync(template)
