"""
Serial interfacing as a class
"""

import time
import logging
import datetime
import serial
import serial.tools.list_ports
from packet_format import PacketFormat

MAX_VALUE = 2 ** 32 / 4000

logging.basicConfig(
    filename=str(datetime.datetime.now().strftime("%Y-%m-%d %H_%M")) + ".log",
    format='%(asctime)s %(message)s',
    filemode='w'
)

logging.getLogger('matplotlib.font_manager').disabled = True
LOGGER = logging.getLogger()
#logger.setLevel(logging.DEBUG)

class SerialInterface():
    """Class representing the connection between the receiver and the graph"""

    def __init__(self):
        """Constructor function for SerialInterface class"""
        self.start_time = time.time()
        self.serial_instance = None
        self.port = None

        #Counter for when time value overflows
        self.overflow_counter = 0
        self.last_time = 0

        self.initialised = False

        for port in serial.tools.list_ports.comports():
            try:
                self.port = str(port.device)
                self.serial_instance = serial.Serial(timeout = 1)
                self.serial_instance.baudrate = 115200
                self.serial_instance.port = self.port
                self.serial_instance.open()

                #This checks for ports sending data - is this an issue?
                #Reason: We get partial packets here: can't check format
                if self.serial_instance.readline():
                    self.initialised = True
                    LOGGER.warning("Opened port %s", self.port)
                    break
            except serial.SerialException:
                continue

        #If we found a receiver reopen it without a timeout
        if self.serial_instance:
            self.serial_instance.close()

        if self.initialised:
            self.serial_instance = serial.Serial(timeout=0)
            self.serial_instance.baudrate = 115200
            self.serial_instance.port = self.port
            self.serial_instance.open()
            LOGGER.warning("Opened port %s", self.port)

        if not self.initialised:
            LOGGER.warning("Failed to automatically detect port")


    def read_buffer(self) -> list:
        """Read full buffer from the serial port"""
        buffer_size = self.serial_instance.in_waiting
        if buffer_size > 0:
            #print(repr(self.serial_instance.read(buffer_size).decode('utf-8')))
            return [
                item for item in
                    self.serial_instance.read(buffer_size).decode('utf-8').split('\n\r')
                if item != ""
            ]
        LOGGER.info("No packets were found")
        return None

    def get_values(self) -> list:
        '''Returns a list of all values in Serial Port buffer'''
        if not self.serial_instance:
            return None

        buffer = self.read_buffer()
        if not buffer:
            return None

        data = []
        for item in buffer:
            packet = PacketFormat()
            try:
                packet_split = item.split(packet.delineator)
                assert(len(packet_split) == len(packet.__slots__))

                for attribute, slot in enumerate(packet.__slots__):
                    if slot == 'reference':
                        packet_split[attribute-1] = str(
                            packet_split[attribute - 1]) + '-' + str(packet_split[attribute]
                        )
                    elif slot == 'time':
                        packet_split[attribute] = int(packet_split[attribute])
                        if self.last_time > packet_split[attribute]:
                            #Clock overflowed its 32bit hardware limit
                            self.overflow_counter += 1
                        self.last_time = packet_split[attribute]

                        packet_split[attribute] += self.overflow_counter * MAX_VALUE
                        packet_split[attribute] /= 1000

                    else:
                        packet_split[attribute] = int(packet_split[attribute])
                    setattr(packet, slot, packet_split[attribute])

                data.append(packet_split)

            except (ValueError, AssertionError) as _:
                LOGGER.info("Received packet: %s", item)
                continue

        return data

    def __del__(self):
        """Destructor for SerialInterface class, closes the serial connection if it was opened"""
        if self.serial_instance:
            self.serial_instance.close()
            LOGGER.info("Serial instance was closed")

    def __str__(self):
        """Return the name of the open port as a string"""
        if self.port:
            return self.port
        return "Serial Interface"

    def get_initialised(self):
        """Returns the serial interfaces' intialisation state"""
        return self.initialised

    def get_serial_instance(self):
        """Returns serial instance (mock/serial)"""
        return self.serial_instance

    def get_port_list(self) -> list:
        """Returns the list of ports that are available"""
        return [str(port.device) for port in serial.tools.list_ports.comports()]

    def set_port_manually(self, device):
        """Sets each port that is available manually"""
        self.port = device
        self.serial_instance = serial.Serial(timeout=None)
        self.serial_instance.baudrate = 115200
        self.serial_instance.port = self.port
        self.serial_instance.open()

if __name__ == "__main__":
    serial_interface_obj = SerialInterface()
    print(serial_interface_obj)
    while True:
        print("values: ", serial_interface_obj.get_values())
        print("End of values")
        print("\n\n")
