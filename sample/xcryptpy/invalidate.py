# A sample of using the invalidate.pm module.
# A job is automatically killed when its running time exceeds specified time.
from xcrypt_python.lib import Xcrypt

@Xcrypt
def invalidate():
    # A sample of using the invalidate.pm module.
    # A job is automatically killed when its running time exceeds specified time.
    from qw import invalidate, core

    template = {
        'RANGE0': [3, 7, 40],
        'id@': lambda VALUE: f"jobinval_{VALUE[0]}",
        'exe0': 'bin/fib 44 > out_44',
        # A job running more than VALUE[0] seconds is automatically killed
        'allotted_time@': lambda VALUE: VALUE[0],
    }

    core.prepare_submit_sync(template)
