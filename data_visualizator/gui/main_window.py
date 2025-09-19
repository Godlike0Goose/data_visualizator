"""Главный модуль GUI приложения.

Определяет класс MainWindow, который собирает все компоненты интерфейса,
и функцию `start` для запуска приложения.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QMessageBox
from PySide6.QtCore import Slot

from .explorer import Explorer
from .tables import DataSetViewer
from .model_configurator import ModelConfigGroup
from .menu_bar import FileMenu, ViewMenu

from ..logging_setup import setup_logger
from .reorderable_splitter import ReorderableSplitter
from ..state import AppState
from .actions import FileActions

logger = setup_logger()


class MainWindow(QMainWindow):
    """Главное окно приложения для визуализации данных.

    Собирает все основные виджеты: проводник, просмотрщик наборов данных
    и конфигуратор модели. Управляет их взаимодействием.

    Attributes:
        app_state (AppState): Централизованное состояние приложения.
        explorer (Explorer): Виджет проводника файлов.
        dataset_viewer (DataSetViewer): Виджет для отображения таблиц данных.
        model_config (ModelConfigGroup): Виджет для настройки моделей ML.
        splitter (QSplitter): Разделитель для управления размерами виджетов.
    """

    def __init__(self):
        """Инициализирует главное окно."""
        super().__init__()

        self.app_state = AppState()

        self.init_central_widget()
        self.init_menu_bar()
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Приложение готово")

        self.app_state.dataset_loaded.connect(self.on_dataset_loaded)
        self.app_state.status_message_requested.connect(self.on_status_message_requested)
        self.app_state.error_occurred.connect(self.on_error_occurred)

        # Связываем сигналы от виджетов с обработчиком в AppState
        # Теперь MainWindow выступает в роли координатора
        self.dataset_viewer.target_var_selected.connect(self.app_state.set_target_var)
        self.model_config.target_select_widget.target_var_selected.connect(
            self.app_state.set_target_var
        )
        self.model_config.target_select_widget.target_var_selected.connect(
            lambda target: self.on_status_message_requested(f"Целевая переменная изменена на: {target}", 3000)
        )
    def on_dataset_loaded(self, df, path):
        """Обработчик сигнала о загрузке нового набора данных."""
        self.statusBar().showMessage(
            f"Загружен файл: {path} ({df.shape[0]} строк, {df.shape[1]} столбцов)", 5000
        )

    @Slot(str, int)
    def on_status_message_requested(self, message, timeout):
        """Отображает сообщение в статус-баре."""
        self.statusBar().showMessage(message, timeout)

    @Slot(str, str)
    def on_error_occurred(self, title, message):
        """Отображает диалоговое окно с сообщением об ошибке."""
        QMessageBox.critical(self, title, message)

    def init_central_widget(self):
        """Инициализирует и размещает центральный виджет и его компоненты."""
        logger.info("Starting application")

        self.setWindowTitle("Data Visualizator")
        self.explorer = Explorer(self.app_state)
        self.dataset_viewer = DataSetViewer(self.app_state)
        self.model_config = ModelConfigGroup(self.app_state)

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

        # Создаем обработчик действий, который будет использоваться меню
        self.file_actions = FileActions(
            parent=self, app_state=self.app_state, explorer=self.explorer
        )

        self.file_menu = FileMenu(self, self.file_actions)
        self.view_menu = ViewMenu(
            self,
            explorer=self.explorer,
            dataset_viewer=self.dataset_viewer,
            model_config=self.model_config,
        )
        menu_bar.addMenu(self.file_menu)
        menu_bar.addMenu(self.view_menu)

def start():
    """Запускает приложение Qt.

    Создает экземпляр QApplication, инициализирует и отображает
    главное окно, а затем запускает цикл обработки событий.
    """
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
