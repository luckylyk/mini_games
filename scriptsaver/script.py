import os
import json
import time
from datetime import datetime


class Script(object):
    def __init__(self, jsonpath):
        self._jsonpath = jsonpath
        self._datas = load(jsonpath)

        self._code = None
        self._author = None
        self._name = None
        self._language = None
        self._date = None
        self._color = None
        self._is_shared = None

        self.isModified = Signal(self)
        self._is_modified = False

    @staticmethod
    def create(jsonpath, name, language):
        pass

    @property
    def author(self):
        if self._author is None:
            self._author = self._datas.get('author')
        return self._author

    def set_author(self, value):
        self._datas['author'] = value
        self._author = None
        self.set_modified()

    @property
    def code(self):
        if self._code is None:
            self._code = self._datas.get('code')
        return self._code

    def set_code(self, value):
        self._datas['code'] = value
        self._code = None
        self.set_modified()

    @property
    def color(self):
        if self._color is None:
            self._color = self._datas.get('color')
        return self._color

    def set_color(self, value):
        self._datas['color'] = value
        self._color = None
        self.set_modified()

    @property
    def date(self):
        if self._date is None:
            self._date = datetime.fromtimestamp(self._datas.get('date'))
        return self._date

    def update_date(self):
        self._datas['date'] = time.time()
        self._date = None
        self.set_modified()

    @property
    def is_shared(self):
        if self._is_shared is None:
            self._is_shared = self._datas.get('shared', False)
        return self._is_shared

    def set_shared(self, value):
        self._is_shared = value
        self.set_modified()

    @property
    def language(self):
        if self._language is None:
            self._language = self._datas.get('language')
        return self._language

    def set_language(self, value):
        self._datas['language'] = value
        self._language = None
        self.set_modified()

    @property
    def name(self):
        if self._name is None:
            self._name = self._datas.get('name')
        return self._name

    def set_name(self, value):
        self._datas['name'] = value
        self._name = None
        self.set_modified()

    def save(self):
        self.update_date()
        folder = os.path.dirname(self._jsonpath)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self._jsonpath, 'w') as jsonfile:
            json.dump(self._datas, jsonfile, sort_keys=True, indent=4)
        self._is_modified = False

    @property
    def json_exists(self):
        return os.path.exists(self._jsonpath)

    @property
    def is_saved(self):
        return not self._is_modified

    def set_modified(self):
        self._is_modified = True
        self.isModified.emit()

    def delete(self):
        print self._jsonfile, 'deleted'
        return


def load(jsonpath):
    if not os.path.exists(jsonpath):
        return {}

    with open(jsonpath, 'r') as jsonfile:
        return json.load(jsonfile)


def get_scripts(folderpath):
    jsonfiles = (
        os.path.join(folderpath, f) for f in os.listdir(folderpath)
        if f.endswith('.json'))

    return [Script(f) for f in jsonfiles]


class Signal():
    def __init__(self, instance):
        self._connected = []
        self._instance = instance

    def connect(self, method):
        self._connected.append(method)

    def emit(self):
        for connected in self._connected:
            connected(self._instance)