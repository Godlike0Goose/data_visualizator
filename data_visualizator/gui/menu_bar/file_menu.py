"""Модуль для создания меню "File" в строке меню."""

from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction  # pylint: disable=no-name-in-module
from ..actions import FileActions


class FileMenu(QMenu):  # pylint: disable=too-few-public-methods
    """Выпадающее меню "File" в строке меню главного окна.

    Предоставляет действия для открытия наборов данных и папок.

    Attributes:
        file_actions (FileActions): Обработчик файловых действий.
        open_dataset_action (QAction): Действие для открытия файла с набором данных.
        open_folder_action (QAction): Действие для открытия папки в проводнике.
        export_dataset_action (QAction): Действие для экспорта набора данных.
    """

    def __init__(self, parent, file_actions: FileActions):
        """Инициализирует меню "File".

        Args:
            parent (QWidget): Родительский виджет.
            file_actions (FileActions): Обработчик файловых действий.
        """
        super().__init__("File", parent)
        self.file_actions = file_actions

        self.open_dataset_action = QAction("Open Dataset", self)
        self.open_dataset_action.setStatusTip("Открыть файл с набором данных")
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.setStatusTip("Открыть папку в проводнике")
        self.export_dataset_action = QAction("Export Dataset", self)
        self.export_dataset_action.setStatusTip("Экспортировать текущий набор данных в файл")
        self.export_dataset_action.setEnabled(False)  # Изначально неактивно

        self.open_folder_action.triggered.connect(self.file_actions.open_folder_in_explorer)
        self.open_dataset_action.triggered.connect(self.file_actions.open_dataset)
        self.export_dataset_action.triggered.connect(self.file_actions.export_dataset)

        self.addAction(self.open_dataset_action)
        self.addAction(self.open_folder_action)
        self.addSeparator()
        self.addAction(self.export_dataset_action)

        # Подписываемся на сигнал загрузки данных, чтобы управлять состоянием действий
        self.file_actions.app_state.dataset_loaded.connect(self._on_dataset_loaded)

    @Slot()
    def _on_dataset_loaded(self):
        """Активирует действия, которые требуют загруженного набора данных."""
        self.export_dataset_action.setEnabled(True)
