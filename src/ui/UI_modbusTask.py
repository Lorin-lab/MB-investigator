from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime


class UiModbusTask(object):
    """This class contains all the widgets and configures them for the modbus task menu."""
    def __init__(self, main_window):
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

        self.read_button = QPushButton()
        self.read_button.setText("Read")
        h_layout.addWidget(self.read_button)

        self.write_button = QPushButton()
        self.write_button.setText("Write")
        h_layout.addWidget(self.write_button)

        self.open_settings_btn = QPushButton()
        self.open_settings_btn.setText("Modbus parameters")
        h_layout.addWidget(self.open_settings_btn)

        # ****************************
        # Status bar
        # ****************************
        self.plain_text_log = QPlainTextEdit()
        self.plain_text_log.setFixedHeight(40)
        self.plain_text_log.setTextInteractionFlags(Qt.TextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard))
        self.log_print("Ready")
        v_layout.addWidget(self.plain_text_log)

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

    def log_print(self, text):
        """insert log into the plain text widget"""
        now = datetime.now()
        current_time = now.strftime("[%H:%M:%S] ")
        self.plain_text_log.insertPlainText("\n" + current_time + text)
        self.plain_text_log.ensureCursorVisible()
