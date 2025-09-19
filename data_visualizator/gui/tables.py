"""Модуль для отображения данных в виде таблицы.

Содержит классы `PandasModel` и `DataSetViewer`, которые обеспечивают
интеграцию `pandas.DataFrame` с `PySide6` для отображения и взаимодействия с данными.
"""

import logging
from PySide6.QtWidgets import QTableView, QStackedLayout, QLabel, QMenu
from PySide6.QtCore import QAbstractTableModel, Qt, Slot
from PySide6.QtGui import QColor
import pandas as pd

from ._base import BaseWidget
from ..core.utils import read_dataset_from_path
from ..core.data_operations import validate_and_update_cell, get_features


logger = logging.getLogger(__name__)


class PandasModel(QAbstractTableModel):
    """Модель данных Qt для отображения pandas DataFrame в QTableView.

    Предоставляет интерфейс между DataFrame и представлением, позволяя
    отображать, форматировать и взаимодействовать с данными.

    Attributes:
        _df (pd.DataFrame): DataFrame, который отображается в модели.
        _column_colors (dict): Словарь для хранения цветов фона столбцов.
    """

    def __init__(self, df: pd.DataFrame):
        """Инициализирует модель с заданным DataFrame.

        Args:
            df (pd.DataFrame): DataFrame для отображения.
        """
        super().__init__()
        logger.debug("Initializing PandasModel")
        self._df = df
        self._column_colors = {}

    def get_df(self):
        """Возвращает внутренний DataFrame."""
        return self._df

    def rowCount(self, parent=None):  # pylint: disable=invalid-name, unused-argument
        """Возвращает количество строк в DataFrame."""
        return len(self._df.index)

    def columnCount(self, parent=None):  # pylint: disable=invalid-name, unused-argument
        """Возвращает количество столбцов в DataFrame."""
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        """Возвращает данные для указанного индекса и роли.

        Args:
            index (QModelIndex): Индекс ячейки.
            role (int): Роль данных (например, Qt.DisplayRole, Qt.BackgroundRole).

        Returns:
            Любой тип: Данные для ячейки или None, если индекс недействителен.
        """
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if role == Qt.DisplayRole:
            return str(self._df.iat[row, col])

        if role == Qt.BackgroundRole:
            if col in self._column_colors:
                return self._column_colors[col]

        return None

    def setData(self, index, value, role=Qt.EditRole):  # pylint: disable=invalid-name
        """Устанавливает данные для указанного индекса.

        Вызывается при редактировании ячейки в представлении.

        Args:
            index (QModelIndex): Индекс ячейки.
            value: Новое значение.
            role (int): Роль данных (должна быть Qt.EditRole).

        Returns:
            bool: True, если данные были успешно установлены, иначе False.
        """
        if role == Qt.EditRole:
            row, col = index.row(), index.column()
            success = validate_and_update_cell(self._df, row, col, value)

            if success:
                self.dataChanged.emit(index, index, [Qt.DisplayRole])
                logger.debug("Set data at (%d, %d) to %s", row, col, value)
                return True

            return False

        return False

    def flags(self, index):
        """Возвращает флаги для элемента, включая возможность редактирования."""
        return super().flags(index) | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Возвращает данные для заголовков строк или столбцов.

        Args:
            section (int): Индекс секции (строки или столбца).
            orientation (Qt.Orientation): Горизонтальная или вертикальная ориентация.
            role (int): Роль данных (обычно Qt.DisplayRole).

        Returns:
            str: Имя столбца или индекс строки.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            if orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

    def set_column_color(self, column_index, color):
        """Устанавливает цвет фона для столбца по его индексу.

        Args:
            column_index (int): Индекс столбца.
            color (str или QColor): Цвет для установки.
        """
        logger.debug("Setting color for column %s to %s", column_index, color)
        self._column_colors[column_index] = QColor(color)
        top_left = self.index(0, column_index)
        bottom_right = self.index(self.rowCount() - 1, column_index)
        self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])

    def set_column_color_by_name(self, col_name, color):
        """Устанавливает цвет фона для столбца по его имени.

        Args:
            col_name (str): Имя столбца.
            color (str или QColor): Цвет для установки.
        """
        if col_name not in self._df.columns:
            logger.debug(
                "Column '%s' not found in DataFrame. Cannot set color.", col_name
            )
            return
        col = self._df.columns.get_loc(col_name)

        logger.debug(
            "Setting color for column '%s' (index %s) to %s", col_name, col, color
        )
        self._column_colors[col] = QColor(color)

        top_left = self.index(0, col)
        bottom_right = self.index(self.rowCount() - 1, col)
        self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])

    def reset_column_color(self, column_name):
        """Сбрасывает цвет фона для столбца по его имени.

        Args:
            column_name (str): Имя столбца, цвет которого нужно сбросить.
        """
        logger.debug("Resetting color for column '%s'", column_name)
        if column_name not in self._df.columns:
            return

        col = self._df.columns.get_loc(column_name)

        if col in self._column_colors:
            del self._column_colors[col]
            logger.debug("Color for column '%s' (index %s) removed", column_name, col)

            top_left = self.index(0, col)
            bottom_right = self.index(self.rowCount() - 1, col)
            self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])


