#!/usr/bin/env python
"""Pull or push the contents of matched local-remote directories.

Works similar to setting the --relative flag with rsync but does not assume that
paths are relative to root. Instead paths can be relative to any two paired
directories.

Usage:
  sync pull --remote=ADDRESS --remote_root=DIR --local_root=DIR [--max_size=MB]
    [--exclude=FILES] [TARGET]
  sync pull (--help | -h)
  sync push --remote=ADDRESS --remote_root=DIR --local_root=DIR [--max_size=MB]
    [--exclude=FILES] [TARGET]
  sync push (--help | -h)

Inputs:
  TARGET                File or directory to pull. [default: Current working
                        directory]

Options:
  -h --help             Show this screen
  --max_size=MB         Files with size > max_size will be ignored
  --remote=ADDRESS      The ssh address of the remote (e.g user@nsa.gov)
  --remote_root=DIR     The path to the root of the matched directories on the
                        remote machine.
  --local_root=DIR      The path to the root of the matched directories on the
                        local machine.
  --exclude=FILES       List of comma separated files to ignore
                        [default:".git"]
"""
import os

from docopt import docopt
from plumbum import (
    FG,
    local,
)
from plumbum.cmd import rsync


def local_to_remote(local_file, local_root, remote_root):
    """Convert a local path to its matched path on the remote machine"""
    relative_local_file = local_file.relative_to(local_root)
    remote_local_file = remote_root / relative_local_file
    return remote_local_file


def construct_rsync_command(method, local_file, remote_file, remote_address,
                            exclude, max_size):
    args = ['--update', '-ravz', '--exclude', exclude]

    if max_size:
        args = args + ["--max-size", max_size]

    if method == "pull":
        source = remote_address + ":" + remote_file
        sink = local_file.parent
    elif method == "push":
        source = local_file
        sink = remote_address + ":" + remote_file.parent
    args = args + [source, sink]

    return rsync.__getitem__(args)


def main(method, local_file, remote_address, max_size, remote_root, local_root,
         exclude):
    remote_file = local_to_remote(local_file, local_root, remote_root)
    rsync_command = construct_rsync_command(method, local_file, remote_file,
                                            remote_address, exclude, max_size)
    print("Running: " + str(rsync_command))
    rsync_command & FG


if __name__ == '__main__':
    opt = docopt(__doc__)

    if opt["TARGET"] == "Current working directory":
        local_file = local.cwd
    else:
        local_file = local.path(opt["TARGET"])
    if opt["--max_size"]:
        max_size = opt["--max_size"] + "m"
    else:
        max_size = None

    if opt["push"]:
        method = "push"
    elif opt["pull"]:
        method = "pull"
    main(
        method=method,
        local_file=local_file,
        remote_address=opt["--remote"],
        max_size=max_size,
        remote_root=local.path(opt["--remote_root"]),
        local_root=local.path(opt["--local_root"]),
        exclude=opt["--exclude"])
