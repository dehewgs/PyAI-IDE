"""
Code Editor with Syntax Highlighting for PyAI IDE
"""

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QSyntaxHighlighter, QTextFormat, QTextDocument
from PyQt5.QtGui import QTextCharFormat, QBrush, QPen, QPainter
import re


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter with theme support"""
    
    def __init__(self, document, theme_config=None):
        super().__init__(document)
        self.theme_config = theme_config
        self._setup_formats()
    
    def _setup_formats(self):
        """Setup text formats based on theme"""
        if self.theme_config:
            keyword_color = self.theme_config.get_editor_color("keyword", "#f92672")
            string_color = self.theme_config.get_editor_color("string", "#e6db74")
            comment_color = self.theme_config.get_editor_color("comment", "#75715e")
            function_color = self.theme_config.get_editor_color("function", "#66d9ef")
            number_color = self.theme_config.get_editor_color("number", "#ae81ff")
        else:
            keyword_color = "#f92672"
            string_color = "#e6db74"
            comment_color = "#75715e"
            function_color = "#66d9ef"
            number_color = "#ae81ff"
        
        # Define formats
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(keyword_color))
        self.keyword_format.setFontWeight(700)
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(string_color))
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(comment_color))
        self.comment_format.setFontItalic(True)
        
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(function_color))
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(number_color))
        
        # Keywords
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'True', 'try', 'while', 'with', 'yield'
        ]
    
    def update_theme(self, theme_config):
        """Update theme configuration
        
        Args:
            theme_config: New theme configuration
        """
        self.theme_config = theme_config
        self._setup_formats()
        self.rehighlight()
    
    def highlightBlock(self, text):
        """Highlight a block of text"""
        # Highlight comments
        comment_index = text.find('#')
        if comment_index >= 0:
            self.setFormat(comment_index, len(text) - comment_index, self.comment_format)
            text = text[:comment_index]
        
        # Highlight strings
        for match in re.finditer(r'["\'].*?["\']', text):
            self.setFormat(match.start(), match.end() - match.start(), self.string_format)
        
        # Highlight numbers
        for match in re.finditer(r'\b\d+\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.number_format)
        
        # Highlight keywords
        for keyword in self.keywords:
            pattern = r'\b' + keyword + r'\b'
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), self.keyword_format)
        
        # Highlight function definitions
        for match in re.finditer(r'\bdef\s+(\w+)', text):
            self.setFormat(match.start(1), len(match.group(1)), self.function_format)


class LineNumberArea(QWidget):
    """Line number area for code editor"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        """Return size hint"""
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        """Paint line numbers"""
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """Code editor with syntax highlighting and line numbers"""
    
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        
        # Setup font
        font = QFont("Courier New", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Setup syntax highlighter
        self.highlighter = PythonSyntaxHighlighter(self.document(), self._get_theme_config())
        
        # Setup line numbers
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        
        # Apply theme
        self._apply_theme()
        
        # Connect to theme changes if theme manager available
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed)
    
    def _get_theme_config(self):
        """Get theme configuration"""
        if self.theme_manager and self.theme_manager.current_config:
            return self.theme_manager.current_config
        return None
    
    def _apply_theme(self):
        """Apply theme to editor"""
        theme_config = self._get_theme_config()
        
        if theme_config:
            bg_color = theme_config.get_editor_color("background", "#272822")
            fg_color = theme_config.get_editor_color("foreground", "#f8f8f2")
        else:
            bg_color = "#272822"
            fg_color = "#f8f8f2"
        
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {bg_color};
                color: {fg_color};
                border: none;
            }}
        """)
    
    def _on_theme_changed(self, theme_id):
        """Handle theme change
        
        Args:
            theme_id: New theme identifier
        """
        self._apply_theme()
        self.highlighter.update_theme(self._get_theme_config())
        self.update_line_number_area_width(0)
    
    def line_number_area_width(self):
        """Calculate line number area width"""
        digits = len(str(self.blockCount()))
        return 3 + self.fontMetrics().horizontalAdvance('9') * digits
    
    def update_line_number_area_width(self, _):
        """Update line number area width"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update line number area"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
    
    def highlight_current_line(self):
        """Highlight current line"""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            theme_config = self._get_theme_config()
            if theme_config:
                line_color_str = theme_config.get_editor_color("current_line_background", "#3e3d32")
            else:
                line_color_str = "#3e3d32"
            
            line_color = QColor(line_color_str)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def line_number_area_paint_event(self, event):
        """Paint line numbers"""
        painter = QPainter(self.line_number_area)
        
        theme_config = self._get_theme_config()
        if theme_config:
            bg_color = theme_config.get_editor_color("line_number_background", "#272822")
            fg_color = theme_config.get_editor_color("line_number_foreground", "#757569")
        else:
            bg_color = "#272822"
            fg_color = "#757569"
        
        painter.fillRect(event.rect(), QColor(bg_color))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(fg_color))
                painter.drawText(0, int(top), self.line_number_area.width() - 2, 
                               self.fontMetrics().height(), Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
