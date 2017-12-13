#!/usr/bin/env python
"""Save the current layout as a json file without comments

File is saved in the directory pointed to by the I3LAYOUTS environment variable.

Usage:
  save_i3_layout.py NAME
  save_i3_layout.py (-h | --help)

Inputs:
    NAME        Filename prefix for the output .json.
Options:
  -h, --help    Show this screen
"""
from __future__ import print_function
from fmbiopy.fmparse import helpful_docopt
from fmi3lib import focused_workspace
from plumbum import local

def is_comment(line):
    """True if line is a .json comment field"""
    return line.strip().startswith('//')

def is_swallow_field(line):
    """True if line is one of the 'swallow' fields in the .json"""
    swallow_fields = [r'"class":', r'"instance":', r'"title":',
                      r'"transient_for":']
    return any(x in line for x in swallow_fields)

def is_transient_for_field(line):
    """True if line is the transient_for field"""
    return r'"transient_for":' in line

def has_trailing_comma(line):
    """True if line has a trailing comma"""
    return line.rstrip().endswith(",")
    
def uncomment(line):
    """Remove .json comment chars from line"""
    return line.replace('/', ' ', 2)

def reformat_json(json, outfile):
    """Remove the comment fields from a json formatted string and write to file
    
    Parameters
    ----------
    json: str
    outfile: local.path
    """
    json = json.split('\n')
    with open(outfile, 'w') as f:
        for line in json:
            if not is_comment(line):
                # If line is a comment, just print it to output
                f.write(line + "\n")
            elif is_swallow_field(line):
                # If it is a swallow field, uncomment it and print
                line = uncomment(line).rstrip()
                if is_transient_for_field(line) and has_trailing_comma(line):
                    # Remove the trailing comma
                    line = line[:-1]
                f.write(line + "\n")
            # If line starts with '//' but is not a swallow field then we just
            # ignore it

def main(outfile):
    # Save the workspace to a json formatted string
    save = local['i3-save-tree']
    _, stdout, _ = save.run(['--workspace', focused_workspace()])
    # Uncomment the json
    reformat_json(stdout, outfile)

if __name__ == "__main__":
    opts = helpful_docopt(__doc__)
    outdir = local.path(local.env['I3LAYOUTS'])
    outfile = outdir / (opts['NAME'] + '.json')
    main(outfile)
