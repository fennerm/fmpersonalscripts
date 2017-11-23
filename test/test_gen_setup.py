from plumbum import local

from fmpersonalscripts.gen_setup import *

def test_runs_without_error(tmpdir):
    with local.cwd(tmpdir):
        gen_setup('test')
