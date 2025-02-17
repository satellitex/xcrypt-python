from xcrypt_python.lib import Xcrypt

@Xcrypt
def sample_code():
    from qw import core

    transfer_variable = ['$i']
    jobs = []

    for i in range(10, 21):
        j = core.spawn(i)
        print(f'Spawned {j["id"]}\n')
        jobs.append(j)

    core.sync(*jobs)

    jobs = []
    for i in range(10, 21):
        j = core.spawn_prepare(i)
        print(f'Prepared {j["id"]}\n')
        jobs.append(j)

    core.submit_sync(*jobs)

    jobs = []
    for i in range(10, 21):
        j = core.spawn_sync(i)
        print(f'Completed {j["id"]}\n')
        jobs.append(j)

if __name__ == '__main__':
    sample_code()
