"""Python driver for Watlow EZ-Zone temperature controllers.

Distributed under the GNU General Public License v2
Copyright (C) 2019 NuMat Technologies
"""
from watlow.driver import TemperatureController, Gateway
from watlow import mock


def command_line():
    """CLI interface, accessible when installed through pip."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Control a Watlow temperature "
                                     "controller or gateway from the command line.")
    parser.add_argument('port', nargs='?', default='/dev/ttyUSB0', help="The "
                        "target serial port or TCP address. Default "
                        "'/dev/ttyUSB0'.")
    parser.add_argument('--set-setpoint', '-f', default=None, type=float,
                        help="Sets the setpoint temperature.")
    parser.add_argument('--zone', '-z', default=None, type=int,
                        help="Specify zone in case of gateway")
    args = parser.parse_args()

    if args.zone:
        gateway = Gateway(args.port)

    temperature_controller = TemperatureController(port=args.port)
    try:
        if args.set_setpoint:
            temperature_controller.set(args.set_setpoint)
        state = temperature_controller.get()
        print(json.dumps(state, indent=2, sort_keys=True))
    finally:
        temperature_controller.close()


if __name__ == '__main__':
    command_line()
