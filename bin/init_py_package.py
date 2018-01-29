#!/usr/bin/env python
"""'Generate a setup.py file

Usage:
  gen_setup.py NAME

Arguments:
  NAME      Name of the python package
"""
from __future__ import print_function
from datetime import datetime

from docopt import docopt
from plumbum import local
from plumbum.cmd import git


PACKAGE_ROOT = local.path(__file__).dirname.dirname


def _template():
    """Get the path to the setup.py template"""
    template = PACKAGE_ROOT / 'fmpersonalscripts' / 'setup_template.py'
    return template


def add_hooks():
    """Add git hooks to the repo"""
    pre_push_hook = PACKAGE_ROOT / 'bin' / 'pre-push'
    destination = local.path('.git/hooks')
    pre_push_hook.copy(destination)


def add_license():
    """Add MIT license to the project"""
    license_template_filename = PACKAGE_ROOT / 'docs' / 'MIT_LICENSE_STUB'
    with license_template_filename.open('r') as f:
        license_body = f.read()
    license_filename = local.path('LICENSE')
    current_year = datetime.now().year
    with license_filename.open('w') as f:
        f.write(' '.join(['Copyright', str(current_year), 'Fenner Macrae']))
        f.write('\n\n')
        f.write(license_body)


def gen_dir_skeleton(name):
    dirs = [name.name, 'test']
    for d in dirs:
        local.path(d).mkdir()
    local.path('README.md').touch()


def gen_setup(name, template=_template()):
    """Generate a setup.py file

    Parameters
    ----------
    name
        Name of the module
    template
        Template setup.py file

    Raises
    ------
    FileExistsError
        If setup.py already exists
    """
    output_path = local.path('setup.py')

    if output_path.exists():
        raise FileExistsError

    with template.open('r') as inp:
        with output_path.open('w') as out:
            for line in inp:
                first_word = line.partition(' ')[0]
                if first_word == 'NAME':
                    print(''.join(["NAME = '", name, "'"]), file=out)
                else:
                    print(line.rstrip(), file=out)


def gen_gitignore():
    """Generate a .gitignore file if one doesn't already exist"""
    local['gen_py_gitignore.sh']()


def main(name):
    name.mkdir()
    with local.cwd(name):
        gen_dir_skeleton(name)
        gen_setup(name.name)
        git['init']()
        gen_gitignore()
        add_hooks()
        add_license()


if __name__ == '__main__':
    args = docopt(__doc__)
    name = local.path(args['NAME'])
    main(name)
