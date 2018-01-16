"""Setup script"""
from setuptools import (
        find_packages,
        setup,
        )

# =============================================================================
# Globals
# =============================================================================
"""Location of the README file"""
README = 'README.md'

"""Github username"""
USERNAME = 'fennerm'

"""Package name"""
NAME = ''


# =============================================================================
# Helpers
# =============================================================================


def long_description(readme=README):
    """Extract the long description from the README"""
    try:
        from pypandoc import convert
        long_description = convert(str(readme), 'md', 'rst')
    except (ImportError, IOError, OSError):
        long_description = readme.read_text()
    return long_description


def url(name=NAME, username=USERNAME):
    """Generate the package url from the package name"""
    return '/'.join(['http://github.com', username, name])


setup(name=NAME,
      version='0.0.1',
      description=long_description()[0],
      long_description=long_description(),
      url=url(),
      author='Fenner Macrae',
      author_email='fennermacrae@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*test*"]),
      zip_safe=False)
