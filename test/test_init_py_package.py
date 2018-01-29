from plumbum import local
from fmbiopy.fmtest import assert_script_produces_files

def test_init_py_package_produces_expected_output(tmpdir):
    name = 'packabc'
    script = local.path('fmpersonalscripts') / 'init_py_package.py'
    with local.cwd(tmpdir):
        assert_script_produces_files(script=script,
                                     args=[name],
                                     output=["setup.py", ".git",
                                             ".git/hooks/pre-push", name, "test",
                                             "LICENSE", "README.md",
                                             '.gitignore'],
                                     outdir=name)
