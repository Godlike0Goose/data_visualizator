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
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing ModelConfigGroup")

        self.main_window = main_window
        self.stack = QStackedLayout(self)

        self.label = QLabel("No CSV opened", alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.stack.addWidget(self.label)
        self.stack.addWidget(self.group_box)
        self.stack.setCurrentIndex(0)

        self.setLayout(self.stack)

    def show_widgets(self):
        logger.debug("ModelConfigGroup: showing widgets")
        self.model_select_widget.show_widget()
        self.target_select_widget.show_widget()
        self.feature_select_widget.show_widget()
        self.target_select_widget.target_changed.connect(
            self.feature_select_widget.update_features
        )
        self.stack.setCurrentIndex(1)
        logger.debug("ModelConfigGroup: widgets shown, stack index set to 1")


class ModelSelectWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing ModelSelectWidget")

        self.main_window = main_window
    
    def show_widget(self):
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
    target_changed = Signal()
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing TargetSelectWidget")
        self.main_window = main_window

    def show_widget(self):
        logger.debug("TargetSelectWidget: showing widget")
        self.target_select_label = QLabel("Select target var:")
        self.target_select_drop_menu = QComboBox()
        self.target_select_drop_menu.addItem("no target")
        columns = self.main_window.get_all_coloumns_names()
        logger.debug(f"TargetSelectWidget: got columns: {columns}")
        self.target_select_drop_menu.addItems(columns)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.target_select_label)
        h_layout.addWidget(self.target_select_drop_menu)

        self.setLayout(h_layout)

        self.target_select_drop_menu.currentTextChanged.connect(self.change_target_var)
        logger.debug("TargetSelectWidget: widget shown")

    def change_target_var(self, target):
        logger.debug(f"TargetSelectWidget: target variable changed to '{target}'")
        self.main_window.change_target_var(target)
        self.target_changed.emit()
        logger.debug("TargetSelectWidget: target_changed signal emitted")

class FeatureSelectWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing FeatureSelectWidget")

        self.main_window = main_window
    
    def show_widget(self):
        logger.debug("FeatureSelectWidget: showing widget")
        self.feature_select_label = QLabel("Select feature vars:")
        self.feature_checkboxes = FeatureCheckBoxes(self.main_window)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.feature_select_label)
        h_layout.addWidget(self.feature_checkboxes)
        
        self.setLayout(h_layout)
        logger.debug("FeatureSelectWidget: widget shown")

    def update_features(self):
        logger.debug("FeatureSelectWidget: updating features")
        self.feature_checkboxes.update_menu()
        logger.debug("FeatureSelectWidget: features updated")

class NonClosingMenu(QMenu):
    """A QMenu that doesn't close when a checkable action is clicked."""
    action_toggled = Signal()

    def mouseReleaseEvent(self, event):
        action = self.activeAction()
        if action and action.isEnabled() and action.isCheckable():
            action.setChecked(not action.isChecked())
            logger.debug(f"NonClosingMenu: toggled action '{action.text()}' to {action.isChecked()}")
            self.action_toggled.emit()
        else:
            super().mouseReleaseEvent(event)

class FeatureCheckBoxes(QWidget):
    def __init__(self, main_window):
        super().__init__()
        logger.debug("Initializing FeatureCheckBoxes")

        self.main_window = main_window

        self.select_button = QPushButton("Features")
        self.feature_menu = NonClosingMenu("")
        self.select_button.setMenu(self.feature_menu)
        self.select_button.setEnabled(False)
        
        self.select_all_checkbox = QCheckBox("Выбрать все")
        self.select_all_checkbox.setEnabled(False)

        h_layout = QHBoxLayout(self)
        h_layout.addWidget(self.select_button)
        h_layout.addWidget(self.select_all_checkbox)

        self.setLayout(h_layout)

        self.select_all_checkbox.stateChanged.connect(self.toggle_all_features)
        self.feature_menu.action_toggled.connect(self.update_select_all_checkbox_state)
    
    def update_menu(self):
        logger.debug("FeatureCheckBoxes: updating menu")
        checked_features = {
            action.text() for action in self.feature_menu.actions() if action.isChecked()
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
        self.update_select_all_checkbox_state()

    def toggle_all_features(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        logger.debug(f"FeatureCheckBoxes: toggling all features to {is_checked}")
        
        # Блокируем сигналы, чтобы избежать рекурсивного вызова
        self.feature_menu.blockSignals(True)
        for action in self.feature_menu.actions():
            action.setChecked(is_checked)
        self.feature_menu.blockSignals(False)
        # Обновляем состояние, если сняли все галочки
        self.update_select_all_checkbox_state()
        logger.debug("FeatureCheckBoxes: all features toggled")

    def update_select_all_checkbox_state(self):
        logger.debug("FeatureCheckBoxes: updating 'select all' checkbox state")
        actions = self.feature_menu.actions()
        if not actions:
            logger.debug("FeatureCheckBoxes: no actions in menu, skipping update")
            return
        all_checked = all(action.isChecked() for action in actions)
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_checked)
        self.select_all_checkbox.blockSignals(False)
        
