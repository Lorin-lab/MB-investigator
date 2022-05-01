from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from enum import Enum
import serial
import serial.tools.list_ports

from ui import UI_comSettings


class ComSettings(QMainWindow):
    """This class contains the communication parameters and is the menu for editing them."""
    def __init__(self, parent, call_back_func):
        super(ComSettings, self).__init__(parent)
        self._call_back_func = call_back_func

        # General Settings
        self.mode = self.MbMode.TCP
        self.timeout = 5.0

        # TCP Settings
        self.ip = "192.168.0.123"
        self.port = 502

        # RTU Settings
        self.serial_port_name = ""
        self.baud_rate = 9600
        self.data_bits = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stop_bits = serial.STOPBITS_ONE
        self.flow_control = self.FlowControl.NONE

        # UI setup
        self._ui = self._setup_ui()
        self._on_mode_changed()

        # Setup Combo options
        baud_rate_list = [50, 75, 110, 134, 150, 200, 300, 600, 1200,
                          1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        for i in baud_rate_list:
            self._ui.baud_rate_cb.add_option(i, str(i))
        self._ui.baud_rate_cb.set_current_by_value(9600)

        self._ui.data_bits_cb.add_option(serial.FIVEBITS, "5"),
        self._ui.data_bits_cb.add_option(serial.SIXBITS, "6"),
        self._ui.data_bits_cb.add_option(serial.SEVENBITS, "7"),
        self._ui.data_bits_cb.add_option(serial.EIGHTBITS, "8", set_as_current=True)

        self._ui.parity_cb.add_option(serial.PARITY_NONE, "None", set_as_current=True),
        self._ui.parity_cb.add_option(serial.PARITY_EVEN, "Even"),
        self._ui.parity_cb.add_option(serial.PARITY_ODD, "Odd"),
        self._ui.parity_cb.add_option(serial.PARITY_MARK, "Mark"),
        self._ui.parity_cb.add_option(serial.PARITY_SPACE, "Space")

        self._ui.stop_bits_cb.add_option(serial.STOPBITS_ONE, "1", set_as_current=True),
        self._ui.stop_bits_cb.add_option(serial.STOPBITS_ONE_POINT_FIVE, "1.5"),
        self._ui.stop_bits_cb.add_option(serial.STOPBITS_TWO, "2")

        self._ui.flow_control_cb.add_option(self.flow_control.NONE, "None", set_as_current=True),
        self._ui.flow_control_cb.add_option(self.flow_control.XON_XOFF, "xON/xOFF (software)"),
        self._ui.flow_control_cb.add_option(self.flow_control.RTS_CTS, "RTS/CTS (hardware)"),
        self._ui.flow_control_cb.add_option(self.flow_control.DSR_DTR, "DSR/DTR (hardware)")

    def showEvent(self, event: QShowEvent) -> None:
        """Called when the settings is open"""
        print("show")
        self._refresh_serial_port()

    def _refresh_serial_port(self):
        """List avaible serial port and refresh combo box"""
        serial_list = serial.tools.list_ports.comports()
        self._ui.serial_port_name_cb.clear_options()

        if len(serial_list) > 0:
            print("__Ports__")
            for port, desc, hwid in sorted(serial_list):
                print("{}: {} [{}]".format(port, desc, hwid))
                self._ui.serial_port_name_cb.add_option(port, "({0}) {1}".format(port, desc))
        else:
            self._ui.serial_port_name_cb.add_option(None, "None found")

    def _validation(self):
        """save the settings close the menu and call the 'call back' function"""
        # General settings
        self.timeout = float(self._ui.timeout.text())
        if self._ui.button_mode_TCP.isChecked():
            self.mode = self.MbMode.TCP
        else:
            self.mode = self.MbMode.RTU

        # TCP settings
        self.ip = self._ui.IP_edit.text()
        self.port = int(self._ui.port_edit.text())

        # RTU settings
        self.serial_port_name = self._ui.serial_port_name_cb.get_current_option_value()
        self.baud_rate = self._ui.baud_rate_cb.get_current_option_value()
        self.data_bits = self._ui.data_bits_cb.get_current_option_value()
        self.parity = self._ui.parity_cb.get_current_option_value()
        self.stop_bits = self._ui.stop_bits_cb.get_current_option_value()
        self.flow_control = self._ui.flow_control_cb.get_current_option_value()

        self.close()
        self._call_back_func()

    def _cancel(self):
        """Reset widget with actual settings and close the menu"""
        # General settings
        self._ui.timeout.setText(str(self.timeout))
        self._ui.button_mode_TCP.setChecked(self.mode == self.MbMode.TCP)
        self._ui.button_mode_RTU.setChecked(self.mode == self.MbMode.RTU)

        # TCP settings
        self._ui.port_edit.setText(str(self.port))
        self._ui.IP_edit.setText(self.ip)

        # RTU settings
        self._ui.serial_port_name_cb.set_current_by_value(self.serial_port_name)
        self._ui.baud_rate_cb.set_current_by_value(self.baud_rate)
        self._ui.data_bits_cb.set_current_by_value(self.data_bits)
        self._ui.parity_cb.set_current_by_value(self.parity)
        self._ui.stop_bits_cb.set_current_by_value(self.stop_bits)
        self._ui.flow_control_cb.set_current_by_value(self.flow_control)

        self.close()

    def _on_mode_changed(self, id: int=0):
        """Is colled when communication mode is changed"""
        is_tcp = self._ui.button_mode_TCP.isChecked()
        self._ui.tcp_group_box.setDisabled(not is_tcp)
        self._ui.rtu_group_box.setDisabled(is_tcp)

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_comSettings.UiComSettings(self)

        # general settings
        ui.mode_button_group.idClicked.connect(self._on_mode_changed)
        ui.timeout.setText(str(self.timeout))

        # TCP settings
        ui.port_edit.setText(str(self.port))
        ui.IP_edit.setText(self.ip)

        # Buttons
        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui

    class MbMode(Enum):
        """Enum of communication mode."""
        TCP = 0
        RTU = 1

    class FlowControl(Enum):
        """Enum of flow control mode for serial com."""
        NONE = 0
        XON_XOFF = 1
        RTS_CTS = 2
        DSR_DTR = 3
