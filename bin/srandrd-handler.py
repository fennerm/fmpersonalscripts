#!/usr/bin/env python
"""Automatically configure xrandr for dual monitors + projector with srandrd."""
import logging
from logging import info
import os
import sys
from time import sleep

from plumbum import BG, local, ProcessExecutionError
from plumbum.cmd import rg, xrandr

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

SRANDRD_ACTION = os.environ.get("SRANDRD_ACTION")
SRANDRD_EDID = os.environ.get("SRANDRD_EDID")

INTERNAL = {"output": "eDP-1", "flags": ["--dpi", "192", "--mode", "3840x2160"]}

EXTERNAL_MONITOR1 = {
    "output": "HDMI-1",
    "edid": "F022318301010101",
    "flags": [
        "--mode",
        "1920x1080",
        "--scale",
        "2x2",
        "--set",
        "Broadcast RGB",
        "Full",
    ],
}

EXTERNAL_MONITOR2 = {
    "output": "DP-2",
    "edid": "F022318301010101",
    "flags": [
        "--mode",
        "1920x1080",
        "--pos",
        "3840x0",
        "--scale",
        "2x2",
        "--set",
        "Broadcast RGB",
        "Full",
    ],
}

PROJECTOR = {
    "output": "HDMI-1",
    "edid": "7436003000000001",
    "flags": ["--mode", "800x600", "--set", "Broadcast RGB", "Full"],
}


def is_connected(output_connection):
    """Test whether a given display output is connected."""
    try:
        (xrandr | rg["-i", output_connection + " connected"])()
        return True
    except ProcessExecutionError:
        return False


def external_monitor_was_connected():
    """Return True if an external monitor was just connected."""
    return SRANDRD_EDID in [
        EXTERNAL_MONITOR1["edid"],
        EXTERNAL_MONITOR2["edid"],
    ]


def display_was_disconnected():
    """Return True if a display was just disconnected."""
    return "disconnected" in SRANDRD_ACTION


def projector_was_connected():
    """Return True if the projector was just connected."""
    return SRANDRD_EDID in PROJECTOR["edid"]


def is_enabled(output_connection):
    """Return True if the device is connected and displaying."""
    try:
        (xrandr | rg["-i", output_connection + r".*mm x .*"])()
        return True
    except ProcessExecutionError:
        return False


def enable(device):
    """Activate a device for display."""
    if not is_enabled(device["output"]):
        xrandr_args = ["--output", device["output"]] + device["flags"]
        xrandr.__getitem__(xrandr_args)()


def disable(device):
    """Disable a device."""
    if is_enabled(device["output"]):
        xrandr("--output", device["output"], "--off")


def launch_polybar():
    """Relaunch polybar."""
    polybar = local["~/dotfiles/polybar/.config/polybar/launch.sh"]
    polybar & BG


def connection_was_changed():
    """Return True if the status of a connection was changed."""
    if SRANDRD_ACTION:
        output_connection = SRANDRD_ACTION.split(" ")[0]
        connection_event = SRANDRD_ACTION.split(" ")[1] == "connected"
        return connection_event != is_enabled(output_connection)
    else:
        return False


def handle_disconnection():
    """Handle the disconnection of a display device."""
    if not is_connected(EXTERNAL_MONITOR1["output"]) and not is_connected(
        EXTERNAL_MONITOR2["output"]
    ):
        info("All external display(s) disconnected, disabling...")
        enable(INTERNAL)
        sleep(5)
        disable(EXTERNAL_MONITOR1)
        disable(EXTERNAL_MONITOR2)
        launch_polybar()
        info("External display(s) successfully disabled...")
    else:
        info(
            "External display disconnected, but not disabling yet because "
            "other external display is still connected"
        )
        info("-> SRANDRD_ACTION = %s", SRANDRD_ACTION)


def enable_external_monitors():
    """Activate both external monitors and deactivate the internal display."""
    enable(EXTERNAL_MONITOR1)
    enable(EXTERNAL_MONITOR2)
    sleep(10)
    disable(INTERNAL)


def handle_new_connection():
    """Handle a new display device connection."""
    if external_monitor_was_connected():
        if is_connected(EXTERNAL_MONITOR1["output"]) and is_connected(
            EXTERNAL_MONITOR2["output"]
        ):
            info("Both external monitors connected, enabling them...")
            enable_external_monitors()
            info("Successfully enabled external monitors")
            info("Relaunching polybar...")
            launch_polybar()
        else:
            info("New display detected, waiting for extra displays...")
    elif projector_was_connected():
        info("Projector connected, enabling...")
        enable(PROJECTOR)
        info("Projector successfully enabled")
    else:
        info("Unrecognized display connected, shutting down...")
        sys.exit(1)


def main():
    if connection_was_changed():
        if display_was_disconnected():
            handle_disconnection()
        else:
            handle_new_connection()
    else:
        if is_connected(EXTERNAL_MONITOR1["output"]) and is_connected(
            EXTERNAL_MONITOR2["output"]
        ):
            enable_external_monitors()
    sys.exit()


if __name__ == "__main__":
    main()
    sys.exit()
