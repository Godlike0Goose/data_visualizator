"""Модуль для инкапсуляции глобальных действий приложения."""

import logging
import re
from PySide6.QtWidgets import QFileDialog, QWidget

from ..state import AppState
from .explorer import Explorer
from ..core.utils import save_dataframe_to_path

logger = logging.getLogger(__name__)


class FileActions:
    """
    Инкапсулирует логику файловых операций, инициируемых из меню или панелей инструментов.
    """

    def __init__(self, parent: QWidget, app_state: AppState, explorer: Explorer):
        """
        Инициализирует обработчик файловых действий.

        Args:
            parent (QWidget): Родительский виджет для диалоговых окон.
            app_state (AppState): Состояние приложения.
            explorer (Explorer): Виджет проводника.
        """
        self.parent = parent
        self.app_state = app_state
        self.explorer = explorer

    def open_dataset(self):
        """Открывает диалоговое окно для выбора и загрузки файла с набором данных."""
        supported_formats = [
            "All supported files (*.csv *.xlsx *.xls *.json *.parquet *.feather *.h5 *.hdf5 *.pkl)",
            "CSV files (*.csv)",
            "Excel files (*.xlsx *.xls)",
            "JSON files (*.json)",
            "Parquet files (*.parquet)",
            "Feather files (*.feather)",
            "HDF5 files (*.h5 *.hdf5)",
            "Pickle files (*.pkl)",
            "All files (*)",
        ]

        open_file_dialog = QFileDialog(self.parent)
        open_file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        open_file_dialog.setNameFilter(";;".join(supported_formats))
        open_file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if open_file_dialog.exec():
            file_path = open_file_dialog.selectedFiles()[0]
            self.app_state.load_dataset_from_path(file_path)

    def export_dataset(self):
        """Экспортирует текущий DataFrame в файл."""
        if self.app_state.df is None:
            logger.warning("No dataset to export.")
            return

        supported_formats = [
            "CSV files (*.csv)",
            "Excel files (*.xlsx *.xls)",
            "JSON files (*.json)",
            "Parquet files (*.parquet)",
            "Feather files (*.feather)",
            "HDF5 files (*.h5 *.hdf5)",
            "Pickle files (*.pkl)",
        ]

        save_file_dialog = QFileDialog(self.parent)
        save_file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        save_file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        save_file_dialog.setNameFilter(";;".join(supported_formats))
        save_file_dialog.setDefaultSuffix("csv")

        def on_filter_selected(file_filter):
            match = re.search(r"\*\.([a-zA-Z0-9_]+)", file_filter)
            if match:
                suffix = match.group(1)
                save_file_dialog.setDefaultSuffix(suffix)

        save_file_dialog.filterSelected.connect(on_filter_selected)

        if save_file_dialog.exec():
            file_path = save_file_dialog.selectedFiles()[0]
            df = self.app_state.df
            save_dataframe_to_path(df, file_path, index=False)
            self.app_state.status_message_requested.emit(f"Данные экспортированы в {file_path}", 5000)

    def open_folder_in_explorer(self):
        """Открывает диалог выбора папки в виджете проводника."""
        self.explorer.open_folder()