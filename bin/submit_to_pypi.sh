#!/usr/bin/env bash
## Submit a package in working directory to pypi

# Strict mode
set -euo pipefail
IFS=$'\n\t'

rm -rf dist
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
