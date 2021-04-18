# !/usr/bin/python3
from argparse import ArgumentParser
import importlib
import logging
from sys import exit

from .version import __version__, __version_comment__  # noqa: F401
from . import get_device_class

log = logging.getLogger("mpp-test")


def main():
    description = f"Solar Device Test Utility, version: {__version__}, {__version_comment__}"
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        help="Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)",
        default="/dev/ttyUSB0",
    )
    parser.add_argument(
        "--porttype",
        type=str,
        help="overrides the device communications port type",
        default=None,
    )
    parser.add_argument(
        "-b",
        "--baud",
        type=int,
        help="Baud rate for serial communications (default: 2400)",
        default=2400,
    )
    parser.add_argument(
        "-P",
        "--protocol",
        type=str,
        help="Specifies the device command and response protocol, (default: PI30)",
        default="PI30",
    )
    parser.add_argument("-v", "--version", action="store_true", help="Display the version")
    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        help="Enable Debug and above (i.e. all) messages",
    )
    parser.add_argument(
        "-I", "--info", action="store_true", help="Enable Info and above level messages"
    )

    args = parser.parse_args()

    # Turn on debug if needed
    if args.debug:
        log.setLevel(logging.DEBUG)
    elif args.info:
        log.setLevel(logging.INFO)
    else:
        # set default log level
        log.setLevel(logging.WARNING)
    logging.basicConfig()

    # Display verison if asked
    log.info(description)
    if args.version:
        print(description)
        exit(0)

    log.info(
        f'Creating device type: "{s_prog_name}" on port "{args.port} (porttype={args.porttype})" using protocol "{args.protocol}"'
    )
    device_class = get_device_class(s_prog_name)
    log.debug(f"device_class {device_class}")
    # The device class __init__ will instantiate the port communications and protocol classes
    device = device_class(
        name=args.name,
        port=args.port,
        protocol=args.protocol,
        baud=args.baud,
        porttype=args.porttype,
        mqtt_broker=mqtt_broker,
        mqtt_port=mqtt_port,
        mqtt_user=mqtt_user,
        mqtt_pass=mqtt_pass,
    )
    #
