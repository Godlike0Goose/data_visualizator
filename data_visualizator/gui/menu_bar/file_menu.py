"""Модуль для создания меню "File" в строке меню."""
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction  # pylint: disable=no-name-in-module


class FileMenu(QMenu):  # pylint: disable=too-few-public-methods
    """Выпадающее меню "File" в строке меню главного окна.

    Предоставляет действия для открытия наборов данных и папок.

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        open_dataset_action (QAction): Действие для открытия файла с набором данных.
        open_folder_action (QAction): Действие для открытия папки в проводнике.
    """

    def __init__(self, main_window):
        """Инициализирует меню "File".

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
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
