#!/usr/bin/env python
"""Switch to a numbered i3 workspace, even if it also has a name"""
import i3
import sys

workspaces = i3.get_workspaces()
target = int(sys.argv[1])
for workspace in workspaces:
    if workspace["num"] == target:
        i3.command(' '.join(["workspace number", str(target),
                             workspace["name"]]))
        quit()
i3.command("workspace " + str(target))
