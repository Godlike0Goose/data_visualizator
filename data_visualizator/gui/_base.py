"""Модуль с базовым классом для основных виджетов приложения."""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)


class BaseWidget(QWidget):
    """Базовый виджет с заголовком для основных компонентов интерфейса.

    Предоставляет заголовок, за который можно перетаскивать виджет,
    и контейнер для размещения основного содержимого.

    Attributes:
        title_bar (QLabel): Виджет заголовка.
        content_widget (QWidget): Контейнер для содержимого дочернего виджета.
    """

    def __init__(self, title, parent=None):
        """Инициализирует BaseWidget.

        Args:
            title (str): Текст для заголовка виджета.
            parent (QWidget, optional): Родительский виджет. Defaults to None.
        """
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = QLabel(title)
        self.title_bar.setStyleSheet(
            "background-color: #e0e0e0; padding: 4px; font-weight: bold;"
        )
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content_widget = QWidget()
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.content_widget)
