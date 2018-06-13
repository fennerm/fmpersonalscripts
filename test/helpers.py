from plumbum import local

from fmbiopy.paths import is_empty


def assert_script_produces_files(
    script, args, output, redirect=None, empty_ok=False, outdir=None
):
    """Assert that a script with given command line args produces expected files

    Parameters
    ----------
    script : str
        Path to the script
    args : List[str]
        List of command line arguments
    output: List[str] or List[plumbum.LocalPath]
        List of output files
    redirect: str or plumbum.LocalPath, optional
        If defined, redirect the stdout of the script to the given file.
    empty_ok : bool
        If True, output files are valid even if they are empty
    outdir: str or plumbum.LocalPath, optional
        If given, the output filenames are relative to this directory
    """
    execute = local[script]
    command = execute.__getitem__(args)

    if redirect:
        (command > redirect)()
    else:
        command()

    for f in output:
        if outdir:
            f = local.path(outdir) / f
        else:
            f = local.path(f)
        assert f.exists()
        if not empty_ok:
            assert not is_empty(f)
