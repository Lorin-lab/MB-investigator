"""
Copyright 2022-2023 Lorin Québatte

This file is part of MB-investigator.

MB-investigator is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MB-investigator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with MB-investigator. If not,
see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations  # for that RemoteDevice recognize as type hint
import serial
from modbus_tk import modbus_tcp, modbus_rtu, modbus


class RemoteDevice:
    """
    A remote device
    """

    def __init__(self):
        self.modbus_client = None

        # General settings
        self.name = "new device"
        # Modbus settings
        self.unit_id = 1
        self.reading_period = 1000
        self.reading_timeout = 2
        self.mb_writing_preference = self.WritingPreference.SINGLE
        # Communication Settings
        self.com_mode = self.ComMode.TCP
        # TCP Settings
        self.ip = "127.0.0.1"
        self.port = 502
        self.tcp_timeout = 5
        # RTU Settings
        self.serial_port_name = ""
        self.baud_rate = 9600
        self.data_bits = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stop_bits = serial.STOPBITS_ONE
        self.flow_control = self.FlowControl.NONE

    def open_connection(self) -> None:
        """
        Open the connection to the remote device
        :return: None
        """
        if self.modbus_client is None:
            self.modbus_client = self.get_modbus_client(self, self)
        self.modbus_client.open()

    def close_connection(self) -> None:
        """
        Close the connection to the remote device
        :return: None
        """
        if self.modbus_client is not None:
            self.modbus_client.close()
        self.modbus_client = None

    @staticmethod
    def get_modbus_client(self, device: RemoteDevice) -> modbus.Master:
        """
        Provides a modbus client configured according to the remote device passed as parameter
        :param self: ...
        :param device: the remote device
        :return: A modbus client configured
        """
        client = None
        # TCP and RTU over TCP
        if device.com_mode == RemoteDevice.ComMode.TCP or device.com_mode == RemoteDevice.ComMode.RTU_OVER_TCP:
            client = modbus_tcp.TcpMaster(
                device.ip,
                device.port,
                float(device.tcp_timeout)
            )
        # RTU MODE
        elif device.com_mode == RemoteDevice.ComMode.RTU:
            serial_port = serial.Serial(
                port=None,  # Set null to avoid automatic opening
                baudrate=device.baud_rate,
                bytesize=device.data_bits,
                parity=device.parity,
                stopbits=device.stop_bits,
                xonxoff=(device.flow_control == RemoteDevice.FlowControl.XON_XOFF),
                rtscts=(device.flow_control == RemoteDevice.FlowControl.RTS_CTS),
                dsrdtr=(device.flow_control == RemoteDevice.FlowControl.DSR_DTR)
            )
            serial_port.port = device.serial_port_name
            client = modbus_rtu.RtuMaster(serial_port)

        return client

    def serialize(self) -> dict:
        """
        Export configuration
        :return: Return parameters into a dictionary.
        """
        data = {
            # general
            "name": self.name,
            # modbus
            "unit_id": self.unit_id,
            "reading_period": self.reading_period,
            "reading_timeout": self.reading_timeout,
            "mb_writing_preference": self.mb_writing_preference,
            # communication
            "com_mode": self.com_mode,
            # tcp
            "ip": self.ip,
            "port": self.port,
            "timeout": self.tcp_timeout,
            # rtu
            "serial_port_name": self.serial_port_name,
            "baud_rate": self.baud_rate,
            "data_bits": self.data_bits,
            "parity": self.parity,
            "stop_bits": self.stop_bits,
            "flow_control": self.flow_control
        }
        return data

    def deserialize(self, data: dict):
        """
        Import data
        :param data: Dict that contains parameters to be imported.
        """
        if data is None:
            return

        # General
        self.name = data.get("name", self.name)
        # modbus
        self.unit_id = data.get("unit_id", self.unit_id)
        self.reading_period = data.get("reading_period", self.reading_period)
        self.reading_timeout = data.get("reading_timeout", self.reading_timeout)
        self.mb_writing_preference = data.get("mb_writing_preference", self.mb_writing_preference)
        # communication
        self.com_mode = data.get("mode", self.com_mode)
        # TCP
        self.port = data.get("port", self.port)
        self.ip = data.get("ip", self.ip)
        self.tcp_timeout = data.get("timeout", self.tcp_timeout)
        # RTU
        self.serial_port_name = data.get("serial_port_name", self.serial_port_name)
        self.baud_rate = data.get("baud_rate", self.baud_rate)
        self.data_bits = data.get("data_bits", self.data_bits)
        self.parity = data.get("parity", self.parity)
        self.stop_bits = data.get("stop_bits", self.stop_bits)
        self.flow_control = data.get("flow_control", self.flow_control)

    class ComMode:
        """Enum of communication mode."""
        TCP = 0
        RTU = 1
        RTU_OVER_TCP = 2

    class FlowControl:
        """Enum of flow control mode for serial com."""
        NONE = 0
        XON_XOFF = 1
        RTS_CTS = 2
        DSR_DTR = 3

    class WritingPreference:
        """Enum of writing function type preference"""
        SINGLE = 0
        MULTIPLE = 1
