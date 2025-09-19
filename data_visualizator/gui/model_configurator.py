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
from PySide6.QtCore import Qt, Signal

logger = logging.getLogger(__name__)


class ModelConfigGroup(QWidget):
    """Группа виджетов для настройки параметров модели машинного обучения.

    Этот виджет содержит элементы управления для выбора модели, целевой переменной
    и признаков. Он скрыт до тех пор, пока не будет открыт набор данных.

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        stack (QStackedLayout): Layout для переключения между плейсхолдером и виджетами.
        model_select_widget (ModelSelectWidget): Виджет для выбора ML модели.
        target_select_widget (TargetSelectWidget): Виджет для выбора целевой переменной.
        feature_select_widget (FeatureSelectWidget): Виджет для выбора признаков.
    """
    def __init__(self, main_window):
        """Инициализирует ModelConfigGroup.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing ModelConfigGroup")

        self.main_window = main_window
        self.stack = QStackedLayout(self)

        self.placeholder_label = QLabel(
            "No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.group_box = QGroupBox(self)
        self.group_box.setTitle("Configuration")

        self.model_select_widget = ModelSelectWidget(main_window)
        self.target_select_widget = TargetSelectWidget(main_window)
        self.feature_select_widget = FeatureSelectWidget(main_window)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.model_select_widget)
        v_layout.addWidget(self.target_select_widget)
        v_layout.addWidget(self.feature_select_widget)

        self.group_box.setLayout(v_layout)

        self.stack.addWidget(self.placeholder_label)
        self.stack.addWidget(self.group_box)
        self.stack.setCurrentIndex(0)

        self.setLayout(self.stack)

    def show_widgets(self):
        """Отображает виджеты конфигурации и скрывает плейсхолдер.

        Вызывается после загрузки набора данных. Обновляет дочерние виджеты
        и переключает QStackedLayout для их отображения.
        """
        logger.debug("ModelConfigGroup: showing widgets")
        self.model_select_widget.show_widget()
        self.target_select_widget.show_widget()
        self.feature_select_widget.show_widget()
        self.stack.setCurrentIndex(1)
        logger.debug("ModelConfigGroup: widgets shown, stack index set to 1")


class ModelSelectWidget(QWidget):
    """Виджет для выбора модели машинного обучения."""
    def __init__(self, main_window):
        """Инициализирует ModelSelectWidget.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing ModelSelectWidget")

        self.main_window = main_window

    def show_widget(self):
        """Создает и отображает элементы управления для выбора модели.

        Этот метод вызывается, когда нужно показать виджет (после загрузки данных),
        а не в `__init__`, чтобы избежать создания виджетов, которые могут
        никогда не понадобиться.
        """
        logger.debug("ModelSelectWidget: showing widget")
        self.model_select_label = QLabel("Select a ML model:")
        self.model_select_drop_menu = QComboBox()
        self.model_select_drop_menu.addItems(["None", "Elastic-Net"])

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.model_select_label)
        h_layout.addWidget(self.model_select_drop_menu)

        self.setLayout(h_layout)
        logger.debug("ModelSelectWidget: widget shown")


class TargetSelectWidget(QWidget):
    """Виджет для выбора целевой переменной из столбцов набора данных."""
    target_changed = Signal()

    def __init__(self, main_window):
        """Инициализирует TargetSelectWidget.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing TargetSelectWidget")
        self.main_window = main_window

    def show_widget(self):
        """Создает и отображает элементы управления для выбора целевой переменной.

        Заполняет выпадающий список именами столбцов из загруженного
        набора данных.
        """
        logger.debug("TargetSelectWidget: showing widget")
        self.target_select_label = QLabel("Select target var:")
        self.target_select_combobox = QComboBox()
        self.target_select_combobox.addItem("no target")
        columns = self.main_window.get_all_column_names()
        logger.debug(f"TargetSelectWidget: got columns: {columns}")
        self.target_select_combobox.addItems(columns)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.target_select_label)
        h_layout.addWidget(self.target_select_combobox)

        self.setLayout(h_layout)

        self.target_select_combobox.currentTextChanged.connect(
            self._on_target_var_changed
        )
        logger.debug("TargetSelectWidget: widget shown")

    def _on_target_var_changed(self, target):
        """Обрабатывает изменение выбора целевой переменной.

        Args:
            target (str): Новое имя целевой переменной.
        """
        logger.debug(f"TargetSelectWidget: target variable changed to '{target}'")
        self.main_window.change_target_var(target)


class FeatureSelectWidget(QWidget):
    """Виджет для выбора признаков для модели."""
    def __init__(self, main_window):
        """Инициализирует FeatureSelectWidget.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing FeatureSelectWidget")

        self.main_window = main_window

    def show_widget(self):
        """Создает и отображает элементы управления для выбора признаков."""
        logger.debug("FeatureSelectWidget: showing widget")
        self.feature_select_label = QLabel("Select feature vars:")
        self.feature_checkboxes = FeatureCheckBoxes(self.main_window)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.feature_select_label)
        h_layout.addWidget(self.feature_checkboxes)

        self.setLayout(h_layout)
        logger.debug("FeatureSelectWidget: widget shown")

    def update_feature_list(self):
        """Обновляет список доступных признаков в дочернем виджете."""
        logger.debug("FeatureSelectWidget: updating features")
        self.feature_checkboxes.update_menu()
        logger.debug("FeatureSelectWidget: features updated")


