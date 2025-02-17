from xcrypt_python.lib import Xcrypt

@Xcrypt
def abort():
    from qw import core
    
    template = {
        'id@': lambda VALUE: f"jobabrt_{VALUE[0]}",
        'exe0@': lambda VALUE: f'bin/fib {VALUE[0]} > out_{VALUE[0]}',
        'RANGE0': [60,61,62,40,41,42],
        'initially': lambda: print(f">initially> {self.id}."),
        'before': lambda: print(f">>before>> {self.id}."),
        'after': lambda: print(f"<<after<< {self.id}."),
        'after_aborted': lambda: print(f"!after_aborted! {self.id}."),
        'finally': lambda: print(f"<finally< {self.id}."),
    }

    jobs = core.prepare_submit(template)
    jobs[0].abort()
    jobs[1].cancel()
    jobs[2].invalidate()
    core.sync(*jobs)
    jobs[3].abort()
    jobs[4].cancel()
    jobs[5].invalidate()

if __name__ == '__main__':
    abort()