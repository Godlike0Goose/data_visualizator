"""Модуль с базовым классом для основных виджетов приложения."""

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
logger = logging.getLogger(__name__)


class BaseWidget(QWidget):
    """Базовый виджет с заголовком для основных компонентов интерфейса.

    Предоставляет заголовок, за который можно перетаскивать виджет,
    и контейнер для размещения основного содержимого.

    Attributes:
        title_bar (QLabel): Виджет заголовка.
        content_widget (QWidget): Контейнер для содержимого дочернего виджета.
    """

    drag_started = Signal(QWidget)

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

        # Включаем отслеживание мыши, чтобы получать события MouseMove
        self.title_bar.setMouseTracking(True)
        self._drag_start_position = None

        self.content_widget = QWidget()
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.content_widget)

    def mousePressEvent(self, event: QMouseEvent):
        """Захватывает начальную позицию клика на заголовке."""
        if event.button() == Qt.MouseButton.LeftButton and self.title_bar.underMouse():
            self._drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """При движении мыши с зажатой кнопкой инициирует сигнал о перетаскивании."""
        if (event.buttons() & Qt.MouseButton.LeftButton) and self._drag_start_position:
            # Проверяем, что мышь сдвинулась на достаточное расстояние
            if (event.pos() - self._drag_start_position).manhattanLength() > 5:
                self.drag_started.emit(self)
                self._drag_start_position = None  # Сбрасываем, чтобы не инициировать снова
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Сбрасывает начальную позицию при отпускании кнопки мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_position = None
        super().mouseReleaseEvent(event)
