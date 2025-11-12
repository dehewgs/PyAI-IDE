"""
Model Panel for PyAI IDE
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
from PyQt5.QtGui import QColor
from utils.logger import logger


class ModelPanel(QWidget):
    """Model panel for model management"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.loaded_models = []
        self._create_ui()
    
    def _create_ui(self):
        """Create model panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(8, 8, 8, 8)
        header_layout.setSpacing(8)
        self.header_label = QLabel("Loaded Models")
        header_layout.addWidget(self.header_label)
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)
        layout.addLayout(header_layout)
        
        # Model list
        self.model_list = QListWidget()
        layout.addWidget(self.model_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(8, 8, 8, 8)
        button_layout.setSpacing(8)
        self.unload_btn = QPushButton("Unload")
        self.unload_btn.clicked.connect(self._on_unload)
        button_layout.addWidget(self.unload_btn)
        layout.addLayout(button_layout)
    
    def _apply_theme(self):
        """Apply theme to panel"""
        if not self.theme_manager:
            return
        
        is_dark = self.theme_manager.current_theme == "dark"
        self.set_theme(is_dark)
    
    def set_theme(self, is_dark):
        """Set theme for the panel
        
        Args:
            is_dark: True for dark theme, False for light theme
        """
        if is_dark:
            # Dark theme
            bg_color = "#1e1e1e"
            fg_color = "#d4d4d4"
            border_color = "#3e3e3e"
            header_bg = "#252526"
        else:
            # Light theme
            bg_color = "#ffffff"
            fg_color = "#333333"
            border_color = "#cccccc"
            header_bg = "#f3f3f3"
        
        # Apply stylesheet to list widget
        self.model_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {bg_color};
                color: {fg_color};
                border: none;
            }}
            QListWidget::item:selected {{
                background-color: #0e639c;
                color: #ffffff;
            }}
            QListWidget::item:hover {{
                background-color: {border_color};
            }}
        """)
        
        # Apply stylesheet to header label
        self.header_label.setStyleSheet(f"""
            QLabel {{
                color: {fg_color};
                background-color: {header_bg};
                padding: 4px 8px;
                font-weight: bold;
            }}
        """)
        
        # Apply stylesheet to buttons
        button_style = f"""
            QPushButton {{
                background-color: #0e639c;
                color: #ffffff;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1177bb;
            }}
            QPushButton:pressed {{
                background-color: #0d5a96;
            }}
        """
        self.refresh_btn.setStyleSheet(button_style)
        self.unload_btn.setStyleSheet(button_style)
        
        # Apply stylesheet to panel itself
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {fg_color};
            }}
        """)
        
        # Force update to ensure changes are applied
        self.update()
        self.model_list.update()
    
    def add_model(self, model_id):
        """Add model to list"""
        if model_id not in self.loaded_models:
            self.loaded_models.append(model_id)
            item = QListWidgetItem(model_id)
            self.model_list.addItem(item)
            logger.info(f"Model added to panel: {model_id}")
    
    def remove_model(self, model_id):
        """Remove model from list"""
        if model_id in self.loaded_models:
            self.loaded_models.remove(model_id)
            for i in range(self.model_list.count()):
                if self.model_list.item(i).text() == model_id:
                    self.model_list.takeItem(i)
                    break
            logger.info(f"Model removed from panel: {model_id}")
    
    def _on_unload(self):
        """Handle unload button"""
        current_item = self.model_list.currentItem()
        if current_item:
            model_id = current_item.text()
            self.remove_model(model_id)
            logger.info(f"Unloaded model: {model_id}")
    
    def refresh(self):
        """Refresh model list"""
        logger.info("Refreshing model list")
    
    def get_loaded_models(self):
        """Get loaded models"""
        return self.loaded_models.copy()