class NonClosingMenu(QMenu):
    """A QMenu that doesn't close when a checkable action is clicked."""

    action_toggled = Signal()

    def mouseReleaseEvent(self, event):
        """Переопределяет событие отпускания кнопки мыши.

        Предотвращает закрытие меню при клике на флажок, позволяя
        выбрать несколько элементов.

        Args:
            event (QMouseEvent): Событие мыши.
        """
        action = self.activeAction()
        if action and action.isEnabled() and action.isCheckable():
            action.setChecked(not action.isChecked())
            logger.debug(
                f"NonClosingMenu: toggled action '{action.text()}' to {action.isChecked()}"
            )
            self.action_toggled.emit()
        else:
            super().mouseReleaseEvent(event)


class FeatureCheckBoxes(QWidget):
    """Виджет с кнопкой, открывающей выпадающее меню с флажками для выбора признаков.

    Также содержит флажок "Select All" для быстрого выбора/снятия выбора
    всех признаков.

    Attributes:
        main_window: Ссылка на главный объект окна приложения.
        select_button (QPushButton): Кнопка, отображающая меню выбора признаков.
        feature_menu (NonClosingMenu): Выпадающее меню с флажками.
        select_all_checkbox (QCheckBox): Флажок для выбора всех признаков.
    """
    def __init__(self, main_window):
        """Инициализирует FeatureCheckBoxes.

        Args:
            main_window: Ссылка на главный объект окна приложения.
        """
        super().__init__()
        logger.debug("Initializing FeatureCheckBoxes")

        self.main_window = main_window

        self.select_button = QPushButton("Features")
        self.feature_menu = NonClosingMenu("")
        self.select_button.setMenu(self.feature_menu)
        self.select_button.setEnabled(False)

        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.setEnabled(False)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.select_button)
        h_layout.addWidget(self.select_all_checkbox)

        self.setLayout(h_layout)

        self.select_all_checkbox.stateChanged.connect(self._toggle_all_features)
        self.feature_menu.action_toggled.connect(self._update_select_all_checkbox_state)

    def update_menu(self):
        """Обновляет содержимое выпадающего меню с признаками.

        Очищает старые элементы и добавляет новые на основе доступных признаков
        из `main_window`. Сохраняет состояние флажков для уже выбранных
        признаков.
        """
        logger.debug("FeatureCheckBoxes: updating menu")
        checked_features = {
            action.text()
            for action in self.feature_menu.actions()
            if action.isChecked()
        }

        self.feature_menu.clear()
        features = self.main_window.get_features()

        if not features:
            self.select_button.setEnabled(False)
            self.select_all_checkbox.setEnabled(False)
            logger.debug("FeatureCheckBoxes: no features to show, disabling controls")
            return

        self.select_button.setEnabled(True)
        for feature in features:
            action = self.feature_menu.addAction(feature)
            action.setCheckable(True)
            if feature in checked_features:
                action.setChecked(True)
        logger.debug(f"FeatureCheckBoxes: menu updated with features: {features}")

        self.select_all_checkbox.setEnabled(True)
        self._update_select_all_checkbox_state()

    def _toggle_all_features(self, state):
        """Обрабатывает изменение состояния флажка "Select All".

        Устанавливает или снимает флажки для всех признаков в меню.

        Args:
            state (int): Новое состояние флажка (Qt.CheckState).
        """
        is_checked = state == Qt.CheckState.Checked.value
        logger.debug(f"FeatureCheckBoxes: toggling all features to {is_checked}")

        # Block signals to avoid recursive calls
        self.feature_menu.blockSignals(True)
        for action in self.feature_menu.actions():
            action.setChecked(is_checked)
        self.feature_menu.blockSignals(False)
        # Update state if all checkboxes were unchecked
        self._update_select_all_checkbox_state()
        logger.debug("FeatureCheckBoxes: all features toggled")

    def _update_select_all_checkbox_state(self):
        """Обновляет состояние флажка "Select All" в зависимости от состояния флажков в меню.

        Если все флажки в меню установлены, устанавливает "Select All".
        В противном случае снимает его.
        """
        logger.debug("FeatureCheckBoxes: updating 'select all' checkbox state")
        actions = self.feature_menu.actions()
        if not actions:
            logger.debug("FeatureCheckBoxes: no actions in menu, skipping update")
            return
        all_checked = all(action.isChecked() for action in actions)
        # Block signals to prevent infinite loop
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_checked)
        self.select_all_checkbox.blockSignals(False)
