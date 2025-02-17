# A sample of the successor module:
# Defining a job which depend on other jobs.
from xcrypt_python.lib import Xcrypt


@Xcrypt
def successor():
    from qw import successor, core

    parent = {
        'id': 'jobsuc_prnt',
        'exe0': 'echo PARENT',
        'successor': ['child1', 'child2']
    }
    child1 = {
        'id': 'jobsuc_chld1',
        'exe0': 'echo CHILD1'
    }
    child2 = {
        'id': 'jobsuc_chld2',
        'exe0': 'echo CHILD2'
    }

    core.prepare_submit_sync(parent)


