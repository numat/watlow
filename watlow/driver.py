"""Drivers for Watlow EZ-Zone temperature controllers."""
import struct
from binascii import unhexlify
import re

import crcmod
import serial
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from .util import AsyncioModbusClient

crc = crcmod.mkCrcFun(0b10001000000100001)


def f_to_c(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32.0) / 1.8


def c_to_f(c):
    """Convert Celsius to Fahrenheit."""
    return c * 1.8 + 32.0


class TemperatureController(object):
    """Driver for the Watlow EZ-ZONE temperature controller.

    This driver borrows heavily from this StackOverflow post:
        https://reverseengineering.stackexchange.com/questions/8303/
        rs-485-checksum-reverse-engineering-watlow-ez-zone-pm

    The EZ-Zone communication protocol is Bacnet MS/TP over a serial line.
    There are libraries for this protocol, namely bacpypes, but they don't
    support serial devices. As we only need three commands, we're going to
    manually build the appropriate request strings.

    The request breakdown is:

    Preamble Req/Res Zone ???    Check ???    Register Instance Value    Check
    55ff     05      10   000006 e8    010301 0401     01       00000000 e399

     * Preamble is always 55ff for BACNET MS/TP.
     * Req/Res is a guess. It looks like all requests are 05 and responses are 06.
     * Zone, only 10 works. Maybe other zones are for splitting RS-485 out into
       a many-to-one configuration.
     * Nothings don't seem to change between valid requests.
     * First checksum is a custom protocol.
     * Only known registers are 0401 for PV and 0701 for SP. Other registers
       return data, so we could hunt around for PID params if needed.
     * Instance, only 01 works. Current understanding is similar to zone.
     * Second checksum is a custom CRC-16 following Bacnet spec.
    """

    commands = {'actual': unhexlify('55ff0510000006e8010301040101e399'),
                'setpoint': unhexlify('55ff0510000006e80103010701018776'),
                'set': {'header': unhexlify('55ff051000000aec'),
                        'body': unhexlify('010407010108')}}
    responses = {
        'actual': re.compile('^55ff060010000b8802030104010108'
                             '([0-9a-f]{8})([0-9a-f]{4})$'),
        'setpoint': re.compile('^55ff060010000b8802030107010108'
                               '([0-9a-f]{8})([0-9a-f]{4})$'),
        'set': re.compile('^55ff060010000a76020407010108'
                          '([0-9a-f]{8})([0-9a-f]{4})$')
    }

    def __init__(self, port, timeout=0.5):
        """Open up a serial connection to the controller.

        This device uses RS-422 instead of RS-232. You will likely need a
        custom converter.
        """
        self.port = port
        self.baudrate = 38400
        self.timeout = timeout
        self.connection = None
        self.open()

    def open(self):
        """Open up a serial connection to the oven."""
        self.connection = serial.Serial(
            self.port,
            self.baudrate,
            timeout=self.timeout
        )

    def close(self):
        """Close the serial connection. Use on cleanup."""
        self.connection.flush()
        self.connection.close()

    def get(self):
        """Get the current temperature and setpoint, in C."""
        output = {'actual': None, 'setpoint': None}
        for key in output:
            output[key] = self._write_and_read(
                request=self.commands[key],
                length=21,
                check=self.responses[key]
            )
        return output

    def set(self, setpoint):
        """Set the setpoint temperature, in C."""
        if not 10 <= setpoint <= 220:
            raise ValueError("Setpoint must be between 10°C and 200°C.")
        body = self.commands['set']['body'] + struct.pack('>f', c_to_f(setpoint))
        checksum = struct.pack('<H', ~crc(body) & 0xffff)
        response = self._write_and_read(
            request=self.commands['set']['header'] + body + checksum,
            length=20,
            check=self.responses['set']
        )
        if round(setpoint, 2) != round(response, 2):
            raise IOError(f"Could not change setpoint from "
                          f"{response:.2f}°C to {setpoint:.2f}°C.")

    def _write_and_read(self, request, length, check, retries=3):
        """Write to and read from the device.

        This function abstracts a whole lot of validation checks and error
        handling. The goal is for this driver to be stable to both incomplete
        messages and temporary disconnects.

        The regex parses out the response checksum but does not use it. A
        description of how to calculate it is in the following manual:
            http://www.bacnet.org/Addenda/Add-135-2010an-APR1-1_chair-approved.pdf
        However, my attempts at reproducing did not go well.
        """
        if not self.connection.is_open:
            self.open()
        if retries <= 0:
            self.close()
            raise IOError("Could not communicate with Watlow.")
        self.connection.flush()
        try:
            self.connection.write(request)
            response = self.connection.read(length)
        except serial.serialutil.SerialException:
            return self._write_and_read(request, length, check, retries-1)
        match = check.match(bytes.hex(response))
        if not match:
            return self._write_and_read(request, length, check, retries-1)
        value = match.group(1)
        # From docstring, `checksum = match.group(2)` could be added and checked.
        temperature = f_to_c(struct.unpack('>f', unhexlify(value))[0])
        if temperature < 0 or temperature > 250:
            return self._write_and_read(request, length, check, retries-1)
        return temperature


class Gateway(AsyncioModbusClient):
    """Watlow communication using their EZ-Zone Modbus Gateway."""

    def __init__(self, address, timeout=1, modbus_offset=5000):
        """Open connection to gateway."""
        super().__init__(address, timeout)
        self.modbus_offset = modbus_offset
        self.actual_temp_address = 360
        self.setpoint_address = 2160
        self.setpoint_range = (10, 220)

    async def get(self, zone: int):
        """Get oven data for a zone.

        For more information on a 'Zone', refer to Watlow manuals.
        """
        output = {
            'actual': self.actual_temp_address,
            'setpoint': self.setpoint_address,
        }
        for k, v in output.items():
            address = (zone - 1) * self.modbus_offset + v
            try:
                result = await self.read_registers(address, 2)
                output[k] = BinaryPayloadDecoder.fromRegisters(
                    result,
                    byteorder=Endian.Big
                ).decode_32bit_float()
            except AttributeError:
                output[k] = None
        return output

    async def set_setpoint(self, zone: int, setpoint: float):
        """Set the temperature setpoint for a zone.

        For more information on a 'Zone', refer to Watlow manuals.
        """
        if not self.setpoint_range[0] <= setpoint <= self.setpoint_range[1]:
            raise ValueError(f"Setpoint ({setpoint}) in not in the valid range from"
                             f" {self.setpoint_range[0]} to {self.setpoint_range[1]}")
        address = (zone - 1) * self.modbus_offset + self.setpoint_address
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_float(setpoint)
        await self.client.protocol.write_registers(address, builder.build(),
                                                   skip_encode=True)
