# A sample of spawn{}: Multithreading language like notation for submitting jobs
from xcrypt_python.lib import Xcrypt

TEMPLATE = {}

@Xcrypt
def spwan():
    from qw import sandbox, core
    import return_transmission

    # Global variable named $i can be read (cannot be written) to from spawn bodies.
    TEMPLATE['transfer_variable'] = ['$i']

    ### spawn {}
    for i in range(10, 21):
        j = sandbox.spawn({
            'id': f'jobspn{i}',
            'exe0': f'../bin/fib {i} > out',
            'before': lambda: print(f'(spawn) Submitting {self["id"]}'),
            'after': lambda: print(f'(spawn) The job {self["id"]} is finished'),
        })

        # # You can set additional parameters as follows (like prepare())
        # # This parenthesis is optional (even 'id'!)
        # # } (id => 'jobspn', JS_cpu => 1);
        print(f'Spawned {j["id"]}')

    core.sync()

    # spawn_prepare {}
    jobs = []
    for i in range(10, 21):
        j = sandbox.spawn_prepare({
            'id': f'jobspn{i}',
            'exe0': f'../bin/fib {i} > out',
            'before': lambda: print(f'(spawn_prepare) Submitting {self["id"]}'),
            'after': lambda: print(f'(spawn_prepare) The job {self["id"]} is finished'),
        })
        print(f'Prepared {j["id"]}')
        jobs.append(j)
    core.submit_sync(jobs)



    # spawn_sync {}
    for i in range(10, 21):
        j = sandbox.spawn_sync({
            'id': f'jobspn{i}',
            'exe0': f'../bin/fib {i} > out',
            'before': lambda: print(f'(spawn_sync) Submitting {self["id"]}'),
            'after': lambda: print(f'(spawn_sync) The job {self["id"]} is finished'),   
        })
        print(f'Completed {j["id"]}')
        jobs.append(j)
