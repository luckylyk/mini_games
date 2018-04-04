
import os
import datetime
from functools import partial
from PySide2 import QtWidgets, QtCore, QtGui

from maya_libs.scriptsaver import ICONPATH
from .highliter import Highliter


ICONS = {}


def icon(filename):
    if not ICONS.get(filename):
        ICONS[filename] = QtGui.QIcon(os.path.join(ICONPATH, filename))
    return ICONS[filename]


class ScriptSaverMainView(QtWidgets.QWidget):
    currentScriptChanged = QtCore.Signal(object)
    currentAuthorChanged = QtCore.Signal(str)
    codeModified = QtCore.Signal(str)
    scriptContextMenuRequested = QtCore.Signal(object)

    script_headers = {
        'name': '<b> - Name: </b>{}',
        'author': '<b> - Author: </b>{}',
        'modification': '<b> - Last Modification: </b>{}',}

    def __init__(self, parent=None):
        super(ScriptSaverMainView, self).__init__(parent, QtCore.Qt.Window)

        self._author_selecter = AuthorSelecter()
        self._author_selecter.currentTextChanged.connect(
            self.currentAuthorChanged.emit)

        self._script_table_model = ScriptTableModel()
        self._script_table_view = ScriptTableView()
        self._script_table_view.set_model(self._script_table_model)
        self._script_table_view.currentScriptChanged.connect(
            self.currentScriptChanged.emit)
        self._script_table_view.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        self._script_table_view.customContextMenuRequested.connect(
            self.scriptContextMenuRequested.emit)

        self.file_menubar = FileMenuBar(self)

        self._scripts_widget = QtWidgets.QWidget()
        self._scripts_layout = QtWidgets.QVBoxLayout(self._scripts_widget)
        self._scripts_layout.setContentsMargins(0, 0, 0, 0)
        self._scripts_layout.addWidget(self._author_selecter)
        self._scripts_layout.addWidget(self._script_table_view)
        self._scripts_layout.addWidget(self.file_menubar)

        self._script_name = QtWidgets.QLabel(
            self.script_headers['name'].format('-'))
        self._script_author = QtWidgets.QLabel(
            self.script_headers['author'].format('-'))
        self._script_modification = QtWidgets.QLabel(
            self.script_headers['modification'].format('-'))

        self._script_descriptions_layout = QtWidgets.QHBoxLayout()
        self._script_descriptions_layout.setContentsMargins(15, 15, 8, 8)
        self._script_descriptions_layout.setSpacing(10)
        self._script_descriptions_layout.addWidget(self._script_name)
        self._script_descriptions_layout.addWidget(self._script_author)
        self._script_descriptions_layout.addWidget(self._script_modification)

        self._script_editor = QtWidgets.QPlainTextEdit()
        self._script_editor.textChanged.connect(
            self._script_table_view_text_modified)
        self._highliter = Highliter(self._script_editor.document())

        self._script_editor_widget = QtWidgets.QWidget()
        self._script_editor_layout = QtWidgets.QVBoxLayout(
            self._script_editor_widget)
        self._script_editor_layout.setContentsMargins(0, 0, 0, 0)
        self._script_editor_layout.addWidget(self._script_editor)
        self._script_editor_layout.addLayout(self._script_descriptions_layout)
 
        self._splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self._splitter.setSizes([200, 600])
        self._splitter.addWidget(self._scripts_widget)
        self._splitter.addWidget(self._script_editor_widget)

        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._splitter)

        self.sizeHint = lambda: QtCore.QSize(800, 450)

    def set_authors(self, authors, current=None):
        self._author_selecter.blockSignals(True)
        self._author_selecter.set_authors(authors)
        if current:
            self._author_selecter.setCurrentText(current)
        self._author_selecter.blockSignals(False)

    def set_language(self, language):
        self._script_editor.blockSignals(True)
        self._highliter.set_language(language)
        self._highliter.rehighlight()
        self._script_editor.blockSignals(False)

    def set_code(self, code):
        self._script_editor.blockSignals(True)
        self._script_editor.document().setPlainText(code)
        self._highliter.rehighlight()
        self._script_editor.blockSignals(False)

    def set_scripts(self, scripts):
        self._script_table_model.set_items(scripts)
        self._script_table_view.clear_selection()

    def set_script(self, script):
        self.set_code(script.code)
        self._script_name.setText(
            self.script_headers['name'].format(script.name))
        self._script_author.setText(
            self.script_headers['author'].format(script.author))
        self._script_modification.setText(
            self.script_headers['modification'].format(
                script.date.strftime('%c')))

    def _script_table_view_text_modified(self):
        self.codeModified.emit(self._script_editor.document().toPlainText())

    def remove_script(self, script):
        self._script_table_model.remove_script(script)
        self._script_table_view.clear_selection()
        self._script_editor.document().setPlainText('')


