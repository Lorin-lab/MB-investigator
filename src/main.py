import sys
import clientConfigMenu
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from easymodbus.modbusClient import ModbusClient
import asyncio


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config_data = {
            "ip": "127.0.0.1",
            "port": 502
        }
        self.MB_client = None
        self.initUI()
        self.statusBar().showMessage("Welcome")

    def openClientConfigMenu(self):
        menu = clientConfigMenu.clientConfigMenu(self, self.setClientConfig, self.config_data)
        menu.show()

    def tryClientConnect(self):
        self.statusBar().showMessage("Try connecting to " + self.config_data["ip"] + " ...")
        print("Try connecting to " + self.config_data["ip"] + " ...")
        self.MB_client = ModbusClient(self.config_data["ip"], self.config_data["port"])
        try:
            self.MB_client.connect()
            if self.MB_client.is_connected():
                self.statusBar().showMessage("Successful connection")
            else:
                self.statusBar().showMessage("Connection failed")
        except ConnectionRefusedError:
            self.statusBar().showMessage("Connection Refused")
        finally:
            print("is coi" + str(self.MB_client.is_connected()))
            #print(self.MB_client.__tcpClientSocket)

    def setClientConfig(self, config_data):
        print(config_data["ip"])
        self.config_data["ip"] = config_data["ip"]
        print(config_data["port"])
        self.config_data["port"] = config_data["port"]

    def initUI(self):
        self.setWindowTitle('MB-Investigator')
        self.setGeometry(400, 400, 600, 400)

        # ****************************
        # menu bar
        # ****************************
        self.menu_bar = self.menuBar()

        # file menu
        self.file_menu = self.menu_bar.addMenu('File')
        self.file_menu.addAction('Save config')
        self.file_menu.addAction('Import config')
        self.file_menu.addAction('Quit')

        # config menu
        self.config_menu = self.menu_bar.addMenu('Config')
        self.config_menu.addAction("Client config")

        # ****************************
        # Status bar
        # ****************************
        self.statusBar()

        # ****************************
        # Tool bar
        # ****************************
        self.toolbar = self.addToolBar("toolBar")

        # config button
        client_config_toolbutton = QToolButton()
        client_config_toolbutton.setArrowType(Qt.LeftArrow)
        client_config_toolbutton.setAutoRaise(True)
        client_config_toolbutton.clicked.connect(self.openClientConfigMenu)
        self.toolbar.addWidget(client_config_toolbutton)

        # connect button
        connect_toolbutton = QToolButton()
        connect_toolbutton.setArrowType(Qt.UpArrow)
        connect_toolbutton.setAutoRaise(True)
        connect_toolbutton.clicked.connect(self.tryClientConnect)
        self.toolbar.addWidget(connect_toolbutton)

        # diconnect button
        diconnect_toolbutton = QToolButton()
        diconnect_toolbutton.setArrowType(Qt.DownArrow)
        diconnect_toolbutton.setAutoRaise(True)
        diconnect_toolbutton.clicked.connect(self.openClientConfigMenu)
        self.toolbar.addWidget(diconnect_toolbutton)

        # Add section button
        Add_section_toolbuton = QToolButton()
        Add_section_toolbuton.setArrowType(Qt.RightArrow)
        Add_section_toolbuton.setAutoRaise(True)
        Add_section_toolbuton.clicked.connect(self.openClientConfigMenu)
        self.toolbar.addWidget(Add_section_toolbuton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
