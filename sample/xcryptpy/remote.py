from xcrypt_python.lib import Xcrypt

@Xcrypt
def remote():
    # A sample of remote job submission.
    # Four jobs are submitted in the four differnt systems.
    # You need to install Xcrypt in the systems to which you can login by OpenSSH
    # and modify account information in add_host in order to use this script.
    from qw import core

    default = core.get_local_env()
    env0 = core.add_host({'host': 'foo@bar1',
              'sched': 'sh',
              'wd': '/home/foo/xcrypt/sample',
              'xd': '/home/foo/xcrypt'})
    env1 = core.add_host({'host': 'foo@bar2',
              'sched': 't2k_tsukuba'})
    env2 = core.add_host({'host': 'foo@bar3',
              'sched': 't2k_tokyo'})
    env3 = core.add_host({'host': 'foo@bar3',
              'sched': 't2k_kyoto'})
    
    template = {
        'id': 'jobremote',
        'JS_cpu': 1,
        'JS_memory': '1GB',
        'JS_queue@': [' ', 'ESCIENCE', 'debug', 'gh', ' '],
        'JS_group': 'gh',
        'JS_limit_time': 300,
        'exe0@': lambda VALUE: f"echo {VALUE[0]} > job4_{VALUE[0]}",
        'RANGE0': [0, 1, 2, 3, 4],
        'env@': [env0, env1, env2, env3, default],
    }

    core.prepare_submit_sync(template)