import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main import ModbusMode


class clientConfigMenu(QMainWindow):

    def __init__(self, parent, data_send_back_fun, config_data):
        super(clientConfigMenu, self).__init__(parent)
        self.data_send_back_fun = data_send_back_fun
        self.config_data = config_data
        self.initUI(config_data)

    def validation(self):
        self.config_data["ip"] = self.IP_edit.text()
        self.config_data["port"] = self.port_edit.text()
        self.data_send_back_fun(self.config_data)
        self.close()

    def cancel(self):
        self.close()

    def initUI(self, config_data):
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

        # ****************************
        # Selection mode
        # ****************************
        mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("TCP", self)
        self.button_mode_TCP.setChecked(True)
        v_layout.addWidget(self.button_mode_TCP)
        mode_button_group.addButton(self.button_mode_TCP)

        self.button_mode_RTU = QRadioButton("RTU", self)
        self.button_mode_RTU.setDisabled(True)
        v_layout.addWidget(self.button_mode_RTU)
        mode_button_group.addButton(self.button_mode_RTU)


        # ****************************
        # Line edit
        # ****************************
        # IP Line edit
        self.IP_edit = QLineEdit()
        self.IP_edit.setMaxLength(15)
        self.IP_edit.setText(config_data["ip"])

        # Port Line edit
        self.port_edit = QLineEdit()
        self.port_edit.setValidator(QIntValidator())
        self.port_edit.setText(config_data["port"])
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

        valid_button = QPushButton()
        valid_button.setText("Validation")
        valid_button.clicked.connect(self.validation)
        h_layout.addWidget(valid_button)

        cancel_button = QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.cancel)
        cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(cancel_button)
