"""
micropython-modbus: Implementation of Modbus protocol for MicroPython
https://gitlab.com/extel-open-source

Based on "Modbus TestKit": https://github.com/ljean/modbus-tk

Copyright (C) 2009, Luc Jean - luc.jean@gmail.com
Copyright (C) 2009, Apidev - http://www.apidev.fr
Copyright (C) 2018, Extel Technologies - https://gitlab.com/extel-open-source

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import struct

# from modbus import LOGGER
from modbus.modbus import (Query, Master,
                           InvalidArgumentError, ModbusInvalidResponseError, ModbusInvalidRequestError
                           )
from modbus.hooks import call_hooks
from modbus import utils

# Some values used in the serial_prep callback
serial_cb_tx_begin = const(0x01)
serial_cb_tx_end = const(0x02)
serial_cb_rx_begin = const(0x03)
serial_cb_rx_end = const(0x04)


class RtuQuery(Query):
    """Subclass of a Query. Adds the Modbus RTU specific part of the protocol"""

    def __init__(self):
        """Constructor"""
        super(RtuQuery, self).__init__()
        self._request_address = 0
        self._response_address = 0

    def build_request(self, pdu, slave):
        """Add the Modbus RTU part to the request"""
        self._request_address = slave
        if (self._request_address < 0) or (self._request_address > 255):
            raise InvalidArgumentError(
                "Invalid address {0}".format(self._request_address))
        data = struct.pack(">B", self._request_address) + pdu
        crc = struct.pack(">H", utils.calculate_crc(data))
        return data + crc

    def parse_response(self, response):
        """Extract the pdu from the Modbus RTU response"""
        if len(response) < 3:
            raise ModbusInvalidResponseError(
                "Response length is invalid {0}".format(len(response)))

        (self._response_address, ) = struct.unpack(">B", response[0:1])

        if self._request_address != self._response_address:
            raise ModbusInvalidResponseError(
                "Response address {0} is different from request address {1}".format(
                    self._response_address, self._request_address
                )
            )

        (crc, ) = struct.unpack(">H", response[-2:])

        if crc != utils.calculate_crc(response[:-2]):
            raise ModbusInvalidResponseError("Invalid CRC in response")

        return response[1:-2]

    def parse_request(self, request):
        """Extract the pdu from the Modbus RTU request"""
        if len(request) < 3:
            raise ModbusInvalidRequestError(
                "Request length is invalid {0}".format(len(request)))

        (self._request_address, ) = struct.unpack(">B", request[0:1])

        (crc, ) = struct.unpack(">H", request[-2:])
        if crc != utils.calculate_crc(request[:-2]):
            raise ModbusInvalidRequestError("Invalid CRC in request")

        return self._request_address, request[1:-2]

    def build_response(self, response_pdu):
        """Build the response"""
        self._response_address = self._request_address
        data = struct.pack(">B", self._response_address) + response_pdu
        crc = struct.pack(">H", utils.calculate_crc(data))
        return data + crc


class RtuMaster(Master):
    """Subclass of Master. Implements the Modbus RTU MAC layer"""

    def __init__(self, serial, serial_prep_cb=None):
        """Constructor. Pass the machine.UART object"""
        self._serial = serial
        self._serial_prep = serial_prep_cb
        super(RtuMaster, self).__init__()

        # For some RS-485 adapters, the sent data(echo data) appears before modbus response.
        # So read echo data and discard it.
        self.handle_local_echo = False

    def _send(self, request):
        """Send request to the slave"""
        retval = call_hooks(
            "modbus_rtu.RtuMaster.before_send", (self, request))
        if retval is not None:
            request = retval

        # Check if there are any bytes waiting
        while self._serial.any() > 0:
            # Throw away any waiting bytes, to clear the buffer
            self._serial.read(1)

        # Call the "serial prepare callback" before writing
        if self._serial_prep:
            self._serial_prep(serial_cb_tx_begin)

        self._serial.write(request)
        print("request: " + "".join("%02x " % i for i in request))

        if self._serial_prep:
            self._serial_prep(serial_cb_tx_end)

        # Read the echo data, and discard it
        if self.handle_local_echo:
            # print("handle_local_echo")
            if self._serial_prep:
                self._serial_prep(serial_cb_rx_begin)
            self._serial.read(len(request))
            if self._serial_prep:
                self._serial_prep(serial_cb_rx_end)

    def _recv(self, expected_length=-1):
        """Receive the response from the slave"""
        response = utils.to_data("")
        # print("start read {} bytes".format(expected_length))

        if self._serial_prep:
            self._serial_prep(serial_cb_rx_begin)

        while True:
            read_bytes = self._serial.read(
                expected_length if expected_length > 0 else 1)

            if not read_bytes:
                break

            response += read_bytes
            if expected_length >= 0 and len(response) >= expected_length:
                # if the expected number of byte is received consider that the response is done
                # improve performance by avoiding end-of-response detection by timeout
                break

        if self._serial_prep:
            self._serial_prep(serial_cb_rx_end)
        # print("read finished")
        # print("response: " + "".join("%02x " % i for i in response))

        retval = call_hooks(
            "modbus_rtu.RtuMaster.after_recv", (self, response))
        if retval is not None:
            return retval
        return response

    def _make_query(self):
        """Returns an instance of a Query subclass implementing the modbus RTU protocol"""
        return RtuQuery()
