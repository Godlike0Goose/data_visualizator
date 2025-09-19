"""Главный модуль GUI приложения.

Определяет класс MainWindow, который собирает все компоненты интерфейса,
и функцию `start` для запуска приложения.
"""

import sys
import re
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget

from .explorer import Explorer
from .tables import DataSetViewer
from .model_configurator import ModelConfigGroup
from .menu_bar import FileMenu, ViewMenu

from ..logging_setup import setup_logger
from ..core.utils import save_dataframe_to_path
from ..core.data_operations import get_features
from .reorderable_splitter import ReorderableSplitter

logger = setup_logger()


class MainWindow(QMainWindow):
    """Главное окно приложения для визуализации данных.

    Собирает все основные виджеты: проводник, просмотрщик наборов данных
    и конфигуратор модели. Управляет их взаимодействием.

    Attributes:
        explorer (Explorer): Виджет проводника файлов.
        dataset_viewer (DataSetViewer): Виджет для отображения таблиц данных.
        model_config (ModelConfigGroup): Виджет для настройки моделей ML.
        splitter (QSplitter): Разделитель для управления размерами виджетов.
    """

    def __init__(self):
        """Инициализирует главное окно."""
        super().__init__()

        self.init_central_widget()
        self.init_menu_bar()

    def init_central_widget(self):
        """Инициализирует и размещает центральный виджет и его компоненты."""
        logger.info("Starting application")

        self.setWindowTitle("Data Visualizator")
        self.explorer = Explorer(self)
        self.dataset_viewer = DataSetViewer(self)
        self.model_config = ModelConfigGroup(self)

        self.splitter = ReorderableSplitter()
        self.splitter.addWidget(self.explorer)
        self.splitter.addWidget(self.dataset_viewer)
        self.splitter.addWidget(self.model_config)
        self.splitter.setSizes([200, 600, 200])

        self.setCentralWidget(self.splitter)

    def init_menu_bar(self):
        """Инициализирует меню приложения."""
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        self.file_menu = FileMenu(self)
        self.view_menu = ViewMenu(self)
        menu_bar.addMenu(self.file_menu)
        menu_bar.addMenu(self.view_menu)

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

        open_file_dialog = QFileDialog(self)
        open_file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        open_file_dialog.setNameFilter(";;".join(supported_formats))
        open_file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if open_file_dialog.exec():
            file_path = open_file_dialog.selectedFiles()[0]
            self.open_dataset_from_path(file_path)

    def open_dataset_from_path(self, path):
        """Открывает набор данных по указанному пути.

        Args:
            path (str): Путь к файлу с набором данных.
        """
        self.dataset_viewer.open_dataset(path)
        self.model_config.show_widgets()
        self.file_menu.export_dataset_action.setEnabled(True)

    def export_dataset(self):
        """Экспортирует текущий DataFrame в CSV файл."""
        if self.dataset_viewer.data_model is None:
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

        save_file_dialog = QFileDialog(self)
        save_file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        save_file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        save_file_dialog.setNameFilter(";;".join(supported_formats))
        save_file_dialog.setDefaultSuffix("csv")

        def on_filter_selected(file_filter):
            """Обновляет суффикс по умолчанию при смене фильтра."""
            # Ищем первое расширение в строке фильтра, например, *.csv
            match = re.search(r"\*\.([a-zA-Z0-9_]+)", file_filter)
            if match:
                suffix = match.group(1)
                save_file_dialog.setDefaultSuffix(suffix)
                logger.debug("Default suffix changed to: %s", suffix)

        # Соединяем сигнал смены фильтра с нашей функцией
        save_file_dialog.filterSelected.connect(on_filter_selected)



        if save_file_dialog.exec():
            file_path = save_file_dialog.selectedFiles()[0]
            df = self.dataset_viewer.data_model.get_df()
            save_dataframe_to_path(df, file_path, index=False)
            logger.info("Dataset exported to %s", file_path)

    def get_all_column_names(self):
        """Возвращает список имен всех столбцов из текущего набора данных.

        Returns:
            list[str]: Список имен столбцов.
        """
        return self.dataset_viewer.get_all_column_names()

    def change_target_var(self, target):
        """Изменяет целевую переменную в приложении.

        Обновляет цвет столбца в таблице и список доступных признаков.

        Args:
            target (str): Имя нового целевого столбца.
        """
        self.dataset_viewer.change_target_var_color(target)
        self.model_config.feature_select_widget.update_feature_list()

    def get_features(self):
        """Возвращает список имен признаков (все столбцы, кроме целевого).

        Returns:
            list[str]: Список имен признаков.
        """
        if self.dataset_viewer.data_model is None:
            return []
        df = self.dataset_viewer.data_model.get_df()
        target = self.dataset_viewer.target_var
        return get_features(df, target)

    def open_folder_in_explorer(self):
        """Открывает диалог выбора папки в виджете проводника."""
        self.explorer.open_folder()

    def toggle_explorer(self, checked):
        """Переключает видимость виджета проводника."""
        logger.debug("Toggling explorer visibility to %s", checked)
        self.explorer.setVisible(checked)

    def toggle_dataset_viewer(self, checked):
        """Переключает видимость виджета для просмотра данных."""
        logger.debug("Toggling dataset viewer visibility to %s", checked)
        self.dataset_viewer.setVisible(checked)

    def toggle_model_config(self, checked):
        """Переключает видимость виджета конфигуратора модели."""
        logger.debug("Toggling model configurator visibility to %s", checked)
        self.model_config.setVisible(checked)


def start():
    """Запускает приложение Qt.

    Создает экземпляр QApplication, инициализирует и отображает
    главное окно, а затем запускает цикл обработки событий.
    """
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
