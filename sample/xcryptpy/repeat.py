# Xcrypt-Python Code:
# A sample of repeat(): user defined timer events
from xcrypt_python.lib import Xcrypt

@Xcrypt
def repeat():
# A sample of repeat(): user defined timer events
    from qw import core

    template = {
        'id': 'jobrep',
        'exe0': 'sleep 10'
    }

    jobs = core.prepare_submit(template)

    core.repeat('print "foo\n";')

    bar = 'baz'
    core.repeat(lambda: print(f"{bar}\n"), 3)

    core.sync(jobs)
