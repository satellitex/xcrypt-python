
from xcrypt_python.lib import Xcrypt

@Xcrypt
def customize():
    from qw import core

    core.nocheck_separator()
    core.set_separator('-')

    core.add_key('added0', 'added1')
    core.add_prefix_of_key('prefix')

    jobs = core.prepare(
        {'id': 'jobcustom',
         'exe0': 'echo',
         'arg0_0': lambda value: value[0],
         'RANGE0': list(range(4)),
         'added0': 100,
         'added1': lambda value: value[0] + 10,
         'prefix0': 300,
         'prefix1': lambda value: value[0] + 30,
         ':auto0': 0,
         ':auto1': lambda value: value[0],
         'unadd0': 200,
         'unadd1': lambda value: value[0] + 20},
    )

    for job in jobs:
        print(job['id'])
        for p in [':auto0', ':auto1', 'added0', 'added1',
                  'prefix0', 'prefix1', 'unadd0', 'unadd1']:
            print(f"{p}:\t{job[p]}")

    core.submit(*jobs)
    core.sync(*jobs)
