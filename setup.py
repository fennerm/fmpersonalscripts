"""Setup script"""
from io import open
import os
from setuptools import find_packages, setup

# =============================================================================
# Globals
# =============================================================================
"""Location of the README file"""
README = "README.md"

"""Github username"""
USERNAME = "fennerm"

"""Package name"""
NAME = "fmpersonalscripts"


# =============================================================================
# Helpers
# =============================================================================


def url(name=NAME, username=USERNAME):
    """Generate the package url from the package name"""
    return "/".join(["http://github.com", username, name])


def list_scripts():
    """Get the names of the scripts in the bin directory"""
    scripts = os.listdir("bin")
    scripts = ["bin/" + script for script in scripts]
    scripts = [f for f in scripts if os.path.isfile(f)]
    scripts = [f for f in scripts if "__init__" not in f]
    scripts = [f for f in scripts if not f.endswith(".pyc")]
    return scripts


setup(
    name=NAME,
    version="0.0.1",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url=url(),
    author="Fenner Macrae",
    author_email="fmacrae.dev@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["*test*"]),
    scripts=list_scripts(),
)
