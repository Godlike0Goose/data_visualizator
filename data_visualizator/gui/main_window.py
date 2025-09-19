import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QSplitter
from PySide6 import QtCore

from .explorer import Explorer
from .tables import DataSetViewer
from .model_configurator import ModelConfigGroup
from ..logging_setup import setup_logger

logger = setup_logger()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_central_widget()
    
    def init_central_widget(self):
        logger.info("Starting application")

        self.setWindowTitle("Data Visualizator")
        self.explorer = Explorer(self)
        self.dataset_viewer = DataSetViewer(self)
        self.model_config = ModelConfigGroup(self)

        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.explorer)
        self.splitter.addWidget(self.dataset_viewer)
        self.splitter.addWidget(self.model_config)
        self.splitter.setSizes([200, 600, 200])

        self.setCentralWidget(self.splitter)    

    def open_dataset(self, path):
        self.dataset_viewer.open_dataset(path)
        self.model_config.show_widgets()

    def get_all_coloumns_names(self):
        return self.dataset_viewer.get_all_coloumns_names()
    
    def change_target_var(self, target):
        self.dataset_viewer.change_target_var_color(target)

    def get_features(self):
        return self.dataset_viewer.get_features()




def start():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
