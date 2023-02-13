"""
Tests for the serial interface
"""

import serial

from src.serial_interface import SerialInterface
serial_interface_obj = SerialInterface();

def test_serial_initialisation() -> None:
    """Test that the creation of the serial interface was successful"""
    assert (type(serial_interface_obj) == SerialInterface)

def test_serial_port() -> None:
    """Test the default name of the serial interface"""

    assert (str(serial_interface_obj) == "serial_interface")

def test_get_latest() -> None:
    """Test that get_latest raises an AssertionError if no connected serial"""
    try:
        serial_interface_obj.get_latest()

    except AssertionError:
        assert (True)

def test_get_values() -> None:
    '''Test get_values and read_buffer'''
    assert (serial_interface_obj.get_values() == None)

def test_str():
    '''Test string representation'''
    assert (str(serial_interface_obj) == "serial_interface")

#def test_delete():
#    '''Test deletion'''
#    del serial_interface_obj
#    assert (True)
