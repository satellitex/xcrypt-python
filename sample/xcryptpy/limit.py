from xcrypt.lib import Xcrypt

@Xcrypt
def limit():
    # A sample of the limit module: limits the number of simultaneously running jobs.
    # Derived from range.xcr:
    # * Added 'limit' in the use statement in the first line
    # * Added limit::initalize before defining and submitting jobs.
    # * (Changed the value of id}
    from qw import limit, core

    # Set the limit number of simultaneously running jobs
    limit.initialize(2);

    template = {
        'id': 'joblmt',
        'RANGE0': [30, 40],
        'RANGE1': list(range(5)),
        'exe0': './bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'arg0_1@': lambda VALUE: f"> out_{VALUE[0]}_{VALUE[1]}",
        'JS_cpu': 1,
        'JS_node': 1,
        'JS_limit_time': 300,
        'before': lambda: print(f"Submitting {self['id']}"),
        'after': lambda: print(f"{self['id']} finished")
    }

    core.prepare_submit_sync(template)
