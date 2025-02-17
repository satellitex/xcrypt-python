# Xcrypt-Python Code:
# A sample of repeat(): user defined timer events
from xcrypt_python.lib import Xcrypt

template = {
    'id'   : 'jobrep',
    'exe0' : 'sleep 10'
}

@Xcrypt
def prepare_submit(template):
    jobs = [template]
    return jobs

jobs = prepare_submit(template)

@Xcrypt
def print_foo():  # Converted Perl anonymous function to Python function
    print("foo")

print_foo.repeat()  # The specified statement is evaluated every n seconds
                     # (n is the system-defined default value. You can specify n
                     # explicitly by the second argument)
                
bar = 'baz'  # Converted Perl scalar to Python variable

@Xcrypt
def print_bar():
    print(bar)
    
print_bar.repeat(3)  # You can also define a timer event as a function.

@Xcrypt
def sync(jobs):  # Converted Perl array to Python list
    pass

sync(jobs)
