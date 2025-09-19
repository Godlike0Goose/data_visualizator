"""Модуль для ReorderableSplitter.

Содержит класс, расширяющий QSplitter для поддержки переупорядочивания
дочерних виджетов с помощью drag-and-drop.
"""

import logging
from PySide6.QtWidgets import QSplitter, QWidget, QApplication
from PySide6.QtCore import Qt, QMimeData, QObject, QEvent
from PySide6.QtGui import (
    QDrag,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QMouseEvent,
)

from ._base import BaseWidget

logger = logging.getLogger(__name__)


class ReorderableSplitter(QSplitter):
    """QSplitter с возможностью переупорядочивания виджетов через drag-and-drop.

    Этот класс позволяет пользователю перетаскивать дочерние виджеты для изменения
    их порядка внутри сплиттера.
    """

    def __init__(self, *args, **kwargs):
        """Инициализирует ReorderableSplitter."""
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setChildrenCollapsible(False)
        self._drag_widget = None

    def addWidget(self, widget: QWidget):
        """Добавляет виджет и устанавливает фильтр событий для его заголовка."""
        super().addWidget(widget)
        # Если у виджета есть сигнал drag_started, подключаемся к нему
        if hasattr(widget, "drag_started"):
            widget.drag_started.connect(self._on_drag_started)

    def _on_drag_started(self, widget: QWidget):
        """Начинает операцию drag-and-drop для указанного виджета."""
        self._drag_widget = widget
        logger.debug(f"Drag started on widget: {self._drag_widget}")
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText("reorder-widget")
        drag.setMimeData(mime_data)
        drag.exec(Qt.DropAction.MoveAction)
        self._drag_widget = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Обрабатывает вход курсора с перетаскиваемым объектом."""
        if event.mimeData().hasText() and event.mimeData().text() == "reorder-widget":
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        """Обрабатывает перемещение перетаскиваемого объекта над виджетом."""
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Обрабатывает 'бросание' объекта для изменения порядка виджетов."""
        if not self._drag_widget:
            return

        target_pos = event.position().toPoint()
        target_index = -1

        for i in range(self.count()):
            widget = self.widget(i)
            if widget.geometry().contains(target_pos):
                target_index = self.indexOf(widget)
                break

        if target_index != -1 and self.widget(target_index) is not self._drag_widget:
            self.insertWidget(target_index, self._drag_widget)
            logger.debug(f"Widget moved to index: {target_index}")
            event.acceptProposedAction()
