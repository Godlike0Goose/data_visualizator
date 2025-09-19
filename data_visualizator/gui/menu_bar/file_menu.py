from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


class FileMenu(QMenu):
    def __init__(self, main_window):
        super().__init__("File", main_window)
        self.main_window = main_window

        self.open_dataset_action = QAction("Open Dataset", self)
        self.open_folder_action = QAction("Open Folder", self)

        self.open_folder_action.triggered.connect(
            self.main_window.open_folder_in_explorer
        )
        self.open_dataset_action.triggered.connect(self.main_window.open_dataset)

        self.addAction(self.open_dataset_action)
        self.addAction(self.open_folder_action)
