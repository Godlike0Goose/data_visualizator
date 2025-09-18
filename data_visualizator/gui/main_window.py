import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from .explorer import Explorer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.explorer = Explorer(self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.explorer)


def start():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())