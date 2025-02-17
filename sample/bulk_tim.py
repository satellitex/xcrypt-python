from xcrypt_python.lib import Xcrypt


@Xcrypt
def bulk_tim():
    # A sample of unifying multiple jobs into a bulk job using the bulk.pm module.
    # Limit the number of jos in each bulk job up to 3.
    from qw import bulk, core

    bulk.initialize(max_time=16384)

    template = {
        'RANGE0': [30, 40],
        'RANGE1': list(range(5)),
        'id': 'jobbulktime',
        'exe0': 'bin/fib',
        'arg0_0@': lambda VALUE: VALUE[0] + VALUE[1],
        'time@': lambda VALUE: 2 ** (VALUE[0] + VALUE[1] - 30),
    }

    jobs = core.prepare(template)
    print("ID              \testimated time")
    for j in jobs:
        print(f"{j['id']}\t{j['time']}")

    bulkedjobs = bulk.bulk('bulktim', jobs)

    core.submit(bulkedjobs)

    core.sync(bulkedjobs)

if __name__ == '__main__':
    bulk_tim()