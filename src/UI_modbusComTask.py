from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class UiModbusComTask(object):
    def init_ui(self, main_window):
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setObjectName("mainWidget")
        widget.setStyleSheet("QWidget#mainWidget { "
                             "background-color : #CFCFCF;"
                             "border-radius: 5px; "
                             "margin: 2px;"
                             "border: 2px solid black;"
                             "}")
        widget.setLayout(v_layout)
        main_window.setWidget(widget)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        self.read_write_button = QPushButton()
        self.read_write_button.setText("Read/write")
        h_layout.addWidget(self.read_write_button)

        self.open_settings_btn = QPushButton()
        self.open_settings_btn.setText("Modbus parameters")
        h_layout.addWidget(self.open_settings_btn)

        # ****************************
        # Status bar
        # ****************************
        self.status_bar = QPlainTextEdit()
        self.status_bar.setFixedHeight(40)
        self.status_bar.setTextInteractionFlags(Qt.TextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard))
        self.status_print("Ready")
        v_layout.addWidget(self.status_bar)

        # ****************************
        # table
        # ****************************
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Address", "Label", "Value"])
        self.table_widget.verticalHeader().hide()
        self.table_widget.setStyleSheet("QTableWidget { "
                                        "background-color : #CFCFCF;"
                                        "border: 2px solid black;"
                                        "}")
        v_layout.addWidget(self.table_widget)

    def status_print(self, text):
        self.status_bar.insertPlainText("\n" + text)