class DataSetViewer(BaseWidget):
    """Виджет для отображения набора данных в виде таблицы.

    Использует QStackedLayout для переключения между плейсхолдером
    (когда данные не загружены) и QTableView (когда данные загружены).

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        data_model (PandasModel): Модель данных для таблицы.
        target_var (str): Имя текущей целевой переменной.
        stack (QStackedLayout): Layout для переключения представлений.
        table_view (QTableView): Виджет таблицы для отображения данных.
    """

    def __init__(self, main_window):
        """Инициализирует DataSetViewer.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__("Dataset Viewer")
        logger.debug("Initializing DataSetViewer")

        self.target_var = None

        self.main_window = main_window
        self.data_model = None

        self.placeholder_label = QLabel(
            "No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.table_view = QTableView(self)

        # Включаем политику кастомного контекстного меню для заголовка
        header = self.table_view.horizontalHeader()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        # Подключаем сигнал к нашему слоту
        header.customContextMenuRequested.connect(self.on_header_context_menu)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.placeholder_label)
        self.stack.addWidget(self.table_view)
        self.stack.setCurrentIndex(0)
        self.content_widget.setLayout(self.stack)

    def open_dataset(self, path):
        """Загружает и отображает набор данных из файла.

        Args:
            path (str): Путь к файлу с набором данных.
        """
        logger.debug("Opening dataset from path: %s", path)
        df = read_dataset_from_path(path)
        self.data_model = PandasModel(df)
        self.table_view.setModel(self.data_model)
        self.stack.setCurrentIndex(1)
        logger.debug("Dataset opened and view updated")

    def get_all_column_names(self):
        """Возвращает список имен всех столбцов в текущем наборе данных.

        Returns:
            list[str]: Список имен столбцов или `["no columns"]`, если данные не загружены.
        """
        if self.data_model is None:
            logger.debug("No data model, returning default column list")
            return ["no columns"]
        columns = list(self.data_model.get_df().columns)
        logger.debug("Returning column names: %s", columns)
        return columns

    def change_target_var_color(self, target):
        """Изменяет цвет столбца, соответствующего целевой переменной.

        Сбрасывает цвет предыдущей целевой переменной (если она была) и
        окрашивает новый целевой столбец в красный цвет.

        Args:
            target (str): Имя нового целевого столбца. "no target" для сброса.
        """
        logger.debug("Changing target variable color. New target: '%s'", target)
        if self.target_var:
            logger.debug(
                "Resetting color for old target variable: '%s'", self.target_var
            )
            self.data_model.reset_column_color(self.target_var)

        if target != "no target":
            logger.debug("Setting color for new target variable: '%s'", target)
            self.data_model.set_column_color_by_name(target, "red")
            self.target_var = target
        else:
            logger.debug("No target variable selected.")
            self.target_var = None

    def get_features(self):
        """Возвращает список признаков.

        Признаками считаются все столбцы, кроме целевой переменной.

        Returns:
            list[str]: Список имен столбцов-признаков.
              Пустой список, если целевая переменная не выбрана.
        """
        if self.target_var is None:
            logger.debug("No target variable set, returning empty list of features.")
            return []
        df = self.data_model.get_df()
        features = get_features(df, self.target_var)
        logger.debug(
            "Returning features (all columns except target '%s'): %s",
            self.target_var,
            features,
        )
        return features

    @Slot()
    def on_header_context_menu(self, pos):
        """
        Создает и отображает контекстное меню при правом клике на заголовок столбца.
        """
        if self.data_model is None:
            return

        header = self.table_view.horizontalHeader()
        # Получаем логический индекс столбца, по которому кликнули
        column_index = header.logicalIndexAt(pos)
        # Получаем имя столбца из модели
        column_name = self.data_model.headerData(column_index, Qt.Horizontal)

        if column_name:
            menu = QMenu(self)
            set_as_target_action = menu.addAction("Set as Target")

            # Соединяем действие с методом главного окна, передавая имя столбца
            set_as_target_action.triggered.connect(
                lambda: self.main_window.change_target_var(column_name)
            )

            # Отображаем меню в позиции курсора
            menu.exec(header.mapToGlobal(pos))
            logger.debug(f"Context menu shown for column '{column_name}'")
