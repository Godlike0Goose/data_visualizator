import sys
import pandas as pd
import logging
from PySide6.QtWidgets import QTableView, QStackedLayout, QWidget, QLabel
from PySide6.QtCore import QAbstractTableModel, Qt, QAbstractTableModel
from PySide6.QtGui import QColor
from PySide6 import QtCore

from ..crud import read_dataset_from_Path

logger = logging.getLogger(__name__)

class PandasModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        logger.debug("Initializing PandasModel")
        self._df = df
        self._column_colors = {}

    def rowCount(self, parent=None):
        return len(self._df.index)

    def columnCount(self, parent=None):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if role == Qt.DisplayRole:
            return str(self._df.iat[row, col])

        if role == Qt.BackgroundRole:
            if col in self._column_colors:
                return self._column_colors[col]

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            if orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

    def set_column_color(self, col, color):
        logger.debug(f"Setting color for column {col} to {color}")
        self._column_colors[col] = QColor(color)
        top_left = self.index(0, col)
        bottom_right = self.index(self.rowCount() - 1, col)
        self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])
    
    def set_column_color_by_name(self, col_name, color):
        if col_name not in self._df.columns:
            logger.debug(f"Column '{col_name}' not found in DataFrame. Cannot set color.")
            return
        col = self._df.columns.get_loc(col_name)
        
        logger.debug(f"Setting color for column '{col_name}' (index {col}) to {color}")
        self._column_colors[col] = QColor(color)

        top_left = self.index(0, col)
        bottom_right = self.index(self.rowCount() - 1, col)
        self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])

    def reset_column_color(self, column_name):
        logger.debug(f"Resetting color for column '{column_name}'")
        if column_name not in self._df.columns:
            return

        col = self._df.columns.get_loc(column_name)

        if col in self._column_colors:
            del self._column_colors[col]
            logger.debug(f"Color for column '{column_name}' (index {col}) removed")

            top_left = self.index(0, col)
            bottom_right = self.index(self.rowCount()-1, col)
            self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])


class DataSetViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing DataSetViewer")

        self.target_var = None

        self.main_window = main_window
        self.data_model = None

        self.stack = QStackedLayout(self)

        self.label = QLabel("No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter)
        self.table_view = QTableView(self)

        self.stack.addWidget(self.label)
        self.stack.addWidget(self.table_view)
        self.stack.setCurrentIndex(0)

        self.setLayout(self.stack)

        self.table_view.doubleClicked.connect(self.change_color)

    def open_dataset(self, path):
        logger.debug(f"Opening dataset from path: {path}")
        df = read_dataset_from_Path(path)
        self.data_model = PandasModel(df)
        self.table_view.setModel(self.data_model)
        self.stack.setCurrentIndex(1)
        logger.debug("Dataset opened and view updated")

    def get_all_coloumns_names(self):
        if self.data_model is None:
            logger.debug("No data model, returning default column list")
            return ["no columns"]
        columns = list(self.data_model._df.columns)
        logger.debug(f"Returning column names: {columns}")
        return list(self.data_model._df.columns)
    
    def change_target_var_color(self, target):
        logger.debug(f"Changing target variable color. New target: '{target}'")
        if self.target_var:
            logger.debug(f"Resetting color for old target variable: '{self.target_var}'")
            self.data_model.reset_column_color(self.target_var)
        
        if target != "no target":
            logger.debug(f"Setting color for new target variable: '{target}'")
            self.data_model.set_column_color_by_name(target,"red")
            self.target_var = target
        else:
            logger.debug("No target variable selected.")
            self.target_var = None

    def get_features(self):
        if self.target_var is None:
            logger.debug("No target variable set, returning empty list of features.")
            return []
        else:
            features = [feature for feature in self.get_all_coloumns_names() if feature != self.target_var]
            logger.debug(f"Returning features (all columns except target '{self.target_var}'): {features}")
            return features



    @QtCore.Slot()
    def change_color(self, index):
        logger.debug(f"Double-clicked on table. Setting color for column index {index.column()}")
        self.data_model.set_column_color(index.column(), "red")
