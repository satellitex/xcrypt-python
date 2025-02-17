# A sample of
# * the n_section_method module
# * the data_generator and data_extractor libraries

from xcrypt_python.lib import Xcrypt

@Xcrypt
def n_section_method():
    # A sample of
    # * the n_section_method module
    # * the data_generator and data_extractor libraries
    # use base qw(sandbox n_section_method core);
    # use data_generator;
    # use data_extractor;
    from qw import sandbox, n_section_method, core
    import data_generator
    import data_extractor

    # &n_section_method::del_extra_job();
    n_section_method.del_extra_job()

    job = {
        'id': 'jobnsec',
        'exe0': './minushalf.pl template.dat',
        'linkedfile0': 'bin/minushalf.pl',
        'before': lambda: data_generator('dat/template.dat', f"{self['id']}/template.dat").replace_key_value("param", self['x']).execute(),
        'after': lambda: data_extractor(f"{self['id']}/output.dat").extract_line_nn('end').execute()[0]
    }

    # 12-section method, the interval [-1,10], the error 0.01.
    # f(-1)=0.5 (positive), f(10)=-5 (negative)
    (x, y) = n_section_method.n_section_method(job, partition=12, epsilon=0.01, x_left=-1, x_right=10, y_left=0.5, y_right=-5)

    print(f'The value is {y} when x = {x}.\n')
