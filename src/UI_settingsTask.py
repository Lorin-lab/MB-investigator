from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UiSettingsTask(object):
    def init_ui(self, main_window):
        main_window.setWindowTitle('Task settings')
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # Settings
        # ****************************

        # Task name edit
        self.task_name_edit = QLineEdit()
        self.task_name_edit.setMaxLength(20)

        # Read function list
        self.read_func_list = QComboBox()

        # Starting address edit
        self.start_address_edit = QLineEdit()
        self.start_address_edit.setValidator(QIntValidator(0, 65535))
        #self.start_address_edit.setMaxLength(15)

        # length edit
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QIntValidator(0, 2000))
        #self.quantity_edit.setMaxLength(5)

        # write function list
        self.write_func_list = QComboBox()

        flo = QFormLayout()
        flo.addRow("Task name", self.task_name_edit)
        flo.addRow("Read function", self.read_func_list)
        flo.addRow("Start address", self.start_address_edit)
        flo.addRow("Quantity of register", self.quantity_edit)
        flo.addRow("Write function", self.write_func_list)
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
