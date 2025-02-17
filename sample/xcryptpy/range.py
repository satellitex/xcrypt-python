from xcrypt_python.lib import Xcrypt

@Xcrypt
def submit_job():
    template = {
        'id': 'jobrng',
        'RANGE0': [30,40],
        'RANGE1': list(range(5)),
        'exe0': './bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'arg0_1@': lambda VALUE: f"> out_{VALUE[0]}_{VALUE[1]}",
        'JS_cpu': 1,
        'JS_node': 1,
        'JS_limit_time': 300,
        'before': lambda self: print(f"Submitting {self['id']}"),
        'after': lambda self: print(f"{self['id']} finished")
    }
    prepare_submit_sync(template)
