# Import required modules
from xcrypt_python.lib import Xcrypt
from data_extractor import DataExtractor

# A template to submit jobs
template = {
    'id': 'jobsave',
    'exe0': 'bin/fib-file',
    'arg0_0': "dat/num40",
    'arg0_1': "jobsave_OUT",
}

@Xcrypt
def job_save_restore(job):
    # prepare and submit the job, as well as synchronize the job 
    jobs = job.prepare_submit_sync(template)
    self = jobs[0]

    # Restore saved job result
    # No effect in the first execution
    self.restore()

    if self.result:
        # In the second (or later) execution, executed here
        # because self.result is restored by restore()
        print("restored: {}".format(self.result))
    else:
        # Executed here in the first execution
        ohandler = DataExtractor(self.arg0_1)
        # Extract 1st line
        ohandler.extract_line_nn(1)
        # Extract the last column
        ohandler.extract_column_nn('end')
        output = ohandler.execute()
        self.result = output[0]
        print("calculated: {}".format(self.result))
        # Save the result
        self.save('result')

# Call the function
job_save_restore()
