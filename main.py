'''
master_main.py - An example MicroPython project, using the micropython-modbus 
library. 

This example code is dedicated to the public domain. To the extent possible 
under law, Extel Technologies has waived all copyright and related or 
neighboring rights to "master_main.py". This work is published from: Australia. 

https://creativecommons.org/publicdomain/zero/1.0/
'''

# import logging
import machine
import struct
import time
import modbus
import modbus.defines as cst
from modbus import modbus_rtu


# LOGGER = logging.getLogger("main")
# LOGGER.setLevel(logging.DEBUG)

pin_cts = machine.Pin(21, machine.Pin.OUT)


def serial_prep(mode):
    if mode == modbus_rtu.serial_cb_tx_begin:
        # print("Begin Tx")
        # SP485E IC needs CTS high to allow transmit
        pin_cts.value(1)

    elif mode == modbus_rtu.serial_cb_tx_end:
        # print("End Tx")
        # Once Tx is done, switch back to allowing receive
        pin_cts.value(0)

    elif mode == modbus_rtu.serial_cb_rx_begin:
        # print("Begin Rx")
        # Probably already in Rx mode, but just in case
        pin_cts.value(0)

    elif mode == modbus_rtu.serial_cb_rx_end:
        # print("End Rx")
        pin_cts.value(0)

    else:
        raise ValueError("Given 'mode' does not have a defined action")


def main():
    pin_cts.value(0)

    # parity is the parity, None, 0 (even) or 1 (odd).
    print("Opening UART 2")
    uart = machine.UART(2, 19200, bits=8, parity=None,
                        stop=1, timeout=1000, timeout_char=50)

    # master = modbus_rtu.RtuMaster(uart)
    master = modbus_rtu.RtuMaster(uart, serial_prep_cb=serial_prep)

    # print("Reading from register 0x00")
    # 'execute' returns a pair of 16-bit words
    while True:
        data1 = master.execute(1, cst.READ_HOLDING_REGISTERS, 0x00, 10)
        print("data1: {}".format(data1))

        # data2 = master.execute(2, cst.READ_HOLDING_REGISTERS, 0x00, 3)
        # print("data2={}".format(data2))

        time.sleep_ms(500)

    # Re-pack the pair of words into a single byte, then un-pack into a float
    # volts = struct.unpack('<f', struct.pack(
    #     '<h', int(f_word_pair[1])) + struct.pack('<h', int(f_word_pair[0])))[0]

    # print("Reading from register 0x06")
    # # 'execute' returns a pair of 16-bit words
    # f_word_pair = master.execute(1, cst.READ_HOLDING_REGISTERS, 0x06, 2)
    # # Re-pack the pair of words into a single byte, then un-pack into a float
    # amps = struct.unpack('<f', struct.pack(
    #     '<h', int(f_word_pair[1])) + struct.pack('<h', int(f_word_pair[0])))[0]

    # print(
    #     "Measured Data:\r\nVolts: {}\r\nAmps: {}".format(volts, amps))


if __name__ == "__main__":
    main()
