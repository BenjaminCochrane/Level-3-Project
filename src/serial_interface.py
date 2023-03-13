"""
Serial interfacing as a class
"""

import time
import logging
import datetime
import serial
import serial.tools.list_ports

logging.basicConfig(
    filename=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ".log",
    format='%(asctime)s %(message)s',
    filemode='w'
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class SerialInterface():
    """Class representing the connection between the receiver and the graph"""

    def __init__(self):
        """Constructor function for SerialInterface class"""
        self.name = "serial_interface"
        self.start_time = time.time()
        self.serial_instance = None
        self.port = None

        self.buffer_obj = ""

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
            logger.info("Opened port %s", self.port)

        if not self.initialised:
            logger.warning("Failed to automatically detect port")


    def read_buffer(self) -> list:
        """Read full buffer from the serial port"""
        buffer_size = self.serial_instance.inWaiting()
        if buffer_size > 0:
            #print(repr(self.serial_instance.read(buffer_size).decode('utf-8')))
            return [
                item for item in
                    self.serial_instance.read(buffer_size).decode('utf-8').split('\r\n')
                if item != ""
            ]
        logger.info("No packets were found")
        return None

    def get_values(self) -> list:
        '''Returns a list of all values in Serial Port buffer'''
        if self.serial_instance:
            buffer = self.read_buffer()

            if buffer is not None:
                current_time = time.time()

                data = []
                for item in buffer:
                    print("Item:", item)
                    try:
                        node_id, ref , rssi_value, frequency, transmitter_power =item.split('_')
                        data.append(
                            [current_time - self.start_time,
                             int(rssi_value),
                             node_id,
                             ref,
                             frequency,
                             transmitter_power]
                        )
                    except ValueError:
                        logger.info("Received packet: %s", item)
                        continue

                return data
        return None


    def get_latest(self, _ = None) -> tuple:
        """Returns a tuple containing the node_id, time (x), and RSSI (y)"""
        if self.serial_instance:
            packet = self.serial_instance.readline()

            try:
                node_id, _ , rssi_value = packet.decode('utf-8').split('_')

                print(node_id, _, rssi_value)

            #return time.time()-self.start_time, int(rssi_value[:len(rssi_value)-4]), str(node_id)
                return time.time()-self.start_time, int(rssi_value), str(node_id)

            except ValueError:
                print(packet.decode('utf-8'))
                return (None, None, None)

        raise AssertionError("No port was opened")

    def __del__(self):
        """Destructor for SerialInterface class, closes the serial connection if it was opened"""
        if self.serial_instance:
            self.serial_instance.close()
            logger.info("Serial instance was closed")

    def __str__(self):
        """Return the name of the open port as a string"""
        if self.port:
            return self.port
        return self.name

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
        time.sleep(3)
