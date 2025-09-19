"""Модуль для создания меню "View" в строке меню."""
from PySide6.QtGui import QAction  # pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMenu


class ViewMenu(QMenu):  # pylint: disable=too-few-public-methods
    """Выпадающее меню "Вид" в строке меню главного окна.

    Предоставляет действия для переключения видимости основных виджетов.

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        toggle_explorer_action (QAction): Действие для переключения проводника.
        toggle_viewer_action (QAction): Действие для переключения просмотрщика данных.
        toggle_config_action (QAction): Действие для переключения конфигуратора модели.
    """

    def __init__(self, main_window):
        """Инициализирует меню "Вид".

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__("Вид", main_window)
        self.main_window = main_window

        self.toggle_explorer_action = QAction("Проводник", self, checkable=True)
        self.toggle_explorer_action.setChecked(True)
        self.toggle_explorer_action.triggered.connect(self.main_window.toggle_explorer)

        self.toggle_viewer_action = QAction("Просмотр данных", self, checkable=True)
        self.toggle_viewer_action.setChecked(True)
        self.toggle_viewer_action.triggered.connect(
            self.main_window.toggle_dataset_viewer
        )

        self.toggle_config_action = QAction("Конфигуратор модели", self, checkable=True)
        self.toggle_config_action.setChecked(True)
        self.toggle_config_action.triggered.connect(
            self.main_window.toggle_model_config
        )

        self.addAction(self.toggle_explorer_action)
        self.addAction(self.toggle_viewer_action)
        self.addAction(self.toggle_config_action)
