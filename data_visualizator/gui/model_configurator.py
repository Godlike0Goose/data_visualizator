"""Модуль для виджетов конфигурации модели.

Содержит классы для выбора модели, целевой переменной и признаков,
которые используются для настройки пайплайна машинного обучения.
"""

import logging
from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QLabel,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout,
    QPushButton,
    QMenu,
    QCheckBox,
)
from PySide6.QtCore import Qt, Signal, QObject, Slot
from ._base import BaseWidget

logger = logging.getLogger(__name__)


class ModelConfigGroup(BaseWidget):
    """Группа виджетов для настройки параметров модели машинного обучения.

    Этот виджет содержит элементы управления для выбора модели, целевой переменной
    и признаков. Он скрыт до тех пор, пока не будет открыт набор данных.

    Attributes:
        app_state: Ссылка на объект состояния приложения.
        stack (QStackedLayout): Layout для переключения между плейсхолдером и виджетами.
        model_select_widget (ModelSelectWidget): Виджет для выбора ML модели.
        target_select_widget (TargetSelectWidget): Виджет для выбора целевой переменной.
        feature_select_widget (FeatureSelectWidget): Виджет для выбора признаков.
    """

    def __init__(self, app_state):
        """Инициализирует ModelConfigGroup.

        Args:
            app_state: Ссылка на объект состояния приложения.
        """
        super().__init__("Model Configuration")
        logger.debug("Initializing ModelConfigGroup")

        self.app_state = app_state

        # Подписываемся на сигнал загрузки датасета, чтобы виджет сам себя обновил
        self.app_state.dataset_loaded.connect(self.on_dataset_loaded)

        self.placeholder_label = QLabel(
            "No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.group_box = QGroupBox(self)
        self.group_box.setTitle("Configuration")

        self.model_select_widget = ModelSelectWidget(app_state)
        self.target_select_widget = TargetSelectWidget(app_state)
        self.feature_select_widget = FeatureSelectWidget()

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.model_select_widget)
        v_layout.addWidget(self.target_select_widget)
        v_layout.addWidget(self.feature_select_widget)

        # ModelConfigGroup становится координатором для FeatureSelectWidget
        self.feature_select_widget.feature_checkboxes.feature_toggled.connect(
            self.app_state.toggle_feature_selection
        )
        self.feature_select_widget.feature_checkboxes.select_all_toggled.connect(
            self.app_state.toggle_all_features
        )
        self.app_state.features_list_changed.connect(self._update_feature_list)
        self.app_state.selected_features_changed.connect(self._update_selected_features)

        self.group_box.setLayout(v_layout)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.placeholder_label)
        self.stack.addWidget(self.group_box)
        self.stack.setCurrentIndex(0)
        self.content_widget.setLayout(self.stack)

    @Slot()
    def on_dataset_loaded(self, df, path):
        """
        Слот, который вызывается при загрузке нового набора данных.
        Обновляет дочерние виджеты и отображает их.
        """
        logger.debug("ModelConfigGroup: dataset loaded, showing widgets")
        self.stack.setCurrentIndex(1)
        # Явно передаем данные дочерним виджетам
        self.model_select_widget.update_widget()
        columns = self.app_state.get_all_column_names()
        self.target_select_widget.update_widget(columns)        
        self._update_feature_list() # Обновляем список и выбранные признаки
        logger.debug("ModelConfigGroup: widgets shown, stack index set to 1")

    def show_widgets(self):
        """Отображает виджеты конфигурации и скрывает плейсхолдер.

        Вызывается после загрузки набора данных. Обновляет дочерние виджеты
        и переключает QStackedLayout для их отображения.
        """
        logger.debug("ModelConfigGroup: showing widgets")
        self.on_dataset_loaded(self.app_state.df, self.app_state.path)

    def _update_feature_list(self):
        """Обновляет список доступных признаков в дочернем виджете."""
        features = self.app_state.get_features()
        selected_features = self.app_state.selected_features
        self.feature_select_widget.update_features(features, selected_features)

    def _update_selected_features(self, selected_features: set):
        """Обновляет только состояние выбора признаков в дочернем виджете."""
        self.feature_select_widget.update_selected(selected_features)

