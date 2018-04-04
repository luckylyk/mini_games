
from PySide2 import QtGui, QtCore
from .languages import python


def convert_dict_to_qcharformat(style):
    char_format = QtGui.QTextCharFormat()
    if style.get('color'):
        char_format.setForeground(QtGui.QColor(style.get('color')))

    if style.get('italic'):
        char_format.setFontItalic(True)

    if style.get('bold'):
        char_format.setFontWeight(QtGui.QFont.Bold)

    return char_format


class Highliter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super(Highliter, self).__init__(document)
        self.rules = []

    def highlightBlock(self, text):
        for expression, nth, format_ in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format_)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    def set_language(self, language):
        self.rules = [
            (QtCore.QRegExp(reg_exp), index, convert_dict_to_qcharformat(frmt))
            for reg_exp, index, frmt in language.RULES]

    #     # Do multi-line strings
    #     in_multiline = self.match_multiline(text, *self.rules[0])
    #     if not in_multiline:
    #         in_multiline = self.match_multiline(text, *self.rules[1])

    # def match_multiline(self, text, delimiter, in_state, style):
    #     """Do highlighting of multi-line strings. ``delimiter`` should be a
    #     ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
    #     ``in_state`` should be a unique integer to represent the corresponding
    #     state changes when inside those strings. Returns True if we're still
    #     inside a multi-line string when this function is finished.
    #     """
    #     # If inside triple-single quotes, start at 0
    #     if self.previousBlockState() == in_state:
    #         start = 0
    #         add = 0
    #     # Otherwise, look for the delimiter on this line
    #     else:
    #         start = delimiter.indexIn(text)
    #         # Move past this match
    #         add = delimiter.matchedLength()

    #     # As long as there's a delimiter match on this line...
    #     while start >= 0:
    #         # Look for the ending delimiter
    #         end = delimiter.indexIn(text, start + add)
    #         # Ending delimiter on this line?
    #         if end >= add:
    #             length = end - start + add + delimiter.matchedLength()
    #             self.setCurrentBlockState(0)
    #         # No; multi-line string
    #         else:
    #             self.setCurrentBlockState(in_state)
    #             length = text.length() - start + add
    #         # Apply formatting
    #         self.setFormat(start, length, style)
    #         # Look for the next match
    #         start = delimiter.indexIn(text, start + length)

    #     # Return True if still inside a multi-line string, False otherwise
    #     if self.currentBlockState() == in_state:
    #         return True
    #     else:
    #         return False