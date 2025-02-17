Below is the equivalent Python code for the provided Perl code:

```python
# Import necessary xcrypt library
from xcrypt_python.lib import Xcrypt

@Xcrypt
def job_submission():
    default = get_local_env()
    env0 = add_host({'host': 'foo@bar1',
                     'sched': 'sh',
                     'wd': '/home/foo/xcrypt/sample',
                     'xd': '/home/foo/xcrypt'})
    env1 = add_host({'host': 'foo@bar2',
                     'sched': 't2k_tsukuba'})
    env2 = add_host({'host': 'foo@bar3',
                     'sched': 't2k_tokyo'})
    env3 = add_host({'host': 'foo@bar3',
                     'sched': 't2k_kyoto'})

    template = {
        'id': 'jobremote',
        'JS_cpu': '1',
        'JS_memory': '1GB',
        'JS_queue': [' ', 'ESCIENCE', 'debug', 'gh', ' '],
        'JS_group': 'gh',  # for t2k-kyoto only
        'JS_limit_time': 300,
        'exe0': lambda value: f"echo {value[0]} > job4_{value[0]}",
        'RANGE0': [0, 1, 2, 3, 4],
        'env': [env0, env1, env2, env3, default],
    }
    prepare_submit_sync(template)

# Call the function
job_submission()
```

Please note: Python doesn't have the exact equivalent of Perl's sub syntax, a lambda function is used in this conversion, be sure that the usage fits appropriately.