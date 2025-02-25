# A sample of user defined signal handler.
# Push CTRL+C during the execution of this script to try this functionality.
from xcrypt_python.lib import Xcrypt

@Xcrypt
def signal_handle():
    from qw import core

    # If defined, called when ^C is pressed.
    def sigint_handler():
        print("User's SIGINT handler is called.\n")
    
    template = {
        'id': 'jobsig',
        'RANGE0': [30, 40],
        'RANGE1': list(range(5)),
        'exe0': './bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'arg0_1@': lambda VALUE: "> out_$self->{id}",
        'before': lambda: print(f"Submitting {self['id']}"),
        'after': lambda: print(f"{self['id']} finished")
    }

    core.prepare_submit_sync(template)
