from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from QCustomComboBox import QCustomComboBox


class UiSettingsTask(object):
    """This class contains all the widgets and configures them for the task configuration menu."""
    def __init__(self, main_window):
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

        # Starting address edit
        self.unit_id_edit = QLineEdit()
        self.unit_id_edit.setValidator(QIntValidator(0, 255))

        # Read function list
        self.read_func_cb = QCustomComboBox()

        # write function list
        self.write_func_cb = QCustomComboBox()

        # Starting address edit
        self.start_address_edit = QLineEdit()
        self.start_address_edit.setValidator(QIntValidator(0, 65535))

        # length edit
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QIntValidator(0, 2000))

        flo = QFormLayout()
        flo.addRow("Task name", self.task_name_edit)
        flo.addRow("Unit ID", self.unit_id_edit)
        flo.addRow("Read function", self.read_func_cb)
        flo.addRow("Write function", self.write_func_cb)
        flo.addRow("Start address", self.start_address_edit)
        flo.addRow("Quantity of register", self.quantity_edit)
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
