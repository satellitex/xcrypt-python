from xcrypt_python.lib import Xcrypt

# Define a function using the decorator
@Xcrypt
def dependency():
    # Submit jobs which have dependencies each other
    # If you want use the limit module in addition, use the followings
    from qw import dependency, limit, core # (limit dependency core) does not work!
    
    limit.initialize (1)

    template = {
        'id': 'jobdep',
        'RANGE0': list(range(1, 6)),
        'exe0': 'bin/fib',
        'arg0_0@': lambda VALUE: 44 - VALUE[0],
    }

    jobs = core.prepare(template)

    # submit jobdep_1 after jobdep_5 finished
    jobs[0]['depend_on'] = jobs[4]
    # submit jobdep_3 after jobdep_2 finished (specify by job ID)
    jobs[2]['depend_on'] = 'jobdep_2'
    # submit jobdep_4 after jobdep_1 and jobdep_3 finished
    jobs[3]['depend_on'] = ['jobdep_1', 'jobdep_3']

    core.submit_sync(jobs)