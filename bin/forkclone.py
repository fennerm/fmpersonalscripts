#!/usr/bin/env python
"""Fork a remote repo and set it up for a pull request


Usage:
  init-pull-req REMOTE

Inputs:
  REMOTE    'username/repo'
"""
from fmbiopy.fmparse import helpful_docopt
from plumbum import FG, local, ProcessExecutionError
from plumbum.cmd import hub


def main(remote):
    repo_split = remote.split("/")
    user = repo_split[0]
    repo = repo_split[1]
    remote_address = "/".join(["https://github.com", remote])
    hub["clone", remote] & FG
    with local.cwd(local.cwd / repo):
        try:
            hub["fork"] & FG
        except ProcessExecutionError:
            # Thrown if the repo is already forked
            pass
        hub["pull"] & FG
        hub["remote", "add", user, remote_address] & FG
        hub["branch", "--set-upstream-to=origin/master", "master"] & FG


if __name__ == "__main__":
    opts = helpful_docopt(__doc__)
    main(opts["REMOTE"])
