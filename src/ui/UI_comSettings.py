from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.QCustomComboBox import QCustomComboBox


class UiComSettings(object):
    """This class contains all the widgets and configures them for the communications configuration menu."""
    def __init__(self, main_window):
        general_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(general_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # Selection mode
        # ****************************
        self.mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("TCP", main_window)
        self.button_mode_TCP.setChecked(True)
        general_layout.addWidget(self.button_mode_TCP)
        self.mode_button_group.addButton(self.button_mode_TCP)

        self.button_mode_RTU = QRadioButton("RTU", main_window)
        general_layout.addWidget(self.button_mode_RTU)
        self.mode_button_group.addButton(self.button_mode_RTU)

        # ****************************
        # TCP settings
        # ****************************
        self.tcp_group_box = QGroupBox("TCP")
        general_layout.addWidget(self.tcp_group_box)
        tcp_group_layout = QVBoxLayout()
        self.tcp_group_box.setLayout(tcp_group_layout)

        # IP Line edit
        self.IP_edit = QLineEdit()
        self.IP_edit.setMaxLength(15)

        # Port Line edit
        self.port_edit = QLineEdit()
        self.port_edit.setValidator(QIntValidator())
        self.port_edit.setMaxLength(5)

        flo = QFormLayout()
        flo.addRow("IP address", self.IP_edit)
        flo.addRow("Port", self.port_edit)
        tcp_group_layout.addLayout(flo)

        # ****************************
        # RTU settings
        # ****************************
        self.rtu_group_box = QGroupBox("RTU")
        general_layout.addWidget(self.rtu_group_box)
        rtu_group_layout = QVBoxLayout()
        self.rtu_group_box.setLayout(rtu_group_layout)

        self.serial_port_name_cb = QCustomComboBox()
        self.baud_rate_cb = QCustomComboBox()
        self.data_bits_cb = QCustomComboBox()
        self.parity_cb = QCustomComboBox()
        self.stop_bits_cb = QCustomComboBox()
        self.flow_control_cb = QCustomComboBox()

        flo = QFormLayout()
        flo.addRow("Port name", self.serial_port_name_cb)
        flo.addRow("Bits per second", self.baud_rate_cb)
        flo.addRow("Data bits", self.data_bits_cb)
        flo.addRow("Parity", self.parity_cb)
        flo.addRow("Stop bits", self.stop_bits_cb)
        flo.addRow("Flow control", self.flow_control_cb)
        rtu_group_layout.addLayout(flo)

        # ****************************
        # Other settings
        # ****************************
        other_group_box = QGroupBox("General settings")
        general_layout.addWidget(other_group_box)
        other_group_layout = QVBoxLayout()
        other_group_box.setLayout(other_group_layout)

        self.timeout = QLineEdit()
        self.timeout.setValidator(QDoubleValidator(0.0, 60.0, 1))

        flo = QFormLayout()
        flo.addRow("Timeout (sec)", self.timeout)
        other_group_layout.addLayout(flo)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        general_layout.addLayout(h_layout)

        self.valid_button = QPushButton()
        self.valid_button.setText("Validation")
        h_layout.addWidget(self.valid_button)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(self.cancel_button)
