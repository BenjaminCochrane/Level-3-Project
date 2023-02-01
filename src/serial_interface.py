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

        initialised = False

        for port in serial.tools.list_ports.comports():
            try:
                self.port = str(port.device)
                self.serial_instance = serial.Serial(timeout = 0.25)
                self.serial_instance.baudrate = 115200
                self.serial_instance.port = self.port
                self.serial_instance.open()

                #This checks for ports sending data - is this an issue?
                #Reason: We get partial packets here: can't check format
                if self.serial_instance.readline():
                    initialised = True
                    break
            except serial.SerialException:
                continue

        #If we found a receiver reopen it without a timeout
        if self.serial_instance:
            self.serial_instance.close()
        if initialised:
            self.serial_instance = serial.Serial(timeout=None)
            self.serial_instance.baudrate = 115200
            self.serial_instance.port = self.port
            self.serial_instance.open()

        if not initialised:
            print("No ports detected")


    def get_latest(self, _ = None) -> tuple:
        """Returns a tuple containing the node_id, time (x), and RSSI (y)"""
        if self.serial_instance:
            packet = self.serial_instance.readline()
            print(packet.decode('utf-8'))

            try:
                node_id, _ , rssi_value = packet.decode('utf-8').split('_')

                print(node_id, _, rssi_value)

            #return time.time()-self.start_time, int(rssi_value[:len(rssi_value)-4]), str(node_id)
                return time.time()-self.start_time, int(rssi_value), str(node_id)

            except ValueError:
                return (None, None, None)

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
