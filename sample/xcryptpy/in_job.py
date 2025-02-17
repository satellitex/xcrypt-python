from xcrypt_python.lib import Xcrypt

@Xcrypt
def in_job():
    from qw import core

    template = {
        'id': 'job_injob',
        'exe0': 'bin/fib-file',
        'arg0_0': 'dat/num40',
        'arg0_1': 'out_0',
        # This procedure runs in the job before executing fib-file
        'before_in_job': lambda: print(f"{self.arg0_0}\n"),
        # This procedure runs in the job after executing fib-file
        'after_in_job': lambda: print(f"{self.exe0}\n"),
    }

    jobs = core.prepare_submit_sync(template)
