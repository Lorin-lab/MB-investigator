from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class UiMain(object):
    def init_ui(self, main_window):
        main_window.setWindowTitle('MB-Investigator')
        main_window.resize(400, 500)

        # ****************************
        # menu bar
        # ****************************
        menu_bar = QMenuBar(main_window)
        main_window.setMenuBar(menu_bar)

        # file menu
        self.action_about = QAction("About", main_window)
        self.action_quit = QAction("Quit", main_window)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.action_about)
        file_menu.addAction(self.action_quit)

        # ****************************
        # Status bar
        # ****************************
        self.status_bar = QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

        # ****************************
        # Tool bar
        # ****************************
        self.toolbar = QToolBar(main_window)
        main_window.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        # config button
        self.client_config_toolbutton = QToolButton()
        self.client_config_toolbutton.setAutoRaise(True)
        self.client_config_toolbutton.setIcon(QIcon("icons/outline_settings_black_24dp.png"))
        self.client_config_toolbutton.setToolTip("Communication settings")
        self.toolbar.addWidget(self.client_config_toolbutton)

        # connect button
        self.connect_toolbutton = QToolButton()
        self.connect_toolbutton.setAutoRaise(True)
        self.connect_toolbutton.setIcon(QIcon("icons/outline_link_black_24dp.png"))
        self.connect_toolbutton.setToolTip("Connection")
        self.toolbar.addWidget(self.connect_toolbutton)

        # diconnect button
        self.diconnect_toolbutton = QToolButton()
        self.diconnect_toolbutton.setAutoRaise(True)
        self.diconnect_toolbutton.setIcon(QIcon("icons/outline_link_off_black_24dp.png"))
        self.diconnect_toolbutton.setToolTip("Disconnection")
        self.toolbar.addWidget(self.diconnect_toolbutton)

        # Add com task button
        self.Add_section_toolbuton = QToolButton()
        self.Add_section_toolbuton.setAutoRaise(True)
        self.Add_section_toolbuton.setIcon(QIcon("icons/outline_add_box_black_24dp.png"))
        self.Add_section_toolbuton.setToolTip("Add task")
        self.toolbar.addWidget(self.Add_section_toolbuton)
