import os
from PySide6.QtWidgets import (
    QWidget,
    QFileSystemModel,
    QTreeView,
    QVBoxLayout,
)
from PySide6.QtCore import QDir

class Explorer(QWidget):
    def __init__(self, main_widow):
        super().__init__()

        self.main_window = main_widow
        self.datasets_dir = os.path.abspath("./datasets")

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath("")
        self.file_system_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        self.files_tree = QTreeView()
        self.files_tree.setModel(self.file_system_model)
        self.files_tree.setRootIndex(self.file_system_model.index(self.datasets_dir))
        self.files_tree.hideColumn(1)
        self.files_tree.hideColumn(2)
        self.files_tree.hideColumn(3)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.files_tree)