class AuthorSelecter(QtWidgets.QComboBox):
    def set_authors(self, authors):
        self.clear()
        self.addItem('Shared')
        self.insertSeparator(1)
        self.addItems(authors)


class ScriptTableView(QtWidgets.QTableView):
    currentScriptChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(ScriptTableView, self).__init__(parent)
        self._model = None
        self._selection_model = None

        self.verticalHeader().hide()
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setShowGrid(False)
        self.setSortingEnabled(True)

    def set_model(self, model):
        super(ScriptTableView, self).setModel(model)
        self._model = model
        self._model.dataChanged.connect(self.update)
        self._model.layoutChanged.connect(self.update)

        self._selection_model = self.selectionModel()
        self._selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self, new_selection_range, old_selection_range):
        if not self._model:
            return

        indexes = new_selection_range.indexes()
        self.currentScriptChanged.emit(
            self._model.data(indexes[0], QtCore.Qt.UserRole))

    def clear_selection(self):
        self._selection_model.blockSignals(True)
        self.clearSelection()
        self._selection_model.blockSignals(False)

    def update(self, *args):
        self.horizontalHeader().resizeSection(0, 12)
        self.horizontalHeader().resizeSections(
            QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)


class ScriptTableModel(QtCore.QAbstractTableModel):
    headers = ['', 'Language', 'Script name']
    sorters = {
        1: lambda script: script.language,
        2: lambda script: script.name,
        3: lambda script: script.date}

    def __init__(self):
        super(ScriptTableModel, self).__init__()
        self.items = []

    def rowCount(self, index=None):
        return len(self.items)

    def columnCount(self, index=None):
        return 3

    def set_items(self, items):
        self.layoutAboutToBeChanged.emit()
        self.items = items
        for item in items:
            item.isModified.connect(self.update_item)
        self.layoutChanged.emit()

    def update_item(self, item):
        try:
            row = self.items.index(item)
        except ValueError:
            return

        begin = self.index(row, 0)
        end = self.index(row, self.columnCount() -1)
        self.dataChanged.emit(begin, end, [])

    def headerData(self, index, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return self.headers[index]

    def remove_script(self, item):
        self.layoutAboutToBeChanged.emit()
        self.items.remove(item)
        self.layoutChanged.emit()

    def setData(self, index, value, role):
        row, column = index.row(), index.column()
        if role == QtCore.Qt.EditRole:
            if column == 2:
                self.items[row].set_name(value)
                return True
        return False

    def sort(self, index, order):
        if not index:
            return

        self.layoutAboutToBeChanged.emit()
        self.items = sorted(
            self.items, key=self.sorters[index],
            reverse=(order is QtCore.Qt.AscendingOrder))
        self.layoutChanged.emit()

    def flags(self, index):
        flags = super(ScriptTableModel, self).flags(index)
        if index.column() == 2:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def data(self, index, role):
        row, column = index.row(), index.column()

        if role == QtCore.Qt.DisplayRole:
            if column == 1:
                return self.items[row].language
            if column == 2:
                return self.items[row].name

        elif role == QtCore.Qt.EditRole:
            if column == 2:
                return self.items[row].name

        elif role == QtCore.Qt.BackgroundColorRole:
            return QtGui.QColor(self.items[row].color)

        elif role == QtCore.Qt.UserRole:
            return self.items[row]

        elif role == QtCore.Qt.TextAlignmentRole:
            if column == 0:
                return QtCore.Qt.AlignHCenter

        elif role == QtCore.Qt.DecorationRole:
            if column != 0:
                return

            item = self.items[row]
            if not item.json_exists:
                return icon('new.png')
            elif not item.is_saved:
                return icon('modified.png')


class FileMenuBar(QtWidgets.QMenuBar):
    newScriptRequested = QtCore.Signal()
    saveCurrentRequested = QtCore.Signal()
    saveAllRequested = QtCore.Signal()
    deleteCurrentScriptRequested = QtCore.Signal()
    reloadRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super(FileMenuBar, self).__init__(parent)
        self._new = QtWidgets.QAction(icon('newfile.png'), '', self)
        self._new.triggered.connect(self.newScriptRequested.emit)
        self._save = QtWidgets.QAction(icon('filesave.ico'), '', self)
        self._save.triggered.connect(self.saveCurrentRequested.emit)
        self._save_all = QtWidgets.QAction(icon('save_all.ico'), '', self)
        self._save_all.triggered.connect(self.saveAllRequested.emit)
        self._recycle_bin = QtWidgets.QAction(
            icon('recycle_bin.png'), '', self)
        self._recycle_bin.triggered.connect(
            self.deleteCurrentScriptRequested.emit)
        self._reload = QtWidgets.QAction(icon('reload.ico'), '', self)
        self._reload.triggered.connect(self.reloadRequested.emit)

        self.addActions([
            self._new, self._save, self._save_all,
            self._recycle_bin, self._reload])


class NewScriptDialog(QtWidgets.QDialog):
    def __init__(self, languages, parent=None):
        super(NewScriptDialog, self).__init__(parent)
        self.setWindowTitle('New Script')
        self._script_name = QtWidgets.QLineEdit('new script')
        self._language_combo = QtWidgets.QComboBox()
        self._language_combo.addItems(languages)

        self._ok = QtWidgets.QPushButton('ok')
        self._ok.clicked.connect(self.accept)
        self._cancel = QtWidgets.QPushButton('cancel')
        self._cancel.clicked.connect(self.reject)

        self._layout_infos = QtWidgets.QHBoxLayout()
        self._layout_infos.setContentsMargins(0, 0, 0, 0)
        self._layout_infos.addWidget(self._script_name)
        self._layout_infos.addWidget(self._language_combo)

        self._layout_buttons = QtWidgets.QHBoxLayout()
        self._layout_buttons.setContentsMargins(0, 0, 0, 0)
        self._layout_buttons.addStretch()
        self._layout_buttons.addWidget(self._ok)
        self._layout_buttons.addWidget(self._cancel)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addLayout(self._layout_infos)
        self._layout.addLayout(self._layout_buttons)

    def accepted(self):
        return self._script_name.text(), self._language_combo.currentText()


class ScriptsContextMenu(QtWidgets.QMenu):
    setColorRequested = QtCore.Signal()
    sharedToggled = QtCore.Signal(bool)
    setLanguageRequested = QtCore.Signal(object)

    def __init__(self, languages, parent=None):
        super(ScriptsContextMenu, self).__init__(parent)
        self._color = QtWidgets.QAction('set color', self)
        self._color.triggered.connect(self.setColorRequested.emit)

        self._shared = QtWidgets.QAction('shared', self)
        self._shared.setCheckable(True)
        self._shared.toggled.connect(self.sharedToggled.emit)

        self._languages = QtWidgets.QMenu('set language')
        for language in languages:
            action = QtWidgets.QAction(language, self)
            action.triggered.connect(
                partial(self.setLanguageRequested.emit, language))
            self._languages.addAction(action)

        self.addAction(self._color)
        self.addAction(self._shared)
        self.addSeparator()
        self.addMenu(self._languages)

    def set_script(self, script):
        self._shared.blockSignals(True)
        self._shared.setChecked(script.is_shared)
        self._shared.blockSignals(False)