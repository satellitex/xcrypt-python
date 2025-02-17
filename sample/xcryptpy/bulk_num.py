from xcrypt_python.lib import Xcrypt

@Xcrypt
def bulk_num():
    # A sample of unifying multiple jobs into a bulk job using the bulk.pm module.
    # Limit the number of jobs in each bulk job up to 3.

    from qw import bulk, core

    initialize = {
        'max_num': "3"    # unify up to 3 jobs.
     }

    template = {
        'RANGE0': [30,40],
        'RANGE1': list(range(0, 5)),
        'id': 'jobbulknum',
        'exe0': 'bin/fib',
        'arg0_0': lambda value: value[0] + value[1],
     }

    jobs = core.prepare(template)
    bulked_jobs = bulk.bulk('bulknum', jobs)
    core.submit(bulked_jobs)
    core.sync(bulked_jobs)
