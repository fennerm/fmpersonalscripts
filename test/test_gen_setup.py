from fmscripts.gen_setup import *
from fmbiopy.fmsystem import working_directory

def test_runs_without_error(tmpdir):
    with working_directory(tmpdir):
        gen_setup('test')
