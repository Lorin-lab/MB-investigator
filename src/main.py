import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.statusBar().showMessage("Welcome")


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
        client_config_toolbutton.clicked.connect(self.openClientConfig)
        self.toolbar.addWidget(client_config_toolbutton)

        # connect button
        connect_toolbutton = QToolButton()
        connect_toolbutton.setArrowType(Qt.UpArrow)
        connect_toolbutton.setAutoRaise(True)
        connect_toolbutton.clicked.connect(self.openClientConfig)
        self.toolbar.addWidget(connect_toolbutton)

        # diconnect button
        diconnect_toolbutton = QToolButton()
        diconnect_toolbutton.setArrowType(Qt.DownArrow)
        diconnect_toolbutton.setAutoRaise(True)
        diconnect_toolbutton.clicked.connect(self.openClientConfig)
        self.toolbar.addWidget(diconnect_toolbutton)

        # Add section button
        Add_section_toolbuton = QToolButton()
        Add_section_toolbuton.setArrowType(Qt.RightArrow)
        Add_section_toolbuton.setAutoRaise(True)
        Add_section_toolbuton.clicked.connect(self.openClientConfig)
        self.toolbar.addWidget(Add_section_toolbuton)


    def openClientConfig(self):
        self.statusBar().showMessage("Close Detail....")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