class ModelSelectWidget(QWidget):
    """Виджет для выбора модели машинного обучения."""

    def __init__(self, app_state):
        """Инициализирует ModelSelectWidget.

        Args:
            app_state: Ссылка на объект состояния приложения.
        """
        super().__init__()
        logger.debug("Initializing ModelSelectWidget")

        self.app_state = app_state
        self.model_select_label = QLabel("Select a ML model:")
        self.model_select_drop_menu = QComboBox()
        self.model_select_drop_menu.setToolTip(
            "Выберите модель машинного обучения для конфигурации"
        )

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.model_select_label)
        h_layout.addWidget(self.model_select_drop_menu)

        self.setLayout(h_layout)

    def update_widget(self):
        """Создает и отображает элементы управления для выбора модели.

        Этот метод вызывается, когда нужно показать виджет (после загрузки данных),
        а не в `__init__`, чтобы избежать создания виджетов, которые могут
        никогда не понадобиться.
        """
        logger.debug("ModelSelectWidget: showing widget")
        self.model_select_drop_menu.clear()
        self.model_select_drop_menu.addItems(["None", "Elastic-Net"])
        logger.debug("ModelSelectWidget: widget shown")


class TargetSelectWidget(QWidget):
    """Виджет для выбора целевой переменной из столбцов набора данных."""

    target_var_selected = Signal(str)

    def __init__(self, app_state):
        """Инициализирует TargetSelectWidget.

        Args:
            app_state: Ссылка на объект состояния приложения.
        """
        super().__init__()
        logger.debug("Initializing TargetSelectWidget")
        self.app_state = app_state
        self.target_select_label = QLabel("Select target var:")
        self.target_select_combobox = QComboBox()
        self.target_select_combobox.currentTextChanged.connect(
            self._on_target_var_changed
        )

        # Подписываемся на сигнал изменения целевой переменной из AppState
        self.app_state.target_var_changed.connect(self._update_combobox_selection)
        # Подписываемся на сигнал загрузки датасета, чтобы виджет сам себя обновил

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.target_select_label)
        h_layout.addWidget(self.target_select_combobox)

        self.setLayout(h_layout)

    def update_widget(self, columns: list):
        """Создает и отображает элементы управления для выбора целевой переменной.

        Заполняет выпадающий список именами столбцов из загруженного
        набора данных.

        Args:
            columns (list): Список имен столбцов для отображения.
        """
        logger.debug("TargetSelectWidget: showing widget")
        # Блокируем сигналы, чтобы избежать рекурсивных вызовов при обновлении
        self.target_select_combobox.blockSignals(True)
        self.target_select_combobox.clear()
        self.target_select_combobox.addItem("no target")
        logger.debug("TargetSelectWidget: got columns: %s", columns)
        self.target_select_combobox.addItems(columns)
        self.target_select_combobox.blockSignals(False)
        logger.debug("TargetSelectWidget: widget shown")

    def _on_target_var_changed(self, target):
        """Обрабатывает изменение выбора целевой переменной.

        Args:
            target (str): Новое имя целевой переменной.
        """
        if target is not None:  # Избегаем вызова при очистке комбобокса
            logger.debug("TargetSelectWidget: target variable changed to '%s'", target)
            message = (
                f"Целевая переменная изменена на: {target}"
                if target != "no target"
                else "Целевая переменная сброшена"
            )
            self.target_var_selected.emit(target)

    @Slot(str)
    def _update_combobox_selection(self, target):
        """Обновляет выбор в комбобоксе, когда целевая переменная меняется извне."""
        logger.debug("TargetSelectWidget: updating combobox to '%s'", target)
        # Блокировка больше не нужна, т.к. мы не создаем петлю обратной связи
        self.target_select_combobox.setCurrentText(target)


class FeatureSelectWidget(QWidget):
    """Виджет для выбора признаков для модели."""

    def __init__(self):
        """Инициализирует FeatureSelectWidget.
        """
        super().__init__()
        logger.debug("Initializing FeatureSelectWidget")

        self.feature_select_label = QLabel("Select feature vars:")
        self.feature_checkboxes = FeatureCheckBoxes()

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.feature_select_label)
        h_layout.addWidget(self.feature_checkboxes)

        self.setLayout(h_layout)
    
    def update_features(self, features: list, selected_features: set):
        """Обновляет список доступных признаков и их состояние выбора."""
        logger.debug("FeatureSelectWidget: updating features")
        self.feature_checkboxes.update_menu(features, selected_features)
        logger.debug("FeatureSelectWidget: features updated")

    def update_selected(self, selected_features: set):
        """Обновляет только состояние выбора признаков."""
        logger.debug("FeatureSelectWidget: updating selected features")
        self.feature_checkboxes.update_selection_state(selected_features)
        logger.debug("FeatureSelectWidget: selected features updated")


