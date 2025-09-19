"""Модуль для создания меню "View" в строке меню."""

from PySide6.QtGui import QAction  # pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMenu, QWidget


class ViewMenu(QMenu):  # pylint: disable=too-few-public-methods
    """Выпадающее меню "Вид" в строке меню главного окна.

    Предоставляет действия для переключения видимости основных виджетов.

    Attributes:
        toggle_explorer_action (QAction): Действие для переключения проводника.
        toggle_viewer_action (QAction): Действие для переключения просмотрщика данных.
        toggle_config_action (QAction): Действие для переключения конфигуратора модели.
    """

    def __init__(
        self,
        parent: QWidget,
        explorer: QWidget,
        dataset_viewer: QWidget,
        model_config: QWidget,
    ):
        """Инициализирует меню "Вид".

        Args:
            parent (QWidget): Родительский виджет (главное окно).
            explorer (QWidget): Виджет проводника для управления видимостью.
            dataset_viewer (QWidget): Виджет просмотра данных для управления видимостью.
            model_config (QWidget): Виджет конфигурации модели для управления видимостью.
        """
        super().__init__("View", parent)

        self.toggle_explorer_action = QAction("Проводник", self, checkable=True)
        self.toggle_explorer_action.setChecked(True)
        self.toggle_explorer_action.setStatusTip("Показать/скрыть панель проводника")
        self.toggle_explorer_action.triggered[bool].connect(explorer.setVisible)

        self.toggle_viewer_action = QAction("Просмотр данных", self, checkable=True)
        self.toggle_viewer_action.setChecked(True)
        self.toggle_viewer_action.setStatusTip(
            "Показать/скрыть панель просмотра набора данных"
        )
        self.toggle_viewer_action.triggered[bool].connect(dataset_viewer.setVisible)

        self.toggle_config_action = QAction("Конфигуратор модели", self, checkable=True)
        self.toggle_config_action.setChecked(True)
        self.toggle_config_action.setStatusTip(
            "Показать/скрыть панель конфигурации модели"
        )
        self.toggle_config_action.triggered[bool].connect(model_config.setVisible)

        self.addAction(self.toggle_explorer_action)
        self.addAction(self.toggle_viewer_action)
        self.addAction(self.toggle_config_action)
