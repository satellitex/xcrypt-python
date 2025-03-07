from xcrypt_python.lib import Xcrypt

@Xcrypt
def bulk_num():
    # A sample of unifying multiple jobs into a bulk job using the bulk.pm module.
    # Limit the number of jobs in each bulk job up to 3.

    from qw import bulk, core

    bulk.initialize('max_num', '3')

    template: dict = {
        'RANGE0': [30,40],
        'RANGE1': list(range(0, 5)),
        'id': 'jobbulknum',
        'exe0': 'bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
     }

    jobs: list = prepare(template)
    bulked_jobs: list = bulk.bulk('bulknum', jobs)
    submit(bulked_jobs)
    sync(bulked_jobs)
