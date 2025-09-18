import sys
import pandas as pd
from PySide6.QtWidgets import QApplication, QTableView, QStackedLayout, QWidget, QLabel
from PySide6.QtCore import QAbstractTableModel, Qt

from ..crud import read_dataset_from_Path

class PandasModel(QAbstractTableModel):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._df = df

    def rowCount(self, parent=None):
        return len(self._df.index)

    def columnCount(self, parent=None):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            if orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

class DataSetViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.data_model = None

        self.stack = QStackedLayout(self)

        self.label = QLabel("No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter)
        self.table_view = QTableView(self)

        self.stack.addWidget(self.label)
        self.stack.addWidget(self.table_view)
        self.stack.setCurrentIndex(0)

        self.setLayout(self.stack)

    def open_dataset(self, path):
        df = read_dataset_from_Path(path)
        self.data_model = PandasModel(df)
        self.table_view.setModel(self.data_model)
        self.stack.setCurrentIndex(1)