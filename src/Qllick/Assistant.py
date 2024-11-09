from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty

class Assistant(QObject):
    def __init__(self, name=None, model=None, prompt=None, parent=None):
        super(Assistant, self).__init__(parent)
        self._name = name
        self._model = model
        self._prompt = prompt

    @pyqtProperty(str, fget=lambda self: self._name, fset=lambda self, value: setattr(self, '_name', value))
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @pyqtProperty(str, fget=lambda self: self._model, fset=lambda self, value: setattr(self, '_model', value))
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @pyqtProperty(str, fget=lambda self: self._prompt, fset=lambda self, value: setattr(self, '_prompt', value))
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value
