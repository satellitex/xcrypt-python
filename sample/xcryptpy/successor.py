Python Code:

```python
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
    job_submit_sync(parent)

# Call the function to prepare and submit jobs
prepare_submit_sync()
```
Please note:

1. The Perl function prepare_submit_sync is replaced with a Python function having the same name.

2. Perl hashes (%) are replaced with Python dictionaries.

3. Perl arrays (@) are replaced with Python lists.

4. The function call &prepare_submit_sync(%parent); is replaced with the Python equivalent prepare_submit_sync().