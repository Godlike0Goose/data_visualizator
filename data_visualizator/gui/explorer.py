import os
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFileSystemModel,
    QTreeView,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
)
from PySide6 import QtCore
from PySide6.QtCore import QDir


class Explorer(QWidget):
    def __init__(self, main_widow):
        super().__init__()

        self.main_window = main_widow
        self.datasets_dir = os.path.abspath("./datasets")

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath("")
        self.file_system_model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )

        self.files_tree = QTreeView()
        self.files_tree.setModel(self.file_system_model)
        self.files_tree.setRootIndex(self.file_system_model.index(self.datasets_dir))
        self.files_tree.hideColumn(1)
        self.files_tree.hideColumn(2)
        self.files_tree.hideColumn(3)

        self.opened_folder_name = QLabel(self.datasets_dir)
        self.choosing_folder_button = QPushButton("choose a dir")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.files_tree)
        self.layout.addWidget(self.opened_folder_name)
        self.layout.addWidget(self.choosing_folder_button)

        self.files_tree.doubleClicked.connect(self.open_table)
        self.choosing_folder_button.clicked.connect(self.open_folder)

    @QtCore.Slot()
    def open_table(self, index):
        path = self.file_system_model.filePath(index)
        if path:
            self.main_window.open_dataset(path)

    @QtCore.Slot()
    def open_folder(self):
        choosen_folder = QFileDialog.getExistingDirectory(
            self,
            caption="выбор папки",
            dir=os.path.expanduser("~"),
        )
        if choosen_folder:
            index = self.file_system_model.index(choosen_folder)
            if index.isValid():
                self.files_tree.setRootIndex(index)
