#!/usr/bin/env python
"""Switch to a numbered i3 workspace, even if it also has a name."""
import sys

import i3


def main(target):
    for workspace in i3.get_workspaces():
        if workspace["num"] == target:
            i3.command(
                "workspace number {} {}".format(str(target), workspace["name"])
            )
            sys.exit()
    i3.command("workspace " + str(target))


if __name__ == "__main__":
    main(sys.argv[1])
