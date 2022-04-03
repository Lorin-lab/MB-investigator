from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UiMain(object):
    def init_ui(self, main_window):
        main_window.setWindowTitle('MB-Investigator')
        main_window.setGeometry(400, 400, 340, 400)

        # ****************************
        # menu bar
        # ****************************
        self.menu_bar = QMenuBar(main_window)
        main_window.setMenuBar(self.menu_bar)

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
        self.status_bar = QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

        # ****************************
        # Tool bar
        # ****************************
        self.toolbar = QToolBar(main_window)
        main_window.addToolBar(self.toolbar)

        # config button
        self.client_config_toolbutton = QToolButton()
        self.client_config_toolbutton.setAutoRaise(True)
        self.client_config_toolbutton.setIcon(QIcon("icons/outline_settings_black_24dp.png"))
        self.toolbar.addWidget(self.client_config_toolbutton)

        # connect button
        self.connect_toolbutton = QToolButton()
        self.connect_toolbutton.setAutoRaise(True)
        self.connect_toolbutton.setIcon(QIcon("icons/outline_link_black_24dp.png"))
        self.toolbar.addWidget(self.connect_toolbutton)

        # diconnect button
        self.diconnect_toolbutton = QToolButton()
        self.diconnect_toolbutton.setAutoRaise(True)
        self.diconnect_toolbutton.setIcon(QIcon("icons/outline_link_off_black_24dp.png"))
        self.toolbar.addWidget(self.diconnect_toolbutton)

        # Add com task button
        self.Add_section_toolbuton = QToolButton()
        self.Add_section_toolbuton.setAutoRaise(True)
        self.Add_section_toolbuton.setIcon(QIcon("icons/outline_add_box_black_24dp.png"))
        self.toolbar.addWidget(self.Add_section_toolbuton)
