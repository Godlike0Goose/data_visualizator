import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QSplitter, QFileDialog
from PySide6 import QtCore

from .explorer import Explorer
from .tables import DataSetViewer
from .model_configurator import ModelConfigGroup
from .menu_bar import FileMenu

from ..logging_setup import setup_logger

logger = setup_logger()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_central_widget()
        self.init_menu_bar()

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

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = FileMenu(self)
        menu_bar.addMenu(file_menu)

    def open_dataset(self):
        open_file_dialog = QFileDialog(self)
        open_file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        open_file_dialog.setNameFilter("CSV files (*.csv)")
        open_file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if open_file_dialog.exec():
            file_path = open_file_dialog.selectedFiles()[0]
            self.open_dataset_from_path(file_path)

    def open_dataset_from_path(self, path):
        self.dataset_viewer.open_dataset(path)
        self.model_config.show_widgets()

    def get_all_column_names(self):
        return self.dataset_viewer.get_all_column_names()

    def change_target_var(self, target):
        self.dataset_viewer.change_target_var_color(target)
        self.model_config.feature_select_widget.update_feature_list()

    def get_features(self):
        return self.dataset_viewer.get_features()

    def open_folder_in_explorer(self):
        self.explorer.open_folder()


def start():
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
