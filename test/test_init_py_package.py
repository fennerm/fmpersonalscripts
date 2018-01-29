from plumbum import local
from fmbiopy.fmtest import assert_script_produces_files


def test_init_py_package_produces_expected_output(tmpdir):
    name = 'packabc'
    outdir = tmpdir / name
    script = local.path('bin') / 'init_py_package.py'
    with local.cwd(tmpdir):
        assert_script_produces_files(script=script,
                                     args=[name],
                                     output=["setup.py", ".git",
                                             ".git/hooks/pre-push",
                                             ".git/hooks/pre-commit",
                                             name, "test",
                                             "LICENSE", "README.md",
                                             '.gitignore'],
                                     outdir=outdir, empty_ok=True)