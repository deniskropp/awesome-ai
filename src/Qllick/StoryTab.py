from PyQt5 import QtWidgets

from qllama import Qllama


class StoryTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super(StoryTab, self).__init__(parent)

        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout(self)

        self.content_input = QtWidgets.QTextEdit(self)
        self.layout.addWidget(self.content_input)

        self.generate_button = QtWidgets.QPushButton('Generate Story', self)
        self.layout.addWidget(self.generate_button)

        self.setLayout(self.layout)

        self.generate_button.clicked.connect(self.generate_story)


    def generate_story(self):
        qllama = Qllama(base_url='http://127.0.0.1:11434', model='qwen2.5:1.5b')
        content = self.content_input.toPlainText()
        response = qllama.generate(content)
        self.parent.text_to_speech(response)
