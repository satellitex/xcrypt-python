
from xcrypt_python.lib import Xcrypt

@Xcrypt
def customize():
    from qw import core

    nocheck_separator()
    set_separator('-')

    add_key('added0', 'added1')
    add_prefix_of_key('prefix')

    jobs: list = prepare(
        {'id': 'jobcustom',
         'exe0': 'echo',
         'arg0_0@': lambda VALUE: VALUE[0],
         'RANGE0': list(range(4)),
         'added0': 100,
         'added1@': lambda VALUE: VALUE[0] + 10,
         'prefix0': 300,
         'prefix1@': lambda VALUE: VALUE[0] + 30,
         ':auto0': 0,
         ':auto1@': lambda VALUE: VALUE[0],
         'unadd0': 200,
         'unadd1@': lambda VALUE: VALUE[0] + 20},
    )

    for job in jobs:
        print(job['id'])
        for p in [':auto0', ':auto1', 'added0', 'added1',
                  'prefix0', 'prefix1', 'unadd0', 'unadd1']:
            print(f"{p}:\t{job[p]}")

    submit(jobs)
    sync(jobs)
