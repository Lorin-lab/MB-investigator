from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class UiAboutWin(object):
    """This class contains all the widgets and configures them for the about window."""
    def __init__(self, main_window):
        main_window.setWindowTitle('About')
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        main_window.setCentralWidget(widget)

        # title
        title = QLabel("MB-investigator \nby Lorin-lab")
        title.setStyleSheet("QLabel {font-size: 20px;}")
        v_layout.addWidget(title)

        # Version
        v_layout.addWidget(QLabel("Version: v0.0.0"))

        # Licence
        v_layout.addWidget(QLabel("Licence: GNU General Public License"))

        # Source code link
        source_code_link = QLabel()
        source_code_link.setText(
            "Source code: "
            "<a href=\"https://github.com/Lorin-lab/MB-investigator\">https://github.com/Lorin-lab/MB-investigator</a>"
        )
        source_code_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        source_code_link.setOpenExternalLinks(True)
        v_layout.addWidget(source_code_link)
