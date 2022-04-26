from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UiSettingsCom(object):
    """This class contains all the widgets and configures them for the communications configuration menu."""
    def __init__(self, main_window):
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # Selection mode
        # ****************************
        mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("TCP", main_window)
        self.button_mode_TCP.setChecked(True)
        v_layout.addWidget(self.button_mode_TCP)
        mode_button_group.addButton(self.button_mode_TCP)

        self.button_mode_RTU = QRadioButton("RTU", main_window)
        self.button_mode_RTU.setDisabled(True)
        v_layout.addWidget(self.button_mode_RTU)
        mode_button_group.addButton(self.button_mode_RTU)

        # ****************************
        # Line edit
        # ****************************
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

        v_layout.addLayout(flo)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        self.valid_button = QPushButton()
        self.valid_button.setText("Validation")
        h_layout.addWidget(self.valid_button)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(self.cancel_button)
