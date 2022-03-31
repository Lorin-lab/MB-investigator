from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UiModbusComTask(object):
    def init_ui(self, main_window):
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setObjectName("mainWidget")
        widget.setStyleSheet("QWidget#mainWidget { "
                                 "background-color : #CFCFCF;"
                                 "border-radius: 10px; "
                                 "margin: 2px;"
                                 "border: 2px solid black;"
                             "}")
        widget.setLayout(v_layout)
        main_window.setWidget(widget)

        # ****************************
        # Selection mode
        # ****************************
        self.cb = QComboBox()
        v_layout.addWidget(self.cb)

        # ****************************
        # Line edit
        # ****************************
        # IP Line edit
        self.start_address_edit = QLineEdit()
        self.start_address_edit.setValidator(QIntValidator(0, 65535))
        self.start_address_edit.setMaxLength(15)
        self.start_address_edit.setText("0")

        # Port Line edit
        self.num_registre_edit = QLineEdit()
        self.num_registre_edit.setValidator(QIntValidator(0, 2000))
        self.num_registre_edit.setText("10")
        self.num_registre_edit.setMaxLength(5)

        flo = QFormLayout()
        flo.addRow("Start address", self.start_address_edit)
        flo.addRow("Number of registre", self.num_registre_edit)
        v_layout.addLayout(flo)

        # ****************************
        # table
        # ****************************
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Address", "Label", "Value"])
        v_layout.addWidget(self.table_widget)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        valid_button = QPushButton()
        valid_button.setText("Read/write")
        # valid_button.clicked.connect(self.validation)
        h_layout.addWidget(valid_button)

