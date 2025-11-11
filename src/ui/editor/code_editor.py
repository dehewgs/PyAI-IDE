"""
Code Editor with Syntax Highlighting for PyAI IDE
"""

from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QSyntaxHighlighter, QTextFormat, QTextDocument
from PyQt5.QtGui import QTextCharFormat, QBrush, QPen, QPainter
import re


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter"""
    
    def __init__(self, document):
        super().__init__(document)
        
        # Define formats
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(249, 38, 114))  # Magenta
        self.keyword_format.setFontWeight(700)
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(230, 219, 116))  # Yellow
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(117, 113, 94))  # Gray
        self.comment_format.setFontItalic(True)
        
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(102, 217, 239))  # Cyan
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(174, 129, 255))  # Purple
        
        # Keywords
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'True', 'try', 'while', 'with', 'yield'
        ]
    
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
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setup font
        font = QFont("Courier New", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Setup syntax highlighter
        self.highlighter = PythonSyntaxHighlighter(self.document())
        
        # Setup line numbers
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        
        # Setup colors
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #272822;
                color: #f8f8f2;
                border: none;
            }
        """)
    
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
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def line_number_area_paint_event(self, event):
        """Paint line numbers"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(39, 40, 34))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(117, 113, 94))
                painter.drawText(0, int(top), self.line_number_area.width() - 2, 
                               self.fontMetrics().height(), Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
