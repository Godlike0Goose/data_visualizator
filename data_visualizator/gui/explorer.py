"""Модуль для виджета проводника файлов.

Содержит класс Explorer, который предоставляет древовидное представление
файловой системы для навигации и открытия наборов данных.
"""

import os
from PySide6.QtWidgets import (
    QVBoxLayout,
    QTreeView,
    QFileDialog,
    QLabel,
    QFileSystemModel,
)
from PySide6.QtCore import QDir, Slot, Qt
from ._base import BaseWidget

import logging

logger = logging.getLogger(__name__)


class Explorer(BaseWidget):
    """Виджет для просмотра файловой системы и открытия наборов данных.

    Отображает древовидную структуру каталога с наборами данных и позволяет
    пользователям открывать файлы двойным щелчком мыши.

    Attributes:
        app_state: Ссылка на объект состояния приложения.
        datasets_dir (str): Путь к каталогу с наборами данных по умолчанию.
        file_system_model (QFileSystemModel): Модель данных файловой системы.
        files_tree (QTreeView): Древовидное представление для отображения файлов.
        opened_folder_name (QLabel): Метка для отображения имени открытой папки.
    """

    def __init__(self, app_state):
        """Инициализирует виджет Explorer.

        Args:
            app_state: Ссылка на объект состояния приложения.
        """
        super().__init__("Explorer")
        logger.debug("Initializing Explorer")

        self.app_state = app_state
        self.datasets_dir = os.path.abspath("./datasets")
        logger.debug(f"Default datasets directory: {self.datasets_dir}")

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

        self.opened_folder_name = QLabel()
        self.opened_folder_name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.opened_folder_name.setWordWrap(True)
        self.opened_folder_name.setStyleSheet("padding: 2px; border-bottom: 1px solid #c0c0c0;")
        # Устанавливаем начальное значение
        self.opened_folder_name.setText(self.datasets_dir)

        layout = QVBoxLayout(self.content_widget)
        layout.addWidget(self.opened_folder_name)
        layout.addWidget(self.files_tree)

        self.files_tree.doubleClicked.connect(self.open_table)

        logger.debug("Explorer initialized")

    @Slot()
    def open_table(self, index):
        """Открывает набор данных, соответствующий выбранному элементу в дереве.

        Слот для обработки сигнала `doubleClicked` от `files_tree`.

        Args:
            index (QModelIndex): Индекс элемента, по которому был сделан двойной щелчок.
        """
        path = self.file_system_model.filePath(index)
        if path:
            logger.debug("Opening dataset: %s", path)
            self.app_state.load_dataset_from_path(path)
        else:
            logger.debug("Path is empty, not opening dataset.")

    @Slot()
    def open_folder(self):
        """Открывает диалоговое окно для выбора папки.

        После выбора папки обновляет корневой элемент в `files_tree`,
        чтобы отобразить ее содержимое.
        """
        logger.debug("Opening folder selection dialog.")
        choosen_folder = QFileDialog.getExistingDirectory(
            self,
            caption="Select Folder",
            dir=os.path.expanduser("~"),
        )
        if choosen_folder:
            logger.debug("Folder chosen: %s", choosen_folder)
            index = self.file_system_model.index(choosen_folder)
            if index.isValid():
                logger.debug("Setting new root index for QTreeView: %s", index)
                self.files_tree.setRootIndex(index)
                # Обновляем метку с путем к новой папке
                self.opened_folder_name.setText(choosen_folder)
                self.app_state.status_message_requested.emit(f"Открыта папка: {choosen_folder}", 3000)
            else:
                logger.debug(
                    "Chosen folder '%s' resulted in an invalid index.", choosen_folder
                )
        else:
            logger.debug("Folder selection was cancelled.")
