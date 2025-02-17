Here is the converted Python code using Xcrypt-Python:

```python
# A sample of submitting jobs for MIC systems in the native mode
# Derived from fib-eval.xcr.
from xcrypt_python.lib import Xcrypt, initialize, prepare_submit_sync

# Uncomment if your system does not support a batch scheduler.
initialize(5)

@Xcrypt
def submit_job():
    prepare_submit_sync (
        'id' = 'jobfibpar',
        'RANGE0' = [1,4,8,16,32,60],     # # of workers
        'RANGE1' = [43],                  # fib's param (problem size)
        'RANGE2' = [i+1 for i in range(3)], # # of trials
        'exe0' = 'aprun -k -n $LSB_PROCS_MIC -d $LSB_CPUS_MIC -N $LSB_PPN_MIC ./bin/fib-par/fib-par-mic',
        'JS_mic_node' = 1,                         # # of procs in MIC requested to a batch scheduler
        'JS_mic_cpu@' = lambda value: value[0],    # # of MIC cores requested to a batch scheduler
        'JS_mic_thread@' = lambda value: value[0], # # of MIC threadss requested to a batch scheduler
        'arg0_0@' = lambda value: "-n {}".format(value[0]),
        'arg0_1@' = lambda value: '-i "1 {}"'.format(value[1]),
        'JS_limit_time' = 180                   # Estimated job execution time sent to a batch scheduler
    )

submit_job()
```

Please Note: Since Python uses zero-indexing, be sure to adjust accordingly when accessing elements in list as compared from Perl script which uses one-indexing. Also, Python does not support `..` operator for ranges as Perl does. Replace it with the `range()` function adjusted to your liking.