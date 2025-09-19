"""Модуль для управления состоянием приложения.

Содержит класс AppState, который является централизованным хранилищем
для общих данных приложения, таких как загруженный DataFrame, целевая переменная
и т.д. Использует сигналы Qt для уведомления об изменениях состояния.
"""

import logging
from PySide6.QtCore import QObject, Signal
import pandas as pd

from .core.data_operations import get_features
from .core.utils import read_dataset_from_path

logger = logging.getLogger(__name__)


class AppState(QObject):
    """Управляет общим состоянием приложения."""

    dataset_loaded = Signal(pd.DataFrame, str)  # Сигнал: (df, path)
    target_var_changed = Signal(str)  # Сигнал: (new_target_var)
    state_changed = Signal()
    status_message_requested = Signal(str, int)  # Сигнал: (message, timeout)
    error_occurred = Signal(str, str)  # Сигнал: (title, message)
    open_folder_dialog_requested = Signal()  # Сигнал для открытия диалога выбора папки
    selected_features_changed = Signal(set)  # Сигнал: (selected_features_set)
    features_list_changed = Signal()  # Сигнал об изменении списка доступных признаков

    def __init__(self):
        """Инициализирует состояние приложения."""
        super().__init__()
        self._df = None
        self._dataset_path = None
        self._target_var = "no target"
        self._selected_features = set()
        self._select_all_features_mode = False  # Флаг для режима "Выбрать все"
        logger.debug("AppState initialized")

    @property
    def df(self):
        """Возвращает текущий DataFrame."""
        return self._df

    @property
    def target_var(self):
        """Возвращает текущую целевую переменную."""
        return self._target_var

    @property
    def selected_features(self):
        """Возвращает множество текущих выбранных признаков."""
        return self._selected_features

    def load_dataset_from_path(self, path):
        """Загружает набор данных из файла и обновляет состояние."""
        logger.debug("AppState: loading dataset from %s", path)
        try:
            self._df = read_dataset_from_path(path)
            self._dataset_path = path
            # Сбрасываем выбранные признаки при загрузке нового датасета
            self._select_all_features_mode = False
            self.set_selected_features(set())
            logger.info("Dataset loaded: %s. Shape: %s", path, self._df.shape)
            self.dataset_loaded.emit(self._df, path)
            self.set_target_var("no target")  # Сбрасываем целевую переменную
        except Exception as e:
            logger.error("Failed to load dataset from %s: %s", path, e)
            self.error_occurred.emit(
                "Ошибка загрузки файла",
                f"Не удалось загрузить данные из файла:\n{path}\n\nПричина: {e}",
            )

    def set_target_var(self, target_var):
        """Устанавливает новую целевую переменную."""
        # Устанавливаем 'no target', если передано None или пустая строка
        new_target = target_var if target_var else "no target"
        old_target = self._target_var
        if old_target != new_target:
            self._target_var = new_target
            logger.debug("AppState: target variable changed to '%s'", new_target)
            self.target_var_changed.emit(new_target)

            # Если был включен режим "Выбрать все", перевыбираем все новые признаки
            if self._select_all_features_mode:
                # Просто заново выбираем все доступные признаки
                self.toggle_all_features(True)
            # Отправляем сигнал, что список фич изменился
            self.features_list_changed.emit()

    def get_all_column_names(self):
        """Возвращает список всех имен столбцов."""
        if self._df is None:
            return []
        return list(self._df.columns)

    def get_features(self):
        """Возвращает список признаков (все столбцы, кроме целевого)."""
        if self._df is None:
            return []
        return get_features(self._df, self._target_var)

    def set_selected_features(self, features: set):
        """Устанавливает новый набор выбранных признаков."""
        if self._selected_features != features:
            self._selected_features = features
            # Отключаем режим "Выбрать все", только если он был включен,
            # а количество выбранных фич перестало совпадать с общим количеством.
            # Это предотвращает ложное отключение во время смены таргета.
            if self._select_all_features_mode and len(self.get_features()) != len(features):
                self._select_all_features_mode = False
            self.selected_features_changed.emit(self._selected_features)
            logger.debug("Selected features set to: %s", features)

    def toggle_feature_selection(self, feature: str, select: bool):
        """Добавляет или удаляет признак из набора выбранных."""
        new_features = self._selected_features.copy()
        if select:
            new_features.add(feature)
        else:
            new_features.discard(feature)
        self.set_selected_features(new_features)

    def toggle_all_features(self, select: bool):
        """Выбирает или снимает выбор со всех доступных признаков."""
        self._select_all_features_mode = select
        if select:
            self.set_selected_features(set(self.get_features()))
        else:
            self.set_selected_features(set())