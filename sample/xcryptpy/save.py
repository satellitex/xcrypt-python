# A sample of using the save()/restore() method.
# Save the specified parameter values job object and
# Resotre the values in the next execution of the script.
# Execute this script (at least) twice to see this functionality.
from xcrypt_python.lib import Xcrypt

@Xcrypt
def save():
    from qw import core
    import dataclasses

    template = {
        'id': 'jobsave',
        'exe0': 'bin/fib-file',
        'arg0_0': "dat/num40",
        'arg0_1': "jobsave_OUT",
    }

    # In the second (or later) execution, the job execution is skipped
    jobs = core.prepare_submit_sync(template)
    self = jobs[0]

    # No effect in the first execution.
    # In the second (or later) execution, the value of $self->{result} calculated
    # in the first execution is restored.
    self.restore()

    if self.result:
        # In the second (or later) execution, executed here
        # because $self->{result} is resotred by resotre()
        print(f"restored: {self.result}\n")
    else:
        # Extract the data from the file specified by $self->{arg0_1}
        ohandler = dataclasses.data_extractor(self.arg0_1)
        # Extract the first line
        ohandler.extract_line_nn(1)
        # Extract the last column
        ohandler.extract_column_nn('end')
        output = ohandler.execute()
        self.result = output[0]
        print(f"calclated: {self.result}\n")
        self.save('result')