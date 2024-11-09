from PyQt5 import QtCore
from Qllick.qllama import Registry

# Create a singleton instance of QllamaRegistry
registry = Registry()


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    async def do_work(self, model, prompt, system, options):
        print(prompt, system, options)
        model = registry.get_model(model)
        response = model.generate(prompt, system, options)

        self.finished.emit(response)
