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

#modbus exception codes
ILLEGAL_FUNCTION = const(1)
ILLEGAL_DATA_ADDRESS = const(2)
ILLEGAL_DATA_VALUE = const(3)
SLAVE_DEVICE_FAILURE = const(4)
COMMAND_ACKNOWLEDGE = const(5)
SLAVE_DEVICE_BUSY = const(6)
MEMORY_PARITY_ERROR = const(8)

#supported modbus functions
READ_COILS = const(1)
READ_DISCRETE_INPUTS = const(2)
READ_HOLDING_REGISTERS = const(3)
READ_INPUT_REGISTERS = const(4)
WRITE_SINGLE_COIL = const(5)
WRITE_SINGLE_REGISTER = const(6)
READ_EXCEPTION_STATUS = const(7)
DIAGNOSTIC = const(8)
REPORT_SLAVE_ID = const(17)
WRITE_MULTIPLE_COILS = const(15)
WRITE_MULTIPLE_REGISTERS = const(16)
READ_WRITE_MULTIPLE_REGISTERS = const(23)
DEVICE_INFO = const(43)

#supported block types
COILS = const(1)
DISCRETE_INPUTS = const(2)
HOLDING_REGISTERS = const(3)
ANALOG_INPUTS = const(4)
