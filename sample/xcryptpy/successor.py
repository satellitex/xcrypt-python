# Import xcrypt library
from xcrypt_python.lib import Xcrypt

# A sample of the successor module:
# Defining a job which depend on other jobs.

@Xcrypt
def prepare_submit_sync():
    parent = {
        'id': 'jobsuc_prnt',
        'exe0': 'echo PARENT',
        # 'child1' and 'child2' are automatically submitted after the job is done.
        'successor': ['child1', 'child2']
    }
    child1 = {
        'id': 'jobsuc_chld1',
        'exe0': 'echo CHILD1',
    }
    child2 = {
        'id': 'jobsuc_chld2',
        'exe0': 'echo CHILD2',
    }

    # Submit and synchronize jobs
    core.prepare_submit_sync(parent, child1, child2)

# Call the function to prepare and submit jobs
prepare_submit_sync()
