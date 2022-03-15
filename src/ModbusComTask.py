from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ModbusComTask(QDockWidget):
    def __init__(self, parent):
        super(ModbusComTask, self).__init__("New task", parent)
        self.MB_function_code_list = (
           "(FC01) Read Colls",
           "(FC02) Read Discrete",
           "(FC03) Read Holding Registers",
           "(FC04) Read Input Registers",
           "(FC05) Write Single Coll",
           "(FC06) Write Single Register",
           "(FC15) Write Multiple Colls",
           "(FC16) Write Multiple Registers"
        )
        self.raw_values = [None]

        self.initUI()
        self.resetTable()

    def resetTable(self):
        print("reset table")
        start_address = int(self.start_address_edit.text())
        num_registre = int(self.num_registre_edit.text())

        for i in range(start_address, start_address + num_registre):
            self.raw_values.append(None)

        self.updateTable()

    def updateTable(self):
        start_address = int(self.start_address_edit.text())
        num_registre = int(self.num_registre_edit.text())

        self.table_widget.setRowCount(num_registre)

        for i in range(num_registre):
            # column 0 : modbus address
            item = QTableWidgetItem(str(start_address + i))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.table_widget.setItem(i, 0, item)
            # column 1 : libelle
            self.table_widget.setItem(i, 1, QTableWidgetItem(""))
            # column 2 : value
            item = QTableWidgetItem(str(self.raw_values[i]))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.table_widget.setItem(i, 2, item)

    def initUI(self):
        self.setStyleSheet("background-color : grey")
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        self.setWidget(widget)

        # ****************************
        # Selection mode
        # ****************************

        self.cb = QComboBox()
        self.cb.addItems(self.MB_function_code_list)
        v_layout.addWidget(self.cb)

        # ****************************
        # Line edit
        # ****************************
        # IP Line edit
        self.start_address_edit = QLineEdit()
        self.start_address_edit.setValidator(QIntValidator())
        self.start_address_edit.setMaxLength(15)
        self.start_address_edit.setText("0")

        # Port Line edit
        self.num_registre_edit = QLineEdit()
        self.num_registre_edit.setValidator(QIntValidator())
        self.num_registre_edit.setText("10")
        self.num_registre_edit.setMaxLength(5)

        flo = QFormLayout()
        flo.addRow("Start address", self.start_address_edit)
        flo.addRow("Number of registre", self.num_registre_edit)
        v_layout.addLayout(flo)

        self.start_address_edit.returnPressed.connect(self.resetTable)
        self.num_registre_edit.returnPressed.connect(self.resetTable)

        # ****************************
        # table
        # ****************************
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        v_layout.addWidget(self.table_widget)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        valid_button = QPushButton()
        valid_button.setText("Read/write")
        #valid_button.clicked.connect(self.validation)
        h_layout.addWidget(valid_button)

