from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class UiMain(object):
    """This class contains all the widgets and configures them for the main window."""
    def __init__(self, main_window):
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
        self.client_config_tool_btn = QToolButton()
        self.client_config_tool_btn.setAutoRaise(True)
        self.client_config_tool_btn.setIcon(QIcon("icons/outline_settings_black_24dp.png"))
        self.client_config_tool_btn.setToolTip("Communication settings")
        self.toolbar.addWidget(self.client_config_tool_btn)

        # connect button
        self.connect_tool_btn = QToolButton()
        self.connect_tool_btn.setAutoRaise(True)
        self.connect_tool_btn.setIcon(QIcon("icons/outline_link_black_24dp.png"))
        self.connect_tool_btn.setToolTip("Connection")
        self.toolbar.addWidget(self.connect_tool_btn)

        # disconnect button
        self.disconnect_tool_btn = QToolButton()
        self.disconnect_tool_btn.setAutoRaise(True)
        self.disconnect_tool_btn.setIcon(QIcon("icons/outline_link_off_black_24dp.png"))
        self.disconnect_tool_btn.setToolTip("Disconnection")
        self.toolbar.addWidget(self.disconnect_tool_btn)

        # Add com task button
        self.Add_section_tool_btn = QToolButton()
        self.Add_section_tool_btn.setAutoRaise(True)
        self.Add_section_tool_btn.setIcon(QIcon("icons/outline_add_box_black_24dp.png"))
        self.Add_section_tool_btn.setToolTip("Add task")
        self.toolbar.addWidget(self.Add_section_tool_btn)
