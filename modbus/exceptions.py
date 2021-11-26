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

class ModbusError(Exception):
    """Exception raised when the modbus slave returns an error"""

    def __init__(self, exception_code, value=""):
        """constructor: set the exception code returned by the slave"""
        if not value:
            value = "Modbus Error: Exception code = %d" % (exception_code)
        Exception.__init__(self, value)
        self._exception_code = exception_code

    def get_exception_code(self):
        """return the exception code returned by the slave (see defines)"""
        return self._exception_code


class ModbusFunctionNotSupportedError(Exception):
    """
    Exception raised when calling a modbus function not supported by modbus
    """
    pass


class DuplicatedKeyError(Exception):
    """
    Exception raised when trying to add an object with a key that is already
    used for another object
    """
    pass


class MissingKeyError(Exception):
    """
    Exception raised when trying to get an object with a key that doesn't exist
    """
    pass


class InvalidModbusBlockError(Exception):
    """Exception raised when a modbus block is not valid"""
    pass


class InvalidArgumentError(Exception):
    """
    Exception raised when one argument of a function doesn't meet
    what is expected
    """
    pass


class OverlapModbusBlockError(Exception):
    """
    Exception raised when adding modbus block on a memory address
    range already in use
    """
    pass


class OutOfModbusBlockError(Exception):
    """Exception raised when accessing out of a modbus block"""
    pass


class ModbusInvalidResponseError(Exception):
    """
    Exception raised when the response sent by the slave doesn't fit
    with the expected format
    """
    pass


class ModbusInvalidRequestError(Exception):
    """
    Exception raised when the request by the master doesn't fit
    with the expected format
    """
    pass
