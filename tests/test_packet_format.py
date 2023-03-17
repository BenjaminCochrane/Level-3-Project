'''
Tests for abstract packet format
'''
import pytest
import sys

from src.packet_format import PacketFormat

packet_format = PacketFormat()

def test_slots() -> None:
    assert (len(packet_format.__slots__))

def test_delineating_char() -> None:
    assert (packet_format.delineator)
