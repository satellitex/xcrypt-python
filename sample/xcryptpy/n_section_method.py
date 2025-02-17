Here's the equivalent Python code:

```python
# A sample of
# * the n_section_method module
# * the data_generator and data_extractor libraries

from xcrypt_python.lib import Xcrypt, data_generator, data_extractor

@Xcrypt
def perl_conversion(self, job=dict(
        id='jobnsec',
        exe0='./minushalf.pl template.dat',
        linkedfile0='bin/minushalf.pl',
        before=self.before_method,
        after=self.after_method)
    ):

    # 12-section method, the interval [-1,10], the error 0.01.
    # f(-1)=0.5 (positive), f(10)=-5 (negative)
    x, y = self.n_section_method(
        job, 'partition' = 12, 'epsilon' = 0.01,
        'x_left'  = -1,  'x_right' = 10,
        'y_left'  = 0.5, 'y_right' = -5
    )
    print('The value is {} when x = {}.\n'.format(y, x))


def before_method(self):
    # In before method, prepare for executing a job (e.g. preparing input files)
    # using the input value assigned to self.x

    # Open the file specified as 1st argument as a template file
    # to generate a file whose path is specified by 2nd argument.
    in_dat = data_generator.new('dat/template.dat',
                                '{}'/template.dat'.format(self.id))
    # The value of 'param' in the template file is replaced by self.x
    # in the generated file.
    in_dat.replace_key_value("param", self.x)
    # Execute this to do generate the file
    in_dat.execute()



def after_method(self):
    # In after method, assign the output value to self.y
    # by extracting the job's output file.

    # Open the file specified as 1st argument to be read.
    out = data_extractor.new(' {}/output.dat'.format(self.id))
    # Extract only the last line.
    out.extract_line_nn('end')
    # Execute this to do extract the file.
    output = out.execute()
    # Get the 0-th column of the last line of the file.
    self.y = output[0]
```

Make sure to call the created function `perl_conversion` to start the execution. Also, ensure that `xcrypt_python.lib` module and `Xcrypt` class have the proper implementations and are correctly imported at the top.