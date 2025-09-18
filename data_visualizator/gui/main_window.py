import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QSplitter
from PySide6 import QtCore

from .explorer import Explorer
from .tables import DataSetViewer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.explorer = Explorer(self)
        self.dataset_viewer = DataSetViewer(self)

        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.explorer)
        self.splitter.addWidget(self.dataset_viewer)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.splitter)

    def open_dataset(self, path):
        self.dataset_viewer.open_dataset(path)


def start():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
