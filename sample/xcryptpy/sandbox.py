from xcrypt_python.lib import Xcrypt

@Xcrypt
def sandbox():

    # A sample of the sandbox module: automatically create a directrory for each job
    # and execute jobs in the directoryies (sandboxes).
    # Derived from range.xcr:
    # * Added 'sandbox' in the use statement in the first line
    # * Added 'copiedfile0' or 'linkedfile0' parameter.
    # * (Changed the value of exe0)
    # * (Changed the value of id}
    from qw import sandbox, core

    template = {
        'id': 'jobsndbox',
        'RANGE0': [30, 40],
        'RANGE1': list(range(5)),
        'exe0': './fib',
        'linkedfile0': './bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'arg0_1@': lambda VALUE: f"> out_{VALUE[0]}_{VALUE[1]}",
        'JS_cpu': 1,
        'JS_node': 1,
        'JS_limit_time': 300,
        'before': lambda: print(f"Submitting {self['id']}"),
        'after': lambda: print(f"{self['id']} finished"),
    }
    
    core.prepare_submit_sync(template)
