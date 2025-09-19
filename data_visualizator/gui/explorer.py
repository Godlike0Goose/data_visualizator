"""Модуль для виджета проводника файлов.

Содержит класс Explorer, который предоставляет древовидное представление
файловой системы для навигации и открытия наборов данных.
"""

import os
import logging
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeView,
    QFileDialog,
    QLabel,
    QFileSystemModel,
)
from PySide6.QtCore import QDir, Slot

logger = logging.getLogger(__name__)


class Explorer(QWidget):
    """Виджет для просмотра файловой системы и открытия наборов данных.

    Отображает древовидную структуру каталога с наборами данных и позволяет
    пользователям открывать файлы двойным щелчком мыши.

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        datasets_dir (str): Путь к каталогу с наборами данных по умолчанию.
        file_system_model (QFileSystemModel): Модель данных файловой системы.
        files_tree (QTreeView): Древовидное представление для отображения файлов.
        opened_folder_name (QLabel): Метка для отображения имени открытой папки.
    """

    def __init__(self, main_window):
        """Инициализирует виджет Explorer.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing Explorer")

        self.main_window = main_window
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

        self.opened_folder_name = QLabel(self.datasets_dir)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.opened_folder_name)
        self.layout.addWidget(self.files_tree)

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
            self.main_window.open_dataset_from_path(path)
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
            else:
                logger.debug(
                    "Chosen folder '%s' resulted in an invalid index.", choosen_folder
                )
        else:
            logger.debug("Folder selection was cancelled.")
