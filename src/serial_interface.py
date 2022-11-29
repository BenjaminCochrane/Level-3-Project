"""
Serial interfacing as a class
"""

import time
import serial
import serial.tools.list_ports

class SerialInterface():
    """Class representing the connection between the receiver and the graph"""

    def __init__(self):
        """Constructor function for SerialInterface class"""
        self.name = "serial_interface"
        self.start_time = time.time()
        self.serial_instance = None
        self.port = None


        for port in serial.tools.list_ports.comports():
            print(port.device)

        #if(serial.tools.list_ports.comports()):
        for port in serial.tools.list_ports.comports():
            if self.serial_instance:
                try:
                    self.port = str(port.device)

                    self.serial_instance = serial.Serial()
                    self.serial_instance.baudrate = 115200
                    self.serial_instance.port = self.port
                    self.serial_instance.open()

                    assert isinstance(self.get_latest(), tuple)
                except AssertionError:
                    print("Port No worky")

                    # If port was opened, but data was in the wrong format try a different port
                    if self.serial_instance:
                        self.serial_instance.close()

        if not self.serial_instance:
            print("No ports detected")


    def get_latest(self) -> tuple:
        """Returns a tuple containing the node_id, time (x), and RSSI (y)"""
        if self.serial_instance:
            packet = self.serial_instance.readline()

            node_id, _ , rssi_value = packet.decode('utf-8').split('_')

            return time.time()-self.start_time, int(rssi_value[:len(rssi_value)-4]), int(node_id)

        raise AssertionError("No port was opened")

    def __del__(self):
        """Destructor for SerialInterface class, closes the serial connection if it was opened"""
        if self.serial_instance:
            self.serial_instance.close()

    def __str__(self):
        """Return the name of the open port as a string"""
        if self.port:
            return self.port
        return self.name

if __name__ == "__main__":
    serial_interface_obj = SerialInterface()
    while True:
        print(serial_interface_obj.get_latest())