class NonClosingMenu(QMenu):  # pylint: disable=too-few-public-methods
    """A QMenu that doesn't close when a checkable action is clicked."""

    feature_toggled = Signal(str, bool)

    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name
        """Переопределяет событие отпускания кнопки мыши.

        Предотвращает закрытие меню при клике на флажок, позволяя
        выбрать несколько элементов и отправляя сигнал об изменении.

        Args:
            event (QMouseEvent): Событие мыши.
        """
        action = self.activeAction()
        if action and action.isEnabled() and action.isCheckable():
            is_checked = not action.isChecked()
            self.feature_toggled.emit(action.text(), is_checked)
        else:
            super().mouseReleaseEvent(event)


class FeatureCheckBoxes(QWidget):  # pylint: disable=too-few-public-methods
    """Виджет с кнопкой, открывающей выпадающее меню с флажками для выбора признаков.

    Также содержит флажок "Select All" для быстрого выбора/снятия выбора
    всех признаков.

    Attributes:
        select_button (QPushButton): Кнопка, отображающая меню выбора признаков.
        feature_menu (NonClosingMenu): Выпадающее меню с флажками.
        select_all_checkbox (QCheckBox): Флажок для выбора всех признаков.
    """
    feature_toggled = Signal(str, bool)
    select_all_toggled = Signal(bool)

    def __init__(self):
        """Инициализирует FeatureCheckBoxes."""
        super().__init__()
        logger.debug("Initializing FeatureCheckBoxes")
 
        # Сначала создаем меню
        self.feature_menu = NonClosingMenu("")
        # Затем соединяем его сигнал с сигналом этого виджета, чтобы "пробросить" его наверх
        self.feature_menu.feature_toggled.connect(self.feature_toggled)
 
        self.select_button = QPushButton("Features")
        self.select_button.setMenu(self.feature_menu)
        self.select_button.setEnabled(False)

        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.setEnabled(False)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.select_button)
        h_layout.addWidget(self.select_all_checkbox)

        self.setLayout(h_layout)

        self.select_all_checkbox.stateChanged.connect(self._on_select_all_toggled)

    def update_menu(self, features: list, selected_features: set):
        """Обновляет содержимое выпадающего меню с признаками.

        Очищает старые элементы и добавляет новые на основе доступных признаков
        
        Args:
            features (list): Список всех доступных признаков.
            selected_features (set): Набор выбранных признаков.
        """
        logger.debug("FeatureCheckBoxes: updating menu")
        self.feature_menu.clear()

        if not features:
            self.select_button.setEnabled(False)
            self.select_all_checkbox.setEnabled(False)
            self.select_all_checkbox.setChecked(False)
            logger.debug("FeatureCheckBoxes: no features to show, disabling controls")
            return

        self.select_button.setEnabled(True)
        for feature in features:
            action = self.feature_menu.addAction(feature)
            action.setCheckable(True)
        logger.debug(f"FeatureCheckBoxes: menu updated with features: {features}")

        self.select_all_checkbox.setEnabled(True)
        self.update_selection_state(selected_features)

    def _on_select_all_toggled(self, state: int):
        """Обрабатывает изменение состояния флажка "Select All".

        Издает сигнал `select_all_toggled`.

        Args:
            state (int): Новое состояние флажка (Qt.CheckState).
        """
        select_all = state == Qt.CheckState.Checked.value
        self.select_all_toggled.emit(select_all)

    def update_selection_state(self, selected_features: set):
        """Обновляет состояние флажков на основе переданных данных."""
        logger.debug("FeatureCheckBoxes: updating selection state")
        # Обновляем флажки в меню
        for action in self.feature_menu.actions():
            action.setChecked(action.text() in selected_features)

        # Обновляем флажок "Select All"
        actions = self.feature_menu.actions()
        all_checked = bool(actions) and (len(selected_features) == len(actions))

        # Блокируем сигналы, чтобы не вызвать _on_select_all_toggled
        # при программном изменении состояния чекбокса
        if self.select_all_checkbox.isChecked() != all_checked:
            self.select_all_checkbox.blockSignals(True)
            self.select_all_checkbox.setChecked(all_checked)
            self.select_all_checkbox.blockSignals(False)
        logger.debug("FeatureCheckBoxes: selection state updated")
