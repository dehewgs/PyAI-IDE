"""
Enhanced Settings Dialog with theme and shortcuts configuration
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QComboBox, QSpinBox, QCheckBox, QPushButton,
    QMessageBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt
from utils.logger import logger
from ui.dialogs.shortcuts_dialog import ShortcutsDialog


class EnhancedSettingsDialog(QDialog):
    """Enhanced settings dialog with multiple tabs"""
    
    def __init__(self, parent=None, app_data_manager=None, shortcuts_manager=None, theme_manager=None):
        super().__init__(parent)
        self.app_data_manager = app_data_manager
        self.shortcuts_manager = shortcuts_manager
        self.theme_manager = theme_manager
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 600, 500)
        self._create_ui()
    
    def _create_ui(self):
        """Create UI"""
        layout = QVBoxLayout(self)
        
        # Tab widget
        tabs = QTabWidget()
        
        # General tab
        general_tab = self._create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Editor tab
        editor_tab = self._create_editor_tab()
        tabs.addTab(editor_tab, "Editor")
        
        # Theme tab
        theme_tab = self._create_theme_tab()
        tabs.addTab(theme_tab, "Theme")
        
        # Shortcuts tab
        shortcuts_tab = self._create_shortcuts_tab()
        tabs.addTab(shortcuts_tab, "Shortcuts")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self) -> QWidget:
        """Create general settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Auto-save
        self.auto_save_check = QCheckBox()
        auto_save = self.app_data_manager.get_config_value('auto_save', True)
        self.auto_save_check.setChecked(auto_save)
        layout.addRow("Auto-save:", self.auto_save_check)
        
        # Auto-save interval
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setMinimum(5000)
        self.auto_save_interval.setMaximum(60000)
        self.auto_save_interval.setSingleStep(5000)
        self.auto_save_interval.setSuffix(" ms")
        interval = self.app_data_manager.get_config_value('auto_save_interval', 30000)
        self.auto_save_interval.setValue(interval)
        layout.addRow("Auto-save interval:", self.auto_save_interval)
        
        return widget
    
    def _create_editor_tab(self) -> QWidget:
        """Create editor settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setMinimum(8)
        self.font_size.setMaximum(32)
        font_size = self.app_data_manager.get_config_value('font_size', 12)
        self.font_size.setValue(font_size)
        layout.addRow("Font size:", self.font_size)
        
        # Tab size
        self.tab_size = QSpinBox()
        self.tab_size.setMinimum(2)
        self.tab_size.setMaximum(8)
        tab_size = self.app_data_manager.get_config_value('tab_size', 4)
        self.tab_size.setValue(tab_size)
        layout.addRow("Tab size:", self.tab_size)
        
        # Use spaces
        self.use_spaces = QCheckBox()
        use_spaces = self.app_data_manager.get_config_value('use_spaces', True)
        self.use_spaces.setChecked(use_spaces)
        layout.addRow("Use spaces:", self.use_spaces)
        
        # Word wrap
        self.word_wrap = QCheckBox()
        word_wrap = self.app_data_manager.get_config_value('word_wrap', False)
        self.word_wrap.setChecked(word_wrap)
        layout.addRow("Word wrap:", self.word_wrap)
        
        # Show line numbers
        self.show_line_numbers = QCheckBox()
        show_line_numbers = self.app_data_manager.get_config_value('show_line_numbers', True)
        self.show_line_numbers.setChecked(show_line_numbers)
        layout.addRow("Show line numbers:", self.show_line_numbers)
        
        # Show minimap
        self.show_minimap = QCheckBox()
        show_minimap = self.app_data_manager.get_config_value('show_minimap', True)
        self.show_minimap.setChecked(show_minimap)
        layout.addRow("Show minimap:", self.show_minimap)
        
        return widget
    
    def _create_theme_tab(self) -> QWidget:
        """Create theme settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        current_theme = self.app_data_manager.get_config_value('theme', 'dark')
        self.theme_combo.setCurrentText(current_theme)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        layout.addRow("Theme:", self.theme_combo)
        
        return widget
    
    def _create_shortcuts_tab(self) -> QWidget:
        """Create shortcuts settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel("Configure keyboard shortcuts")
        layout.addWidget(label)
        
        btn = QPushButton("Edit Shortcuts")
        btn.clicked.connect(self._on_edit_shortcuts)
        layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def _on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        if self.theme_manager:
            self.theme_manager.set_theme(theme_name)
    
    def _on_edit_shortcuts(self):
        """Open shortcuts editor"""
        dialog = ShortcutsDialog(self, self.shortcuts_manager)
        dialog.exec_()
    
    def accept(self):
        """Save settings and close"""
        try:
            # Save general settings
            self.app_data_manager.set_config_value('auto_save', self.auto_save_check.isChecked())
            self.app_data_manager.set_config_value('auto_save_interval', self.auto_save_interval.value())
            
            # Save editor settings
            self.app_data_manager.set_config_value('font_size', self.font_size.value())
            self.app_data_manager.set_config_value('tab_size', self.tab_size.value())
            self.app_data_manager.set_config_value('use_spaces', self.use_spaces.isChecked())
            self.app_data_manager.set_config_value('word_wrap', self.word_wrap.isChecked())
            self.app_data_manager.set_config_value('show_line_numbers', self.show_line_numbers.isChecked())
            self.app_data_manager.set_config_value('show_minimap', self.show_minimap.isChecked())
            
            # Save theme
            self.app_data_manager.set_config_value('theme', self.theme_combo.currentText())
            
            logger.info("Settings saved")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
            logger.error(f"Failed to save settings: {e}")
