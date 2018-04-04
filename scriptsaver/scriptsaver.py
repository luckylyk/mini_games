

import pkgutil
import os

from PySide2 import QtCore, QtWidgets
from maya_libs.scriptsaver import highliter
from .script import get_scripts, Script
from .widgets import ScriptSaverMainView, NewScriptDialog, ScriptsContextMenu


APPLICATION_DATA = r'd:/temp/scipts'
LANGUAGES_PATH = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)), 'languages')

LANGUAGES_AVAILABLES = {}
for importer, name, _ in pkgutil.iter_modules([LANGUAGES_PATH]):
    LANGUAGES_AVAILABLES[name] = importer.find_module(name).load_module(name)


class ScriptSaver():
    def __init__(self, view):
        self._scripts = []
        self._current_author = 'Shared'
        self._current_script = None
        self._view = view
        self._view.currentScriptChanged.connect(self._current_script_changed)
        self._view.codeModified.connect(self._code_modified)
        self._view.currentAuthorChanged.connect(self._current_author_changed)
        self._view.scriptContextMenuRequested.connect(self._call_script_context_menu)

        self._view.file_menubar.newScriptRequested.connect(
            self._create_new_script)
        self._view.file_menubar.saveCurrentRequested.connect(
            self._save_current_script)
        self._view.file_menubar.saveAllRequested.connect(
            self._save_all_scripts)
        self._view.file_menubar.deleteCurrentScriptRequested.connect(
            self._delete_current_script)
        self._view.file_menubar.reloadRequested.connect(self.load_files)

        self._script_context_menu = ScriptsContextMenu(
            LANGUAGES_AVAILABLES.keys())
        self._script_context_menu.setColorRequested
        self._script_context_menu.sharedToggled.connect(
            self._set_script_shared)
        self._script_context_menu.setLanguageRequested.connect(
            self._set_script_language)
        self.load_files()

    def load_files(self):
        self._scripts = get_scripts(APPLICATION_DATA)
        self.update()

    def update(self):
        if self._current_author != 'Shared':
            author = self._current_author 
        else:
            author = None
        shared = self._current_author == 'Shared'

        self._view.set_authors(
            sorted(list({s.author for s in self._scripts})), current=author)
        self._view.set_scripts(self.filter_scripts(author, shared))

    def _current_script_changed(self, script):
        self._current_script = script
        self._view.set_script(script)
        self._view.set_language(LANGUAGES_AVAILABLES[script.language])
        self._script_context_menu.set_script(script)

    def _code_modified(self, code):
        if self._current_script:
            self._current_script.set_code(code)

    def _save_current_script(self):
        self._current_script.save()

    def _save_all_scripts(self):
        for script in self._scripts:
            script.save()

    def _current_author_changed(self, text):
        self._current_author = text
        self.update()

    def filter_scripts(self, author=None, shared=True):
        scripts=self._scripts
        if author:
            scripts = [s for s in scripts if s.author == author]
        if shared:
            scripts = [s for s in scripts if s.is_shared]
        return scripts

    def _create_new_script(self):
        dialog = NewScriptDialog(LANGUAGES_AVAILABLES.keys())
        dialog.exec_()
        if dialog.result() == QtWidgets.QDialog.Rejected:
            return

        name, language = dialog.accepted()
        script = Script.create(
            APPLICATION_DATA, name, LANGUAGES_AVAILABLES[language])

    def _delete_current_script(self):
        dialog = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            'Delete {} ?'.format(self._current_script.name),
            ('{} will be delete.\nThis action cannot be cancelled.\n'
            'Are you sure to continue ?').format(
                self._current_script._jsonpath),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if dialog.exec_() == 65536: # find the constant with this value
            return

        self._view.remove_script(self._current_script)
        self._current_script.delete()

    def _call_script_context_menu(self, point):
        self._script_context_menu.exec_(
            self._view.mapToGlobal(point))

    def _set_script_shared(self, state):
        self._current_script.set_shared(state)
        self.update()

    def _set_script_language(self, language):
        self._current_script.set_language(language)
        self._view.set_language(LANGUAGES_AVAILABLES[language])
